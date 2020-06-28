import csv
import os
import re
import requests
from csv import DictReader
from random import randint, choices

import scrapy
import logging
from bs4 import BeautifulSoup
from scrapy_splash import SplashRequest

from ..items import School
from ..util import print_color

SCHOOL_SITES_FILE = 'scraping-sites.csv'
TIMESTAMPS = ["20191201", "20181201", "20171201", "20161201", "20151201"]


class SchoolSpider(scrapy.Spider):
    name = 'school'

    def start_requests(self):
        schools_list = self.get_schools()
        for school in schools_list:
            url = school.get('website')
            if (url.find('http://') == -1):
                school['website'] = f'http://{url}'
            # if school.get('district_name') == 'SARASOTA':
            try:
                yield SplashRequest(url=school.get('website'), callback=self.parse, args={'wait': 5},
                                    cb_kwargs=dict(school=school))
                # yield scrapy.Request(url=school.get('website'), callback=self.parse, errback=self.request_err, cb_kwargs=dict(school=school))
            except:
                yield {
                    "Error": f"Unable to make a Scrapy Request on url {school.get('website')}"
                }

    def request_err(self, response):
        print('Error ocurred:', repr(response))

    def get_schools(self):
        schools_list = []
        with open(SCHOOL_SITES_FILE, 'r') as file:
            reader = DictReader(file)
            schools_list = list(reader)

        return schools_list[:25]
        # Get 10 random items from list
        rand_schools_list = choices(schools_list, k=5)
        print_color(rand_schools_list)
        return rand_schools_list
        # Return 10 random ones for now

    def parse(self, response, school):
        soup = BeautifulSoup(response.body, 'lxml')
        # Redirect to proper school page for dade schools
        if (self.is_redirect_page(soup, school)):
            redirect_btn = soup.find('li', 'btn btn-primary')
            if redirect_btn is not None:
                url = redirect_btn.parent['href']
                try:
                    yield SplashRequest(url=url, callback=self.parse, args={'wait': 5},
                                        cb_kwargs=dict(school=school))
                    # yield scrapy.Request(url=school.get('website'), callback=self.parse, errback=self.request_err, cb_kwargs=dict(school=school))
                except:
                    logging.warning(
                        f"Unable to make a Scrapy Request on url {school.get('website')}")

        element_list = self.get_href_elements(soup)

        if len(element_list) != 0:
            staff_found = 1

        # yield {
        #     "District": school.get('district_name'),
        #     "School": school.get('school_name'),
        #     "School site": school.get('website'),
        #     "Staff found": staff_found,
        # }

        for element in element_list:
            # Grab href link to staff dir
            dir_href = None
            try:
                dir_href = element['href']
            except KeyError:
                print('Error: href attribute not found')

            if dir_href is not None:
                dir_page = response.urljoin(dir_href)
                school['staff_href'] = dir_href
                # yield scrapy.Request(url=dir_page, callback=self.parse_staff_page, cb_kwargs=dict(school=school))
                yield (SplashRequest(url=dir_page, callback=self.parse_staff_page, args={'wait': 5},
                                     meta={'school': school, 'page_title': dir_href}))

    def parse_staff_page(self, response):
        school = response.meta.get('school')
        page_title = response.meta.get('page_title')
        real_url = response.url

        html_text = response.css('body').get()
        soup = BeautifulSoup(html_text, 'lxml')
        grade_elements = soup.find_all(text=re.compile(
            r"principal|grade|teacher|superintendent", re.IGNORECASE))

        if len(grade_elements) > 0:
            missing_snapshots = 0
            for timestamp in TIMESTAMPS:
                wayback_url = f'http://archive.org/wayback/available?url={real_url}&timestamp={timestamp}'
                year = int(timestamp[:4])
                historical_url = self.fetch_wayback_snapshot(wayback_url, year)
                if historical_url is not None:
                    # yield SplashRequest(url=historical_url, callback=self.save_page, args={'wait': 25}, meta={'school': school, 'page_title': page_title, 'year': year})
                    yield scrapy.Request(url=historical_url, callback=self.save_page,
                                         cb_kwargs=dict(school=school, page_title=page_title, year=year))
                else:
                    missing_snapshots += 1

            if missing_snapshots >= len(TIMESTAMPS):
                save_path = self.get_save_path(school, page_title, '2020')
                self.write_file(save_path, html_text)

        yield {
            'district': school.get('district_name'),
            'school': school.get('school_name'),
            'website': school.get('website'),
            'grade_found': len(grade_elements)
        }

    def get_href_elements(self, soup):
        element_list = self.get_soup_elements(soup, 'a')
        span_elements = self.get_soup_elements(soup, 'span')

        for elem in span_elements:
            href_elem = elem.find_parent("a")
            if href_elem is not None:
                element_list.append(href_elem)

        return element_list

    def fetch_wayback_snapshot(self, wayback_url, year):
        session = requests.Session()
        res = session.get(wayback_url)
        if res.status_code == 200:
            json = res.json()
            snapshot = json['archived_snapshots']
            if bool(snapshot) and self.has_correct_timestamp(snapshot, year):
                return snapshot['closest']['url']
            else:
                print(
                    f"Timestamp doesn't match required date range for {year}")
        else:
            print(res.status_code, 'Unable to fetch url: ', wayback_url)
        return None

    def save_page(self, response, school, page_title, year):
        save_path = self.get_save_path(school, page_title, year)
        html_text = response.css('body').get()
        self.write_file(save_path, html_text)

    def write_file(self, file_path, file_content):
        try:
            with open(file_path, mode='w+') as file:
                file.write(file_content)
        except Exception:
            print(
                f'Exception occured when saving response to file for {file_path}')

    def get_save_path(self, school, page_title, year):
        '''Determines the path of where school html needs to be saved and returns it'''
        ROOT_SAVE_PATH = os.path.join(os.getcwd(), 'school_site_files')
        year = str(year)
        page_title = page_title.replace('/', '-').replace(".", "-")

        school_name = school.get('school_name')
        county_name = school.get('district_name')
        county_path = os.path.join(
            ROOT_SAVE_PATH, county_name, school_name, year)

        if not os.path.exists(county_path):
            os.makedirs(county_path)
        site_save_path = os.path.join(
            county_path, f'{page_title}.html')
        return site_save_path

    def is_redirect_page(self, soup, school):
        if school.get('website').find('dadeschools') != -1:
            redirect_notice = soup.find(text=re.compile(
                r"By accessing this website link", re.IGNORECASE))
            return redirect_notice is not None
        return False

    def has_correct_timestamp(self, snapshot, year):
        start, end = self.get_daterange_by_year(year)
        snapshot_timestamp = snapshot['closest']['timestamp'][:8]
        snapshot_date = (
            int(snapshot_timestamp[:4]),
            int(snapshot_timestamp[4:6]),
            int(snapshot_timestamp[6:8]),
        )
        is_within_range = start < snapshot_date < end
        return is_within_range

    def get_daterange_by_year(self, year):
        '''Returns a start and end date tuple for the passed academic year'''
        start = (year, 6, 1)
        end = (year + 1, 5, 31)
        return start, end

    def redirect_to_page(self, soup, school):
        ''' For Miami Dade schools checks if there's a redirect page and if so mocks a click on continue redirecting'''
        redirect_btn = soup.find('li', 'btn btn-primary')
        if redirect_btn is not None:
            url = redirect_btn.parent['href']
            print_color('button found')
            # yield scrapy.Request(url=url, callback=self.parse, cb_kwargs=dict(school=school))
            try:
                yield SplashRequest(url=url, callback=self.parse, args={'wait': 5},
                                    cb_kwargs=dict(school=school))
                # yield scrapy.Request(url=school.get('website'), callback=self.parse, errback=self.request_err, cb_kwargs=dict(school=school))
            except:
                yield {
                    "Error": f"Unable to make a Scrapy Request on url {school.get('website')}"
                }

    def get_soup_elements(self, soup, tag='a'):
        return soup.find_all(tag, text=re.compile(
            r"staff|faculty|directory|employee", re.IGNORECASE))

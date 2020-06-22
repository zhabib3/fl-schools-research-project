import csv
import os
import re
import requests
from csv import DictReader
from random import randint, choices

import scrapy
from bs4 import BeautifulSoup
from scrapy_splash import SplashRequest

from ..items import School
from ..util import print_color

SCHOOL_SITES_FILE = 'scraping-sites.csv'
TIMESTAMPS = ["20190501", "20180501", "20170501", "20160501", "20150501"]


class SchoolSpider(scrapy.Spider):
    name = 'school'

    def start_requests(self):
        schools_list = self.get_schools()
        for school in schools_list:
            url = school.get('website')
            if (url.find('http://') == -1):
                school['website'] = f'http://{url}'
            # yield SplashRequest(url=school.get('website'), callback=self.parse, args={'wait': 5},
            #                     meta={'school': school})
            yield scrapy.Request(url=school.get('website'), callback=self.parse, errback=self.request_err, cb_kwargs=dict(school=school))

    def request_err(self, response):
        print('Error ocurred:', repr(response))

    def get_schools(self):
        schools_list = []
        with open(SCHOOL_SITES_FILE, 'r') as file:
            reader = DictReader(file)
            schools_list = list(reader)

        return schools_list[306:307]
        # Get 10 random items from list
        rand_schools_list = choices(schools_list, k=5)
        print_color(rand_schools_list)
        return rand_schools_list
        # Return 10 random ones for now

    def parse(self, response, school):
        # html_text = response.request.meta['driver'].page_source
        # school = response.meta.get('school')
        soup = BeautifulSoup(response.body, 'lxml')
        # Redirect to proper school page for dade schools
        if (self.is_redirect_page(soup, school)):
            redirect_btn = soup.find('li', 'btn btn-primary')
            if redirect_btn is not None:
                url = redirect_btn.parent['href']
                yield scrapy.Request(url=url, callback=self.parse, cb_kwargs=dict(school=school))

        element_list = soup.find_all('a', text=re.compile(
            r"staff|faculty|directory|employee", re.IGNORECASE))

        span_elements = soup.find_all('span', text=re.compile(
            r"staff|faculty|directory|employee", re.IGNORECASE))

        for elem in span_elements:
            href_elem = elem.find_parent("a")
            if href_elem is not None:
                element_list.append(href_elem)

        staff_found = 0
        if len(element_list) != 0:
            staff_found = 1

        yield {
            "District": school.get('district_name'),
            "School": school.get('school_name'),
            "School site": school.get('website'),
            "Staff found": staff_found,
        }

        for element in element_list:
            # Grab href link to staff dir
            dir_href = None
            try:
                dir_href = element['href']
            except KeyError:
                print('Error: href attribute not found')

            if dir_href is not None:
                dir_page = response.urljoin(dir_href)
                # print_color(f'School staff link: {dir_page}')
                school['staff_href'] = dir_href
                # yield scrapy.Request(url=dir_page, callback=self.parse_staff_page, cb_kwargs=dict(school=school))
                yield (SplashRequest(url=dir_page, callback=self.parse_staff_page, args={'wait': 5},
                                     meta={'school': school, 'page_title': dir_href}))

    def parse_staff_page(self, response):
        school = response.meta.get('school')
        page_title = response.meta.get('page_title')

        real_url = response.url
        print_color(f'>> {response.url}')

        html_text = response.css('body').get()
        soup = BeautifulSoup(html_text, 'lxml')
        grade_elements = soup.find_all(text=re.compile(
            r"principal|grade", re.IGNORECASE))

        if len(grade_elements) > 0:
            for timestamp in TIMESTAMPS:
                wayback_url = f'http://archive.org/wayback/available?url={real_url}&timestamp={timestamp}'
                historical_url = self.fetch_wayback_snapshot(wayback_url)
                if historical_url is not None:
                    year = timestamp[:4]
                    # TODO uncomment below to make splash request back in time
                    # yield SplashRequest(url=historical_url, callback=self.save_page, args={'wait': 25},
                    #                     meta={'school': school, 'page_title': page_title, 'year': year})

        yield {
            'district': school.get('district_name'),
            'school': school.get('school_name'),
            'website': school.get('website'),
            'grade_found': len(grade_elements)
        }

    def fetch_wayback_snapshot(self, wayback_url):
        res = requests.get(wayback_url)
        if res.status_code == 200:
            json = res.json()
            print_color(json)
            # TODO check is snapshot url is available and matches year, if true return historical url
        else:
            print(res.status_code, 'Unable to fetch url: ', wayback_url)
        return None

    def save_page(self, response):
        school = response.meta.get('school')
        page_title = response.meta.get('page_title')
        year = response.meta.get('year')
        save_path = self.get_save_path(school, page_title)
        html_text = response.css('body').get()
        try:
            with open(save_path, mode='w+') as file:
                file.write(f'{year}_{html_text}')
        except TypeError:
            print(
                f'TypeError occured when saving response to file for {school["school_name"]}')

    def get_save_path(self, school, page_title):
        '''Determines the path of where school html needs to be saved and returns it'''
        ROOT_SAVE_PATH = os.path.join(os.getcwd(), 'school_site_files')
        school_name = school.get(
            'school_name', f'School Staff Page {randint(0, 100)}')
        page_title = page_title.replace(
            '/', '-').replace(".", "-")
        county_name = school.get('district_name')
        county_path = os.path.join(ROOT_SAVE_PATH, county_name)
        # Check if a county dir has been created if not create one
        if not os.path.exists(county_path):
            os.mkdir(county_path)
        site_save_path = os.path.join(
            # county_path, f'{school_name}-Page#{randint(0, 100)}.html')
            county_path, f'{school_name}#{page_title}.html')
        return site_save_path

    def is_redirect_page(self, soup, school):
        print_color(f'{school.get("website")} ==> ')
        if school.get('website').find('dadeschools') != -1:
            redirect_notice = soup.find(text=re.compile(
                r"By accessing this website link", re.IGNORECASE))
            print_color(f'{redirect_notice is not None}')
            return redirect_notice is not None
        return False


    def redirect_to_page(self, soup, school):
        ''' For Miami Dade schools checks if there's a redirect page and if so mocks a click on continue redirecting'''
        redirect_btn = soup.find('li', 'btn btn-primary')
        if redirect_btn is not None:
            url = redirect_btn.parent['href']
            print_color('button found')
            yield scrapy.Request(url=url, callback=self.parse, cb_kwargs=dict(school=school))

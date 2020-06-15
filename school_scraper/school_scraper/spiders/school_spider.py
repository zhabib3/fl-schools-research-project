import csv
import os
import re
from csv import DictReader
from random import randint, choices

import scrapy
from bs4 import BeautifulSoup
from scrapy_splash import SplashRequest

from ..items import School
from ..util import print_color

SCHOOL_SITES_FILE = 'scraping-sites.csv'


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
            yield scrapy.Request(url=school.get('website'), callback=self.parse, cb_kwargs=dict(school=school))


    def get_schools(self):
        schools_list = []
        with open(SCHOOL_SITES_FILE, 'r') as file:
            reader = DictReader(file)
            schools_list = list(reader)

        return schools_list[:15]
        # Get 10 random items from list
        rand_schools_list = choices(schools_list, k=10)
        return rand_schools_list
        # Return 10 random ones for now

    def parse(self, response, school):
        # html_text = response.request.meta['driver'].page_source
        # school = response.meta.get('school')
        soup = BeautifulSoup(response.body, 'lxml')

        element_list = soup.find_all('a', text=re.compile(
            r"staff|faculty|directory|employee", re.IGNORECASE))

        for element in element_list:
            # Grab href link to staff dir
            dir_href = None
            try:
                dir_href = element['href']
            except KeyError:
                print('Error: href attribute not found')

            if dir_href is not None:
                dir_page = response.urljoin(dir_href)
                print_color(f'School staff link: {dir_page}')
                school['staff_href'] = dir_href
                # yield scrapy.Request(url=dir_page, callback=self.save_page, cb_kwargs=dict(school=school))
                yield (SplashRequest(url=dir_page, callback=self.save_page, args={'wait': 5},
                                    meta={'school': school, 'page_title': dir_href}))

    def save_page(self, response):
        school = response.meta.get('school')
        page_title = response.meta.get('page_title')
        save_path = self.get_save_path(school, page_title)
        html_text = response.css('body').get()

        try:
            with open(save_path, mode='w+') as file:
                file.write(html_text)
            print(
                f'Saved file {school.get("school_name")} from url {response.request.url}')
        except TypeError:
            print(
                'TypeError occured when saving response to file for {response.request.url}')
        yield {
            'district': school.get('district_name', 'District name not found'),
            'school': school.get('school_name', 'School name not found'),
            'website': response.request.url,
        }

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
            county_path, f'{school_name}#{page_title}-#{randint(0, 100)}.html')
        return site_save_path

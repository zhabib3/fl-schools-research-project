import scrapy
from random import randint
import re
import csv
from csv import DictReader
from ..items import School
from bs4 import BeautifulSoup
"""
Staff Dir link found in:
- Faculty/Staff in Nav -> Staff dir
- About / About us : hover -> Staff Directory

xPath
response.xpath("//*[contains(text(), 'MY TEXT')]")

regex
/\bstaff|faculty\b/gi

Sites with staff element on home page
    'http://gablese.dadeschools.net/',
    'http://pinecrestacademysouth.dadeschools.net/'

"""

SCHOOL_SITES_FILE = 'scraping-sites.csv'


class SchoolSpider(scrapy.Spider):
    name = 'school'
    # start_urls = [
    #     'http://www.bayschools.com/lhes'
    # ]

    def start_requests(self):
        schools_list = self.get_school_urls()
        for school in schools_list:
            url = school.get('website')
            if (url.find('http://') == -1):
                school['website'] = f'http://{url}'

            yield scrapy.Request(url=school.get('website'), callback=self.parse,
                                 cb_kwargs=dict(school=school))

    def get_school_urls(self):
        schools_list = []
        with open(SCHOOL_SITES_FILE, 'r') as file:
            reader = DictReader(file)
            schools_list = list(reader)
        return schools_list[:50]
        # Return 10 random ones for now

    def parse(self, response, school):   
        soup = BeautifulSoup(response.text, 'lxml')
        print(school)
        element_list = soup.find_all('a', text=re.compile(
            r"staff|faculty|directory|employee", re.IGNORECASE))

        if len(element_list) == 0:
            yield {
                'district': school.get('district_name', 'District name not found'),
                'school': school.get('school_name', 'School name not found'),
                'website': response.request.url,
                'staff_href': 'Not found'
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
                school['staff_href'] = dir_href
                yield scrapy.Request(dir_page, callback=self.save_page, cb_kwargs=dict(school=school))
                yield {
                    'district': school.get('district_name', 'District name not found'),
                    'school': school.get('school_name', 'School name not found'),
                    'website': response.request.url,
                    'staff_href': element.get('href', 'Link not found')
                }

    def save_page(self, response, school):
        school_name = school.get('school_name', f'School Staff Page {randint(0, 100)}')
        staff_href = school.get('staff_href', 'href').replace('/', '-').replace(".", "-")
        try:
            with open(f'{school_name}_{staff_href}.html', mode='w+') as file:
                file.write(response.text)
            self.log(
                f'Saved file {school_name}_{staff_href} from url {response.request.url}')
        except TypeError:
            print(
                'TypeError occured when saving response to file for {response.request.url}')

import scrapy
import re
import csv
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
    schools_list = []
    name = 'school'
    start_urls = [
        'http://quotes.toscrape.com/tag/humor/',
        # 'http://gablese.dadeschools.net/',
        # 'http://pinecrestacademysouth.dadeschools.net/'
    ]

    def get_school_urls(self):
        schools_list = []
        count = 0
        with open(SCHOOL_SITES_FILE) as file:
            reader = csv.reader(file, delimiter=",")
            for line in reader:
                if (count == 0):
                    count += 1
                    continue
                school = School(*line)
                schools_list.append(school)
        return schools_list
        # Return 10 random ones for now

    def parse(self, response):
        self.schools_list = self.get_school_urls()
        print(self.schools_list)
        soup = BeautifulSoup(response.text, 'lxml')
        # for element in soup.find_all('a', text=re.compile(r"staff|faculty|directory|employee", re.IGNORECASE)):
        #     # Grab href link to staff dir
        #     dir_href = None
        #     try:
        #         dir_href = element['href']
        #     except KeyError:
        #         print('Error: href attribute not found')

        #     if dir_href is not None:
        #         dir_page = response.urljoin(dir_href)
        #         self.school_name = 'Test'
        #         yield scrapy.Request(dir_page, callback=self.save_page)

        #     yield {
        #         'site_name': response.request.url,
        #         'staff_dir_href': dir_href
        #     }

    def save_page(self, response):
        try:
            with open(f'{self.school_name}.html', mode='w+') as file:
                file.write(response.text)
            self.log(
                f'Saved file {self.school_name} from url {response.request.url}')
            self.school_name += '1'
        except TypeError:
            print(
                'TypeError occured when saving response to file for {response.request.url}')

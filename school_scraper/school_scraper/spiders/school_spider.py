import scrapy
from bs4 import BeautifulSoup
import re
""" 
Staff Dir link found in:
- Faculty/Staff in Nav -> Staff dir
- About / About us : hover -> Staff Directory

xPath
response.xpath("//*[contains(text(), 'MY TEXT')]")

regex
/\bstaff|faculty\b/gi
"""

"""
Sites with staff element on home page
    'http://gablese.dadeschools.net/',
    'http://pinecrestacademysouth.dadeschools.net/'

"""


class SchoolSpider(scrapy.Spider):
    name = 'school'
    start_urls = [
        'http://gablese.dadeschools.net/',
        'http://pinecrestacademysouth.dadeschools.net/'
    ]

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        for element in soup.find_all('a', text=re.compile(r"staff|faculty", re.IGNORECASE)):
            yield {
                'site_name': response.request.url,
                'staff_element': element.parent
            }
        # staff_xpath = response.xpath(
        # "//*[contains(text(), 'Staff') or contains(text(), 'Faculty')]")
        # staff_dir_link = staff_xpath.get()

    def write_to_file(self, data, filename):
        with open(filename, 'wb') as f:
            f.write(data)
        self.log(f'Saved file {filename}')

    # def get_random_sites(num):
    #     with open('scraping-sites.csv', mode='r'):

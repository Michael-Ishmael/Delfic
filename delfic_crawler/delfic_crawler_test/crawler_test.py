from delfic.crawler.sitelocator import WebsiteLocator
from delfic.crawler.xgoogle.search import GoogleSearch

__author__ = 'scorpio'

import unittest


class GoogleSearchTest(unittest.TestCase):

    def get_results_test(self):
        search = GoogleSearch('AFRICAN MINERALS ENGINEERING LIMITED', tld='co.uk')

        result = search.get_results()

        self.assertEqual(len(result), 8)


class WebsiteLocatorTest(unittest.TestCase):

    def find_website_test(self):
        locator = WebsiteLocator('A SHADE GREENER LIMITED', '06922318')
        url = locator.find_website()

        self.assertEqual(url, 'http://ashadegreener.co.uk')

        locator.reload('AFRICAN MINERALS ENGINEERING LIMITED', '06954023')

        url = locator.find_website()
        self.assertEqual(url, 'http://www.african-minerals.com')


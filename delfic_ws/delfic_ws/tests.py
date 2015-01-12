import unittest
from delfic_ws.business.web import WebsiteLocator

__author__ = 'scorpio'


class WebsiteLocatorTest(unittest.TestCase):

    def get_website_meta_test(self):
        locator = WebsiteLocator()
        result = locator.get_website_meta("http://www.woodburypark.co.uk/")
        self.assertEqual(len(result.metaDict), 3)


    def find_website_links_test(self):
        locator = WebsiteLocator()
        result = locator.find_website_links("http://www.woodburypark.co.uk")
        self.assertEqual(len(result.all_links), 3)


    def get_calais_tags_test(self):
        locator = WebsiteLocator()
        result = locator.get_calais_tags("http://www.woodburypark.co.uk/")
        self.assertEqual(len(result.all_links), 3)


    def find_website_text_test(self):
        locator = WebsiteLocator()
        result = locator.get_page_text("http://www.woodburypark.co.uk", 5)
        self.assertTrue(result['success'])
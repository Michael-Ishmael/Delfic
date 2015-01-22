import unittest

from delfic_ws.business.web.web import WebsiteLocator


__author__ = 'scorpio'


class WebsiteLocatorTest(unittest.TestCase):

    def find_website_test(self):
        locator = WebsiteLocator()
        result = locator.find_website('06920905')
        self.assertEqual(result, 'dd')

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




html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<div class="story">This is </p>
"""
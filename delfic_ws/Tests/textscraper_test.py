import unittest
from delfic_ws.business.web.textscraper import TextScraper
from pygoogle import pygoogle

__author__ = 'scorpio'


class WebsiteLocatorTest(unittest.TestCase):

    def get_page_text_html_test(self):
        scraper = TextScraper()
        result = scraper.get_page_text(html=html_doc)
        if not result.success:
            print(result.message)
        self.assertEqual(result.success, True)

    def get_page_text_test(self):
        scraper = TextScraper()
        result = scraper.get_page_text(page_url='http://mclarensaviation.com/')
        if not result['success']:
            print(result['message'])
        self.assertEqual(result['success'], True)

    def pygoogle_test(self):
        g = pygoogle()

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<div class="story">
This is a story about them:
<div>This is highlighted</div>
And this continues
</div>
"""

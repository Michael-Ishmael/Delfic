from django.test import TestCase

# Create your tests here.
from delfic_ws.business.data import CsvLoader
from delfic_ws.business.web import WebsiteLocator


class TestCsvLoader(TestCase):
    def test_handle_uploaded_file(self):
        loader = CsvLoader()

        with open('/Users/funhead/Dev/Work/GNR/GnRCrawler/data/ShortComps.csv', 'rb') as f:
            companies = loader.handle_uploaded_file(f)
        self.assertTrue(len(companies) > 0)


class TestWebsiteLocator(TestCase):
    def test_find_website(self):
        locator = WebsiteLocator()

        company_url = locator.find_website('SO303372')
        self.assertTrue(len(company_url) > 0)


    def test_find_website_links(self):
        locator = WebsiteLocator()

        link_obj = locator.find_website_links('http://thorntons-law.co.uk')

        self.assertTrue(link_obj.success)


    def test_find_page_text(self):
        locator = WebsiteLocator()

        link_obj = locator.find_website_text('http://thorntons-law.co.uk/about-us', 20)

        self.assertTrue(link_obj['success'])
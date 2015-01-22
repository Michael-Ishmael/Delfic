from htmlentitydefs import name2codepoint
import re
import urllib
import urllib2
import urlparse
from bs4 import BeautifulSoup
from delfic.crawler.xgoogle.search import GoogleSearch

__author__ = 'scorpio'


class WebsiteLocator:
    def __init__(self, company_name, reg_no, post_code='', run_google_search=False):
        self.run_google_search = run_google_search
        self.post_code = post_code
        self.reg_no = reg_no
        self.company_name = company_name

    def reload(self, company_name, reg_no, post_code=''):
        self.post_code = post_code
        self.reg_no = reg_no
        self.company_name = company_name

    def find_website(self):
        url = self.method1()
        if not url and self.run_google_search:
            url = self.method2()
        if url and url.endswith('/'):
            url = url[:-1]
        return url

    def method1(self):
        cc_search = CompanyCheckSearch()
        return cc_search.find_website(self.reg_no)

    def method2(self):
        g_search = GoogleSearch(self.company_name)
        results = g_search.get_results()
        if len(results) > 0:
            return results[0].url


class CompanyCheckSearch:
    def __init__(self):
        self.tag_types = {}
        self.rootSite = "http://companycheck.co.uk/company/"

    def find_website(self, company_ref):
        target_url = urlparse.urljoin(self.rootSite, company_ref)
        try:
            response = urllib2.urlopen(target_url)
            html = response.read()
            soup = BeautifulSoup(html)
            site_link_area = soup.find('div', 'website-area')
            if site_link_area and site_link_area.a:
                site_link = site_link_area.a
                if site_link:
                    if site_link.text == 'Add Website':
                        return None
                    else:
                        company_url = site_link.get('href')
                        try:
                            company_resp = urllib2.urlopen(company_url)
                            company_url = company_resp.url
                        except Exception as ex:
                            pass

                        return company_url
                else:
                    return None
            else:
                return None

        except Exception as ex:
            return None


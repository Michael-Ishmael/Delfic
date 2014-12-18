import json

__author__ = 'funhead'

import urllib2
import urlparse
from calais.base.client import Calais

from bs4 import BeautifulSoup, SoupStrainer


class CompanyWebLink:
    def __init__(self, link, title):
        self.link = link
        self.title = title.strip()

    def __unicode__(self):
        str = ""
        if self.title and len(self.title):
            str += self.title + ": "
        str += self.link
        return str

    def __str__(self):
        return self.__unicode__()

    def to_json(self):
        return json.dumps({"title": self.title, "link": self.link})


class CompanyScrapeResult:
    def __init__(self, company_name, company_url):
        self.company_name = company_name
        self.company_url = company_url
        self.url_parts = urlparse.urlparse(company_url)
        self.all_links = []
        self.direct_links = []
        self.success = True
        self.message = ""


    def test_add_link(self, url, title):
        stored_link = None

        if url == "#":
            return

        if url.startswith('/'):
            stored_link = self.url_parts.scheme + '://' + self.url_parts.netloc + url
        elif url.startswith('http'):
            if self.url_parts.hostname in url:
                stored_link = url
        elif url.startswith('#'):
            stored_link = self.company_url + url
        else:
            stored_link = self.company_url + '/' + url

        if stored_link and stored_link not in self.all_links:
            link_obj = CompanyWebLink(stored_link, title)
            self.all_links.append(link_obj)
            link_parts = urlparse.urlparse(stored_link)
            depth = link_parts.path.count('/')
            if depth == 1:
                self.direct_links.append(link_obj)

    def to_json_dict(self):
        return {
            "success": self.success,
            "message": self.message,
            "links": [x.__dict__ for x in self.direct_links]
        }


class WebsiteLocator:
    def __init__(self):
        self.rootSite = "http://companycheck.co.uk/company/"
        API_KEY = "n6fmydbypqcp5u8wrbxu725v"

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
                        return {"success": False, "message": "Company doesn't have a website"}
                    else:
                        return {"success": True, "url": site_link.get('href')}
                else:
                    return {"success": False, "message": "Link not found"}
            else:
                return {"success": False, "message": "Link area not found"}
        except Exception as ex:
            return {"success": False, "message": ex.message}


    def find_website_links(self, company_url):
        result = CompanyScrapeResult("test", company_url)
        try:
            response = urllib2.urlopen(company_url)
            for link in BeautifulSoup(response, "html.parser", parse_only=SoupStrainer('a')):
                if "href" in link.attrs and link.attrs['href'] != '#':
                    url = link.attrs["href"]
                    title = link.text
                    if len(title.strip()) == 0 and 'title' in link.attrs:
                        title = link.attrs['title']
                    result.test_add_link(url, title)
            result.success = True
        except Exception as ex:
            result.success = False
            result.message = ex.message
        return result


    def find_website_text(self, page_url, min_len):
        try:
            response = urllib2.urlopen(page_url)
            soup = BeautifulSoup(response, 'html.parser')
            [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
            texts = soup.findAll(text=True)

            visible_texts = filter(self.visible, texts)
            visible_texts = filter(lambda t: len(t.split()) >= min_len, visible_texts)
            return {"success": True, "result": visible_texts}
        except Exception as ex:
            return {"success": False, "message": ex.message}


    def visible(self, element):
        try:
            if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
                return False
            elif element.strip() == '':
                return False
            # elif re.match('<!--.*-->', str(element)):
            # return False
            return True
        except Exception as ex:
            return False

            result.success = False
            result.message = ex.message
        return result


    def get_calais_tags(self, url):
        calais = Calais(self.API_KEY, submitter="python-calais demo")
        result = calais.analyze_url(url)
        return result;
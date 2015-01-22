import json
import string

__author__ = 'funhead'

import urllib2
import urlparse
from calais.base.client import Calais

from bs4 import BeautifulSoup, SoupStrainer, NavigableString


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


class CompanyMetaResult:
    def __init__(self, company_url):
        self.company_url = company_url
        self.metaDict = {}
        self.success = True
        self.message = ""

    def add_meta_tag(self, tag_name, tag_value):
        self.metaDict[tag_name] = tag_value

    def to_json_dict(self):
        return {
            "success": self.success,
            "message": self.message,
            "tags": self.metaDict
        }


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
            link_path = str(urlparse.urlparse(stored_link).path)
            if link_path.endswith('/'):
                link_path = link_path[:-1]
                if str(link_path).startswith('//'):
                    link_path = link_path[2:]
            depth = link_path.count('/')
            if depth == 1:
                self.direct_links.append(link_obj)


    def to_json_dict(self):
        return {
            "success": self.success,
            "message": self.message,
            "links": [x.__dict__ for x in self.direct_links]
        }


class CompanyCalaisResult:
    def __init__(self, calais_result):
        self.calais_result = calais_result
        self.success = False
        self.message = ""
        self.entity_dict = {}
        self.topics = []

    def clean_result(self):

        if self.calais_result:
            if hasattr(self.calais_result, "entities"):
                for k, e in self.calais_result.entities.iteritems():
                    e_type = e["_type"]
                    e_text = e["name"]
                    e_relevance = e['relevance']
                    if e_type not in self.entity_dict:
                        self.entity_dict[e_type] = []
                    if (e_text, e_relevance) not in self.entity_dict[e_type]:
                        self.entity_dict[e_type].append((e_text, e_relevance))
                    self.success = True

            if hasattr(self.calais_result, "topics"):
                for k, t in self.calais_result.topics.iteritems():
                    t_category = t["category"]
                    t_category_name = t["categoryName"]
                    t_score = t["score"]
                    if (t_category_name, t_score, t_category) not in self.topics:
                        self.topics.append((t_category_name, t_score, t_category))
                    self.success = True


    def to_json_dict(self):
        self.clean_result()
        return {
            "success": self.success,
            "message": self.message,
            "entities": self.entity_dict,
            "topics": self.topics
        }


class PageTextResult:
    def __init__(self):
        self.text_elements = []
        self.current_element = None
        self.current_page_part = 'BODY'
        self.page_parts = []
        self.in_list_item = False

    def add_text_element(self, text_element):
        text_element.is_heading = self.current_page_part == 'HEADING'
        text_element.is_link = self.current_page_part == 'LINK'
        text_element.is_list = self.current_page_part == 'LIST'
        self.text_elements.append(text_element)
        self.current_element = text_element

    def append_text_to_current_element(self, text, newline=False):
        if self.current_element is None:
            new_element = PageTextElement()
            new_element.text = text
            self.add_text_element(new_element)
        else:
            if newline:
                self.current_element.text += '\r\n' + text
            else:
                self.current_element.text += ' ' + text

    def set_current_page_part(self, page_part):
        self.page_parts.append(page_part.upper())
        self.current_page_part = self.page_parts[-1]

    def revert_current_page_part(self):
        del self.page_parts[-1]
        self.current_page_part = self.page_parts[-1]


class PageTextElement:
    def __init__(self):
        self.text = None
        self.url = None
        self.is_heading = False
        self.page_part = None
        self.abbr = None
        self.is_link = False
        self.is_list = False
        self.probably_nav = False


class WebsiteLocator:
    def __init__(self):
        self.tag_types = {}
        self.rootSite = "http://companycheck.co.uk/company/"
        self.API_KEY = "n6fmydbypqcp5u8wrbxu725v"

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
                        company_url = site_link.get('href')
                        try:
                            company_resp = urllib2.urlopen(company_url)
                            company_url = company_resp.url
                        except Exception as ex:
                            pass

                        return {"success": True, "url": company_url}
                else:
                    return {"success": False, "message": "Link not found"}
            else:
                return {"success": False, "message": "Link area not found"}
        except Exception as ex:
            return {"success": False, "message": ex.message}

    def get_website_meta(self, company_url):
        result = CompanyMetaResult(company_url)
        try:
            response = urllib2.urlopen(company_url)
            soup = BeautifulSoup(response, "html.parser", parse_only=SoupStrainer('head'))
            title = soup.find('title')
            if title is not None:
                title_text = title.text
                if len(title_text) > 0:
                    result.add_meta_tag("title", title_text.strip())

            desc = soup.find(attrs={"name": "description"})
            if desc is not None:
                desc_text = desc.attrs["content"]
                if len(desc_text) > 0:
                    result.add_meta_tag("description", desc_text.strip())

            keywords = soup.find(attrs={"name": "keywords"})
            if keywords is not None:
                keywords_text = desc.attrs["content"]
                if len(keywords_text) > 0:
                    result.add_meta_tag("description", keywords_text.strip())

            result.success = True
        except Exception as ex:
            result.success = False
            result.message = ex.message
        return result

    def find_website_links(self, company_url):
        result = CompanyScrapeResult("test", company_url)
        try:
            response = urllib2.urlopen(company_url)
            links = BeautifulSoup(response, "html.parser", parse_only=SoupStrainer('a'))
            for link in links:
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

    def get_page_text(self, page_url=None, html=None):
        try:
            if page_url is None and html is None:
                return None

            if page_url is not None:
                html = urllib2.urlopen(page_url)

            soup = BeautifulSoup(html, 'html.parser')
            [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
            text_parts = {}
            test_add = set()
            headers = soup.find_all(['h1', 'h2', 'h3'])
            self.add_to_string_collection(headers, 'headers', text_parts, test_add)
            links = soup.find_all('a')
            self.add_to_string_collection(links, 'links', text_parts, test_add)
            visible_text = soup.stripped_strings
            self.add_to_string_collection(visible_text, 'text', text_parts, test_add)
            # for k in text_parts:
            #     for v in text_parts[k]:
            #         print(k, v)
            # print(text_parts)

            return {"success": True, "result": text_parts}

        except Exception as ex:
            return {"success": False, "message": ex.message}

    def add_to_string_collection(self, tag_string_list, key, tag_dict, check_list):
        """
        :type tag_dict: dict
        :type check_list: set
        :param tag_string_list:
        :param key:
        :param dict:
        :param check_list:
        :return:
        """

        for tag_str in tag_string_list:
            try:
                if type(tag_str) is unicode or type(tag_str) is str:
                    stp_str = tag_str.strip()
                elif hasattr(tag_str, 'stripped_strings'):
                    stp_str = " ".join(tag_str.stripped_strings)

                if not stp_str:
                    continue

                stp_str = ''.join(filter(lambda x: x in string.printable, stp_str)).strip()
                if stp_str:
                    if stp_str.lower() not in check_list:
                        check_list.add(stp_str.lower())
                        tag_string_list = tag_dict.setdefault(key, [])
                        tag_string_list.append(stp_str)
            except Exception as ex:
                pass

    def get_calais_tags(self, url):
        calais = Calais(self.API_KEY, submitter="python-calais demo")
        calais_result = calais.analyze_url(url)
        result = CompanyCalaisResult(calais_result)
        result.clean_result()
        return result





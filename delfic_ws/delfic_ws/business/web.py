import json

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
            link_path = urlparse.urlparse(stored_link).path
            if link_path[-1:] == '/':
                link_path = link_path[:-1]
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


class WebsiteLocator:
    def __init__(self):
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
                        return {"success": True, "url": site_link.get('href')}
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


    def find_website_text(self, page_url, min_len):
        try:
            response = urllib2.urlopen(page_url)
            soup = BeautifulSoup(response, 'html.parser')
            [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
            texts = soup.body.find_all(text=True)

            visible_texts = filter(self.visible, texts)
            visible_texts = filter(lambda t: len(t.split()) >= min_len, visible_texts)
            # visible_texts = soup.get_text()
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
        calais_result = calais.analyze_url(url)
        result = CompanyCalaisResult(calais_result)
        result.clean_result()
        return result


    def get_lists(self, url):

        list_dict = {}

        # Anchor, pick up text and URL - bookmark or link?
        # a

        # Table store as headings and cells.  Extract keywords
        #table, tr, thead, th, tbody, td, tfoot


        #Container, process sub elements and text
        list_dict['containers'] = ['div', 'p', 'span', 'frame']

        #Heading store as such
        list_dict['headings'] = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']

        #Abbreviations, pickup 'title' attribute also
        list_dict['abbr'] = ['abbr', 'acronym']

        #List container, could be nav, mark and format
        list_dict['list_container'] = ['dl', 'ul', 'ol']

        #List item, could be nav, mark and format
        list_dict['list_item'] = ['li', 'dt', 'dd']

        #Semantic containers, process sub elements and text, store type of container
        list_dict['containers'] = ['header', 'footer', 'nav', 'main', 'aside', 'address', 'article', 'section', 'aside',
                                   'summary', 'details']

        # Formatting, take only text and ignore
        list_dict['containers'] = ['b', 'u', 'i', 'em', 'center', 'cite', 'font', 'mark', 'q',
                   'samp', 'small', 'sub', 'sup', 'time', 'var']

        # Pullouts store but ignore
        list_dict['pullouts'] = ['blockquote', 'caption', 'pre']

        # Pullouts store but ignore
        list_dict['pullouts'] = ['blockquote', 'caption', 'pre']





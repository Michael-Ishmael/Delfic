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

    def get_page_text(self, page_url, min_len):
        try:
            response = urllib2.urlopen(page_url)
            soup = BeautifulSoup(response, 'html.parser')
            [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
            text_result = PageTextResult
            self.set_lists()
            self.walk_tree(text_result, soup.body, 0)

            # visible_texts = filter(self.visible, texts)
            # visible_texts = filter(lambda t: len(t.split()) >= min_len, visible_texts)
            # visible_texts = soup.get_text()
            return {"success": True, "result": True}
            # visible_texts}
        except Exception as ex:
            return {"success": False, "message": ex.message}

    def walk_tree(self, text_result, parent_node, depth):
        tag_text = None
        new_page_part_set = False
        if hasattr(parent_node, 'children') and len(parent_node.children) > 0:

            for child in parent_node.children:
                if hasattr(child, 'name'):
                    if child.name is not None:
                        node_name = child.name
                        if node_name in self.tag_types['containers'] or node_name in self.tag_types['list_container']:
                            # Simple container, gather child elements
                            self.walk_tree(text_result, child, depth + 1)
                        elif node_name in self.tag_types['semantic_containers']:
                            text_result.set_current_page_part(node_name)
                            new_page_part_set = True
                            self.walk_tree(text_result, child, depth + 1)
                        elif node_name in self.tag_types['headings']:
                            tag = PageTextElement()
                            tag.text = child.string.strip()
                            tag.is_heading = True
                            tag.url = child.get('href')
                            text_result.add_text_element(tag)
                        elif node_name == 'a':

                            tag = PageTextElement()
                            tag.text = child.string.strip()
                            tag.is_link = True
                            tag.url = child.get('href')
                            text_result.add_text_element(tag)

                        if new_page_part_set:
                            text_result.revert_current_page_part()
                else:
                    self.walk_tree(text_result, child, depth + 1)



        else:
            if isinstance(parent_node, NavigableString):
                tag = PageTextElement()
                tag.text = parent_node.string.strip()
                text_result.add_text_element(tag)
            else:
                raise NameError('Unexpected element')
        return

    def has_significant_children(self, node):
        significant = False
        if hasattr(node, 'children') and len(node.children) > 0:
            for child in node.children:
                if hasattr(child, 'name'):
                    if child.name is not None:
                        node_name = child.name
                        if node_name in self.tag_types['containers'] or node_name in self.tag_types[
                            'semantic_containers']:
                            significant = self.has_significant_children(child)
                            if significant:
                                break
                        elif node_name in self.tag_types['headings'] or node_name in self.tag_types['list_item']:
                            significant = True
                            break
            return significant
        else:
            return False

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


    def set_lists(self):

        # Anchor, pick up text and URL - bookmark or link?
        # a

        # Table store as headings and cells.  Extract keywords
        # table, tr, thead, th, tbody, td, tfoot

        # Container, process sub elements and text
        self.tag_types['containers'] = ['div', 'p', 'span', 'frame']

        #Heading store as such
        self.tag_types['headings'] = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']

        #Abbreviations, pickup 'title' attribute also
        self.tag_types['abbr'] = ['abbr', 'acronym']

        #List container, could be nav, mark and format
        self.tag_types['list_container'] = ['dl', 'ul', 'ol']

        #List item, could be nav, mark and format
        self.tag_types['list_item'] = ['li', 'dt', 'dd']

        #Semantic containers, process sub elements and text, store type of container
        self.tag_types['semantic_containers'] = ['header', 'footer', 'nav', 'main', 'aside', 'address', 'article',
                                                 'section', 'aside',
                                                 'summary', 'details']

        # Formatting, take only text and ignore
        self.tag_types['formatting'] = ['b', 'u', 'i', 'em', 'center', 'cite', 'font', 'mark', 'q',
                                        'samp', 'small', 'sub', 'sup', 'time', 'var']

        # Pullouts store but ignore
        self.tag_types['pullouts'] = ['blockquote', 'caption', 'pre']

        # Pullouts store but ignore
        #self.tag_types['pullouts'] = ['blockquote', 'caption', 'pre']





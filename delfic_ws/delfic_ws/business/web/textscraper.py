import urllib2
from bs4 import BeautifulSoup, SoupStrainer, NavigableString

__author__ = 'scorpio'


class TextScraper:
    def __init__(self):
        self.tag_types = {}

    def get_page_text(self, page_url=None, html=None):
        try:
            if page_url is None and html is None:
                return None

            if page_url is not None:
                html = urllib2.urlopen(page_url)

            soup = BeautifulSoup(html, 'html.parser')
            [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
            # text_result = PageTextResult()
            # text_result.start_new_text_block()
            # self.set_lists()
            # self.walk_tree(text_result, soup.body, 0)
            visible_text = soup.stripped_strings
            for txt in soup.stripped_strings:
                print(txt)
            # visible_texts = filter(self.visible, texts)
            # visible_texts = filter(lambda t: len(t.split()) >= min_len, visible_texts)
            # visible_texts = soup.get_text()
            return {"success": True, "result": visible_text}
            # visible_texts}
        except Exception as ex:
            return {"success": False, "message": ex.message}

    def walk_tree(self, text_result, parent_node, depth):
        tag_text = None
        new_page_part_set = False
        if hasattr(parent_node, 'children') and hasattr(parent_node, 'contents') and len(parent_node.contents) > 0:

            for child in parent_node.children:
                if hasattr(child, 'name'):
                    if child.name is not None:
                        node_name = child.name
                        if node_name in self.tag_types['containers']:
                            # Simple container, gather child elements
                            if node_name == 'div' or node_name == 'p':
                                text_result.start_new_text_block()
                            self.walk_tree(text_result, child, depth + 1)
                        elif node_name in self.tag_types['list_container']:
                            self.walk_tree(text_result, child, depth + 1)
                        elif node_name in self.tag_types['list_item']:
                            tag = PageTextElement()
                            tag.text = child.string.strip()
                            tag.is_list = True
                            text_result.add_text_element(tag)
                            text_result.start_new_text_block()
                            if self.has_significant_children(child):
                                self.walk_tree(text_result, child, depth + 1)
                            else:
                                text_result.current_text_block.append_text(child.stripped_strings())
                        elif node_name in self.tag_types['semantic_containers']:
                            text_result.set_current_page_part(node_name)
                            new_page_part_set = True
                            text_result.start_new_text_block()
                            self.walk_tree(text_result, child, depth + 1)
                        elif node_name in self.tag_types['headings']:
                            tag = PageTextElement()
                            tag.text = child.string.strip()
                            tag.is_heading = True
                            text_result.start_new_text_block()
                            text_result.add_text_element(tag)
                            if self.has_significant_children(child):
                                self.walk_tree(text_result, child, depth + 1)
                            else:
                                text_result.current_text_block.append_text(child.stripped_strings())
                        elif node_name == 'a':
                            tag = PageTextElement()
                            tag.text = child.string.strip()
                            tag.is_link = True
                            tag.url = child.get('href')
                            text_result.add_text_element(tag)

                            text_result.current_text_block.append_text(child.stripped_strings())

                        if new_page_part_set:
                            text_result.revert_current_page_part()
                    else:
                        if isinstance(child, NavigableString):
                            text_result.current_text_block.append_text(child.stripped_strings())
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

    def set_lists(self):

        # Anchor, pick up text and URL - bookmark or link?
        # a

        # Table store as headings and cells.  Extract keywords
        # table, tr, thead, th, tbody, td, tfoot

        # Container, process sub elements and text
        self.tag_types['containers'] = ['div', 'p', 'span', 'frame']

        # Heading store as such
        self.tag_types['headings'] = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']

        # Abbreviations, pickup 'title' attribute also
        self.tag_types['abbr'] = ['abbr', 'acronym']

        # List container, could be nav, mark and format
        self.tag_types['list_container'] = ['dl', 'ul', 'ol']

        # List item, could be nav, mark and format
        self.tag_types['list_item'] = ['li', 'dt', 'dd']

        # Semantic containers, process sub elements and text, store type of container
        self.tag_types['semantic_containers'] = ['header', 'footer', 'nav', 'main', 'aside', 'address', 'article',
                                                 'section', 'aside',
                                                 'summary', 'details']

        # Formatting, take only text and ignore
        self.tag_types['formatting'] = ['b', 'u', 'i', 'em', 'center', 'cite', 'font', 'mark', 'q',
                                        'samp', 'small', 'sub', 'sup', 'time', 'var']

        # Pullouts store but ignore
        self.tag_types['pullouts'] = ['blockquote', 'caption', 'pre']

        # Pullouts store but ignore
        # self.tag_types['pullouts'] = ['blockquote', 'caption', 'pre']


class PageTextResult:
    def __init__(self):
        self.text_elements = []
        self.text_blocks = []
        self.current_element = None
        self.current_page_part = 'BODY'
        self.page_parts = []
        self.in_list_item = False
        self.current_text_block = None

    def start_new_text_block(self):
        if self.current_text_block is not None and self.current_text_block.is_empty():
            return
        block = PageTextBlock()
        self.text_blocks.append(block)
        self.current_text_block = block

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


class PageTextBlock:
    def __init__(self):
        self.text = None

    def append_text(self, text, newline=False):
        if len(text) == 0:
            return
        if self.text is None:
            self.text = text
        else:
            if newline:
                self.text += '\r\n'
            else:
                self.text += ' '
            self.text += text

    def is_empty(self):
        return self.text is None or len(self.text) == 0

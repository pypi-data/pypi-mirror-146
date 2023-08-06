
__all__ = [
    "BaseExtractor",
    "PDFExtractor",
    "MdpiExtractor",
    "PMCExtractor",
    "NihExtractor",
    "ScienceDirectExtractor",
    "SpringerExtractor",
    "ApsNetExtractor",
    "WileyExtractor",
    "DailyGroupExtractor",
    "FreshFruitPortalExtractor",
    "HuffingtonExtractor",
    "CitrusIndustryExtractor",
    "UsdaExtractor",
    "NewsroomExtractor",
    "VniikrExtractor",
    "TheGuardianExtractor",
    "TeatroNaturaleExtractor",
    "OliveoilTimesExtractor",
    "IcaExtractor",
    "MonVitiExtractor",
    "NieuweoogstExtractor",
    "AgronewsExtractor",
    "AnsaExtractor"
]

import re
from requests import get
from requests.compat import urljoin
from requests.exceptions import InvalidURL
from requests.utils import default_headers, urlparse
from bs4 import BeautifulSoup as B
from tldextract import extract
from html import unescape
from json import loads
from pprint import pprint as cat, pformat as pcat
from datetime import datetime


from rollet import settings
from rollet.rollet import get_content
from rollet.pdfclient import GrobidClient
from rollet.utils import (
    rfinditem
)


class Extractor:
    
    def __repr__(self):
        string = "Title: {}\nFrom: {}\nFetched at: {}\nStatus: {}\nType: {}\n{} Abstract {}\n{}\n{} Full Text {}\n{}"
        return string.format(
            self.title, self.url, self.date,
            self._status, self.content_type,
            '-'*5, '-'*5, pcat(self.abstract),
            '-'*5, '-'*5, pcat(self.fulltext)
        )

    @staticmethod
    def _clean_url(url):
        return url
    
    def _init_kwargs(self, **kwargs):
        self._fulltext_kwargs, self._abstract_kwargs, self._title_kwargs, self._lang_kwargs = {}, {}, {}, {}
        for k,v in kwargs.items():
            field, key, *_ = k.split('__') + [None]
            if field == 'fulltext': self._fulltext_kwargs.update({key:v})
            elif field == 'abstract': self._abstract_kwargs.update({key:v})
            elif field == 'title': self._title_kwargs.update({key:v})
            elif field == 'lang': self._lang_kwargs.update({key:v})
    
    def _content_type(self):
        if self.url[-3:] == 'pdf': content = 'pdf'
        else:
            charset = self._header.get('Content-Type', '')
            content = re.findall('(html|pdf|json|xml)', charset)
            content = content[0] if len(content) else 'html'
        self.content_type = content

    def to_dict(self, fulltext: bool = False):
        return {
            'url': self.url,
            'status': self._status,
            'title': self.title,
            'title_tag': self.title_tag,
            'abstract': self.abstract,
            'abstract_tag': self.abstract_tag,
            'fulltext': self.fulltext if fulltext else None,
            'fulltext_tag': self.fulltext_tag if fulltext else None,
            'lang': self.lang,
            'content_type': self.content_type,
            'date': self.date
        }
    
    def to_list(self, *args):
        if len(args): listed = [getattr(self, arg, None) for arg in args]
        else: listed = list(self.to_dict().values())
        return listed



class BaseExtractor(Extractor):

    def __new__(cls, url, **kwargs):
        headers = default_headers()
        headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        })
        timeout = float(kwargs.get('timeout', 1))
        response = get(url, headers = headers, timeout = timeout, verify = False)
        if 'pdf' in response.headers.get('Content-Type', '').lower():
            self = PDFExtractor.__new__(PDFExtractor, url, **kwargs)
            self._response = response
            self.__init__(url, **kwargs)
        else:
            self = super(BaseExtractor, cls).__new__(cls)
            self._response = response
        return self


    def __init__(self, url, **kwargs):
        """
        Create BaseExtractor instance
        url: string
        timeout: float, request timeout. Default 1 sec.
        rebond: bool, request <a> tag. Default False.
        abstract_**kwargs: **kwargs for abstract fetch
        title_**kwargs: **kwargs for title fetch
        """
        
        self.url = self._clean_url(url)
        self.domain = extract(url).domain
        self.rebond = bool(kwargs.get('rebond', False))
        self.date = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self._scrap(**kwargs)
        self._init_kwargs(**kwargs)
    

    def _scrap(self, **kwargs):
        timeout = kwargs.pop('timeout', 1)
        headers = default_headers()
        headers.update({
            'User-Agent':
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        })
        headers = kwargs.pop('headers', headers)

        if not hasattr(self, '_response'):
            with get(self.url, timeout = timeout, headers = headers, verify = False) as response:
                response = response
        else:
            response = self._response
        self._status = response.status_code
        self._header = response.headers
        self._content_type()
        if self.content_type == 'html':
            self._page = B(response.text, 'html.parser')
        else:
            self._page = B()


    def _get_content(self, tag, get_tag = False, **kwargs):
        """
        Get content from element Tag
        tag: bs4.element.Tag
        script_keys: List, of keys if tag is script
        attr: str, key attribute if tag is neither a meta nor a script
        fields: List, of fields to concat if rebond
        :return: content
        """
        fields = kwargs.get('fields', ['fulltext'])
        
        if get_tag and tag.name != 'a': content = tag.decode()
        elif tag.name == 'meta':
            content = tag.attrs.get('content', [])
        elif tag.name == 'a' and tag.attrs.get('href') and self.rebond:
            self._presave = True
            raw_content = get_content(urljoin(self.url, tag.attrs['href']), rebond = False)
            content = '. '.join(raw_content.get(field, '') if raw_content.get(field, '') else '' for field in fields )
        elif tag.name == 'script':
            keys = kwargs.get('script_keys', [])
            try:
                serie = loads(tag.content[0])
            except:
                content = list()
            else:
                content = [rfinditem(serie, key) for key in keys]
        elif kwargs.get('attr'):
            content = tag.attrs.get(kwargs.get('attr'))
        else:
            content = tag.get_text(separator = ' ').strip().replace('\n', ' ')

        content = content[0] if isinstance(content, list) and len(content) else content
        content = unescape(content) if isinstance(content, str) else content
        return content
    

    def __repr__(self):
        string = "Title: {}\nFrom: {}\nFetched at: {}\nStatus: {}\nType: {}\n{} Abstract {}\n{}\n{} Full Text {}\n{}"
        return string.format(
            self.title, self.url, self.date,
            self._status, self.content_type,
            '-'*5, '-'*5, pcat(self.abstract),
            '-'*5, '-'*5, pcat(self.fulltext)
        )


    def fetch(self, selectors, get_tag=False, which='first', **kwargs):
        content = list()
        arg_w = ('first', 'min', 'max')
        if which not in arg_w:
            raise ValueError(f'which should be one of {arg_w}')
        for s in selectors:
            contents_ = list()
            tags = self._page.select(s)
            if len(tags): contents_ = [self._get_content(tag, get_tag, **kwargs) for tag in tags]
            if len(contents_) and which == 'first': 
                content = [contents_[0]]
                break
            else:
                try: content += ['. '.join(set(contents_))]
                except: pass
        content = content if len(content) else [None]
        if which == 'max': content = max(content, key=lambda x: len(str(x)))
        else: content = min(content, key=lambda x: len(str(x)))
        return content
    
    @property
    def title(self):
        title = None
        if self.content_type == 'html':
            title = self.fetch(settings.TITLE, **self._title_kwargs)
        return title
    
    @property
    def title_tag(self):
        return self.fetch(
            settings.TITLE, get_tag=True, **
            self._title_kwargs) if self.content_type == 'html' else None
            
    @property
    def abstract(self):
        abstract = None
        if self.content_type == 'html':
            abstract = self.fetch(settings.ABSTRACT, **self._abstract_kwargs)
        return abstract
    
    @property
    def abstract_tag(self):
        return self.fetch(
            settings.ABSTRACT, get_tag=True, **
            self._abstract_kwargs
        ) if self.content_type == 'html' else None
    
    @property
    def fulltext(self):
        fulltext = getattr(self, '_fulltext', None)
        if not fulltext and self.content_type == 'html':
            fulltext = self.fetch(settings.FULLTEXT, fields = ['fulltext'], **self._fulltext_kwargs)
            self._fulltext = fulltext if getattr(self, '_presave', False) else None
        return fulltext
    
    @property
    def fulltext_tag(self):
        fulltext_tag = getattr(self, '_fulltext_tag', None)
        if not fulltext_tag and self.content_type == 'html':
            fulltext_tag = self.fetch(settings.FULLTEXT, get_tag = True, fields = ['fulltext_tag'], **self._fulltext_kwargs)
            self._fulltext_tag = fulltext_tag if getattr(self, '_presave', False) else None
        return fulltext_tag
    
    @property
    def lang(self):
        lang = None
        if self.content_type == 'html':
            lang = self._page.html.get('lang', None)
        return lang



class PDFExtractor(Extractor):
    def __init__(self, url, **kwargs):
        """
        Create PDFExtractor instance
        url: string
        timeout: float, request timeout. Default 1 sec.
        rebond: bool, request <a> tag. Default False.
        abstract_**kwargs: **kwargs for abstract fetch
        title_**kwargs: **kwargs for title fetch
        """
        
        self.url = self._clean_url(url)
        self.domain = extract(url).domain
        self.date = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self._scrap(**kwargs)
        
    def _scrap(self, **kwargs):
        timeout = float(kwargs.pop('timeout', 1))
        headers = default_headers()
        headers.update({
            'User-Agent':
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        })
        headers = kwargs.pop('headers', headers)

        if not hasattr(self, '_response'):
            with get(self.url, timeout = timeout, headers = headers, verify = False) as response:
                response = response
        else:
            response = self._response
        self._status = response.status_code
        self._header = response.headers
        self._content_type()
        if self.content_type == 'pdf':
            try: self._page = self._pdf_parse(response.content)
            except: self._page = B()
        else:
            self._page = B()
        
        
    @staticmethod
    def _pdf_parse(pdf_file):
        grobid_client = GrobidClient()
        req = grobid_client.serve('processFulltextDocument', pdf_file)
        if req.status_code == 200:
            return B(req.text, 'html.parser')
        else: return B()
    
    @property
    def title(self):
        titles = self._page.select('title[level=a i][type=main i]')
        try: title = titles[0].get_text(' ', True)
        except: title = None
        return title
    
    @property
    def title_tag(self):
        titles = self._page.select('title[level=a i][type=main i]')
        try: title_tag = titles[0].decode()
        except: title_tag = None
        return title_tag
    
    @property
    def abstract(self):
        if not hasattr(self._page, 'body'): return None
        abstracts = self._page.select(':is(abstract,details,summary)')
        abstracts += [self._page.body.find('div')] if self._page.body and self._page.body.find('div') else []
        try:abstract = abstracts[0].get_text(' ', True)
        except: abstract = None
        return abstract
    
    @property
    def abstract_tag(self):
        if not hasattr(self._page, 'body'): return None
        abstracts = self._page.select(':is(abstract,details,summary)')
        abstracts += [self._page.body.find('div')] if self._page.body and self._page.body.find('div') else []
        try:abstract_tag = abstracts[0].decode()
        except: abstract_tag = None
        return abstract_tag
    
    @property
    def fulltext(self):
        try:
            fulltext = '. '.join(
                map(lambda x: x.get_text(' ', True),
                    self._page.body.findAll('div', recursive = False)))
        except: fulltext = None
        return fulltext
    
    @property
    def fulltext_tag(self):
        try:
            fulltext_tag = '. '.join(
                map(lambda x: x.decode(),
                    self._page.body.findAll('div', recursive = False)))
        except: fulltext_tag = None
        return fulltext_tag
    
    @property
    def lang(self):
        try: lang = self._page.select(':is(teiheader,text)')[-1].get('xml:lang', 'en')
        except: lang = None
        return lang



class BaseContentExtractor(BaseExtractor):
    """
    Extractor for content in list
    """
    
    def _content(self):
        return list()
    
    @property
    def abstract(self):
        abstract = None
        try: abstract = self._content()[0].get_text(' ', True)
        except: abstract = super().abstract
        return abstract
    
    @property
    def abstract_tag(self):
        abstract_tag = None
        try: abstract_tag = self._content()[0].decode()
        except: abstract_tag = super().abstract_tag
        return abstract_tag
    
    @property
    def fulltext(self):
        fulltext = None
        try: fulltext = '. '.join(map(lambda x:x.get_text(' ', True), self._content()[1:]))
        except: fulltext = super().fulltext
        return fulltext
    
    @property
    def fulltext_tag(self):
        fulltext_tag = None
        try: fulltext_tag = '. '.join(map(lambda x:x.decode(), self._content()[1:]))
        except: fulltext_tag = super().fulltext_tag
        return fulltext_tag



class MdpiExtractor(BaseExtractor):
    """
    Extractor for base mdpi.com domain
    """
    
    @staticmethod
    def _clean_url(url):
        parsed = urlparse(url)
        path = re.sub(r'/(htm|pdf|xml|scifeed_display|notes|reprints|s[0-9]|review_report)?/?$', '', parsed.path) + '/htm'
        return f'{urljoin(url, path)}?{parsed.query}'
    
    @property
    def abstract(self):
        try: abstract = self._page.find(class_='art-abstract').get_text(separator = ' ').strip()
        except: abstract = super().abstract
        return abstract
    
    @property
    def abstract_tag(self):
        try: abstract_tag = self._page.find(class_='art-abstract').decode()
        except: abstract_tag = super().abstract_tag
        return abstract_tag

    @property
    def title(self):
        try:
            title = self._page.find(class_='title', attrs={
                'itemprop': 'name'
            }).get_text(separator = ' ').strip()
        except: title = super().title
        return title
    
    @property
    def title_tag(self):
        try:
            title_tag = self._page.find(class_='title', attrs={
                'itemprop': 'name'
            }).decode()
        except: title_tag = super().title_tag
        return title_tag
    
    @property
    def fulltext(self):
        self._fulltext = '. '.join(map(
            lambda x:x.get_text(' ', True),
            self._page.select('div[class="html-body"] section')))
        fulltext = super().fulltext if not len(self._fulltext) else self._fulltext
        return fulltext
    
    @property
    def fulltext_tag(self):
        self._fulltext = '. '.join(map(
            lambda x:x.decode(),
            self._page.select('div[class="html-body"] section')))
        fulltext_tag = super().fulltext_tag if not len(self._fulltext) else self._fulltext
        return fulltext_tag



class PMCExtractor(BaseContentExtractor):
    """
    Extractor for PubMed Central articles
    """
    
    def _content(self):
        return self._page.select('div[class="tsec sec" i]')
    
    @property
    def title(self):
        title = None
        try: title = self._page.find('h1', class_='content-title').get_text(' ', True)
        except: title = super().title
        return title
    
    @property
    def title_tag(self):
        title_tag = None
        try: title_tag = self._page.find('h1', class_='content-title').decode()
        except: title_tag = super().title_tag
        return title_tag



class NihExtractor(BaseExtractor):
    """
    Extractor for base nih.gov domain
    """
    
    def __new__(cls, url, **kwargs):
        """
        Redirect to PMC version if exist
        """
        headers = default_headers()
        headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        })
        timeout = float(kwargs.get('timeout', 1))
        response = get(url, headers = headers, timeout = timeout, verify = False)
        links = B(response.text, 'html.parser').select('a[class*="pmc"][data-ga-category*="full_text"]')
        if len(links):
            pmc_url = list({u.attrs['href'] for u in links if u.attrs.get('href')})[0]
            pmc_url = urljoin(url, pmc_url)
            return PMCExtractor(pmc_url, **kwargs)
        self = super(NihExtractor, cls).__new__(cls, url, **kwargs)
        self._response = response
        return self
    
    @property
    def abstract(self):
        try: abstract = self._page.find(id='enc-abstract').get_text(separator = ' ').strip()
        except: abstract = None
        finally: abstract = super().abstract if not abstract else abstract
        return abstract
    
    @property
    def abstract_tag(self):
        try: abstract_tag = self._page.find(id='enc-abstract').decode()
        except: abstract_tag = None
        finally: abstract_tag = super().abstract_tag if not abstract_tag else abstract_tag
        return abstract_tag

    @property
    def title(self):
        try: title = self._page.find('h1', class_='heading-title').get_text(separator = ' ').strip()
        except: title = None
        finally: title = super().title if not title else title
        return title
    
    @property
    def title_tag(self):
        try: title_tag = self._page.find('h1', class_='heading-title').decode()
        except: title_tag = None
        finally: title_tag = super().title_tag if not title_tag else title_tag
        return title_tag
    
    @property
    def fulltext(self):
        if getattr(self, '_fulltext', None): return self._fulltext
        full_url = list({
            u.attrs['href']
            for u in self._page.select('a[data-ga-category*="full_text" i]')
            if u.attrs.get('href')})
        try: _fulltext = get_content(full_url[-1], rebond = False)['fulltext']
        except: _fulltext = None
        if _fulltext:
            self._presave = True
            self._fulltext = _fulltext
        return super().fulltext
    
    @property
    def fulltext_tag(self):
        if getattr(self, '_fulltext_tag', None): return self._fulltext_tag
        full_url = list({
            u.attrs['href']
            for u in self._page.select('a[data-ga-category*="full_text" i]')
            if u.attrs.get('href')})
        try: _fulltext_tag = get_content(full_url[-1], rebond = False)['fulltext_tag']
        except: _fulltext_tag = None
        if _fulltext_tag:
            self._presave = True
            self._fulltext_tag = _fulltext_tag
        return super().fulltext_tag



class ScienceDirectExtractor(BaseExtractor):
    """
    Extractor for base sciencedirect.com domain
    """

    @property
    def abstract(self):
        try:
            abstract = self._page.find(id='abstracts',
                                   class_='Abstracts').get_text(' ').strip()
        except: abstract = None
        abstract = super().abstract if not abstract else abstract
        return abstract
    
    @property
    def abstract_tag(self):
        try: abstract_tag = self._page.find(id='abstracts',
                                   class_='Abstracts').decode()
        except: abstract_tag = None
        abstract_tag = super().abstract_tag if not abstract_tag else abstract_tag
        return abstract_tag

    @property
    def title(self):
        try: title = self._page.find('span', class_='title-text').get_text(' ').strip()
        except: title = None
        title = super().title if not title else title
        return title
    
    @property
    def title_tag(self):
        try: title_tag = self._page.find('span', class_='title-text').decode()
        except: title_tag = None
        title_tag = super().title_tag if not title_tag else title_tag
        return title_tag



class SpringerExtractor(BaseExtractor):
    """
    Extractor for base springer.com domain
    """
    
    @property
    def title(self):
        title = self._page.find('h1', class_ = 'c-article-title')
        title = title.get_text(' ').strip() if title else super().title
        return title
    
    @property
    def title_tag(self):
        title_tag = self._page.find('h1', class_ = 'c-article-title').decode()
        title_tag = title_tag if title_tag else super().title_tag
        return title_tag
    
    @property
    def abstract(self):
        try:
            abstract = list(set(map(
                lambda x:x.get_text(' ', True),
                self._page.select(
                    'div[id^="Abs"][class*="c-article-section__content"]'
                ))))[0]
        except: abstract = super().abstract
        return abstract
    
    @property
    def abstract_tag(self):
        try: abstract_tag = list(set(map(
            lambda x:x.decode(),
            self._page.select(
                'div[id^="Abs"][class*="c-article-section__content"]'
            ))))[0]
        except: abstract_tag = super().abstract_tag
        return abstract_tag
    
    @property
    def fulltext(self):
        try:
            self._fulltext = '. '.join(set(map(
                lambda x:x.get_text(' ', True),
                self._page.select(
                    'div[id^="Sec"][class="c-article-section"]'
                ))))
        except: self._fulltext = None
        return super().fulltext
    
    @property
    def fulltext_tag(self):
        try:
            self._fulltext_tag = '. '.join(set(map(
                lambda x:x.decode(),
                self._page.select(
                    'div[id^="Sec"][class="c-article-section"]'
                ))))
        except: self._fulltext_tag = None
        return super().fulltext_tag



class ApsNetExtractor(BaseExtractor):
    
    @staticmethod
    def _clean_url(url):
        return re.sub(
            r'(/doi/)[a-zA-Z]*/?([0-9])',
            r'\1full/\2', url)
    
    @property
    def title(self):
        try: title = self._page.find('h1', class_ = 'citation__title').get_text(' ', True)
        except: title = None
        finally: title = title if title else super().title
        return title
    
    @property
    def title_tag(self):
        try: title_tag = self._page.find('h1', class_ = 'citation__title').decode()
        except: title_tag = None
        finally: title_tag = title_tag if title_tag else super().title_tag
        return title_tag
        
    @property
    def abstract(self):
        try: abstract = self._page.find('div', class_ = 'hlFld-Abstract').get_text(' ', True)
        except: abstract = None
        finally: abstract = abstract if abstract else super().abstract
        return abstract
    
    @property
    def abstract_tag(self):
        try: abstract_tag = self._page.find('div', class_ = 'hlFld-Abstract').decode()
        except: abstract_tag = None
        finally: abstract_tag = abstract_tag if abstract_tag else super().abstract_tag
        return abstract_tag
    
    @property
    def fulltext(self):
        try: self._fulltext = self._page.find('div', class_ = 'hlFld-Fulltext').get_text(' ', True)
        except: self._fulltext = None
        return super().fulltext
    
    @property
    def fulltext_tag(self):
        try: self._fulltext_tag = self._page.find('div', class_ = 'hlFld-Fulltext').decode()
        except: self._fulltext_tag = None
        return super().fulltext_tag



class WileyExtractor(BaseExtractor):
    
    @staticmethod
    def _clean_url(url):
        return re.sub(
            r'(/doi/)[a-zA-Z]*/?([0-9])',
            r'\1full/\2', url)
        
    @property
    def abstract(self):
        try: abstract = self._page.find(
            class_ = 'article-section article-section__abstract').get_text(' ', True)
        except: abstract = None
        finally: abstract = abstract if abstract else super().abstract
        return abstract
    
    @property
    def abstract_tag(self):
        try: abstract_tag = self._page.find(
            class_ = 'article-section article-section__abstract').decode()
        except: abstract_tag = None
        finally: abstract_tag = abstract_tag if abstract_tag else super().abstract_tag
        return abstract_tag
    
    @property
    def fulltext(self):
        try: self._fulltext = self._page.find(
            class_ = 'article-section article-section__full').get_text(' ', True)
        except: self._fulltext = None
        return super().fulltext
    
    @property
    def fulltext_tag(self):
        try: self._fulltext_tag = self._page.find(
            class_ = 'article-section article-section__full').decode()
        except: self._fulltext_tag = None
        return super().fulltext_tag



class DailyGroupExtractor(BaseContentExtractor):
    """
    Extractor for Daily Group
    """
    
    def _content(self):
        return self._page.select('div[itemprop="articleBody" i] p')
    
    @property
    def title(self):
        title = None
        try: title = self._page.find('h1', itemprop = 'name headline').get_text(' ', True)
        except: title = super().title
        return title
    
    @property
    def title_tag(self):
        title_tag = None
        try: title_tag = self._page.find('h1', itemprop = 'name headline').decode()
        except: title_tag = super().title_tag
        return title_tag



class FreshFruitPortalExtractor(BaseContentExtractor):
    """
    Extractor for Daily Group
    """
    
    def _content(self):
        return self._page.select('div[class="post-content" i] p')
    
    @property
    def title(self):
        title = None
        try: title = self._page.find(class_ = 'post-title').get_text(' ', True)
        except: title = super().title
        return title
    
    @property
    def title_tag(self):
        title_tag = None
        try: title_tag = self._page.find(class_ = 'post-title').decode()
        except: title_tag = super().title_tag
        return title_tag



class HuffingtonExtractor(BaseContentExtractor):
    """
    Extractor for HuffingtonPost
    """
    
    def _content(self):
        return self._page.select('.post-contents .content-list-component.text > p')
    
    @property
    def title(self):
        title = None
        try: title = self._page.find(class_ = 'headline__title').get_text(' ', True)
        except: title = super().title
        return title
    
    @property
    def title_tag(self):
        title_tag = None
        try: title_tag = self._page.find(class_ = 'headline__title').decode()
        except: title_tag = super().title_tag
        return title_tag



class CitrusIndustryExtractor(BaseContentExtractor):
    """
    Extractor for Citrusindustry
    """
    
    def _content(self):
        return self._page.select('.entry-content.content > p')
    
    @property
    def title(self):
        try: title = self._page.find(class_ = 'entry-title').get_text(' ', True)
        except: title = super().title
        return title
    
    @property
    def title_tag(self):
        try: title_tag = self._page.find(class_ = 'entry-title').decode()
        except: title_tag = super().title_tag
        return title_tag



class UsdaExtractor(BaseContentExtractor):
    """
    Extractor for Usda
    """
    
    def _content(self):
        return self._page.select('#MainContent :is(p,ul,ol)')
    
    @property
    def title(self):
        try: title = self._page.find(class_ = 'contentTitle').get_text(' ', True)
        except: title = super().title
        return title
    
    @property
    def title_tag(self):
        try: title_tag = self._page.find(class_ = 'contentTitle').decode()
        except: title_tag = super().title_tag
        return title_tag



class NewsroomExtractor(UsdaExtractor, BaseContentExtractor):
    """
    Extractor for Aphis.usda Newsroom
    """
    
    def _content(self):
        try: content = self._page.find(class_ = 'contentTitle').parent.select(':is(p,ul,ol)')
        except: content = super()._content()
        return content



class VniikrExtractor(BaseExtractor):
    """
    Extractor for vniikr
    """
    def _content(self):
        try:
            contents = [
                x.strip() for x in self._page.select_one(
                    '.article-content.container').contents
                if isinstance(x, str) and x != '\n'
            ]
        except: contents = list()
        return contents

    @property
    def title(self):
        try:
            title = self._page.select_one(
                '.article-content.container h2').get_text(' ', True)
        except: title = super().title
        return title
    
    @property
    def title_tag(self):
        try:
            title_tag = self._page.select_one(
                '.article-content.container h2').decode()
        except: title_tag = super().title_tag
        return title_tag
    
    @property
    def abstract(self):
        try: abstract = self._content()[0]
        except: abstract = super().abstract
        return abstract
    
    @property
    def abstract_tag(self):
        try: abstract_tag = self._content()[0]
        except: abstract_tag = super().abstract_tag
        return abstract_tag
    
    @property
    def fulltext(self):
        try: fulltext = ' '.join(self._content()[1:])
        except: fulltext = super().fulltext
        return fulltext
    
    @property
    def fulltext_tag(self):
        try: fulltext_tag = ' '.join(self._content()[1:])
        except: fulltext_tag = super().fulltext_tag
        return fulltext_tag



class TheGuardianExtractor(BaseExtractor):
    """
    Extractor for the Guardian
    """

    @property
    def title(self):
        try:
            title = self._page.select_one(
                'article h1').get_text(' ', True)
        except: title = super().title
        return title
    
    @property
    def title_tag(self):
        try:
            title_tag = self._page.select_one(
                'article h1').decode()
        except: title_tag = super().title_tag
        return title_tag
    
    @property
    def abstract(self):
        try: abstract = self._page.select_one('article p').get_text(' ', True)
        except: abstract = super().abstract
        return abstract
    
    @property
    def abstract_tag(self):
        try: abstract_tag = self._page.select_one('article p').decode()
        except: abstract_tag = super().abstract_tag
        return abstract_tag
    
    @property
    def fulltext(self):
        try:
            fulltext = ' '.join(
                map(lambda x: x.get_text(' ', True),
                    self._page.select('#maincontent div[class^=article i] :is(p,ul,ol)')))
        except: fulltext = super().fulltext
        return fulltext
    
    @property
    def fulltext_tag(self):
        try:
            fulltext_tag = ' '.join(
                map(lambda x: x.decode(),
                    self._page.select('#maincontent div[class^=article i] :is(p,ul,ol)')))
        except: fulltext_tag = super().fulltext_tag
        return fulltext_tag



class TeatroNaturaleExtractor(BaseExtractor):
    """
    Extractor for teatronaturale
    """

    @property
    def title(self):
        try:
            title = self._page.select_one(
                'main h1').get_text(' ', True)
        except: title = super().title
        return title
    
    @property
    def title_tag(self):
        try:
            title_tag = self._page.select_one(
                'main h1').decode()
        except: title_tag = super().title_tag
        return title_tag
    
    @property
    def abstract(self):
        try: abstract = self._page.select_one('.sommario p').get_text(' ', True)
        except: abstract = super().abstract
        return abstract
    
    @property
    def abstract_tag(self):
        try: abstract_tag = self._page.select_one('.sommario p').decode()
        except: abstract_tag = super().abstract_tag
        return abstract_tag
    
    @property
    def fulltext(self):
        try:
            fulltext = ' '.join(
                map(lambda x: x.get_text(' ', True),
                    self._page.select('.contenuto :is(p,ul,ol)')))
        except: fulltext = super().fulltext
        return fulltext
    
    @property
    def fulltext_tag(self):
        try:
            fulltext_tag = ' '.join(
                map(lambda x: x.decode(),
                    self._page.select('.contenuto :is(p,ul,ol)')))
        except: fulltext_tag = super().fulltext_tag
        return fulltext_tag



class OliveoilTimesExtractor(BaseExtractor):
    """
    Extractor for oliveoiltimes
    """

    @property
    def title(self):
        try:
            title = self._page.select_one(
                'div[id*=cover-news i] h2').get_text(' ', True)
        except: title = super().title
        return title
    
    @property
    def title_tag(self):
        try:
            title_tag = self._page.select_one(
                'div[id*=cover-news i] h2').decode()
        except: title_tag = super().title_tag
        return title_tag
    
    @property
    def abstract(self):
        try: abstract = self._page.select_one('div[id*=cover-news i] .bigger-p').get_text(' ', True)
        except: abstract = super().abstract
        return abstract
    
    @property
    def abstract_tag(self):
        try: abstract_tag = self._page.select_one('div[id*=cover-news i] .bigger-p').decode()
        except: abstract_tag = super().abstract_tag
        return abstract_tag
    
    @property
    def fulltext(self):
        try:
            fulltext = ' '.join(
                map(lambda x: x.get_text(' ', True),
                    self._page.select('#single-post-content :is(p,ul,ol)')))
        except: fulltext = super().fulltext
        return fulltext
    
    @property
    def fulltext_tag(self):
        try:
            fulltext_tag = ' '.join(
                map(lambda x: x.decode(),
                    self._page.select('#single-post-content :is(p,ul,ol)')))
        except: fulltext_tag = super().fulltext_tag
        return fulltext_tag




class IcaExtractor(BaseExtractor):
    """
    Extractor for ica.gov
    """

    @property
    def title(self):
        try:
            title = self._page.select_one(
                'article h2').get_text(' ', True)
        except: title = super().title
        return title
    
    @property
    def title_tag(self):
        try:
            title_tag = self._page.select_one(
                'article h2').decode()
        except: title_tag = super().title_tag
        return title_tag
    
    @property
    def abstract(self):
        try: abstract = self._page.select_one(
            'article :is(p,ul,ol)').get_text(' ', True)
        except: abstract = super().abstract
        return abstract
    
    @property
    def abstract_tag(self):
        try: abstract_tag = self._page.select_one(
            'article :is(p,ul,ol)').decode()
        except: abstract_tag = super().abstract_tag
        return abstract_tag
    
    @property
    def fulltext(self):
        try:
            fulltext = self._page.select_one('article').find(
            'hr').fetchNextSiblings('div')[0].get_text(' ', True)
        except: fulltext = super().fulltext
        return fulltext
    
    @property
    def fulltext_tag(self):
        try:
            fulltext_tag = self._page.select_one('article').find(
            'hr').fetchNextSiblings('div')[0].decode()
        except: fulltext_tag = super().fulltext_tag
        return fulltext_tag



class MonVitiExtractor(BaseContentExtractor):
    """
    Extractor for mon-viti
    """
    
    def _content(self):
        return self._page.select('article section :is(p,ul,ol,blockquote)')
    
    @property
    def title(self):
        try:
            title = self._page.select_one(
                'article h1[class*=title i]').get_text(' ', True)
        except: title = super().title
        return title
    
    @property
    def title_tag(self):
        try:
            title_tag = self._page.select_one(
                'article h1[class*=title i]').decode()
        except: title_tag = super().title_tag
        return title_tag



class NieuweoogstExtractor(BaseExtractor):
    """
    Extractor for nieuweoogst
    """
    
    @property
    def title(self):
        try:
            title = self._page.select_one(
                '.content h1').get_text(' ', True)
        except: title = super().title
        return title
    
    @property
    def title_tag(self):
        try:
            title_tag = self._page.select_one(
                '.content h1').decode()
        except: title_tag = super().title_tag
        return title_tag
    
    @property
    def abstract(self):
        try: abstract = self._page.select_one(
            '.content p.intro').get_text(' ', True)
        except: abstract = super().abstract
        return abstract
    
    @property
    def abstract_tag(self):
        try: abstract_tag = self._page.select_one(
            '.content p.intro').decode()
        except: abstract_tag = super().abstract_tag
        return abstract_tag
    
    @property
    def fulltext(self):
        try:
            fulltext = ' '.join(
                map(lambda x: x.get_text(' ', True),
                    self._page.select('.content [id*=lightgallery i] :is(p,ul,ol)')))
        except: fulltext = super().fulltext
        return fulltext
    
    @property
    def fulltext_tag(self):
        try:
            fulltext_tag = ' '.join(
                map(lambda x: x.decode(),
                    self._page.select('.content [id*=lightgallery i] :is(p,ul,ol)')))
        except: fulltext_tag = super().fulltext_tag
        return fulltext_tag



class AgronewsExtractor(BaseExtractor):
    """
    Extractor for agronews
    """
    
    @property
    def title(self):
        try:
            title = self._page.select_one(
                'main section [class*=titlewrp i] h1').get_text(' ', True)
        except: title = super().title
        return title
    
    @property
    def title_tag(self):
        try:
            title_tag = self._page.select_one(
                'main section [class*=titlewrp i] h1').decode()
        except: title_tag = super().title_tag
        return title_tag
    
    @property
    def abstract(self):
        try: abstract = self._page.select_one(
            'main section [class*=titlewrp i] div[class*=txt i]').get_text(' ', True)
        except: abstract = super().abstract
        return abstract
    
    @property
    def abstract_tag(self):
        try: abstract_tag = self._page.select_one(
            'main section [class*=titlewrp i] div[class*=txt i]').decode()
        except: abstract_tag = super().abstract_tag
        return abstract_tag
    
    @property
    def fulltext(self):
        try:
            fulltext = ' '.join(
                map(lambda x: x.get_text(' ', True),
                    self._page.select('article [class*=desc i] :is(p,ul,ol,blockquote)')))
        except: fulltext = super().fulltext
        return fulltext
    
    @property
    def fulltext_tag(self):
        try:
            fulltext_tag = ' '.join(
                map(lambda x: x.decode(),
                    self._page.select('article [class*=desc i] :is(p,ul,ol,blockquote)')))
        except: fulltext_tag = super().fulltext_tag
        return fulltext_tag



class AnsaExtractor(BaseExtractor):
    """
    Extractor for ansa
    """
    
    @property
    def title(self):
        try:
            title = self._page.select_one(
                'header h1[class*=title i]').get_text(' ', True)
        except: title = super().title
        return title
    
    @property
    def title_tag(self):
        try:
            title_tag = self._page.select_one(
                'header h1[class*=title i]').decode()
        except: title_tag = super().title_tag
        return title_tag
    
    @property
    def abstract(self):
        try: abstract = self._page.select_one(
            'header h2[class*=news i]').get_text(' ', True)
        except: abstract = super().abstract
        return abstract
    
    @property
    def abstract_tag(self):
        try: abstract_tag = self._page.select_one(
            'header h2[class*=news i]').decode()
        except: abstract_tag = super().abstract_tag
        return abstract_tag
    
    @property
    def fulltext(self):
        try:
            fulltext = ' '.join(
                map(lambda x: x.get_text(' ', True),
                    self._page.select('div[class*=news-txt i] :is(p,ul,ol)')))
        except: fulltext = super().fulltext
        return fulltext
    
    @property
    def fulltext_tag(self):
        try:
            fulltext_tag = ' '.join(
                map(lambda x: x.decode(),
                    self._page.select('div[class*=news-txt i] :is(p,ul,ol)')))
        except: fulltext_tag = super().fulltext_tag
        return fulltext_tag

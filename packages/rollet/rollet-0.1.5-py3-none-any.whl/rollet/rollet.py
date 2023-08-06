"""
Rollet functions
"""

__all__ = [
    "get_content"
]

from datetime import datetime
from tldextract import extract
from requests.exceptions import ConnectTimeout

from rollet import settings
from rollet.utils import lookup
from rollet import extractor

def get_content(url, **kwargs):
    """
    Pull content from url to formated data
    url: string url
    timeout: float, request timeout limit. Defaut 1
    rebond: bool, perform a subquery in the main one. Default False
    fulltext: bool, extract fulltext. Default False
    :return: dict of content
    """
    use_blacklist = bool(kwargs.get('blacklist', True))
    blacklist = kwargs['blacklist'] if isinstance(kwargs.get('blacklist'), list) else settings.BLACKLIST
    ft = kwargs.get('fulltext', False)
    c_kwargs = {
        'timeout': float(kwargs.get('timeout', 1)),
        'rebond': bool(kwargs.get('rebond', False)),
    }

    content = {
        'url': url,
        'status': None,
        'title': 'blacklisted',
        'abstract': None,
        'fulltext': None,
        'lang': None,
        'content_type': None,
        'date': datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    }
    domain = extract(url).domain
    if domain in blacklist and use_blacklist: return content
    f_kwargs = settings.FETCH_KWARGS[settings.TYPES.get(domain, 'default')]
    f_kwargs = {**f_kwargs, **c_kwargs}
    extractor = lookup(
        url,
        settings.EXTRACTORS.get(domain, settings.EXTRACTORS['default']))
    extractor = extractor if extractor else extractor.BaseExtractor
    try:
        content = extractor(url, **f_kwargs).to_dict(fulltext = ft)
    except ConnectTimeout:
        content['title'] = "Timeout error"
    except Exception as e:
        content['title'] = str(e)
    return content
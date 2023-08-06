"""
Rollet settings and its methods
"""

__all__ = [
    "FULLTEXT",
    "ABSTRACT",
    "TITLE"
]

from rollet.extractor import *

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))


# CSS rules selectors for each field
FULLTEXT = (
    ':is(span,div)[class="contenuto" i]',
    'div[class*="full" i][class*="text" i] a',
    *[f'a[{attr}*="full" i][{attr}*="text" i]' for attr in ('class', 'data-ga-category')],
    *[f':is(div,section)[{attr}*="sec-" i]' for attr in ('class', 'id')],
    ':is(div,section,article)[class*="article" i][class*="section" i][class*="content" i]',
    ':is(div,section,article)[class*="full" i][class*="text" i]',
    'a[class*="pdf" i]',
    *[f'div[{attr}*="download" i] a' for attr in ('class', 'label')],
    'div[id^="Sec"]',
    *[f'div[{attr}*="{value}" i]' for attr in ('class', 'id') for value in ('article', 'content')],
    *[f':is(article,div)[{attr}*="body" i]' for attr in ('id', 'class', 'itemprop')]
)

ABSTRACT = (
    *[f':is(div,span)[class*="{value}" i]' for value in ('contenuto', 'sommario')],
    *[f':is(article,section,div)[{attr}*="blog" i][{attr}*="post" i]' for attr in ('class', 'id')],
    *[f':is(div,p)[class*="{value}" i]' for value in ('news-txt', 'desc', 'intro')],
    *[f'meta[name="{attr}" i]'
    for attr in ('description', 'twitter:description', 'citation_abstract')],
    'script[type*="json" i]',
    'meta[name="dc.description" i]',
    'meta[property="og:description" i]',
    *[f':is(div,section)[{attr}*="abs" i]' for attr in ('class', 'id')],
    'div[class*=content i]',
    *[f':is(div,section)[{attr}*="{value}" i]' for attr in ('class', 'id')
    for value in ('-abstract', 'abstract')],
    *[f'div[{attr}*="article" i][{attr}*="body" i]'
    for attr in ('class', 'itemprop')],
)

TITLE = (
    'meta[property="og:title" i]',
    *[f'meta[name="{attr}" i]'
    for attr in ('citation_title', 'dc.title', 'twitter:title', 'title')],
    'script[type*="json" i]',
    *[f':is(h1,h2,h3,div,span)[{attr}*=title i]'
    for attr in ('class', 'id', 'itemprop')],
    *[f':is(h1,h2,h3)[itemprop*=head i]'],
    'title'
)

# Domains types
types = {
    'article': [
        'agronews', 'ansa', 'berkeley', 'citrusindustry', 'europa', 'europafm',
        'europalibera', 'europapress', 'europatat', 'floraldaily',
        'freshfruitportal', 'freshplaza', 'groentennieuws', 'hortidaily',
        'hortweek', 'huffingtonpost', 'ica', 'mon-viti', 'nieuweoogst', 'nvwa',
        'oliveoiltimes', 'phytoma', 'phytoma-ldv', 'teatronaturale',
        'terrenature', 'theguardian', 'usda', 'vniikr'
    ],
    'paper': [
        'apsnet', 'biorxiv', 'chinapubmed', 'europepmc', 'mdpi', 'nature',
        'nih', 'nl', 'researchgate', 'sciencedirect', 'springer',
        'srpingeropen', 'wiley'
    ]
}
TYPES = dict(sum([[(i,k) for i in v] for k,v in types.items()], []))

# Types defaults keywords arguments for fetch
FETCH_KWARGS = {
    'default': {
        'fulltext__which': 'first',
        'fulltext__script_keys': [],
        'abstract__which': 'max',
        'abstract__script_keys': [],
        'lang__attr': 'lang',
        'title__which': 'first',
        'title__script_keys': []
    },'article': {
        'fulltext__which': 'max',
        'fulltext__script_keys': [],
        'abstract__which': 'max',
        'abstract__script_keys': ['abstract', 'summary'],
        'lang__attr': 'lang',
        'title__which': 'first',
        'title__script_keys': ['title', 'heading']
    },
    'paper': {
        'fulltext__which': 'max',
        'fulltext__script_keys': [],
        'abstract__which': 'first',
        'abstract__script_keys': ['abstract', 'summary'],
        'lang__attr': 'lang',
        'title__which': 'first',
        'title__script_keys': ['title', 'heading', 'name']
    },
}

# Blacklisted domains
with open(os.path.join(dir_path, 'blacklist'), errors = 'ignore') as f:
    BLACKLIST = list(map(lambda x:x.strip(), f.readlines()))

# Custom domains extractors
# {domain: [(schema1, Extractor1), (schema2, Extractor2)]}
EXTRACTORS = {
    'default': [(r'.*', BaseExtractor),],
    'mdpi': [(r'.*', MdpiExtractor),],
    'nih': [
        (r'/pmc/articles/', PMCExtractor),
        (r'.*', NihExtractor),],
    'sciencedirect': [(r'.*', ScienceDirectExtractor),],
    'springer': [(r'.*', SpringerExtractor),],
    'apsnet': [(r'.*', ApsNetExtractor),],
    'wiley': [(r'.*', WileyExtractor),],
    'agronews': [(r'.*', AgronewsExtractor),],
    'ansa': [(r'.*', AnsaExtractor),],
    'citrusindustry': [(r'.*', CitrusIndustryExtractor),],
    'usda': [
        (r'/aphis/newsroom/', NewsroomExtractor),
        (r'.*', UsdaExtractor),],
    'freshplaza': [(r'.*', DailyGroupExtractor),],
    'floraldaily': [(r'.*', DailyGroupExtractor),],
    'groentennieuws': [(r'.*', DailyGroupExtractor),],
    'hortidaily': [(r'.*', DailyGroupExtractor),],
    'verticalfarmdaily': [(r'.*', DailyGroupExtractor),],
    'mmjdaily': [(r'.*', DailyGroupExtractor),],
    'oliveoiltimes': [
        (r'/(business|briefs|production|world)/', OliveoilTimesExtractor),],
    'phytoma': [(r'.*', DailyGroupExtractor),],
    'freshfruitportal': [(r'.*', FreshFruitPortalExtractor),],
    'huffingtonpost': [(r'.*', HuffingtonExtractor),],
    'ica': [(r'/noticias/', IcaExtractor),],
    'mon-viti': [(r'.*', MonVitiExtractor),],
    'nieuweoogst': [(r'/nieuws/', NieuweoogstExtractor),],
    'teatronaturale': [(r'.*', TeatroNaturaleExtractor),],
    'theguardian': [(r'.*', TheGuardianExtractor),],
    'vniikr': [(r'/news/', VniikrExtractor),],
}

# Methods

def add_types(dict_types):
    """
    Add new type domains
    dict_types: dict, {type: [domain1, domain2, ...],}
    :return: None
    """
    global TYPES
    news = dict(sum([[(i,k) for i in v] for k,v in dict_types.items()], []))
    TYPES = {**TYPES, **news}


def add_fetch_kwargs(dict_types):
    """
    Add new fetch kwargs for type domains
    dict_types: dict, {type: {kwargs1:value1, kwargs2:value2,},}
    :return: None
    """
    global FETCH_KWARGS
    news = FETCH_KWARGS.copy()
    for d_type, key_args in dict_types.items():
        news[d_type] = {**news.get(d_type, news['default']), **key_args}
    FETCH_KWARGS = news.copy()
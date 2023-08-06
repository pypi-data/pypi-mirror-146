# Rollet
`Rollet` collects, standardizes and completes from various sources.

[![PyPI](https://img.shields.io/pypi/v/Rollet?logo=PyPI&style=for-the-badge&labelColor=%233775A9&logoColor=white)](https://pypi.org/project/rollet/)
![PyPI - Status](https://img.shields.io/pypi/status/rollet?style=for-the-badge)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/rollet?logo=python&logoColor=yellow&style=for-the-badge)](https://pypi.org/project/rollet/)



# Installation
## Pypi
The safest way to install `rollet` is to go through pip
```bash
python -m pip install rollet
```

# How to use?
## Command script

```properties
rollet {extract-txt,extract-csv,extract-json} path
       [-h] [-o [OUTFILE]] [-l [LINK]] [-f [FIELDS]] [--start [START]]
       [--size [SIZE]] [-t [TIMESLEEP]] [--timeout [TIMEOUT]]
       [--blacklist [BLACKLIST]]
```
```console
positional arguments:
  {extract-txt,extract-csv,extract-json} Choose file type option extraction
  path                                   file path

optional arguments:
  -h, --help                    show this help message and exit
  -o [OUTFILE], --outfile       output file path
  -l [LINK], --link             link field if csv or json
  -f [FIELDS], --fields         fields to keep separated by comma
  --start [START]               number of rows to skip
  --size [SIZE]                 max number of rows to keep
  -t [TIMESLEEP], --timesleep   sleep time in seconds between two pulling
  --timeout [TIMEOUT]           Max GET request timeout in second
  --blacklist [BLACKLIST]       0 (do not use), 1 (use), path (one column domain blacklist file)
```

## Python
### Basic usage
```python
from rollet import get_content
from rollet.extractor import BaseExtractor

url = 'https://example.url.com/content-id'

content_dict = get_content(url)

content_object = BaseExtractor(url)
content_object.title            # Title
content_object.abstract         # Abstract
content_object.lang             # Language
content_object.content_type     # Type (pdf, json, html, ...)
content_object.to_dict()        # Same as get_content
```

### Custom extractors
```python
class CustomExtractor(BaseExtractor):
    
    @property
    def title(self):
        return self._page.find('title')
```

### PDF extractors
PDF extraction require [Grobid service](https://grobid.readthedocs.io/en/latest/Grobid-service/).  
Assuming Grobid API runs on `http://localhost:8070`
```python
from rollet import grobid_service, get_content
from rollet.extractor import PDFExtractor

grobid_service('localhost', '8070')

url = 'https://example.url.com/pdf-content-id'

content_dict = get_content(url)

pdf_content_object = PDFExtractor(url)
```
Reading PDF with `BaseExtractor` will instanciate PDFExtractor object.


And More!
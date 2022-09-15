#!/usr/bin/env python3

import datetime
import re
import requests
import unicodedata

def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

response = requests.get("https://v1.nocodeapi.com/chrisroat/medium/ZmFgonONWEJJfAuy")
data = response.json()

TEMPLATE = """---
title: %(title)s
date: %(date)s
publication: '*Medium*'
publication_link: "https://medium.com"
external_link: "%(link)s"
---
"""

for item in data:
    slug = slugify(item['title'])
    ts = datetime.date.fromtimestamp(item['created'] / 1000)
    item['date'] = ts.isoformat()
    
    with open(f'../content/post/{slug}.md', 'w') as f:
        f.write(TEMPLATE % item)
    
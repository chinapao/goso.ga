# -*- coding: utf-8 -*-

"""
 Baidu (Images)

 @website     https://image.baidu.com/
 @provide-api no

 @using-api   no (because of query limit)
 @results     HTML (using search portal)
 @stable      no (HTML can change)
 @parse       url, title, img_src
"""

from json import loads
from searx.url_utils import urlencode
import re

# engine dependent config
categories = ['images']
paging = True
language_support = False

# search-url
base_url = 'https://image.baidu.com/'
search_string = 'search/acjson?tn=resultjson_com&ipn=rj&istype=2&ie=utf-8&{query}&pn={offset}'
image_length = 20


# do search-request
def request(query, params):
    offset = (params['pageno'] - 1) * image_length

    search_path = search_string.format(
        query=urlencode({'word': query}),
        offset=offset)

    params['url'] = base_url + search_path

    return params


# get response from search-request
def response(resp):
    from searx.webapp import sentry
    use_resp = resp.content
    try:
        resultdic = loads(use_resp)
    except Exception:
        resultdic = loads(re.sub(r'(?<!\\)\\(?!["\\/bfnrt]|u[0-9a-fA-F]{4})', r'', resp.text).encode(encoding="utf-8"))
    resultlist = resultdic["data"]
    results = []

    for image in resultlist:
        try:
            url = image["replaceUrl"][0]["FromURL"]
            title = image["fromPageTitle"].replace("<strong>", "").replace("</strong>", "")
            thumbnail = image["thumbURL"]
            img_src = image["thumbURL"]
            width = image["width"]
            height = image["height"]

            # append result
            results.append({'template': 'images.html',
                            'url': url,
                            'title': title,
                            'content': '',
                            'thumbnail_src': thumbnail,
                            'width': width,
                            'height': height,
                            'img_src': img_src})
        except Exception as e:
            sentry.captureException()

    # return results
    return results

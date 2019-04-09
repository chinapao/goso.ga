# -*- coding: utf-8 -*-

"""
 360sousuo (Images)
 @website     https://image.so.com/
 @provide-api no

 @results     HTML (using search portal)
 @stable      no (HTML can change)
 @parse       url, title, img_src
"""

from json import loads
from searx.url_utils import urlencode

# engine dependent config
categories = ['images']
paging = True

# search-url
base_url = 'https://image.so.com/'
search_string = 'j?{query}&sn={offset}'


# do search-request
def request(query, params):
    offset = (params['pageno'] - 1) * 18

    search_path = search_string.format(
        query=urlencode({'q': query}),
        offset=offset)

    params['url'] = base_url + search_path

    return params


# get response from search-request
def response(resp):
    from searx.webapp import sentry
    resultdic = loads(resp.text)
    resultlist = resultdic["list"]
    results = []

    for image in resultlist:
        try:
            url = image["link"]
            title = image["title"].replace("<em>", "").replace("</em>", "")
            thumbnail = image["thumb"]
            img_src = image["img"]
            width = image["width"]
            height = image["height"]

            # append result
            results.append({'template': 'images.html',
                            'url': url,
                            'title': title,
                            'content': '',
                            'thumbnail_src': thumbnail,
                            'img_src': img_src,
                            'width': width,
                            'height': height})
        except Exception:
            sentry.captureException()

    # return results
    return results

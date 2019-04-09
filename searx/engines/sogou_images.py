# -*- coding: utf-8 -*-

"""
 Sogou (Images)

 @website     https://pic.sogou.com/
 @provide-api no

 @using-api   no
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
base_url = 'https://pic.sogou.com/'
search_string = 'pics?{query}&start={offset}&mode=1&reqType=ajax&len={imageLen}'
image_length = 20


# do search-request
def request(query, params):
    offset = (params['pageno'] - 1) * image_length

    search_path = search_string.format(
        query=urlencode({'query': query}),
        offset=offset,
        imageLen=image_length)

    params['url'] = base_url + search_path

    return params


# get response from search-request
def response(resp):
    from searx.webapp import sentry
    unicode_resp = resp.text
    utf8resp = unicode_resp.encode('utf8')
    resultdic = loads(utf8resp)
    resultlist = resultdic["items"]
    results = []

    for image in resultlist:
        try:
            url = image["page_url"]
            title = image["title"]
            thumbnail = image["thumbUrl"]
            img_src = image["pic_url"]
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
        except Exception:
            sentry.captureException()

    # return results
    return results

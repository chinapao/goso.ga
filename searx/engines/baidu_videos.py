# -*- coding: utf-8 -*-

"""
 Baidu (Videos)

 @website     https://v.baidu.com
 @provide-api no

 @using-api   no
 @results     HTML
 @stable      no
 @parse       url, title, content, thumbnail
"""

from lxml import html
from searx.url_utils import urlencode

categories = ['videos']
paging = True
safesearch = False
number_of_results = 10
language_support = False
imageLength = 20

search_url = 'https://v.baidu.com/v?rn={imagelength}&pn={offset}&ie=utf-8&{query}'


# do search-request
def request(query, params):
    offset = (params['pageno'] - 1) * imageLength
    # query and paging
    params['url'] = search_url.format(query=urlencode({'word': query}),
                                      offset=offset,
                                      imagelength=imageLength)

    return params


# get response from search-request
def response(resp):
    from searx.webapp import sentry
    results = []

    dom = html.fromstring(resp.text)

    for result in dom.xpath('//li[@class="result"]'):
        try:
            url = result.xpath('./a')[0].attrib.get('href')
            title = result.xpath('./a')[0].attrib.get('title')
            content = title
            thumbnail = result.xpath('.//div[@class="view"]/img[@class="img-blur-layer"]')[0].attrib.get('src')

            results.append({'url': url,
                            'title': title,
                            'content': content,
                            'thumbnail': thumbnail,
                            'template': 'videos.html'})
        except Exception:
            sentry.captureException()

        if len(results) >= imageLength:
            break

    return results

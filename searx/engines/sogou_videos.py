# -*- coding: utf-8 -*-

"""
 sogou (Videos)

 @website     https://v.sogou.com
 @provide-api no
 @using-api   no
 @results     HTML
 @stable      no
 @parse       url, title, content, thumbnail
"""

from lxml.html.soupparser import fromstring

from searx.url_utils import urlencode

categories = ['videos']
paging = True

search_url = 'https://v.sogou.com/v?{query}&page={offset}'


# do search-request
def request(query, params):
    offset = params['pageno']

    # query and paging
    params['url'] = search_url.format(query=urlencode({'query': query}),
                                      offset=offset)

    return params


# get response from search-request
def response(resp):
    from searx.webapp import sentry
    results = []

    dom = fromstring(resp.text)

    for result in dom.xpath('//div[@class="srch-all-result"]//li[@class="sort_lst_li"]'):
        try:
            url = 'https://v.sogou.com' + result.xpath('./a')[0].attrib.get('href')
            title = result.xpath('./a')[0].attrib.get('title')
            content = title
            thumbnail = result.xpath('./a/img')[0].attrib.get('src')

            results.append({'url': url,
                            'title': title,
                            'content': content,
                            'thumbnail': thumbnail,
                            'template': 'videos.html'})
        except:
            sentry.captureException()

    return results

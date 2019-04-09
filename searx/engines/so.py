# -*- coding: utf-8 -*-

"""
 360 so (Web)

 @website     https://www.so.com
 @provide-api no
 @results     HTML (using search portal)
 @stable      no (HTML can change)
 @parse       url, title, content
"""

from lxml import html
from searx.engines.xpath import extract_text
from searx.url_utils import urlencode
from searx.utils import gen_useragent, new_hmac
from searx import settings
from urllib import parse


# engine dependent config
categories = ['general']
paging = True
language_support = False

# search-url
base_url = 'https://www.so.com/'
search_string = 's?{query}&pn={offset}'


# do search-request
def request(query, params):
    offset = params['pageno']

    search_path = search_string.format(
        query=urlencode({'q': query}),
        offset=offset)

    params['url'] = base_url + search_path

    params['headers']['User-Agent'] = gen_useragent('Windows NT 6.3; WOW64')

    return params


# get response from search-request
def response(resp):
    from searx.webapp import sentry
    results = []
    dom = html.fromstring(resp.text)

    try:
        results.append({'number_of_results': int(dom.xpath('//span[@class="nums"]/text()')[0]
                                                 .split(u'\u7ea6')[1].split(u'\u4e2a')[0].replace(',', ''))})
    except Exception:
        sentry.captureException()

    # parse results
    for result in dom.xpath('//li[@class="res-list"]'):
        try:
            title = extract_text(result.xpath('.//h3')[0])
            url = result.xpath('.//h3/a')[0].attrib.get('href')
            try:
                if result.xpath('.//p[@class="res-desc"]'):
                    content = extract_text(result.xpath('.//p[@class="res-desc"]'))
                if result.xpath('.//div[starts-with(@class,"res-rich")]'):
                    content = extract_text(result.xpath('.//div[starts-with(@class,"res-rich")]'))
                if result.xpath('.//div[@class="cont mh-pc-hover"]'):
                    content = extract_text(result.xpath('.//div[@class="cont mh-pc-hover"]'))
                if result.xpath('.//div[@class="g-card g-shadow"]'):
                    content = extract_text(result.xpath('.//div[@class="g-card g-shadow"]'))
                if result.xpath('.//p[@class="mh-more"]'):
                    content = extract_text(result.xpath('.//p[@class="mh-more"]'))
            except Exception:
                content = ''
                sentry.captureException()

            # append result
            if 'www.so.com/link?' in url:
                url = settings['result_proxy'].get('server_name') + "/url_proxy?proxyurl=" + parse.quote(
                    url) + "&token=" + new_hmac(settings['result_proxy']['key'], url.encode("utf-8"))
                try:
                    showurl = extract_text(result.xpath(".//p[@class='res-linkinfo']/cite"))
                    if len(showurl) == 0:
                        showurl = url
                except Exception:
                    showurl = url
                    sentry.captureException()
            else:
                showurl = url
            results.append({'url': url,
                            'showurl': showurl,
                            'title': title,
                            'content': content})
            content = ''
        except Exception:
            sentry.captureException()

    # return results
    return results

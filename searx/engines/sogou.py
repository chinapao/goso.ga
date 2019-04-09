from lxml import html
from searx.engines.xpath import extract_text
from searx.url_utils import urlencode
from searx.utils import gen_useragent, new_hmac
from searx import settings
import re


# engine dependent config
categories = ['general']
paging = True
language_support = True

# search-url
base_url = 'https://www.sogou.com/'
search_string = 'web?{query}&page={offset}'

"""
The regex patterns in this gist are intended only to match web URLs -- http,
https, and naked domains like "example.com".
"""
WEB_URL_REGEX = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""


# do search-request
def request(query, params):
    offset = params['pageno']

    search_path = search_string.format(
        query=urlencode({'query': query}),
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
        results.append({'number_of_results': int(dom.xpath('//p[@class="num-tips"]/text()')[0]
                                                 .split(u'\u7ea6')[1].split(u'\u6761')[0].replace(',', ''))})
    except Exception:
        sentry.captureException()

    # parse results
    try:
        for result in dom.xpath('//div[@class="vrwrap"]'):
            try:
                url = result.xpath('.//a')[0].attrib.get('href') if result.xpath('.//a')[0].attrib.get(
                    'href').startswith("http") else "https://sogou.com" + result.xpath('.//a')[0].attrib.get('href')
                # parse weixin.sogou html
                if "http://weixin.sogou.com/" == url.strip():
                    url = result.xpath('.//div[@class="str-pd-box str-pd-none"]//a')[0].attrib.get('href')
                    title = extract_text(
                        result.xpath('.//div[@class="str-pd-box str-pd-none"]//p[@class="str_time"]/a')[0])
                    content = extract_text(
                        result.xpath('.//div[@class="str-pd-box str-pd-none"]//p[@class="str_info"]')[0])
                else:
                    title = extract_text(result.xpath('.//h3/a')[0])
                    content = extract_text(result.xpath('.//div')[0])

                if 'sogou.com/link?url' in url:
                    url = settings['result_proxy'].get('server_name') + "/url_proxy?proxyurl=" + \
                        url + "&token=" + new_hmac(settings['result_proxy']['key'], url.encode("utf-8"))
                    showurl = re.findall(WEB_URL_REGEX, extract_text(result.xpath('.//div[@class="fb"]')))[0]
                    showurl = showurl.lstrip('.')
                else:
                    showurl = url

                # append result
                results.append({'url': url,
                                'showurl': showurl,
                                'title': title,
                                'content': content})
            except Exception:
                sentry.captureException()
                continue

    except Exception as e:
        sentry.captureException()

    try:
        for result in dom.xpath('//div[@class="rb"]'):
            try:
                url = result.xpath('.//a')[0].attrib.get('href') if result.xpath('.//a')[0].attrib.get(
                    'href').startswith("http") else "https://sogou.com" + result.xpath('.//a')[0].attrib.get('href')
                # to parse sogou weixin html
                if "http://weixin.sogou.com/" == url.strip():
                    url = result.xpath('.//div[@class="str-pd-box str-pd-none"]//a')[0].attrib.get('href')
                    title = extract_text(
                        result.xpath('.//div[@class="str-pd-box str-pd-none"]//p[@class="str_time"]/a')[0])
                    content = extract_text(
                        result.xpath('.//div[@class="str-pd-box str-pd-none"]//p[@class="str_info"]')[0])
                else:
                    title = extract_text(result.xpath('.//h3/a')[0])
                    content = extract_text(result.xpath('.//div')[0])

                if 'sogou.com/link?url' in url:
                    url = settings['result_proxy'].get('server_name') + "/url_proxy?proxyurl=" + \
                        url + "&token=" + new_hmac(settings['result_proxy']['key'], url.encode("utf-8"))
                    showurl = re.findall(WEB_URL_REGEX, extract_text(result.xpath('.//div[@class="fb"]')))[0]
                    showurl = showurl.lstrip('.')
                else:
                    showurl = url

                results.append({'url': url,
                                'showurl': showurl,
                                'title': title,
                                'content': content})
            except Exception as e:
                sentry.captureException()
                continue

    except Exception as e:
        sentry.captureException()

    # return results
    return results
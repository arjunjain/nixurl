import json
import urllib
import urllib2


def shorten(url):
    gurl = 'http://goo.gl/api/url?url=%s' % urllib.quote(url)
    req = urllib2.Request(gurl, data='')
    req.add_header('User-Agent','toolbar')
    results = json.load(urllib2.urlopen(req))
    return results['short_url']
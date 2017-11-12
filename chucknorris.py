import json
import sys
if sys.version < '3':
    from urllib2 import urlopen
    from urllib import quote as urlquote
else:
    from urllib.request import urlopen
    from urllib.parse import quote as urlquote

# chuck norris database API
CND_RANDOM_URL = 'http://api.icndb.com/jokes/random'


class ChuckNorrisDefinition(object):

    def __init__(self, id, joke):
        self.id = id
        self.joke = joke

    def __str__(self):
        return "%s" % (self.joke)


def _get_chuckn_json(url, fname, lname):
    url = url + "?firstName=%s&lastName=%s" % (fname, lname)
    f = urlopen(url)
    data = json.loads(f.read().decode('utf-8'))
    f.close()
    return data


def _parse_chuckn_json(json, check_result=True):
    if json is None or any(e in json for e in ('error', 'errors')):
        raise ValueException('CN: Invalid input for Chuck Norris API')
    if check_result and json['type'] != 'success':
        return []
    data = json['value']
    d = ChuckNorrisDefinition(
        data['id'],
        data['joke']
    )
    return d


def random(fname='Chuck', lname='Norris'):
    """Return random joke"""
    json = _get_chuckn_json(CND_RANDOM_URL, fname, lname)
    return _parse_chuckn_json(json, check_result=False)

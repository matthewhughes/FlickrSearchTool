import json
import sys
from flickrapi import FlickrAPI, shorturl
import scraperwiki
from collections import OrderedDict

API_KEY = "8812d02940ff6669b30904b807ecc49b"
flickr = FlickrAPI(API_KEY)


UNIQUE_KEYS = ['id']

class InvalidArgumentError(Exception):
    pass

def main():
     try:
        if len(sys.argv) != 2:
            raise InvalidArgumentError("Please supply a single argument. An example would be 'kittens'")
        else:
            search_flickr(sys.argv[1])

    except Exception, e:
        scraperwiki.status('error', type(e).__name__)
        print json.dumps({
            'error': {
                'type': type(e).__name__,
                'message': str(e),
                'trace': traceback.format_exc()
            }
        })

    else:
        scraperwiki.status('ok')
        print json.dumps({
            'success': {
                'type': 'ok',
                'message': "Saved Flickr photo information"
            }
        })

def search_flickr(searchvalue):
    favs = flickr.walk(tags=searchvalue, extras="geo")
    rows = []
    for photo in favs:
        if photo.get('latitude') != '0':
            row = OrderedDict()
            row['id'] = photo.get('id')
            row['title'] = photo.get('title')
            row['latitude'] = float(photo.get('latitude'))
            row['longitude'] = float(photo.get('longitude'))
            row['url'] = shorturl.url(photo.get('id'))
            rows.append(row)
    submit_to_scraperwiki(rows, searchvalue)

def submit_to_scraperwiki(rows, tablename):
    scraperwiki.sqlite.save(UNIQUE_KEYS, rows, tablename )


if __name__ == '__main__':
    main()

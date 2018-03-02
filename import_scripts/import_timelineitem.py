

import os
import csv
import json
import codecs
from common import create_fixture, CODE_DIR, MEDIA_DIR, BASE
from common import sh, load_fixture, ENCODING, DELIMITER, DELIMITER, DELIMITER, DELIMITER
from common import to_date

BASE = os.path.join(BASE,  'Harta Karun/HK Intro and Categories/HK Timeline/')
FN = 'hartaKarunTimelineItemInstance.csv'
MODEL = 'dasa.timelineitem'
#IMAGES_DIR = os.path.join(BASE, HARTAKARUN )
#/home/jelle/Dropbox/DASA POC Gerbrandy/Testdata/retrobooks/RB items/1 Corpus Diplomaticum/
IMAGES_DIRS = os.listdir(BASE)
IMAGES_DIRS = dict([(x.split()[0], x) for x in IMAGES_DIRS if x.split()[0] in [str(i) for i in range(0, 20)]])

MAP_FIELDS_TO_MODEL= {
    'ID':'pk',
	'year':'year',
	'month':'month',
	'day':'day',
	'captionENG':'caption_en',
	'captionBAH':'caption_id',
}

OUT_FN = out_fn = os.path.abspath('%s.json' % MODEL)

def read_items():
    fn = os.path.join(BASE, FN)
#    images_dir = os.path.join(BASE, HARTAKARUN, 'HK Category Images')
    lines = csv.reader(codecs.open(fn, encoding=ENCODING), delimiter=DELIMITER)
    lines = list(lines)
    records = []
    headers = lines[0]
    print headers
    headers = [MAP_FIELDS_TO_MODEL[k] for k in headers]
    for i, l in enumerate(lines[1:]):
        l = [unicode(x) for x in l]
        r = dict(zip(headers, l))
#        r['date'] = '%(year)s-%(month)s-%(day)s' % r
        for k, v in r.items():
            if k in ['day', 'month', 'year']:
                if r[k]:
	                r[k] = int(r[k])
                else:
                    r[k] = None

        records.append(r)
        
    for x in records:
        print x
    print headers
    return records
 
 
def load_items():
    data = read_items()
    create_fixture(model=MODEL, data=data, out_fn=out_fn)
    load_fixture(out_fn)


if __name__ == '__main__':
    load_items()

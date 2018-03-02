

import os
import csv
import json
import codecs
from common import create_fixture, CODE_DIR, MEDIA_DIR, BASE, sh, load_fixture
BASE = os.path.join(BASE,  'retrobooks/RB items')
FN = 'retrobookInstance.csv'
ENCODING = 'utf8'
DELIMITER = ','
MODEL = 'dasa.retrobook'
OUT_FN = 'fixtures/retrobook.json'
#IMAGES_DIR = os.path.join(BASE, HARTAKARUN )

MAP_FIELDS_TO_MODEL= {
	'ID':'pk',
	'shortTitleDUT':'short_title_dutch',
	'shortTitleENG':'short_title_en',
	'shortTitleBAH':'short_title_id',
	'fullTitleDUT': 'full_title_dutch',
	'fullTitleENG': 'full_title_en',
	'fullTitleBAH': 'full_title_id',
	'author': 'author',
	'placePublication': 'publication_place',
	'yearPublication': 'publication_year',
	'originalLanguageENG': 'original_language_en',
	'originalLanguageBAH': 'original_language_id',
	'shortSummaryENG': 'short_summary_en',
	'shortSummaryBAH': 'short_summary_id', 
	'commentsENG': 'comments_en',
	'commentsBAH': 'comments_id',
	'citationString': 'citation',
}

def read_items():
    fn = os.path.join(BASE, FN)
#    images_dir = os.path.join(BASE, HARTAKARUN, 'HK Category Images')
    lines = csv.reader(codecs.open(fn, encoding=ENCODING), delimiter=DELIMITER)
    lines = list(lines)
    records = []
    headers = lines[0]
    print headers
    headers = [MAP_FIELDS_TO_MODEL[k] for k in headers]
    for l in lines[1:]:
        l = [unicode(x) for x in l]
        r = dict(zip(headers, l))
        for k, v in r.items():
        	if len(v) > 255:
        		print k, v
        records.append(r)
        
    for x in records:
        print x
    print headers
    return records
   
 
def load_items():
	data = read_items()
	out_fn = os.path.abspath(OUT_FN)
	create_fixture(model=MODEL, data=data, out_fn=out_fn)
	load_fixture(out_fn)


if __name__ == '__main__':
	load_items()


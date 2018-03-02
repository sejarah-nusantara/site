

import os
import csv
import json
import codecs
from common import create_fixture, CODE_DIR, MEDIA_DIR, BASE, sh, load_fixture, ENCODING, DELIMITER, DELIMITER, DELIMITER, DELIMITER
from common import to_date  
raise Exception('JOURNALENTRyCLASS is not to be imported int he DB - it s is a fragment of the archive description')
BASE = os.path.join(BASE,  '2nd entry daily journals')
FN = 'journalEntryPointerClass.csv'
MODEL = 'dasa.journalentryclass'
OUT_FN = 'fixtures/%s.json'  % MODEL
#IMAGES_DIR = 'Daily Journals Folio Images' 
#/home/jelle/Dropbox/DASA POC Gerbrandy/Testdata/retrobooks/RB items/1 Corpus Diplomaticum/

MAP_FIELDS_TO_MODEL= {
'ID':'pk',
'fullNameENG':'full_name_en',
'shortNameENG':'short_name_en',
'periodStartYear':'period_start',
'periodEndYear':'period_end',
'summaryENG': 'summary_en',
'fileGroup ':'filegroup',
'publicENG': 'public_en',
'digitalENG': 'digital_en',
'authorizedENG': 'authorized_en',
'explanationENG': 'explanation_en',
'historyInstituteENG': 'history_institute_en',
'historyArchiveENG': 'history_archive_en',
'contentsENG': 'contents_en',
'usageENG': 'usage_en',
'author ': 'author',
'yearCreated ': 'year_created',
'colofonENG': 'colofon_en',

}

from import_resolutionpointerinstance import OUT_FN as resolution_json 
import json
def read_resolutions():    
    resolutions =  json.load(open(resolution_json))
    resolutions = dict([(x['fields']['file'], x) for x in resolutions])
    return resolutions
    
    
def read_items():
    fn = os.path.join(BASE, FN)
#    images_dir = os.path.join(BASE, HARTAKARUN, 'HK Category Images')
    lines = csv.reader(codecs.open(fn, encoding=ENCODING), delimiter=DELIMITER)
    lines = list(lines)
    records = []
    headers = [l[0] for l in lines]
    values  = [l[1] for l in lines]
    print headers
    headers = [MAP_FIELDS_TO_MODEL[k] for k in headers]
    resolutions = read_resolutions()
    lines = [headers, values]
    
    
    for i, l in enumerate(lines[1:]):
        
        l = [unicode(x) for x in l]
        r = dict(zip(headers, l))
        for k, v in r.items():
            if 'date' in k or 'time' in k:
                r[k] = to_date(v)

            if len(v) > 255:
                print k
                print v
                print '-' * 20
        
        r['pk'] = str(i + 1)
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

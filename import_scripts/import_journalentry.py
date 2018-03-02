

import os
import csv
import json
import codecs
from common import create_fixture, CODE_DIR, MEDIA_DIR, BASE, sh, load_fixture, ENCODING, DELIMITER, DELIMITER, DELIMITER, DELIMITER
from common import to_date  
BASE = os.path.join(BASE,  '2nd entry daily journals')
FN = 'journalEntryPointerInstance.csv'
MODEL = 'dasa.journalentry'
OUT_FN = 'fixtures/%s.json'  % MODEL
IMAGES_DIR = 'Daily Journals Folio Images' 
#/home/jelle/Dropbox/DASA POC Gerbrandy/Testdata/retrobooks/RB items/1 Corpus Diplomaticum/

MAP_FIELDS_TO_MODEL= {
'ID':'pk',
 'journalEntryDescription':'description',
 'journalEntryDate':'date',
 'journalEntryPriority':'priority',
 'journalEntryFromFolioNumber':'folio_number_from',
 'journalEntryToFolioNumber':'folio_number_to',
 'journalEntryAnnotation':'annotation',
 'institutionID':'institution',
 'fondsID':'fonds',
 'fileID': 'file_id',

}

from import_resolutionpointerinstance import OUT_FN as resolution_json 
import json

    
    
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
            if 'date' in k or 'time' in k:
                r[k] = to_date(v)

        
        
        r['journalentry_class'] = '1' #
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

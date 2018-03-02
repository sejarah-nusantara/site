

import os
import csv
import json
import codecs
from common import create_fixture, CODE_DIR, MEDIA_DIR, BASE, sh, load_fixture, ENCODING, DELIMITER, DELIMITER, DELIMITER, DELIMITER
from common import to_date  
from common import Importer
BASE = os.path.join(BASE,  '2nd entry resolutions')
FN = 'duplicateScanInstance_RES.csv'
MODEL = 'dasa.retrobookscan'
OUT_FN = 'fixtures/resolutionscan.json'
IMAGES_DIR = 'Resolutions Folio Images' 
#/home/jelle/Dropbox/DASA POC Gerbrandy/Testdata/retrobooks/RB items/1 Corpus Diplomaticum/

MAP_FIELDS_TO_MODEL= {
'ID':'pk',
'retrobookInstanceID':'retrobook',
 'scanSequenceNumber':'position',
 'scanPageNumber':'pagenumber',
 'scanContentImageReference':'image',
 'scanCreator':'creator',
 'scanContributor':'contributor',
 'scanPublisher':'publisher',
 'scanRights': 'rights',
 'scanURI':'URI',
 'scanDate':'date',
 'scanFormat': 'format',
 'scanLanguageENG':'language_en',
 'scanTypeENG': 'type_en',
 'scanSourceENG': 'source_en',
 'scanTitleENG': 'title_en',
 'scanTimeFrameFrom': 'time_frame_from',
 'scanTimeFrameTo': 'time_frame_to',
 'scanKeywordsENG': 'keywords_en',
 'scanTranscription' : 'transcription',
 'scanTranslationENG': 'translation_en',
 'scanTranslationBAH': 'translation_id',
 'scanAuthorTranscription':'transcription_author',
 'scanAuthorTranslationENG': 'translation_author_english',
 'scanAuthorTranslationBAH': 'translation_author_bahassa',
 'scanDateTranscription': 'transcription_date',
 'scanDateTranslationENG': 'translation_en',
 'scanDateTranslationBAH': 'translation_id',
 'scanRelation': 'relation',
 'institutionID': 'institution',
  'fondsID': 'fonds',
 'fileID': 'file_id',
 'scanFolioNumber': 'folio_number',
# 'scanContentImageReference',
# 'scanCreator',
# 'scanContributor',
# 'scanPublisher',
# 'scanRights',
# 'scanURI',
# 'scanDate',
# 'scanFormat',
# 'scanLanguageENG',
# 'scanTypeENG',
# 'scanSourceENG',
# 'scanTitleENG',
# 'scanTimeFrameFrom',
# 'scanTimeFrameTo',
 'scanSubjectENG': 'subject_en',
# 'scanTranscription',
# 'scanTranslationENG',
# 'scanTranslationBAH',
}

#from import_resolutioninstance import OUT_FN as resolution_json 
resolution_json = 'fixtures/dasa.resolution.json'
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
    headers = lines[0]
    print headers
    headers = [MAP_FIELDS_TO_MODEL[k] for k in headers]
    resolutions = read_resolutions()
    
    for l in lines[1:]:
        l = [unicode(x) for x in l]
        r = dict(zip(headers, l))
        for k, v in r.items():
            if 'date' in k or 'time' in k:
                r[k] = to_date(v)

        
        img_fn = r['image']
        img_src = os.path.join(BASE, IMAGES_DIR, img_fn)
        assert os.path.exists(img_src), img_src
        
        img_dst_folder = os.path.join(MEDIA_DIR, IMAGES_DIR) 
        img_dst = os.path.join(img_dst_folder, img_fn)
        if not os.path.exists(img_dst_folder):
            os.makedirs(os.path.join(img_dst_folder))  
        if not os.path.exists(img_dst) :
            cmd = 'cp "%s" "%s"' % (img_src, img_dst)
            print cmd
            sh(cmd)
        r['image'] = os.path.join(IMAGES_DIR, img_fn)                
        
        
        try:
	        resolution = resolutions[r['file_id']]
	    	r['resolution'] = resolution['pk']  
    	except KeyError:
	    	r['resolution'] = None
	    
        
        
        records.append(r)
        
    for x in records:
        print x
    print headers
    return records
   
class ScanImporter(Importer): 
    model =MODEL
    
def load_items():
    data = read_items()
    out_fn = os.path.abspath(OUT_FN)
    create_fixture(model=MODEL, data=data, out_fn=out_fn)
    importer = ScanImporter()
    importer.load_fixture(out_fn)


if __name__ == '__main__':
    load_items()

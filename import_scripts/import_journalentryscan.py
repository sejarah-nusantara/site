

import os
import csv
import codecs
from common import create_fixture, CODE_DIR, MEDIA_DIR, BASE, sh, load_fixture, ENCODING, DELIMITER, DELIMITER, DELIMITER, DELIMITER
from common import to_date  
from common import Importer 
BASE = os.path.join(BASE,  '2nd entry daily journals')
#OUT_FN = 'fixtures/%s.json' % MODEL
#/home/jelle/Dropbox/DASA POC Gerbrandy/Testdata/retrobooks/RB items/1 Corpus Diplomaticum/

import json
class JournalScansImporter(Importer):
    source_fn = os.path.join(BASE, 'duplicateScanInstance_DJ.csv')
    model = 'dasa.retrobookscan'
    
    IMAGES_DIR = 'Daily Journals Folio Images'
#    IMAGES_DIRS = [IMAGES_DIR]
    
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
        
    def postproduction(self, records):
        IMAGES_DIR = self.IMAGES_DIR
        for r in records:
            for k, v in r.items():
                if 'date' in k or 'time' in k:
                    if r[k]:
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
            print r['image']
                
             
            from import_journalentry import OUT_FN as fn_journalentries_json 
            journalentries =  json.load(open(fn_journalentries_json))
            for je in journalentries:
                fr = je['fields']['folio_number_from']
                fr = int(fr)
                to = je['fields']['folio_number_to']
                to = int(to)
                if fr <=  int(r['folio_number']) <= to:
                    r['journalentry'] = je['pk']
        return records
                
            


if __name__ == '__main__':
    JournalScansImporter().load_items()
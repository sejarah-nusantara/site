

import os
import csv
import json
import codecs
from common import create_fixture, CODE_DIR, MEDIA_DIR, BASE, sh, load_fixture, ENCODING, DELIMITER, DELIMITER, DELIMITER, DELIMITER
from common import Importer 

class RetroBookScanImporter(Importer):
    
#    source_fn = os.path.join(BASE,  'retrobooks/RB items', 'retrobookScanInstance.csv')
    source_fn = os.path.join(BASE,  'retrobooks/RB items', 'duplicateScanInstance_RB_20120524.csv')
    model = 'dasa.retrobookscan'
    #/home/jelle/Dropbox/DASA POC Gerbrandy/Testdata/retrobooks/RB items/1 Corpus Diplomaticum/
    IMAGES_DIRS = os.listdir(os.path.join(BASE,'retrobooks/RB items'))
    IMAGES_DIRS = dict([(x.split()[0], x) for x in IMAGES_DIRS if x.split()[0] in [str(i) for i in range(0, 20)]])

    MAP_FIELDS_TO_MODEL= {
        'ID':'pk',
        'institutionID': 'institution',
        'fondsID': 'fonds',
        'fileID': 'file_id',
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
        'scanSubjectENG':'keywords_en',
        'scanTypeENG': 'type_en',
        'scanSourceENG': 'source_en',
        'scanTitleENG': 'title_en',
        'scanTimeFrameFrom': 'time_frame_from',
        'scanTimeFrameTo': 'time_frame_to',
#        'scanKeywordsENG': 'keywords_en',
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
        'scanFolioNumber': 'folio_number',
    }
    
    def postproduction(self, records): 
        IMAGES_DIRS = self.IMAGES_DIRS
        print IMAGES_DIRS
        fn = os.path.join(BASE,  'retrobooks/RB items', 'retrobookDuplicateScanReferenceInstance_20120524.csv')
        lines = csv.reader(codecs.open(fn, encoding=ENCODING), delimiter=DELIMITER)
        scanid2retrobookid = dict([(l[2], l[1]) for l in lines])
        for i in range(0, len(records)):
            r = records[i]
            r['retrobook'] = scanid2retrobookid[r['pk']]
            if int(r['retrobook']) >= 5:
                r['retrobook'] = None                
            
            if r['retrobook']:
                img_fn = r['image']
                img_src = os.path.join(BASE,'retrobooks/RB items', IMAGES_DIRS[r['retrobook']], 'CD FolioImages', img_fn)
                img_dst_folder = os.path.join(MEDIA_DIR, IMAGES_DIRS[r['retrobook']], 'CD FolioImages') 
                if not os.path.exists(img_src):
                    print 'could not find', img_src
                img_dst = os.path.join(img_dst_folder, img_fn)
                print img_dst
                if not os.path.exists(img_dst) :
                    cmd = 'cp "%s" "%s"' % (img_src, img_dst)
                    print cmd
                    sh(cmd)
                r['image'] = os.path.join(IMAGES_DIRS[r['retrobook']], 'CD FolioImages', img_fn)
            
            
        return records
   
 


if __name__ == '__main__':
    RetroBookScanImporter().load_items()
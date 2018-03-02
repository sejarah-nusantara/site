

import os
import csv
import json
import codecs
from common import create_fixture, CODE_DIR, MEDIA_DIR, BASE, sh, load_fixture, ENCODING, DELIMITER, DELIMITER, DELIMITER, DELIMITER
from common import Importer 
from import_bookshelve_books import file_ids2pk
import sys
BASE = '/home/jelle/Dropbox/DASA Beta/Testdata'
class BookShelveScanImporter(Importer):
    
#    source_fn = os.path.join(BASE,  'retrobooks/RB items', 'retrobookScanInstance.csv')
    source_fn = os.path.join(BASE,  'retrobooks/RB items', 'duplicateScanInstance_RB_20120524.csv')
    model = 'dasa.retrobookscan'
    #/home/jelle/Dropbox/DASA POC Gerbrandy/Testdata/retrobooks/RB items/1 Corpus Diplomaticum/
    IMAGES_DIRS = os.listdir(os.path.join(BASE,'retrobooks/RB items'))
    IMAGES_DIRS = dict([(x.split()[0], x) for x in IMAGES_DIRS if x.split()[0] in [str(i) for i in range(0, 20)]])
    SOURCE_DIRS = [
       os.path.join(BASE, 'Bookshelves', 'ANRI_HR859', 'ANRI_HR859 FolioImages'),
       os.path.join(BASE, 'Bookshelves', 'ANRI_HR2075', 'ANRI_HR2075 FolioImages'),
       os.path.join(BASE, 'Bookshelves', 'ANRI_HR2496', 'ANRI_HR2496 FolioImages'),           
       ]
    def read_items(self, limit=None): 
        print '/home/jelle/Dropbox/DASA Beta/Testdata/Bookshelves/ANRI_HR859/ANRI_HR859 FolioImages'
        images = []
        for dirname in self.SOURCE_DIRS:
            images += [os.path.join(dirname, fn) for fn in os.listdir(dirname)]
        records = []
        images.sort()
        backcovers =[]
        frontcovers =[]
        for img in images:
            if img.endswith('backcover.png'):
                backcovers.append(img)
            elif img.endswith('cover.png'):
                frontcovers.append(img)
        images = frontcovers + [x for x in images if x not in backcovers and x not in frontcovers] + backcovers
                
        for i, img in enumerate(images):
#            if 'cover.png' in img:
#                continue
                
            
            relative_path_to_local_copy_of_image = os.path.join(img.split('/')[-3], img.split('/')[-1])
            dir = os.path.split(os.path.join(MEDIA_DIR, relative_path_to_local_copy_of_image))[0]
            if not os.path.exists(dir):
                os.makedirs(dir)
            sh('cp "%s" "%s"' % (img, dir))
            pagenumber = img.split('.')[0].split('f')[-1]
            try:
                pagenumber = int(pagenumber)
                pagenumber = str(pagenumber)
            except:
                pagenumber = ''
            record = {
                'pk': str(i+1),
                'institution':'ANRI',
                'fonds':'HR',
                'file_id': img.split('/')[-3].split('_')[1][2:],
                'image' : relative_path_to_local_copy_of_image,
                'position': str(i+1),
                'pagenumber': pagenumber,
             }
            
            record['retrobook'] = file_ids2pk[record['file_id']]
            records.append(record)
        return records 
    


if __name__ == '__main__':
    BookShelveScanImporter().load_items()
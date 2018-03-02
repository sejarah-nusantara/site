

import os
import csv
import json
import codecs
from common import create_fixture, CODE_DIR, MEDIA_DIR, BASE, sh, load_fixture
ENCODING = 'utf8'
DELIMITER = ','
#IMAGES_DIR = os.path.join(BASE, HARTAKARUN )
from common import Importer 
file_ids2pk = {
        '2496':1000,
        '859':1001,
        '2075':1002,
    }
class BookShelveBookImporter(Importer):
    model = 'dasa.retrobook'
    
    def read_items(self, limit=None):
        file_ids = file_ids2pk.keys()

        records = []
        for i, file_id in enumerate(file_ids):
            records.append(dict(
                pk = str(file_ids2pk[file_id]),
                file_id=file_id,
                institution='ANRI',
                fonds='HR',
                short_title='ANRI HR %s' % file_id,
            ))             
        return records   
 

if __name__ == '__main__':
    BookShelveBookImporter().load_items()


import os
import csv
import json
import codecs
import sys
sys.path.append(os.path.dirname(__file__))
from common import create_fixture, CODE_DIR, MEDIA_DIR, BASE, sh, load_fixture, Importer, unicode_csv_reader

HARTAKARUN = 'Harta Karun/HK Intro and Categories'
FN_CATEGORYINSTANCE = 'hartaKarunCategoryInstance.csv'

MAP_FIELDS_TO_MODEL = {
    'ID':'pk',                    
    'categoryParentID':'hartakarun_main_category',
    'categoryOrder':'position',
    'categoryImageReference':'image',
    'categoryIntroImageReference':'image_intro',
    'categoryNameENG':'name_en',
    'categoryNameBAH':'name_id',
    'categoryShortIntrotextENG':'shortIntroText_en',
    'categoryShortIntrotextBAH':'shortIntroText_id',
    'categoryLongIntrotextENG':'longIntroText_en',
    'categoryLongIntrotextBAH':'longIntroText_id',
    }

class HartaKarunCategoyImporter(Importer):
    source_fn = os.path.join(BASE, HARTAKARUN, FN_CATEGORYINSTANCE)
    model = 'dasa.resolution'
def read_category_instance():
    fn = os.path.join(BASE, HARTAKARUN, FN_CATEGORYINSTANCE)
    images_dir = os.path.join(BASE, HARTAKARUN, 'HK Category Images')
    print 'reading', fn
#    lines = csv.reader(codecs.open(fn, encoding='utf8'), delimiter=';')
    lines = unicode_csv_reader(fn)
    lines = [x for x in lines]
    headers = lines[0]
    headers = [MAP_FIELDS_TO_MODEL[k] for k in headers]
    records_category = []
    records_maincategory = []
    assert os.path.exists(images_dir), images_dir
    for l in lines[1:]:
#        l = [to_unicode(x) for x in l]
        r = dict(zip(headers, l))
        if r['name_en'] in ['None']:
            continue
        if r['hartakarun_main_category'] == '0':
            r['hartakarun_main_category'] = None
            
        if not r['image'] or r['image'] == 'dummy.png':
            r['image'] = 'HK Category I.6.png'
         
        sh('cp "%s" "%s"' % (os.path.join(images_dir, r['image']), MEDIA_DIR))
       
         
        if r['image_intro'] == 'dummy.png':
            r['image_intro'] = None
            
        if not r['image_intro']:
            r['image_intro'] = r['image']
        else:
            cmd= 'cp "%s" "%s"' % (os.path.join(images_dir, r['image_intro']), MEDIA_DIR)
            sh(cmd)
            print cmd
            
        if r['hartakarun_main_category']:
            records_category.append(r) 
        else:
            del r['hartakarun_main_category']
            records_maincategory.append(r) 
            
#        assert type(r['position']) == type(0), r['position']
        
#    for x in records:
#        print x
    print headers
    return records_maincategory, records_category
 

    
    
if __name__ == '__main__':
    records_maincategory, records_category = read_category_instance()
    
    model = 'dasa.hartakaruncategory'
    out_fn = 'fixtures/hartakaruncategory.json'
    out_fn = os.path.abspath(out_fn)
    create_fixture(model=model, data=records_category, out_fn=out_fn)
    load_fixture(out_fn, model=model)
    
    model = 'dasa.hartakarunmaincategory'
    out_fn = 'fixtures/hartakarunmaincategory.json'
    out_fn = os.path.abspath(out_fn)
    create_fixture(model=model, data=records_maincategory, out_fn=out_fn)
    load_fixture(out_fn, model=model)

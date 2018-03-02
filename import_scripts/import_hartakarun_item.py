

import os
import csv
import json
import codecs
from common import create_fixture, CODE_DIR, MEDIA_DIR, BASE, sh, load_fixture
HARTAKARUN = 'Harta Karun/HK Items'
FN_HKITEM = 'hartaKarunItemInstance.csv'
FN_HKSCAN = 'hartaKarunDuplicateScanReferenceInstance.csv'
IMAGES_DIR = os.path.join(BASE, HARTAKARUN )

MAP_FIELDS_TO_MODEL_HKITEM = {
	'ID':'pk',
	'hartaKarunCategoryInstanceID':'hartakaruncategory',
	'shortTitleENG':'short_title_en',
	'shortTitleBAH':'short_title_id',
	'longTitleENG':'long_title_en',
	'longTitleBAH':'long_title_id',
	'itemImageReference':'image',
	'selectedBy':'selected_by',
	'introducedBy':'introduced_by',
	'introductionText':'introduction',
	'introductionAnnotation':'introduction_annotation',
	'transcribedBy':'transcribed_by',
	'translatedEnglishBy':'translated_en_by',
	'translatedBahasaBy':'translated_id_by',
	'editedBy':'edited_by',
	'releaseDateYYYYMMDD':'date_of_release',
	'literatureReferences':'literature',
	'citationString':'citation',
	'comments':'comment',
	'timelineDateYYYYMMDD':'date_on_timeline',
 }

MAP_FIELDS_TO_MODEL_HKSCAN = {
	'ID':'pk',
	'hartakarunItemInstanceID':'hartakarun_item',
	'duplicateScanReferenceID':'reference',
	'duplicateScanReferenceInstitutionID':'institution',
	'duplicateScanReferenceFondsID':'fonds',
	'duplicateScanReferenceFileID':'file_id',
	'duplicateScanReferenceSequenceNumber':'position',
}
def read_hk_items():
    fn = os.path.join(BASE, HARTAKARUN, FN_HKITEM)
#    images_dir = os.path.join(BASE, HARTAKARUN, 'HK Category Images')
    lines = csv.reader(codecs.open(fn, encoding='iso-8859-1'), delimiter=';')
    lines = list(lines)
    records = []
    headers = lines[0]
    print headers
    headers = [MAP_FIELDS_TO_MODEL_HKITEM[k] for k in headers]
    for l in lines[1:]:
        l = [unicode(x) for x in l]
        r = dict(zip(headers, l))
        if r['image'] == 'dummy.png':
            r['image'] = None
        else:
            sub_dir = r['image'][:3]
            sh('cp "%s" "%s"' % (os.path.join(IMAGES_DIR, sub_dir, r['image']), MEDIA_DIR))
            
            
        records.append(r)
        
    for x in records:
        print x
    print headers
    return records
   
def read_hk_scans():
    fn = os.path.join(BASE, HARTAKARUN, FN_HKSCAN)
#    images_dir = os.path.join(BASE, HARTAKARUN, 'HK Category Images')
    lines = csv.reader(codecs.open(fn, encoding='iso-8859-1'), delimiter=';')
    lines = list(lines)
    records = []
    headers = lines[0]
    print headers
    headers = [MAP_FIELDS_TO_MODEL_HKSCAN[k] for k in headers]
    for l in lines[1:]:
        l = [unicode(x) for x in l]
        r = dict(zip(headers, l))
        records.append(r)
        
        if int(r['hartakarun_item']) <= 3:
	        sub_dir = 'HK%s/HK%s Folio Images' % (r['hartakarun_item'], r['hartakarun_item']) 
	        image_fns = [
				'ID_ANRI_HR_%s_%s.png' % (r['file_id'], r['position']),
				'ID_ANRI_HR_%s_%s.jpg' % (r['file_id'], r['position']),
				]
	        for image_fn in image_fns:
		        src = os.path.join(IMAGES_DIR, sub_dir, image_fn) 
	        	if os.path.exists(src):
	        		break
	        	
	        	
				
#	        src = os.path.join(IMAGES_DIR, sub_dir, image_fn) 
	        dst = os.path.join( MEDIA_DIR, sub_dir, image_fn)
		    	
	        
	        try:
		        os.makedirs(os.path.join(MEDIA_DIR, sub_dir)) 
	        except OSError:
		    	#probably because it already existed
		    	pass
		    
	        cmd = 'cp "%s" "%s"' % (src, dst)
	        print cmd
	        sh(cmd)
	        r['image'] = dst
	        
        if int(r['hartakarun_item']) > 3:
        	r['hartakarun_item'] = None
    for x in records:
        print x
    print headers
    return records
 
 
def load_hk_items():
	model = 'dasa.hartakarunitem'
	data = read_hk_items()
	out_fn = 'fixtures/hartakarunitem.json'
	out_fn = os.path.abspath(out_fn)
	create_fixture(model=model, data=data, out_fn=out_fn)
	load_fixture(out_fn)


def load_hk_scans():	
	model = 'dasa.scan'
	data = read_hk_scans()
	out_fn = 'fixtures/hartakarunscan.json'
	out_fn = os.path.abspath(out_fn)
	create_fixture(model=model, data=data, out_fn=out_fn)
	load_fixture(out_fn)

if __name__ == '__main__':
	load_hk_scans()
	load_hk_items()


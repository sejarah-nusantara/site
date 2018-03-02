# encoding=utf-8

#
#
#
#
#
#
#
#
#
#   THIS MIGHT BE OLD: CHECK OUT AT LEAST "import_realia"
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
import os
import csv
import json
import codecs
import sys
sys.path.append(os.path.dirname(__file__))
from common import create_fixture, CODE_DIR, MEDIA_DIR, BASE
from common import sh, load_fixture, ENCODING, DELIMITER, DELIMITER, DELIMITER, DELIMITER
from common import to_date, Importer


class ResolutionImporter(Importer):
#    source_fn = os.path.join(BASE,  '2nd entry resolutions', 'resolutionPointerInstance.csv')
    source_fn = os.path.join(BASE, '2nd entry resolutions', 'resolutionPointerInstance_ALL_20120524.csv')
    model = 'dasa.resolution'


    # IMAGES_DIR = os.path.join(BASE, HARTAKARUN )
    # /home/jelle/Dropbox/DASA POC Gerbrandy/Testdata/retrobooks/RB items/1 Corpus Diplomaticum/
    IMAGES_DIRS = os.listdir(BASE)
    IMAGES_DIRS = dict([(x.split()[0], x) for x in IMAGES_DIRS if x.split()[0] in [str(i) for i in range(0, 20)]])

    MAP_FIELDS_TO_MODEL = {
        'ID':'pk',
        'resolutionType': 'type',
        'resolutionSubjectName':'subject',
        'resolutionSummaryDescription': 'description',
        'resolutionDate':'date',
        'resolutionDatePriority':'priority',
        'dataSource': 'source',
        'registerFolioNumber': 'register_folionumber',
        'resolutionFolioNumber':'resolution_folionumber',
        'institutionID':'institution',
        'fondsID': 'fonds',
        'fileID': 'file',
        'comment': 'comment',
    }

    def postproduction(self, records):
        for i in range(0, len(records) - 1):
            records[i]['next_resolution'] = records[i + 1]['pk']

        return records

if __name__ == '__main__':
    ResolutionImporter().load_items()

#!../bin/python
# encoding=utf-8
import datetime
import os
import sys
sys.path.append(os.path.dirname(__file__))
from common import BASE
from common import Importer


REALIA_SOURCE_FN = '/home/jelle/projects_active/dasa/original_data/realia_20130531.csv'
ERR_LOG = 'import_realia_output.txt'


class ResolutionImporter(Importer):
    source_fn = REALIA_SOURCE_FN
    error_log = ERR_LOG
    model = 'dasa.resolution'

    # IMAGES_DIR = os.path.join(BASE, HARTAKARUN )
    # /home/jelle/Dropbox/DASA POC Gerbrandy/Testdata/retrobooks/RB items/1 Corpus Diplomaticum/
#     IMAGES_DIRS = os.listdir(BASE)
#     IMAGES_DIRS = dict([(x.split()[0], x) for x in IMAGES_DIRS if x.split()[0] in [str(i) for i in range(0, 20)]])

    MAP_FIELDS_TO_MODEL = {
        'ID': 'pk',
        'resolutionType': 'type',
        'realiumSubjectName': 'subject',
        'resolutionSummaryDescription': 'description',
        'resolutionDateYear': 'y',
        'resolutionDateMonth': 'm',
        'resolutionDateDay': 'd',
        'titlePriority': 'priority',
        'dataSource': 'source',
        'registerFolioNumber': 'register_folionumber',
        'resolutionFolioNumber': 'resolution_folionumber',
        'institutionID': 'institution',
        'fondsID': 'fonds',
        'fileID': 'file',
        'comment': 'comment',
    }

    def postproduction(self, records):
        # TODO: this assumes that the resolutions are imported in the correct order (which may or may not be true)
        for i, record in enumerate(records):
            record['pk'] = unicode(i + 1)
            record['order'] = unicode(i + 1)
            record['source'] = 'realia'
            if i < len(records) - 1:
                record['next_resolution'] = unicode(i + 2)

            try:
                if not record['y']:
                    if record['m'] and record['m'] != '0':
                        raise ValueError
                    if record['d']:
                        raise ValueError
                else:
                    y = int(record['y'])
                    m = int(record['m'])
                    d = int(record['d'])
                    record['date'] = unicode(datetime.date(y, m, d))
            except ValueError, error:
                d = record
                d['line_no'] = i + 2
                msg = "Invalid date in line %(line_no)s: %(y)s-%(m)s-%(d)s" % d
                self.log_error(msg, error)
                del d['line_no']

            for fld in ['d', 'm', 'y']:
                del record[fld]

        for error, msg in self.errors:
            print msg, error
        print len(self.errors), 'errors'
        return records

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'load_fixture':
        ResolutionImporter().load_fixture()
    else:
        ResolutionImporter().load_items()

#!../bin/python
# encoding=utf-8
import datetime
import os
import sys
import copy

sys.path.append(os.path.dirname(__file__))
from common import Importer


SOURCE_FN = '/home/jelle/projects/dasa/data/BijlagenResToegang_V20171009_final.xlsx'


class AppendixImporter(Importer):
    """importer for appendices to the resolution books"""
    ignore_first_line = False
    sheet_name = 'BijlagenRes METADATA'
    model = 'dasa.appendix'

    # headers from the excel file
    # checkedBy    addedBy    fileIdent    folioFrom    folioTo    folioExtra    documentTypeNL    docdateYear
    # docdateMonth    docdateDay    resdateYear    resdateMonth    resdateDay    documentTitleNL    vesselNames    notes
    MAP_FIELDS_TO_MODEL = {
        # 'ID': 'pk',
        # 'checkedBy': '',
        # 'addedBy': '',
        'LU1': None,
        'LU2': None,
        'ANRI1': None,
        'ANRI2': None,
        'fileIdent': 'archiveFile',
        'folioFrom': 'folio_number_from',
        'folioTo': 'folio_number_to',
        'folioExtra'  : 'folio_number_extra',
        'documentTypeNL': 'document_type_nl',
        'docdateYear': 'doc_y',
        'docdateMonth': 'doc_m',
        'docdateDay': 'doc_d',
        'resdateYear': 'res_y',
        'resdateMonth': 'res_m',
        'resdateDay': 'res_d',
        'documentTitleNL': 'title_nl',
        'vesselNames': 'vessel_names',
        'notes': 'notes',
        'personNamesEuropean': 'person_names_european',
        'personNamesAsian': 'person_names_asian',
        'placeNames': 'place_names',
    }

    def __init__(self, source_fn, offset=0):
        self.source_fn = source_fn
        self.offset = offset

    def postproduction(self, records):
        errors = []
        for i, record in enumerate(records):
            record['pk'] = i + 1 + self.offset
            record['order'] = i + 1 + self.offset

            for fld in [
                'doc_d',
                'doc_m',
                'doc_y',
                'res_d',
                'res_m',
                'res_y',
                ]:
                if record[fld]:
                    record[fld] = int(float(record[fld]))
                else:
                    record[fld] = None

            # excel reader returns floats that we convert to integers
            if record['folio_number_from']:
                record['folio_number_from'] = int(float(record['folio_number_from']))
            if record['folio_number_to']:
                record['folio_number_to'] = int(float(record['folio_number_to']))
            if record['folio_number_extra']:
                try:
                    record['folio_number_extra'] = int(float(record['folio_number_extra']))
                except:
                    pass
            record['archiveFile'] = int(float(record['archiveFile']))
            del record[None]
        for error, msg in errors:
            print msg, error
        print len(errors), 'errors'

        print 'input: %s' % self.source_fn
        print 'output: %s' % self.out_fn
        return records


def import_appendices():
    print SOURCE_FN
    data = []
    offset = 0
    rs = AppendixImporter(SOURCE_FN, offset=offset)
    data += rs.read_items()
    offset = len(data)

    print 'TOTAL:', len(data), ' records'
    print 'creating fixture...'
    rs.create_fixture(data=data)


def load_fixture():
    rs = AppendixImporter(source_fn=None)  # source_fn is not relevant
    print 'loading fixture...'
    rs.load_fixture()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('An argument needs to be provided')

    if sys.argv[1] == 'import_appendices':
        import_appendices()
    elif sys.argv[1] == 'load_fixture':
        load_fixture()
    else:
        raise Exception("This function should be called with either 'import_appendices' or 'load_fixture' as its argument")

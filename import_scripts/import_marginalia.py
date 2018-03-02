#!../bin/python
# encoding=utf-8
import datetime
import os
import sys
import copy

this_dir = os.path.dirname(__file__)
sys.path.append(this_dir)

from common import Importer  # NOQA

MARGINALIA_SOURCE = '/home/jelle/projects/dasa/data/MarginaliaDagregistersIndexed_V20171009_final.xlsx'

def splitnames(s):
    result = s.split(';')
    result = [n.strip() for n in result]
    result = filter(lambda n: n, result)
    return result

class MarginaliaImporter(Importer):

    ignore_first_line = False
    sheet_name = 'Entries'
    model = 'dasa.journalentry'

    MAP_FIELDS_TO_MODEL = {
        'ID': 'pk',
        'journalEntryDescription': 'description',
        'journalEntryDateYear': 'y',
        'journalEntryDateMonth': 'm',
        'journalEntryDateDay': 'd',
        'journalEntryDate Priority': 'priority',
        'journalEntryFromFolioNumber': 'folio_number_from',
        'journalEntryToFolioNumber': 'folio_number_to',
        'journalEntryAnnotations': 'annotation',
        'journalEntryAnnotation': 'annotation',
        'vesselNames': 'vessel_names',
        'Vesselname': 'vessel_names',
        'journalEntryFileNumber': 'archiveFile',
        'naamControle1': None,
        'naamControle2': None,
        'personNamesEuropean': 'person_names_european',
        'personNamesAsian': 'person_names_asian',
        'placeNames': 'place_names',
    }

    marginalia_personnameseuropean = []
    marginalia_personnamesasian = []
    marginalia_placenames = []

    def __init__(self, source_fn, offset=0):
        self.source_fn = source_fn
        self.offset = offset

    def postproduction(self, records):
        errors = []
        for i, record in enumerate(records):
            record['pk'] = i + 1 + self.offset
            record['order'] = i + 1 + self.offset
#            record['source'] = 'marginalia'
            if i < len(records) - 1:
                record['next'] = unicode(record['pk'] + 1)

            try:
                if not record['y']:
                    raise ValueError
                    if record['m'] and record['m'] != '0':
                        raise ValueError
                    if record['d']:
                        raise ValueError
                else:
                    y = int(float(record['y']))
                    m = int(float(record['m']))
                    d = int(float(record['d']))
                    record['date'] = unicode(datetime.date(y, m, d))
            except ValueError as error:
                record_copy = copy.deepcopy(record)
                record_copy['line_no'] = i + 2
                record_copy['source_fn'] = self.source_fn
                msg = "Invalid date in line %(line_no)s: %(y)s-%(m)s-%(d)s [in file %(source_fn)s" % record_copy
                errors.append((error, msg))
                del record_copy['line_no']  # so what does this 'd' stuff actually do?

            for fld in ['d', 'm', 'y']:
                del record[fld]

            # excel reader returns floats that we convert to integers
            if record['folio_number_from']:
                record['folio_number_from'] = int(float(record['folio_number_from']))
            if record['folio_number_to']:
                record['folio_number_to'] = int(float(record['folio_number_to']))
            record['archiveFile'] = int(float(record['archiveFile']))
            record['priority'] = int(float(record['priority']))
            # for name in splitnames(record['person_names_european']):
            #     if name not in self.marginalia_personnameseuropean:
            #         self.marginalia_personnameseuropean.append(name)
            # # del record['personNamesEuropean']
            # for name in splitnames(record['person_names_asian']):
            #     if name not in self.marginalia_personnamesasian:
            #         self.marginalia_personnamesasian.append(name)
            #     marginalia_personnamesasian = []
            # # del record['personNamesAsian']
            # for name in splitnames(record['place_names']):
            #     if name not in self.marginalia_placenames:
            #         self.marginalia_placenames.append(name)
            # del record['placeNames']
            del record[None]
        for error, msg in errors:
            print msg, error
        print len(errors), 'errors'

        print 'input: %s' % self.source_fn
        print 'output: %s' % self.out_fn
        return records


def import_marginalia():
    # crate fixtures from the data inthe excel file MARGINALIA_SOURCE
    # sources = MARGINALIA_SOURCES
    # for fn in sources:
    #     print '\t{fn}'.format(**locals())
    data = []
    offset = 0
    # for i, source_fn in enumerate(sources):
    source_fn = MARGINALIA_SOURCE
    print('Importing data from {}'.format(source_fn))
    rs = MarginaliaImporter(source_fn, offset=offset)
    # if i > 0:
    #     rs.DELETE_OLD_RECORDS = False
    LIMIT = 100000000
    rs.read_items(limit=LIMIT)
    data = rs.data
    # data += rs.read_items()
    offset = len(data)

    print 'TOTAL:', len(data), ' records'
    print 'creating fixture...'
    rs.create_fixture(data=data)

def load_fixture():
    # improt the main set
    rs = MarginaliaImporter(source_fn=None)  # source_fn is not relevant
    print 'loading fixture for marginalia'
    rs.load_fixture()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('An argument needs to be provided')

    if sys.argv[1] == 'import_marginalia':
        import_marginalia()
    elif sys.argv[1] == 'load_fixture':
        load_fixture()
    else:
        raise Exception("This function should be called with either 'import_marginalia' or 'load_fixture' as its argument")

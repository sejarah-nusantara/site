#!../bin/python
# encoding=utf-8
import datetime
import os
import sys
import copy

DEBUG = False

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(THIS_DIR)
from common import Importer

DATA_DIR = os.path.abspath(os.path.join(THIS_DIR, '..', '..', 'data'))
PERSONEN_SOURCE_FN = os.path.join(DATA_DIR, 'corpusdiplomaticum', 'CD_personen_V20190712.xlsx')
PLAATSEN_SOURCE_FN = os.path.join(DATA_DIR, 'corpusdiplomaticum', 'CD_plaatsen_V20190703.xlsx')
CORPUS_SOURCE_FN =   os.path.join(DATA_DIR, 'corpusdiplomaticum', 'DASA_CorpsDiplFull_V20190226.xlsx')


class PersonenImporter(Importer):

    model = 'dasa.corpusdiplomaticumpersoon'

    MAP_FIELDS_TO_MODEL = {
        'name': 'name',
        'ref': 'ref',
        'volumePage': 'volumePage',

    }

    def __init__(self, verbose=False):
        super(PersonenImporter, self).__init__(fn=PERSONEN_SOURCE_FN, verbose=verbose)

    def postproduction(self, records):
        for i, record in enumerate(records):
            record['pk'] = i + 1
            # del record['_ignored']
            # for k in ['period_start', 'period_end']:
            #     if record[k].endswith('.0'):
            #         record[k] = record[k][:-2]
        return records


class PlaatsenImporter(Importer):

    model = 'dasa.corpusdiplomaticumplaats'

    MAP_FIELDS_TO_MODEL = {
        'name': 'name',
        'ref': 'ref',
        'volumePage': 'volumePage',

    }

    def __init__(self, verbose=False):
        super(PlaatsenImporter, self).__init__(fn=PLAATSEN_SOURCE_FN, verbose=verbose)

    def postproduction(self, records):
        for i, record in enumerate(records):
            record['pk'] = i + 1
            # del record['_ignored']
            # for k in ['period_start', 'period_end']:
            #     if record[k].endswith('.0'):
            #         record[k] = record[k][:-2]
        return records


class CorpusImporter(Importer):

    model = 'dasa.corpusdiplomaticumcontract'

    MAP_FIELDS_TO_MODEL = {
        u'checked': u'_ignored',
        u'volumeNumber': u'volumeNumber',
        u'pageFrom': u'pageFrom',
        u'pageTo': u'pageTo',
        u'pageSupp': u'pageSupp',
        u'NumberRoman': u'numberRoman',
        u'NumberDigits': u'numberDigits',
        u'areaName': u'areaName',
        u'dayFrom': u'dayFrom',
        u'monthFrom': u'monthFrom',
        u'yearFrom': u'yearFrom',
        u'dayTo': u'dayTo',
        u'monthTo': u'monthTo',
        u'yearTo': u'yearTo',
        u'checked2': u'_ignored',
        u'kingdomName': u'kingdomName',
        u'contractSourceDescription': u'contractSourceDescription',
        u'signedPlace': u'signedPlace',
        u'signedAsians': u'signedAsians',
        u'signedEuropeans': u'signedEuropeans',
    }

    def __init__(self, verbose=False):
        super(CorpusImporter, self).__init__(fn=CORPUS_SOURCE_FN,  verbose=verbose)
        # self.rs_locations = rs_locations
        # self.rs_rulers = rs_rulers

    def postproduction(self, records):
        errors = []
        for i, record in enumerate(records):
            record['pk'] = i + 1
            record['order'] = i + 1
            keys_to_delete = ['_ignored']
            for k in keys_to_delete:
                if k in record:
                    del record[k]
            for k in record:
                if type(record[k]) == type(u'') and record[k].endswith('.0'):
                    record[k] = record[k][:-2]
                if k in ['dayFrom', 'monthFrom', 'yearFrom', 'dayTo', 'monthTo', 'yearTo']:
                    if record[k]:
                        record[k] = int(record[k])
                    else:
                        record[k] = None
                # if record[k]:
                #     record[k] = str(int(float(record[k])))

        for error, msg in errors:
            print msg, ':', error
        self.data = records
        print len(errors), 'errors'

        print 'input: %s' % self.source_fn
        print 'output: %s' % self.out_fn

        return records


def import_records():
    verbose = False
    rs = PersonenImporter(verbose=verbose)
    data = rs.read_items()
    print 'TOTAL:', len(data), ' records in', rs.sheet_name
    print 'creating fixture...'
#     if DEBUG:
#         data = data[:100]
    rs.create_fixture(data=data)

    rs_plaatsen = rs = PlaatsenImporter(verbose=verbose)
    data = rs.read_items()

    print 'TOTAL:', len(data), ' records in', rs.sheet_name
    print 'creating fixture...'
    rs.create_fixture(data=data)

    rs_letters = rs = CorpusImporter(verbose=verbose)
    data = rs.read_items()
    if DEBUG:
        data = data[:100]
    print 'TOTAL:', len(data), ' records in', rs.sheet_name
    print 'creating fixture...'
    rs.create_fixture(data=data)
    print 'Done'


def load_fixture():

    rs_locations = rs = PersonenImporter()
    print 'loading fixture for {rs}...'.format(**locals())
    rs.load_fixture()

    rs_rulers = rs = PlaatsenImporter()
    print 'loading fixture for {rs}...'.format(**locals())
    rs.load_fixture()

    rs_letters = rs = CorpusImporter()
    print 'loading fixture for {rs}...'.format(**locals())
    rs.load_fixture()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('An argument needs to be provided')

    if sys.argv[1] == 'import':
        import_records()
    elif sys.argv[1] == 'load_fixture':
        load_fixture()
    else:
        raise Exception("This function should be called with either 'import_corpusdiplomaticum' or 'load_fixture' as its argument")

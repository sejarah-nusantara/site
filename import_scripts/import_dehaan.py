#!../bin/python
# encoding=utf-8
import os
import sys
import requests

DEBUG = False

sys.path.append(os.path.dirname(__file__))

from common import Importer
from common import to_date

SOURCE = '/media/data2/projects/dasa/data/dehaan/CollDeHaan_inventory_V20180725.xlsx'


class PlacardImporter(Importer):

    model = 'dasa.dehaan'

    MAP_FIELDS_TO_MODEL = {
        'ID': 'IDSource',
        'originalMissingYN': 'originalMissingYN',
        'scanMissingYN': 'scanMissingYN',
        'refScanFrontImage': 'refScanFrontImage',
        'refScanBackImage': 'refScanBackImage',
        'descriptionByDeHaanNL': 'descriptionByDeHaanNL',
        'descriptionOnMapNL': 'descriptionOnMapNL',
        'titleNL': 'titleNL',
        'titleEN': 'titleEN',
        'typeMap': 'typeMap',
        'scale': 'scale',
        'locationEN': 'locationEN',
        'dimensionHWinCM': 'dimensionHWinCM',
        'Color': 'Color',
        'typeGraphics': 'typeGraphics',
        'Blurred': 'Blurred',
        'maker': 'maker',
        'date': 'date',
        'commentsEN': 'commentsEN',
        'refOtherMaps': 'refOtherMaps',
        'refOriginalEN': 'refOriginalEN',
        'refArchiveFile': 'refArchiveFile',
        'refArchiveDateBijlagen': 'refArchiveDateBijlagen',
        'refArchiveDescription': 'refArchiveDescription',
        'indexTerms': 'indexTerms',
        'numIndexTerms': 'numIndexTerms',
    }
    CONVERT_DATES = False

    def __init__(self):
        super(PlacardImporter, self).__init__(fn=SOURCE)  # , worksheet_name='lettersDailyJournals')

    def postproduction(self, records):
        errors = []
        for i, record in enumerate(records):
            record['pk'] = i + 1
            record['order'] = i + 1
            # if record['refScanFrontImage']:
            #     # print record['refScanFrontImage']
            #     code = record['refScanFrontImage'].split('_')[-1]
            #     # print code
            #     # print code.split('-')
            #     archiveFile, folioNumber = code.split('-')
            #     record['refScanFrontImageArchiveFile'] = archiveFile
            #     record['refScanFrontImageFolioNumber'] = folioNumber
            #     url = 'https://repository.cortsfoundation.org/scans'
            #     params = {
            #         'folioNumber': folioNumber,
            #         'archiveFile': archiveFile
            #     }
            #     response = requests.get(url, params=params, timeout=10)
            #     result = response.json()
            #     # print result
            #     if result['total_results'] == 1:
            #         print '[{i}] Scan found for {refScanFrontImage}'.format(i=i, **record)
            #         record['refScanFrontImageThumb'] = result['results'][0]['images'][0]['URL']
            #     else:
            #         print '[{i}] WARNING: No scan found for {refScanFrontImage}'.format(i=i, **record)
            #         record['refScanFrontImageThumb'] = None
            # else:
            #     print '[{i}] This record has no refScanBackImage defined'.format(i=i, **record)
            #
            # if record['refScanBackImage']:
            #     # print record['refScanBackImage']
            #     code = record['refScanBackImage'].split('_')[-1]
            #     # print code
            #     # print code.split('-')
            #     archiveFile, folioNumber = code.split('-')
            #     record['refScanBackImageArchiveFile'] = archiveFile
            #     record['refScanBackImageFolioNumber'] = folioNumber
            #     url = 'https://repository.cortsfoundation.org/scans'
            #     params = {
            #         'folioNumber': folioNumber,
            #         'archiveFile': archiveFile
            #     }
            #     response = requests.get(url, params=params, timeout=10)
            #     result = response.json()
            #     # print result
            #     if result['total_results'] == 1:
            #         print '[{i}] Scan found for {refScanBackImage}'.format(i=i, **record)
            #         record['refScanBackImageThumb'] = result['results'][0]['images'][0]['URL']
            #     else:
            #         print '[{i}] WARNING: No scan found for {refScanBackImage}'.format(i=i, **record)
            #         record['refScanBackImageThumb'] = None
            # else:
            #     print '[{i}] This record has no refScanBackImage defined'.format(i=i, **record)


#             if i < len(records) - 1:
#                 record['next'] = unicode(record['pk'] + 1)
#
#             # we have two dates:
#             # 1. data isued
#             # 2. date published
#
#             # for both of them, we check if they represent a valid date
#             y = m = d = None
#             for fld in ['issued_date', 'published_date']:
#                 for s in 'ymd':
#                     if record[fld + '_' + s].endswith('.0'):
#                         record[fld + '_' + s] = record[fld + '_' + s][:-2]
#                 vals = [record[fld + '_' + s] for s in 'ymd']
#                 vals = [v for v in vals if v]
#                 if len(vals) == 3:
#                     try:
#                         vals = [str(int(v)) for v in vals]
#                     except Exception, error:
#                         errors.append((error, 'In record {pk}: invalid date for {fld}: {vals}'.format(fld=fld, vals=vals, **record)))
#                         for s in 'ymd':
#                             if not record[fld + '_' + s].isdigit():
#                                 record[fld + '_' + s] = None
#                         continue
#                     try:
#                         to_date('-'.join([record[fld + '_' + s] for s in 'ymd']))
#                     except Exception as error:
#                         raise Exception(unicode(error) + ' in record {record}'.format(**locals()))
#                 elif len(vals) != 0 and fld == 'published_date':
#                     errors.append((None, 'In record {pk}: incomplete date for {fld}: {vals}'.format(fld=fld, vals=vals, **record)))
# #                     raise Exception('{vals} - {record}'.format(**locals()))
#             for k in record:
#                 if not record[k]:
#                     record[k] = None
#
#         self.data = records
#         self.complete_data = copy.deepcopy(records)
#
#         for error, msg in errors:
#             print 'ERROR:', msg, ':', error
#         print len(errors), 'errors'
#
#         print 'input: %s' % self.source_fn
#         print 'output: %s' % self.out_fn
        if DEBUG:
            records = records[:100]

        return records


def import_records():

    rs_letters = rs = PlacardImporter()
    data = rs.read_items()
    print 'TOTAL:', len(data), ' records in', rs.sheet_name
    print 'creating fixture...'
    rs.create_fixture(data=data)



def load_fixture():

    rs_letters = rs = PlacardImporter()
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
        raise Exception("This function should be called with either 'import_marginalia' or 'load_fixture' as its argument")

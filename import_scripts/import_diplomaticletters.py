#!../bin/python
# encoding=utf-8
import datetime
import os
import sys
import copy

DEBUG = False

sys.path.append(os.path.dirname(__file__))
from common import Importer

SOURCE_FN = 'AsianLetters integration 1625-1812 V4 20151125_lab1100.xlsx'
SOURCE = '/home/jelle/projects_active/dasa/original_data/' + SOURCE_FN


class LetterImporter(Importer):

    model = 'dasa.diplomaticletter'

    MAP_FIELDS_TO_MODEL = {
        'checkThis': '_ignored',
        'excelSource': '_ignored',
        # 1. officiallyDiplomaticYN: aanduiding of de brief echt officieel is (N=nee, Y=ja) (nieuw), zal worden
        # gebruikt om in Excel te filteren voordat er online gepubliceerd wordt (in de aanlevering naar Jelle zal
        # deze rubriek dus altijd op Y staan)
        'officiallyDiplomaticYN': '_ignored',
        # 2. scanReference: geeft een URL naar de scanviewer op de juiste pagebrowser folio (tbv Nodegoat, door
        # Marco gegenereerd op basis van de velden FileNumber en FromFolioNumber)
        'scanReference': '_ignored',
        # 3. volume: aanduiding van het volume deel gepubliceerde dagregisters (nieuw), wordt toegevoegd door
        # Marco, obv letterInsertionDateYear, voordat er aan Jelle wordt geleverd
        'volume': 'volume',
        # 4. pagePubFirst: eerste pagina van de brief in gepubliceerde dagregisters (nieuw)
        'pagePubFirst': 'pagePubFirst',
        # 5. pagePubLast: laatste pagina van de brief in gepubliceerde dagregisters (nieuw)
        'pagePubLast': 'pagePubLast',
        # 6. letterArchiveFileNumber: de ID van het inv.nr.
        # 7. letterArchiveFileFromFolioNumber: eerste folio van de brief
        # 8. letterArchiveFileToFolioNumber: laatste folio van de brief
        # 9. letterInsertionDateYear: jaartal van de datum waarop de brief in Dagregisters is opgenomen
        # 10. letterInsertionDateMonth: maand van de datum waarop de brief in Dagregisters is opgenomen
        # 11. letterInsertionDateDay: dag van de datum waarop de brief in Dagregisters is opgenomen
        # 12. letterOriginalDateYear: jaartal van de datum waarop de brief in Dagregisters is gedateerd
        # 13. letterOriginalDateMonth: maand van de datum waarop de brief in Dagregisters is gedateerd
        # 14. letterOriginalDateDay: dag van de datum waarop de brief in Dagregisters is gedateerd

        'letterArchiveFileNumber': 'archiveFile',
        'letterArchiveFileFromFolioNumber': 'folio_number_from',
        'letterArchiveFileToFolioNumber': 'folio_number_to',
        'letterInsertionDateYear': 'insertion_y',
        'letterInsertionDateMonth': 'insertion_m',
        'letterInsertionDateDay': 'insertion_d',
        'letterOriginalDateYear': 'original_y',
        'letterOriginalDateMonth': 'original_m',
        'letterOriginalDateDay': 'original_d',
        # 15. originalLetterAvailableYN: aanduiding of het een origineel betreft (nieuw)
        # 16. sealedYN: aanduiding of er een zegel aanwezig is (nieuw)
        # 17. originalLanguage: originele taal van de brief (nieuw)
        # 18. translatedInto: vertaald in taal (nieuw)
        # 19. letterSourceModern1..21: naam locatie brief is verzonden (ref: locations)
        # 20. letterDestinationModern1..19: naam van de locatie waar de brief naartoe is verzonden (ref:locations)
        # 21. letterRulerNameOriginal: transcriptie van deel van de originele tekst, die de verzender(s) bevat
        # 22. letterRulerNameModern1..16: naam van verzender van de brief (ref: rulers)
        # 23. notes: aantekeningen
        'originalLetterAvailableYN': 'originalLetterAvailableYN',
        'sealedYN': 'sealedYN',
        'originalLanguage': 'originalLanguage',
        'translatedInto': 'translatedInto',
        'letterSourceModern1': 'sourcename1',
        'letterSourceModern2': 'sourcename2',
        'letterSourceModern3': 'sourcename3',
        'letterSourceModern4': 'sourcename4',
        'letterSourceModern5': 'sourcename5',
        'letterSourceModern6': 'sourcename6',
        'letterSourceModern7': 'sourcename7',
        'letterSourceModern8': 'sourcename8',
        'letterSourceModern9': 'sourcename9',
        'letterSourceModern10': 'sourcename10',
        'letterSourceModern11': 'sourcename11',
        'letterSourceModern12': 'sourcename12',
        'letterSourceModern13': 'sourcename13',
        'letterSourceModern14': 'sourcename14',
        'letterSourceModern15': 'sourcename15',
        'letterSourceModern16': 'sourcename16',
        'letterSourceModern17': 'sourcename17',
        'letterSourceModern18': 'sourcename18',
        'letterSourceModern19': 'sourcename19',
        'letterSourceModern20': 'sourcename20',
        'letterSourceModern21': 'sourcename21',
        'letterDestinationModern1': 'destinationname1',
        'letterDestinationModern2': 'destinationname2',
        'letterDestinationModern3': 'destinationname3',
        'letterDestinationModern4': 'destinationname4',
        'letterDestinationModern5': 'destinationname5',
        'letterDestinationModern6': 'destinationname6',
        'letterDestinationModern7': 'destinationname7',
        'letterDestinationModern8': 'destinationname8',
        'letterDestinationModern9': 'destinationname9',
        'letterDestinationModern10': 'destinationname10',
        'letterDestinationModern11': 'destinationname11',
        'letterDestinationModern12': 'destinationname12',
        'letterDestinationModern13': 'destinationname13',
        'letterDestinationModern14': 'destinationname14',
        'letterDestinationModern15': 'destinationname15',
        'letterDestinationModern16': 'destinationname16',
        'letterDestinationModern17': 'destinationname17',
        'letterDestinationModern18': 'destinationname18',
        'letterDestinationModern19': 'destinationname19',
#         'letterDestinationModern20': 'destinationname20',
#         'letterDestinationModern21': 'destinationname21',
        'letterRulerNameOriginal': 'rulername_original',
        'letterRulerNameModern1': 'rulername1',
        'letterRulerNameModern2': 'rulername2',
        'letterRulerNameModern3': 'rulername3',
        'letterRulerNameModern4': 'rulername4',
        'letterRulerNameModern5': 'rulername5',
        'letterRulerNameModern6': 'rulername6',
        'letterRulerNameModern7': 'rulername7',
        'letterRulerNameModern8': 'rulername8',
        'letterRulerNameModern9': 'rulername9',
        'letterRulerNameModern10': 'rulername10',
        'letterRulerNameModern11': 'rulername11',
        'letterRulerNameModern12': 'rulername12',
        'letterRulerNameModern13': 'rulername13',
        'letterRulerNameModern14': 'rulername14',
        'letterRulerNameModern15': 'rulername15',
        'letterRulerNameModern16': 'rulername16',
#         'letterDescriptionEN': 'letterDescriptionEN',  # empty field
#         'letterDescriptionID': 'letterDescriptionID',  # empty field
#         'letterNanArchiveReference': 'letterNanArchiveReference',
        'notes': 'notes',
    }

    def __init__(self, rs_locations, rs_rulers, verbose=False):
        super(LetterImporter, self).__init__(fn=SOURCE, worksheet_name='letters', verbose=verbose)
        self.rs_locations = rs_locations
        self.rs_rulers = rs_rulers

    def postproduction(self, records):
        errors = []
        locations = self.rs_locations.data
        locations_dict = dict([(location['city'].strip(), location) for location in locations])
        rulers = self.rs_rulers.data
        rulers_dict = dict([(ruler['name_modern'].strip(), ruler) for ruler in rulers])

        rulers_not_found = []
        locations_not_found = []
        for i, record in enumerate(records):
            record['pk'] = i + 1
            record['order'] = i + 1
            if i < len(records) - 1:
                record['next'] = unicode(record['pk'] + 1)

            # we have two dates:
            # 1. insertiondate, which should alway sbe a valid date (?)
            # 2. original date, which may be partial or not given at all
            # we convert the insertino date into a 'real' date
            # and if we dont succeed, we log the error
            # the original date we only check for typos

            y = m = d = None
            for s in 'ymd':
                record['original_' + s] = record['original_' + s].strip()
                if record['original_' + s].endswith('.0'):
                    record['original_' + s] = record['original_' + s][:-2]
                if record['original_' + s] and not record['original_' + s].strip().isdigit():
                    msg = "Invalid original date in line {line_no}: {original_y}-{original_m}-{original_d}".format(line_no=i, **record)
                    error = 'Not all values are digits'
                    errors.append((error, unicode(msg)))
                    break
            for s in 'ymd':
                if not record['original_' + s].strip() or not record['original_' + s].strip().isdigit():
                    record['original_' + s] = None

            y = m = d = None
            insertion_valid = True

            for s in 'ymd':
                record['insertion_' + s] = record['insertion_' + s].strip()
                if record['insertion_' + s].endswith('.0'):
                    record['insertion_' + s] = record['insertion_' + s][:-2]
                if not record['insertion_' + s].strip().isdigit():
                    msg = "Invalid insertion date in line {line_no}: {insertion_y}-{insertion_m}-{insertion_d}".format(line_no=i, **record)
                    error = 'Not all values are digits'
                    errors.append((error, unicode(msg)))
                    insertion_valid = False
                    break
            for s in 'ymd':
                if not record['insertion_' + s].strip() or not record['insertion_' + s].strip().isdigit():
                    record['insertion_' + s] = None

            if insertion_valid:
                y = int(record['insertion_y'].strip())
                m = int(record['insertion_m'].strip())
                d = int(record['insertion_d'].strip())
                prefix = 'insertion'
                try:
                    record[prefix + '_date'] = unicode(datetime.date(y, m, d))
                except ValueError as error:
                    record[prefix + '_date'] = None
                    msg = "Invalid {prefix} date in line {line_no}: {y}-{m}-{d}".format(prefix=prefix, line_no=i, y=y, m=m, d=d, source_fn=self.source_fn, **record)
                    errors.append((error, unicode(msg)))

            for column_name in [
                'archiveFile',
                'folio_number_from',
                'folio_number_to',
                ]:
                if record[column_name].endswith('.0'):
                    record[column_name] = record[column_name][:-2]

            for j in range(1, 20):
#             for j in range(1, 2):
                recordname = 'destinationname{j}'.format(j=j)
                columnname = 'letterDestinationModern{j}'.format(j=j)
#                 destrecord = 'destination{j}'.format(j=j)
                destrecord = 'destinations'
                if destrecord not in record:
                    record[destrecord] = []
                if record[recordname]:
                    try:
                        record[destrecord].append(locations_dict[record[recordname]]['pk'])
                    except KeyError as error:
                        msg = u'Destination "{destinationname}" not found in line {i} in column {columnname}'.format(
                            i=i + 2,
                            destinationname=record[recordname],
                            columnname=columnname,
                            )
                        errors.append((error, msg))
                        locations_not_found.append(record[recordname])
                del record[recordname]
            for j in range(1, 22):
#             for j in range(1, 2):
                recordname = 'sourcename{j}'.format(j=j)
                columnname = 'letterSourceModern{j}'.format(j=j)
#                 destrecord = 'source{j}'.format(j=j)
                destrecord = 'sources'
                if destrecord not in record:
                    record[destrecord] = []

                if record[recordname]:
                    try:
                        record[destrecord].append(locations_dict[record[recordname]]['pk'])
                    except KeyError as error:
                        msg = u'Source "{sourcename}" not found in line {i} in column {columnname}'.format(
                            i=i + 2,
                            sourcename=record[recordname],
                            columnname=columnname,
                            )
                        errors.append((error, msg))
                        locations_not_found.append(record[recordname])
                del record[recordname]

            for j in range(1, 17):
                recordname = 'rulername{j}'.format(j=j)
                columnname = 'letterRulerNameModern{j}'.format(j=j)
                destrecord = 'rulers'
                if destrecord not in record:
                    record[destrecord] = []

                if record[recordname]:
                    try:
                        record[destrecord].append(rulers_dict[record[recordname]]['pk'])
                    except KeyError as error:
                        msg = u'Ruler "{rulername}" not found in line {i} in column {columnname}'.format(
                            i=i + 2,
                            rulername=record[recordname],
                            columnname=columnname,
                            )
                        errors.append((error, msg))
                        rulers_not_found.append(record[recordname])
                del record[recordname]

            # volume comes thourhg as '1.0'
            if record['volume']:
                record['volume'] = str(int(float(record['volume'])))

        self.data = records
        self.complete_data = copy.deepcopy(records)

        for record in self.data:
            keys_to_delete = ['_ignored', 'rulername_original']
            for k in keys_to_delete:
                del record[k]

        for error, msg in errors:
            print msg, ':', error
        print len(errors), 'errors'

        print 'input: %s' % self.source_fn
        print 'output: %s' % self.out_fn

        return records


class RulersImporter(Importer):

    model = 'dasa.diplomaticletterruler'

    MAP_FIELDS_TO_MODEL = {
        'checkthis': '_ignored',
        'excelSource': '_ignored',
        'letterRulerNameModern': 'name_modern',
        'rulerPeriodBegin': 'period_start',
        'rulerPeriodEnd': 'period_end',
        'location': 'location',
        'rulerAlternativeName1': 'alternative_name1',
        'rulerAlternativeName2': 'alternative_name2',
        'rulerAlternativeName3': 'alternative_name3',
        'rulerAlternativeName4': 'alternative_name4',
        'rulerAlternativeName5': 'alternative_name5',
        'rulerAlternativeName6': 'alternative_name6',
        'rulerAlternativeName7': 'alternative_name7',
        'rulerAlternativeName8': 'alternative_name8',
        'reference': 'reference',
        'knownHistory': '_ignored',
    }

    def __init__(self, verbose=False):
        super(RulersImporter, self).__init__(fn=SOURCE, worksheet_name='rulers', verbose=verbose)

    def postproduction(self, records):
        for i, record in enumerate(records):
            record['pk'] = i + 1
            del record['_ignored']
            for k in ['period_start', 'period_end']:
                if record[k].endswith('.0'):
                    record[k] = record[k][:-2]
        return records


class LocationsImporter(Importer):

    model = 'dasa.diplomaticletterlocation'

    MAP_FIELDS_TO_MODEL = {
        'checkThis': '_ignored',
        'excelSource': '_ignored',
        'continent': 'continent',
        'region': 'region',
        'regionAlternativeName': 'region_altenative_name',
        'location': 'city',
        'locationAlternativeName1': 'city_alternative_name',
        'locationAlternativeName2': 'city_alternative_name2',
        'locationAlternativeName3': 'city_alternative_name3',
        'place': 'place',
#         'geoData': '_ignored',  # duplicated in latitute and longitude
        'reference': 'reference',
        'exact': 'exact',
        'latitude': 'latitude',
        'longitude': 'longitude',
    }

    def __init__(self, verbose=False):
        super(LocationsImporter, self).__init__(fn=SOURCE, worksheet_name='locations', verbose=verbose)

    def postproduction(self, records):
        for i, record in enumerate(records):
            record['pk'] = i + 1
            del record['_ignored']
            for k in record:
                if isinstance(record[k], type(u'')):
                    record[k] = record[k].strip()
            for k in ['latitude', 'longitude']:
                if record[k]:
                    record[k] = record[k].strip().strip(',')
                    record[k] = float(record[k])
                else:
                    record[k] = None

        return records


class RelLetterLocationSourceImporter(Importer):
    model = 'dasa.diplomaticletter_sources'
    source_fixture = 'dasa.diplomaticletter_source_notfound_locations.json'

    def __init__(self, rs_letters, rs_locations):
        self.rs_letters = rs_letters
        self.rs_locations = rs_locations

    def read_items(self):
        records = []
        not_found = {}
        errors = []
        letters = self.rs_letters.complete_data
        locations = self.rs_locations.data

        locations_dict = dict([(location['city'].strip(), location) for location in locations])
        for location in locations:
            if location['city_alternative_name']:
                locations_dict[location['city_alternative_name'].strip()] = location
            if location['region_altenative_name']:
                locations_dict[location['region_altenative_name'].strip()] = location
            if location['region']:
                locations_dict[location['region'].strip()] = location

        for letter in letters:
            letter_pk = letter['pk']
            for k in ['source1', 'source2', 'source3', 'source4', 'source5']:
                location_name = letter[k].strip()
                if location_name:
                    try:
                        location = locations_dict[location_name]
                    except KeyError:
                        if k == 'source1':
                            # these should all be found in the existing list
                            msg = 'Location not found: {location_name} for {k}'.format(**locals())
                            errors.append(msg)
                        if location_name not in not_found:
                            location_pk = len(not_found) + 20000
                            not_found[location_name] = {
                                'pk': location_pk,
                                'city': location_name,
                            }
                        else:
                            location_pk = not_found[location_name]['pk']
                    location_pk = location['pk']
                    d = {'diplomaticletter': letter_pk, 'diplomaticletterlocation': location_pk}
                    if d not in records:
                        records.append(d)

        for i, record in enumerate(records):
            record['pk'] = i + 1
        for k in not_found:
            print 'LOCATION NOT FOUND:', k
        print len(not_found), 'locations not found'
        if errors:
            errors = list(set(errors))
            print '*' * 50
            print 'ERRORS!'
            for error in errors:
                print error
            print '*' * 50
            print
        data = not_found.values()
        self.create_fixture(data, self.source_fixture, model='dasa.diplomaticletterlocation')

        return records

    def load_fixture(self):
        return super(RelLetterLocationSourceImporter, self).load_fixture([self.source_fixture, self.out_fn])


class RelLetterLocationDestinationImporter(Importer):
    model = 'dasa.diplomaticletter_destinations'
    destination_fixture = 'dasa.diplomaticletter_destination_notfound_locations.json'

    def __init__(self, rs_letters, rs_locations):
        self.rs_letters = rs_letters
        self.rs_locations = rs_locations

    def read_items(self):
        records = []
        not_found = {}
        errors = []
        letters = self.rs_letters.complete_data
        locations = self.rs_locations.data

        locations_dict = dict([(location['city'].strip(), location) for location in locations])
        for location in locations:
            if location['city_alternative_name']:
                locations_dict[location['city_alternative_name'].strip()] = location
            if location['region_altenative_name']:
                locations_dict[location['region_altenative_name'].strip()] = location
            if location['region']:
                locations_dict[location['region'].strip()] = location

        for letter in letters:
            letter_pk = letter['pk']
            for k in [
                'destination1',
                'destination2',
                'destination3',
                'destination4',
                'destination5',
                'destination6',
                ]:

                location_name = letter[k].strip()
                if location_name:
                    try:
                        location = locations_dict[location_name]
                    except KeyError:
                        if location_name not in not_found:
                            location_pk = len(not_found) + 10000
                            not_found[location_name] = {
                                'pk': location_pk,
                                'city': location_name,
                            }
                        else:
                            location_pk = not_found[location_name]['pk']

                        if k == 'destination1':
                            msg = 'Location not found: {location_name} in {k}'.format(**locals())
                            errors.append(msg)
                    location_pk = location['pk']
                    d = {'diplomaticletter': letter_pk, 'diplomaticletterlocation': location_pk}
                    if d not in records:
                        records.append(d)

        for i, record in enumerate(records):
            record['pk'] = i + 1
        for k in not_found:
            print 'LOCATION NOT FOUND:', k
        print len(not_found), 'locations not found'

        if errors:
            errors = list(set(errors))
            print '*' * 50
            print 'ERRORS!'
            for error in errors:
                print error
            print '*' * 50
            print
        data = not_found.values()
        self.create_fixture(data, self.destination_fixture, model='dasa.diplomaticletterlocation')

        return records

    def load_fixture(self):
        return super(RelLetterLocationDestinationImporter, self).load_fixture([self.destination_fixture, self.out_fn])


class RelLetterRulerImporter(Importer):
    model = 'dasa.diplomaticletter_rulers'
    rulername_fixture = 'dasa.rulers_notfound_from_letters.json'

    def __init__(self, rs_letters, rs_rulers):
        self.rs_letters = rs_letters
        self.rs_rulers = rs_rulers

    def read_items(self):
        records = []
        not_found = {}
        errors = []
        letters = self.rs_letters.complete_data
        rulers = self.rs_rulers.data
        rulers_dict = dict([(ruler['name_modern'].strip(), ruler) for ruler in rulers])

        for letter in letters:
            letter_pk = letter['pk']
            for k in [
                'rulername1',
                'rulername2',
                'rulername3',
                'rulername4',
                'rulername5',
                'rulername6',
                'rulername7',
                'rulername8',
                'rulername9',
                'rulername10',
                'rulername11',
                ]:
                ruler_name = letter[k].strip()
                if ruler_name:
                    try:
                        ruler = rulers_dict[ruler_name]
                        ruler_pk = ruler['pk']
                    except KeyError:
                        if ruler_name not in not_found:
                            ruler_pk = len(not_found) + 10000
                            not_found[ruler_name] = {
                                'pk': ruler_pk,
                                'name_modern': ruler_name,
                            }
                        else:
                            ruler_pk = not_found[ruler_name]['pk']
                            if k == 'rulername1':
                                msg = u'Ruler not found: {ruler_name} in {k}'.format(**locals())
                                errors.append(msg)
                    d = {'diplomaticletter': letter_pk, 'diplomaticletterruler': ruler_pk}
                    if d not in records:
                        records.append(d)

        for i, record in enumerate(records):
            record['pk'] = i + 1
        for ruler_name in not_found:
            print 'RULER NOT FOUND:', ruler_name
        print len(not_found), 'rulers not found'
        if errors:
            errors = list(set(errors))
            print '*' * 50
            print 'ERRORS!'
            for error in errors:
                print error
            print '*' * 50
            print
        data = not_found.values()
        self.create_fixture(data, self.rulername_fixture, model='dasa.diplomaticletterruler')

        return records

    def load_fixture(self):
        return super(RelLetterRulerImporter, self).load_fixture([self.rulername_fixture, self.out_fn])


def import_records():
    verbose = False
    rs_rulers = rs = RulersImporter(verbose=verbose)
    data = rs.read_items()
    print 'TOTAL:', len(data), ' records in', rs.sheet_name
    print 'creating fixture...'
#     if DEBUG:
#         data = data[:100]
    rs.create_fixture(data=data)

    rs_locations = rs = LocationsImporter(verbose=verbose)
    data = rs.read_items()

    print 'TOTAL:', len(data), ' records in', rs.sheet_name
    print 'creating fixture...'
    rs.create_fixture(data=data)

    rs_letters = rs = LetterImporter(rs_locations=rs_locations, rs_rulers=rs_rulers, verbose=verbose)
    data = rs.read_items()
    if DEBUG:
        data = data[:100]
    print 'TOTAL:', len(data), ' records in', rs.sheet_name
    print 'creating fixture...'
    rs.create_fixture(data=data)
#
#     rs = RelLetterLocationSourceImporter(rs_locations=rs_locations, rs_letters=rs_letters)
#     data = rs.read_items()
#     print 'TOTAL:', len(data), 'relations between letters adn source locations'
#     print 'creating fixture...'
#     rs.create_fixture(data=data)
#
#     rs = RelLetterLocationDestinationImporter(rs_locations=rs_locations, rs_letters=rs_letters)
#     data = rs.read_items()
#     print 'TOTAL:', len(data), 'relations between letters and destinations'
#     print 'creating fixture...'
#     rs.create_fixture(data=data)
#
#     rs = RelLetterRulerImporter(rs_rulers=rs_rulers, rs_letters=rs_letters)
#     data = rs.read_items()
#     print 'TOTAL:', len(data), 'relations between letters and rulers'
#     print 'creating fixture...'
#     rs.create_fixture(data=data)


def load_fixture():

    rs_locations = rs = LocationsImporter()
    print 'loading fixture for {rs}...'.format(**locals())
    rs.load_fixture()

    rs_rulers = rs = RulersImporter()
    print 'loading fixture for {rs}...'.format(**locals())
    rs.load_fixture()

    rs_letters = rs = LetterImporter(rs_locations=rs_locations, rs_rulers=rs_rulers)
    print 'loading fixture for {rs}...'.format(**locals())
    rs.load_fixture()

#     rs = RelLetterLocationSourceImporter(rs_locations=rs_locations, rs_letters=rs_letters)
#     print 'loading fixture for {rs}...'.format(**locals())
#     rs.load_fixture()
#
#     rs = RelLetterLocationDestinationImporter(rs_locations=rs_locations, rs_letters=rs_letters)
#     print 'loading fixture for {rs}...'.format(**locals())
#     rs.load_fixture()
#
#     rs = RelLetterRulerImporter(rs_rulers=rs_rulers, rs_letters=rs_letters)
#     print 'loading fixture for {rs}...'.format(**locals())
#     rs.load_fixture()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('An argument needs to be provided')

    if sys.argv[1] == 'import':
        import_records()
    elif sys.argv[1] == 'load_fixture':
        load_fixture()
    else:
        raise Exception("This function should be called with either 'import_marginalia' or 'load_fixture' as its argument")

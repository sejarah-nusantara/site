# encoding=utf-8
#
# copyright Gerbrandy SRL
# www.gerbrandy.com
# 2013
#

import os
import csv
import json
import codecs
import datetime
import xlrd
import copy

CODE_DIR = os.path.abspath('..')
MEDIA_DIR = os.path.join(CODE_DIR, 'project', 'media')
BASE = '/home/jelle/Dropbox/DASA Beta/Testdata/'
ENCODING = 'utf8'
DELIMITER = ','
OUTPUT_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fixtures'))


def unicode_csv_reader(fn, encoding=ENCODING, delimiter=DELIMITER):
    lines = csv.reader(open(fn), delimiter=delimiter)
    for row in lines:
        try:
            yield [unicode(cell, encoding) for cell in row]
        except:
            # try some basic stuff for
            def _replace_windows_chars(s):
                s = s.replace('\x91', '\'').replace('\x92', "'")
                s = s.replace('\x96', '-')
            yield [unicode(_replace_windows_chars(cell)) for cell in row]


class Importer(object):
    """a class to help importing data into the database"""

    model = None
    error_log = None
    errors = []
    verbose = False
    DELETE_OLD_RECORDS = True
    MAP_FIELDS_TO_MODEL = {}
    CONVERT_DATES = True

    def __init__(self, fn=None, worksheet_name=None, ignore_first_line=False, verbose=False):
        self.source_fn = fn
        self.ignore_first_line = ignore_first_line
        self.offset = 0
        self.sheet_name = worksheet_name
        self.verbose = verbose

    def log(self, msg):
        print msg

    def warn(self, msg):
        print 'WARNING: {msg}'.format(msg=msg)

    def create_fixture(self, data, out_fn=None, model=None):
        """create a fixture

        model : the name of a model (e.g. 'dasa.hartakaruncategory')
        data : a list of dictionaries
        out_fn : path to a file - if given, write data to this file, otherwise return it

        """
        result = []
        if not model:
            model = self.model
        for _i, orig_record in enumerate(data):
            r = {}
            record = copy.deepcopy(orig_record)
            if 'pk' in record:
                r['pk'] = record['pk']
                del record['pk']
            r['model'] = model
            r['fields'] = record
            result.append(r)

        if not out_fn:
            out_fn = self.out_fn
        result = json.dumps(result)
        if out_fn:
            codecs.open(out_fn, 'w', encoding='utf8').write(result)
            message('written output to %s' % out_fn)
        else:
            return result

    def load_items(self, limit=None):
        data = self.read_items(limit=limit)
        self.create_fixture(data=data)
        self.load_fixture()
        message('Done!')
        return data

    def load_fixture(self, fixture_fn=None):
        """load fixture in the main db"""
        if not fixture_fn:
            fixture_fn = self.out_fn
        if not isinstance(fixture_fn, type([])):
            fixture_fn = [fixture_fn]
        fixture_fns = fixture_fn
        django_script = '../bin/django'
        table_name = 'dasa_%s' % self.model.lower().split('.')[-1]
        if self.DELETE_OLD_RECORDS:
            message('deleting records from table %(table_name)s' % locals())
            cmd = 'echo "TRUNCATE %(table_name)s CASCADE;" | %(django_script)s dbshell --settings=project.settings' % locals()
            stdin, stdout, stderr = sh(cmd)
            stderr = stderr.read()
            if 'ERROR' in stderr.upper():
                raise Exception(stderr)

        for fixture_fn in fixture_fns:
            message('loading fixture %(fixture_fn)s in database....' % locals())
            cmd = '%(django_script)s loaddata %(fixture_fn)s --settings=project.settings_import -v 2' % locals()
            message(cmd)
            stdin, stdout, stderr = sh(cmd)
            stderr = stderr.read()
            if 'ERROR' in stderr.upper():
                raise Exception(stderr)

    @property
    def output_directory(self):
        return OUTPUT_DIRECTORY

    @property
    def out_fn(self):
        out_fn = os.path.abspath(os.path.join(self.output_directory, '%s.json' % self.model))
        return out_fn

    def read_items(self, limit=None):
        """returns a list of records (= dictionaries)"""
        ignore_first_line = self.ignore_first_line
        fn = self.source_fn
    #    images_dir = os.path.join(BASE, HARTAKARUN, 'HK Category Images')
        self.log(self)
        self.log('reading data from {fn}'.format(fn=fn))
        if fn.endswith('.csv'):
            lines = unicode_csv_reader(fn)
        elif os.path.splitext(fn)[1] in ['.xls', '.xlsx']:
            lines = []
            workbook = xlrd.open_workbook(fn)
            if self.sheet_name:
                worksheet = workbook.sheet_by_name(self.sheet_name)
            else:
                self.sheet_name = workbook.sheet_names()[0]
                worksheet = workbook.sheet_by_name(self.sheet_name)
            num_rows = worksheet.nrows - 1
            num_cells = worksheet.ncols - 1
            curr_row = -1
            while curr_row < num_rows:
                if limit and curr_row > limit:
                    break
                print '\r{curr_row}/{num_rows}'.format(**locals()),
                line = []
                curr_row += 1
                row = worksheet.row(curr_row)
                curr_cell = -1
                while curr_cell < num_cells:
                    curr_cell += 1
                    # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
                    cell_type = worksheet.cell_type(curr_row, curr_cell)
                    cell_value = worksheet.cell_value(curr_row, curr_cell)
                    line.append(cell_value)
                lines.append(line)
            print '\n'

        lines = list(lines)
        records = []
        if ignore_first_line:
            headers = lines[1]
        else:
            headers = lines[0]
        # tmp code to find offending lines
        while headers[-1] == '':
            headers = headers[:-1]
        expected_length = len(headers)
        # assert expected_length > 3, 'We found less than 3 headers: {}'.format(headers)
        for i, l in enumerate(lines):
            for j in range(expected_length, len(l)):
                if l[j] != '':
                    x = l[j]
                    self.warn(u'Truncated line {i}: {l} = ignored value for {x} in column {j}'.format(**locals()))
        lines = [l[:expected_length] for l in lines]
        try:
            headers = [self.MAP_FIELDS_TO_MODEL[k] for k in headers]
        except KeyError:
            for k in headers:
                if k not in self.MAP_FIELDS_TO_MODEL:
                    msg = 'Expected to find the key "{k}" in the mapping self.MAP_FIELDS_TO_MODEL'.format(k=k)
                    raise Exception(msg)
            msg = 'Mismatch between headers in excel and mapping: \n{} \nversus mapping:\n {}'.format(headers, self.MAP_FIELDS_TO_MODEL.keys())
            raise Exception(msg)

        if ignore_first_line:
            start = 2
        else:
            start = 1
        for i, l in enumerate(lines[start:]):
            l = [unicode(x).strip() for x in l]
            if self.verbose:
                self.log(l)
            r = dict(zip(headers, l))

            # convert dates to dates (if requested)
            if self.CONVERT_DATES:
                for k, v in r.items():
                    if k and ('date' in k or 'time' in k):
                        r[k] = to_date(v)
            records.append(r)
            if limit and i + 1 >= limit:
                break

        records = self.postproduction(records)
        if self.error_log:
            self.write_error_log()

        self.log('finished reading %s records from %s' % (len(records), self.source_fn))
        self.data = records
        return records

    def log_error(self, msg, error=None):
        self.errors.append((msg, error))

    def write_error_log(self):
        if not self.error_log:
            raise Exception('self.error_log is not defined')
        f = codecs.open(self.error_log, 'w', 'utf8')
        for msg, error in self.errors:
            f.write('%s: %s\n' % (msg, error))
        f.write('%s errors\n' % len(self.errors))
        f.close()

    def postproduction(self, records):
        """some more operations while all records are known"""
        return records


def create_fixture(model, data, out_fn=None):
    x = Importer()
    x.model = model
#    x.out_fn = out_fn
    return x.create_fixture(data=data, out_fn=out_fn)


def message(s):
    """log a message """
    print s


def load_fixture(fn, model=None):
    """load fixture in the main db"""
    x = Importer()
    x.model = model
    return x.load_fixture(fixture_fn=fn)


def sh(cmd):
    """run a shell command"""
    return os.popen3(cmd)


def to_date(s):

    if s in ['not applicable']:
        return None
    if '/' in s:
        m, d, y = s.split('/')  # ?really
    elif '-' in s:
        y, m, d = s.split('-')
    else:
        raise Exception('Unknown data format %s' % s)
    if int(m) == 0:
        m = '1'
    if int(d) == 0:
        d = '1'
    if int(m) in [4, 6, 9] and int(d) == 31:
        d = '30'
    if int(m) in [2] and int(d) == 29:
        d = '28'
    # check if we have a valid date
    try:
        datetime.date(int(y), int(m), int(d))
    except ValueError, error:
        raise Exception('%s - %s' % (s, error))

    result = '%s-%s-%s' % (y, m.zfill(2), d.zfill(2))
    return result

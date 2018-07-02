import copy
import urllib
import datetime
import os
import types

from django.http import Http404
from django.conf import settings
from django.utils import translation
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from haystack.utils import Highlighter


def first_words(s, num_chars=100):
    """return a string of length not more than num_chars with the first words of the given string

    appends "..." if the original string is longer than num_chars
    """
    result = s[:100]
    result = ' '.join(result.split()[:-1])
    if len(s) > 100:
        result += '...'
    return result


def urlencode(d):
    """call urllib.urlencode, but first tries to avoid encoding errors"""
    try:
        return urllib.urlencode(d)
    except UnicodeEncodeError:
        d = copy.copy(d)
        for k in d:
            if type(d[k]) == type(u''):
                d[k] = d[k].encode('utf8')
        return urllib.urlencode(d)


class DasaHighlighter(Highlighter):
    def __init__(self, query, **kwargs):
        self.query = query

        if 'max_length' in kwargs:
            self.max_length = int(kwargs['max_length'])

        if 'html_tag' in kwargs:
            self.html_tag = kwargs['html_tag']

        if 'css_class' in kwargs:
            self.css_class = kwargs['css_class']

        boolean_operators = ['AND', 'OR', 'NOT']
        self.query_words = set([word.lower() for word in self.query.split() if not word.startswith('-') and word not in boolean_operators])

    def find_window(self, highlight_locations):
        best_start, best_end = super(DasaHighlighter, self).find_window(highlight_locations)
        # if we are close to the start, we just go to the beginning
        if best_start < 20:
            best_start = 0
        return (best_start, best_end)


def format_date_for_timeglider(d):
    return '%04d-%02d-%02d 01:00:00' % (d.year, d.month, d.day)


MONTHS = {
    1: _('Jan.'),
    2: _('Feb.'),
    3: _('Mar.'),
    4: _('Apr.'),
    5: _('May.'),
    6: _('Jun.'),
    7: _('Jul.'),
    8: _('Aug.'),
    9: _('Sep.'),
    10: _('Oct.'),
    11: _('Nov.'),
    12: _('Dec.'),
}


def prettyprint_date(y, m=None, d=None):
    if isinstance(m, types.IntType) and int(m) in range(1, 13):
        month = MONTHS[int(m)]
    elif isinstance(m, types.StringTypes) and m.isdigit() and int(m) in range(1, 13):
        month = MONTHS[int(m)]
    else:
        month = str(m)
    if y and m and d:
        if month:
            return u'{month} {d}, {y}'.format(d=d, month=month, y=y)
        else:
            return u'{d}-{m}-{y}'.format(d=d, m=m, y=y)
    elif y and m:
        if month:
            return u'{month} {y}'.format(month=month, y=y)
        else:
            return u'{m}-{y}'.format(m=m, y=y)
    elif y:
        return u'{y}'.format(y=y)


def to_date(y, m=None, d=None):
    if not y:
        return None
    if not m:
        m = 1
    if not d:
        d = 1
    return datetime.date(y, m, d)


def sluggify(s):
    """Turn s into a friendlier URL fragment

    removes underscores, and strips forward slashes from beginning and end

    returns:
        a string
    """
    # XXX make this smarter
    s = s.lower()
    s = s.strip()
    s = s.replace(' ', '-')
    while '--' in s:
        s = s.replace('--', '-')

    if s.startswith('/'):
        s = s[1:]
    if s.endswith('/'):
        s = s[:-1]

    return s


def slugs2breadcrumbs(ls):
    """given a list of slugs, return a list of (title, url) tuples"""
    result = []
    for slug in ls:
        page = get_page(slug=slug)
        result.append(page)
    result = [(page.title, page.get_absolute_url()) for page in result]
    return result


def fix_date(s):
    if s.isdigit() and len(s) == 4:
        s = '%s-1-1' % s
    return s


def pagebrowser_id(ead_id, archive_id, archiveFile):
    result = '%s-%s-%s' % (ead_id, archive_id, archiveFile)
    result = result.replace('/', '-')
    result = result.replace('.', '-')
    return result


def get_page(slug, default=None):
    from dasa import models
    try:
        page = models.BasicPage.objects.get(slug=slug)
    except models.BasicPage.DoesNotExist:
        if default is None:
            msg = 'Could not find BasicPage with slug "%s" - please add one on /admin/dasa/basicpage/' % slug
            raise Http404(msg)
        else:
            return default
    return page


def to_integer(s):
    # transform '1.0' into '1'
    try:
        return str(int(float(s)))
    except Exception:
        return s


def print_link_to_pagebrowser(scans, archive='K66a'):
    """return nicely groups set of links to the pagebrowser to the given set of scans"""
    # exclude scans without folioNumber
    scans = [scan for scan in scans if scan.get('folioNumber')]
    if not scans:
        return ''
    scans_to_sort = [(scan.get('archiveFile', ''), scan.get('folioNumber'), scan) for scan in scans]
    scans_to_sort.sort()
    scans = [scan for _archivefile, _folionumber, scan in scans_to_sort]
    scan_groups = []
    for scan in scans:
        if scan_groups and \
            scan_groups[-1][-1]['archiveFile'] == scan['archiveFile'] and \
            scan_groups[-1][-1]['folioNumber'] and \
            scan['folioNumber'] and \
            scan_groups[-1][-1]['folioNumber'].isdigit() and \
            scan['folioNumber'].isdigit() and \
            int(scan['folioNumber']) == int(scan_groups[-1][-1]['folioNumber']) + 1:
            scan_groups[-1].append(scan)
        else:
            scan_groups.append([scan])
    language_code = translation.get_language()
    ead_id = settings.LANGUAGE2EAD.get(language_code, settings.LANGUAGE_CODE)

    results = []
    archive_id = settings.ARCHIVE_IDS[archive]

    for i, scan_group in enumerate(scan_groups):
        scan = scan_group[0]
        archiveFile = scan['archiveFile']
        pb_url = os.path.join(settings.PAGEBROWSER_PUBLIC_URL, pagebrowser_id(ead_id=ead_id, archive_id=archive_id, archiveFile=archiveFile))
        pb_url += '?page_number=%s' % scan['folioNumber']
        if i > 0 and scan_groups[i - 1][0]['archiveFile'] == archiveFile:
            if len(scan_group) == 1:
                description = '{folioNumber}'.format(**scan)
            else:
                description = '{folioNumber}-{last_number}'.format(last_number=scan_group[-1]['folioNumber'], **scan)
        else:
            if len(scan_group) == 1:
                description = 'file {archiveFile}, folio {folioNumber}'.format(**scan)
            else:
                description = 'file {archiveFile}, folios {folioNumber}-{last_number}'.format(last_number=scan_group[-1]['folioNumber'], **scan)
        results.append('<a href="#" onClick="return openPageBrowser(\'{pb_url}\')">{description}</a>'.format(**locals()))

    return mark_safe(', '.join(results))


def sort_string(s):
    """a string used for sorting
    """
    original_s = s
    s = s.strip()
    for prefix in ['de ', "'t ", "l'", "'s "]:
        if s.startswith(prefix):
            s = s[len(prefix):]
    s = s + original_s
    return s.lower().strip()

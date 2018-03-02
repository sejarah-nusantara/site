# utility functions for getting data from the repository
import os
import hashlib
import datetime

import requests
import logging

from django.conf import settings

from dasa.utils import pagebrowser_id
from dasa import config


class ArchiveFileWrapper(object):
    """this wrapper of an archiveFile object is used for publishing information the pagebrowser"""
    def __init__(self, d, ead_id=None):
        """initialize with a dictionary"""
        for x in d:
            setattr(self, x, d[x])
        self.ead_id = ead_id

    def pagelist_url(self):
        return os.path.join(settings.REPOSITORY_PUBLIC_URL, 'pagebrowser', self.id, 'pagelist')

    def link_to_pagebrowser(self, ead_id=None):
        return os.path.join(settings.PAGEBROWSER_PUBLIC_URL, self.pagebrowser_id(ead_id)) + '/'

    def link_to_pagebrowser_en(self):
        ead_id = settings.LANGUAGE2EAD['en']
        return os.path.join(settings.PAGEBROWSER_PUBLIC_URL, self.pagebrowser_id(ead_id=ead_id)) + '/'

    def link_to_pagebrowser_id(self):
        ead_id = settings.LANGUAGE2EAD['id']
        return os.path.join(settings.PAGEBROWSER_PUBLIC_URL, self.pagebrowser_id(ead_id=ead_id)) + '/'

    def link_to_pagebrowser_nl(self):
        ead_id = settings.LANGUAGE2EAD['nl']
        return os.path.join(settings.PAGEBROWSER_PUBLIC_URL, self.pagebrowser_id(ead_id=ead_id)) + '/'

    def debug_info(self):
        return self.__dict__

    def pagebrowser_id(self, ead_id=None):
        if not ead_id:
            ead_id = self.ead_id

        if not ead_id:
            ead_id = 'CorpusDiplomaticum'
            # raise Exception('No ead_id argument provided')

        return pagebrowser_id(ead_id, self.archive_id, self.archiveFile)


class Repository(object):
    """Serves as a wrapper that communicates with the repository at settings.REPOSITORy_URL"""

    def __init__(self):
        self.url = settings.REPOSITORY_URL
        self.errors = []
        self._cache = {}

    def open_url(self, url, **kwargs):
        """GET the url with the parameters given by kwargs, and return the result

        the result is expected to be a JSON string, and is returned as a dictionary

        if we get a timeout, we will try to return a cached value instead
            TimeOut errors are logged, but not raised
        """
        cache_key = self.compute_hash((url, kwargs))
        try:
            print url, kwargs
            response = requests.get(url, params=kwargs, timeout=10)
            result = response.json()
        except requests.exceptions.Timeout as error:
            # log the exception (cf. settings.LOGGERS)
            now = datetime.datetime.now().isoformat()
            message = '[%s] Timeout error opening %s %s: %s (using cached value instead)' % (now, url, kwargs, unicode(error))
            logging.getLogger('repository.interaction').warning(message)
            # try to use the cached value
            result = self.cache_get(cache_key)
            return result
        except ValueError, error:
            msg = error.msg + '. Is {url} responding? [params={params}'.format(url=url, params=kwargs)
            raise Exception(msg)
        except requests.ConnectionError, error:
            msg = ''
            msg += 'Expected to find a repository on {url}. '.format(**locals())
            msg += '(Check settings.REPOSITORY_PUBLIC_URL) '
            msg += unicode(error)
            raise requests.ConnectionError(msg)

        self.cache_set(cache_key, result)
        return result

    def cache_set(self, k, v):
        self._cache[k] = v

    def cache_get(self, k, default=None):
        return self._cache.get(k, default)

    def compute_hash(self, k):
        k = unicode(k)
        m = hashlib.md5()
        m.update(k)
        return m.digest()

    def get_scans_in_timeframe(self, timeFrame, published_archivefiles=[]):
        """get scans that are in the current given timeFrames

        timeFrames is a list of dates

        published_archivefiles, if given, is a list of archiveFile identifiers, and we will only return scans associated with that archiveFile
        """
        url = os.path.join(self.url, 'scans')
        response = self.open_url(url, timeFrames=timeFrame, status=config.STATUS_PUBLISHED)
        if response:
            scans = response['results']
            # we have published scans, but we need to check taht the archiveFiles are published as well
            if scans:
                if not published_archivefiles:
                    published_archivefiles = [arch['archiveFile'] for arch in self.get_archivefiles_json()]
                published_scans = [scan for scan in scans if scan['archiveFile'] in published_archivefiles]
                return published_scans
            else:
                return []
        else:
            return []

    def get_archivefiles_json(self, **kwargs):
        """get information of archivefiles from the repository

        returns a list of dictionaries, one for each archive
        """
        url = os.path.join(self.url, 'archivefiles')
        # if 'archive_id' not in kwargs:
        #     kwargs['archive_id'] = settings.ARCHIVE_ID

        if 'archiveFiles' in kwargs:
            kwargs['archiveFile'] = kwargs['archiveFiles']
            del kwargs['archiveFiles']

        # if 'status' not in kwargs:
        #     kwargs['status'] = config.STATUS_PUBLISHED
        response = self.open_url(url, **kwargs)
        if response:
            return response['results']
        else:
            return []

    def get_archivefiles(self, limit=99999, start=None, end=None, **kwargs):
        """return an archivewrapper instance for each pair of ead_id, archivefile in the repository"""

        if start or end:
            if not 'archiveFile' in kwargs:
                 kwargs['archiveFile'] = '[{start} TO {end}]'.format(start=start, end=end)
        results = self.get_archivefiles_json(limit=limit, **kwargs)

        def toNumber(s):
            try:
                return int(s)
            except:
                raise

        if start and end:
            results = [r for r in results if start <= toNumber(r['archiveFile']) <= end]
        return [ArchiveFileWrapper(archivefile) for archivefile in results]

    def get_archivefiles_with_eads(self, **kwargs):
        """return an ArchiveWrapper instance for archivefile in the repository"""
        results = self.get_archivefiles_json(**kwargs)
        return [ArchiveFileWrapper(archivefile, ead_id=ead_id) for archivefile in results for ead_id in
            (archivefile['ead_ids'] or [None])]

    def get_daily_journal_books(self):
        """return all Books that are daily journals"""
        # daily journals have archive numbers 2457 to 2623
        start = 2457
        end = 2623
        return self.get_archivefiles(start=start, end=end)

    def get_resolution_books(self):
        # the archiveFile ids or the resoltuion books are in this range: 853 - 1182.
        # split thie "TO" queries, because the repository does alphabetic ordering, not numeric
        archiveFiles = ['[853 TO 999]', '[1000 TO 1182]', '4486', '4487']
        return self.get_archivefiles(archiveFile=archiveFiles, start=853, end=4487)

    def get_appendices_resolutions(self):
        # de serie 1196..1957 (bijlagen bij de resolutieboeken).
        archiveFiles = ['[1196 TO 1957]', '4550']
        return self.get_archivefiles(archiveFile=archiveFiles, start=1196, end=4550)

    def get_besogne_books(self):
        return self.get_archivefiles()


#
# make repository constant globally available
#
repository = Repository()

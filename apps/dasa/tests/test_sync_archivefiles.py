#
# copyright Gerbrandy SRL
# www.gerbrandy.com
# 2013
#


# encoding=utf-8
from django.core.urlresolvers import reverse

from basic_tests import EAD_ID, ARCHIVEFILE
from basic_tests import BaseTestCase
from dasa.views import syncarchivefiles
from dasa.views.syncarchivefiles import SyncArchiveFiles
from dasa.utils import pagebrowser_id
from django.conf import settings
from dasa import config


class SyncArchiveFilesTestCase(BaseTestCase):
    def test_sync_archivefiles(self):
        url = reverse('sync_archivefiles')
        response = self.app.get(url)

        # we should find our book 855/855 in our page, which wa last changed on last_changed2
        self.assertContains(response, '855/855')
        self.assertContains(response, 'last_changed2')

        # we publish an example ead file
        response = self.app.get(url, params={'publish': '1', 'ead_id': EAD_ID, 'archivefile': ARCHIVEFILE})
        self.assertEqual(response.status_code, 200)

        # when no ead file is known, we publish with other info
        response = self.app.get(url, params={'publish': '1', 'ead_id': None, 'archivefile': '2'})
        self.assertEqual(response.status_code, 200)

    def test_publish_in_pagebrowser(self):
        view = SyncArchiveFiles()
        view.pagebrowser = syncarchivefiles.PageBrowserBook(settings.PAGEBROWSER_URL, auth=settings.PAGEBROWSER_AUTH)
        view.published_archivefiles_from_repo = syncarchivefiles.repository.get_archivefiles_with_eads(status=config.STATUS_PUBLISHED, limit=10000)

        msg = view.publish_in_pagebrowser(ead_id=EAD_ID, archivefile_id=ARCHIVEFILE)
        self.assertIn('refreshed book', msg)
        msg = view.publish_in_pagebrowser(ead_id='', archivefile_id='2')
        self.assertIn('refreshed book', msg)

    def test_pagebrowser_id(self):
        self.assertEqual(pagebrowser_id(ead_id='something', archive_id='1', archiveFile='3'), 'something-1-3')
        self.assertEqual(pagebrowser_id(ead_id='something/or/other', archive_id='1', archiveFile='3'), 'something-or-other-1-3')
        return False

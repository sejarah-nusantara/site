# encoding=utf-8
#
# copyright Gerbrandy SRL
# www.gerbrandy.com
# 2013
#
import datetime
import types

from mock import Mock

from django.contrib.auth.models import User
from django.utils.translation import trans_real
from django_webtest import WebTest


import dasa
from dasa import config
from dasa.repository import ArchiveFileWrapper
from dasa import models
from dasa.utils import get_page

EAD_ID = 'ead.xml'
ARCHIVEFILE = '855'


class RepositoryMock(Mock):
    """We cannot count on a working repository during testing, so we use a mock"""

    def get_daily_journal_books(self, **kwargs):
        return []

    def get_resolution_books(self):
        return []

    def get_besogne_books(self):
        return []

    def get_appendices_resolutions(self):
        return []

    def get_archivefiles(self, **kwargs):
        return []

    def get_archivefiles_json(self, **kwargs):
        return []

    def get_archivefiles_with_eads(self, **kwargs):
        """return an archivewrapper instance for archivefile in the repository"""
        return [
            ArchiveFileWrapper({
                'archiveFile': ARCHIVEFILE,
                'status': config.STATUS_PUBLISHED,
                'id': ARCHIVEFILE,
                'archive_id': ARCHIVEFILE,
                }, ead_id=EAD_ID),
            ArchiveFileWrapper({
                'archiveFile': '2',
                'status': config.STATUS_PUBLISHED,
                'id': '2',
                'archive_id': ARCHIVEFILE,
                }, ead_id=None),
            ]

    def get_scans_in_timeframe(self, timeFrame, published_archivefiles=[]):
        if isinstance(timeFrame, types.ListType) and len(timeFrame) == 1:
            timeFrame = timeFrame[0]
        if timeFrame == datetime.date(1801, 2, 3):
            scan = dict(
                archiveFile=853,
                folioNumber=888,
            )
            return [scan]
        elif timeFrame == datetime.date(1803, 2, 1):
            scan1 = dict(
                archiveFile='853',
                folioNumber='112',
            )
            scan2 = dict(
                archiveFile='853',
                folioNumber='111',
            )
            scan3 = dict(
                archiveFile='851',
                folioNumber='11',
            )
            scan4 = dict(
                archiveFile='853',
                folioNumber='11',
            )
            return [scan1, scan2, scan3, scan4]
        elif isinstance(timeFrame, types.ListType):
            scan1 = dict(
                archiveFile='853',
                folioNumber='112',
                timeFrameFrom='1600-01-01',
                timeFrameTo='1800-01-01',
            )
            scan2 = dict(
                archiveFile='853',
                folioNumber='111',
                timeFrameFrom='1700-01-01',
                timeFrameTo='1800-01-01',
                date='1744-01-03',
            )
            return [scan1, scan2]
        else:
            return []

    def open_url(self, url, **kwargs):
        """open the url with the given parameters, and return the result

        the result is expected to be a JSON string, and is returned as a dictionary

        if we get a timeout, we will try to read from the cache (what???)
            TimeOut errors are logged, but not raised
        """
        if url.endswith('/ead/{0}'.format(EAD_ID)):
            return {
                'status': 1,
                'archive_id': 1,
                'language': "en",
                'title': "(EN) Archive of the Governor-General and Councillors of the Indies (Asia), the Supreme Government of the Dutch United East India Company and its successors (1612 - 1811)",
                'country': "ID",
                'institution': "ID-ANRI",
                'dateLastModified': "2013-10-02T23:04:19Z",
                'ead_id': "icaatom.cortsfoundation.org_339.ead.xml",
                'findingaid': "ID-ANRI_K66a_EN",
                'archive': "K66a"
            }
        elif url.endswith('lists/get_component_for_viewer'):
            return {
                'results': [{
                    'archiveFile': ARCHIVEFILE,
                    'title': 'sometitle',
                    'children': [
                        {'xpath': '/ead/archdesc/did/unittitle/text()',
                         'title': 'xx',
                         'text': 'xx', },
                        {'xpath': '/ead/eadheader/eadid/text()',
                         'title': 'xx',
                         'text': 'xx', },
                        {'xpath': '/ead/eadheader/eadid/@mainagencycode',
                         'title': 'xx',
                         'text': 'xx', },
                        {'xpath': '/ead/eadheader/filedesc/titlestmt/titleproper/text()',
                         'title': 'xx',
                        'text': 'xx', },
                        {'xpath': '/ead/archdesc/did/unitid/text()',
                         'title': 'xx',
                         'text': 'xx', },
                        {
                        'xpath': '/ead/archdesc/did/unitdate/text()',
                        'title': 'xx',
                        'text': 'xx', },
                        {
                        'xpath': '/ead/archdesc/did/physdesc/extent/text()',
                        'title': 'xx',
                        'text': 'xx', }, ]
                }]
            }

        return {}


class PageBrowserMock(Mock):
    def __init__(self, *args, **kwargs):
        Mock.__init__(self)

    _type = 'book'

    def test_connection(self):
        assert '@' not in self.base_url, 'Object should be instantiated as PageBrowser("http://some_url/", auth=(user, pass)), not with {0}'.format(self.base_url)
        return True

    def add_book(self, *args, **kwargs):
        return self

    def list_objects(self, extra_fields=[]):
        return [
            ['pagebrowserbook_id', 'last_changed_date'],
            ['ead-xml-855-855', 'last_changed2'],
            ]


class BaseTestCase(WebTest):
    """
    """
    longMessage = True

    fixtures = [
        'test.json',
        ]

    def setUp(self):

        trans_real.activate('en')
        # path the repository object
        # patch repository object
        global repository
        from dasa import views
        from dasa.views import syncarchivefiles

        self.repository = views.repository = dasa.repository = syncarchivefiles.repository = dasa.repository.repository = dasa.models.repository = repository = RepositoryMock()
        # patch pagebrowser
        views.PageBrowser = views.syncarchivefiles.PageBrowser = dasa.pagebrowser.PageBrowser = PageBrowserMock
        views.PageBrowserBook = views.syncarchivefiles.PageBrowserBook = dasa.pagebrowser.PageBrowserBook = PageBrowserMock

        # adding these pages in setup, as re-creating the fixture test.json is too much hassle
        self.add_page('account_edit')
        self.add_page('account_password_reset_done')
        self.add_page('accounts_signin', content='XXX'),
        self.add_page('accounts_signup'),
        self.add_page('accounts_profile_edit'),
        self.add_page('accounts_password_reset'),
        self.add_page('accounts_password_reset_done'),
        self.add_page('accounts_profile_password'),
        self.add_page('accounts_signup_complete'),
        self.add_page('accounts_password_reset_confirm')
        self.add_page('accounts_password_reset_complete')
        self.add_page('accounts_password_reset_failed')
        self.add_page('accounts_password_complete')
        self.add_page('accounts_activate_fail')
        self.add_page('weblinks')
        for k in config.__dict__:
            if k.startswith('SLUG_'):
                slug = getattr(config, k)
                if k == 'SLUG_REALIA_SUBJECTS':
                    title = 'Realia Subjects'
                else:
                    title = slug
                self.add_page(slug=slug, title=title)

        home_page = get_page('home')
        home_page.title = 'Homepage Title'
        self.add_page('signin')
        home_page.save()

        self.add_page(config.SLUG_APPENDIX_BROWSE)
        self.add_page(config.SLUG_APPENDIX_SEARCH)

        add_menuitem = self.add_menuitem

        self.menuitem1 = add_menuitem(config.SLUG_FOREWORD)
        self.menuitem1_1 = add_menuitem(config.SLUG_ARCHIVE_GENERALRESOLUTIONS, parent=self.menuitem1)
        self.menuitem1_2 = add_menuitem(config.SLUG_ARCHIVE_DAILY_JOURNALS, parent=self.menuitem1)
        self.menuitem2 = add_menuitem(config.SLUG_INTRODUCTION)
        self.menuitem3 = add_menuitem(config.SLUG_HARTAKARUN)
#         self.menuitem3_1 = add_menuitem(json.SLUG_HARTAKARUN_ALL_ARTICLES, parent=self.menuitem3)
        self.menuitem4 = add_menuitem(config.SLUG_ARCHIVE)
        self.menuitem4_1 = add_menuitem(config.SLUG_INVENTORY, parent=self.menuitem4)
        self.menuitem4_2 = add_menuitem(config.SLUG_DAILY_JOURNALS, parent=self.menuitem4)
        self.menuitem4_2_1 = add_menuitem(config.SLUG_ARCHIVE_DAILY_JOURNALS, parent=self.menuitem4_2)
        self.menuitem4_2_3 = add_menuitem(config.SLUG_MARGINALIA_BROWSE, parent=self.menuitem4_2)
        self.menuitem5 = add_menuitem(config.SLUG_NEWS)

        self.superuser = self.create_superuser()

    # set up the menu
    def add_menuitem(self, slug, parent=None):
        menuitem = models.MenuItem(parent=parent, page=get_page(slug))
        menuitem.save()
        return menuitem

    def add_page(self, slug, title=None, content=None):
        page = models.BasicPage(slug=slug)
        if not title:
            title = slug
        page.title = title
        if content:
            page.content = content
        page.save()
        return page

    def create_superuser(self):
        """
        Create a superuser names 'admin'
        """
        self._username = "admin"
        self._password = "admin"
        args = (self._username, "example@example.com", self._password)
        try:
            self._user = User.objects.get(username='admin')
        except User.DoesNotExist:
            self._user = User.objects.create_superuser(*args)
        return self._user

    def tearDown(self):
        trans_real.deactivate()

    def assert_description_and_content_on_page(self, slug):
        # add a page, test if description and content arrive at the page, and also are updated when the page is

        self.add_page(slug)
        page = models.BasicPage.objects.get(slug=slug)
        page.description = 'description_en1'
        page.content_en = 'content_en1'
        page.save()
        response = self.app.get('/{}/'.format(slug))
        self.assertEqual(response.context['page'].description, 'description_en1')
        self.assertContains(response, 'description_en1')
        self.assertContains(response, 'content_en1')

        page.description = 'description_en2'
        page.content_en = 'content_en2'
        page.save()
        response = self.app.get('/{}/'.format(slug))
        self.assertEqual(response.context['page'].description, 'description_en2', msg='.. for slug {}'.format(slug))
        self.assertContains(response, 'description_en2')
        self.assertContains(response, 'content_en2')

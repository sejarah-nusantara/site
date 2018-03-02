# encoding=utf-8
#
# copyright Gerbrandy SRL
# www.gerbrandy.com
# 2013ff
#

import datetime
from dasa import config

from basic_tests import BaseTestCase

from dasa.models import JournalEntry
from dasa.forms import MarginaliaSearchForm
from dasa.views import MarginaliaSearch


class MarginaliaTestCase(BaseTestCase):

    def setUp(self):
        super(MarginaliaTestCase, self).setUp()
        self.marginalia1 = JournalEntry.objects.all()[0]

    def test_sanity(self):
        self.assertEqual(JournalEntry.objects.count(), 100)

    def test_marginalia_browse(self):
        url = '/{}/'.format(config.SLUG_MARGINALIA_BROWSE)
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context['paginator_page'].object_list), 20)

    def test_marginalia_search(self):
        url = '/{}/'.format(config.SLUG_MARGINALIA_SEARCH)
        response = self.app.get(url)
        # the search page should load the django-selectable javascript
        self.assertContains(response, 'jquery.dj.selectable.js')

    def test_marginalia_admin(self):

        url = '/admin/dasa/journalentry/'
        response = self.app.get(url, user=self.superuser.username)
        self.assertEqual(response.status_code, 200)

        url = '/admin/dasa/journalentry/{self.marginalia1.id}/'.format(**locals())
        response = self.app.get(url, user=self.superuser.username)
        self.assertEqual(response.status_code, 200)

    def test_description_and_content(self):
        self.assert_description_and_content_on_page(config.SLUG_MARGINALIA_BROWSE)
        self.assert_description_and_content_on_page(config.SLUG_MARGINALIA_SEARCH)
        self.assert_description_and_content_on_page(config.SLUG_MARGINALIA_SHIPS)
        self.assert_description_and_content_on_page(config.SLUG_MARGINALIA_PLACENAMES)
        self.assert_description_and_content_on_page(config.SLUG_MARGINALIA_ASIANNAMES)
        self.assert_description_and_content_on_page(config.SLUG_MARGINALIA_EUROPEANNAMES)

    def test_selected_parameter(self):
        url = '/{}/'.format(config.SLUG_MARGINALIA_BROWSE)

        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.app.get(url, {'selected': '1'})
        self.assertEqual(response.status_code, 200)
        response = self.app.get(url, {'selected': ''})
        self.assertEqual(response.status_code, 200)
        response = self.app.get(url, {'selected': 'xxx'}, expect_errors=True)
        self.assertEqual(response.status_code, 404)

    def test_marginalia_form(self):
        view = MarginaliaSearch()
        form_class = view.form_class
        form = form_class()
        self.assertEqual(form.search()[0].model, JournalEntry)
        self.assertEqual(form.search().count(), JournalEntry.objects.count())

        # now search for an archiveFile  in different ways
        self.assertEqual(self.marginalia1.date, datetime.date(1683, 1, 1))

        self.assertEqual(self.marginalia1.archiveFile, '1585')

        form = form_class(data={'archiveFile': '1585'})
        results = form.search()
        self.assertEqual(results.count(), len([obj for obj in JournalEntry.objects.filter(archiveFile='1585')]))
        self.assertTrue(results.count() > 0)

# encoding=utf-8
#
# copyright Gerbrandy SRL
# www.gerbrandy.com
# 2013ff.
#

import datetime
from dasa import config

from basic_tests import BaseTestCase

from dasa import models
from dasa.models import Resolution
from dasa.views import RealiaSearch
from dasa import utils


class ResolutionTestCase(BaseTestCase):

    def setUp(self):
        super(ResolutionTestCase, self).setUp()
        self.resolution1 = Resolution.objects.all()[0]

    def test_sanity(self):
        self.assertEqual(Resolution.objects.count(), 100)

    def test_realia_browse(self):
        url = '/{}/'.format(config.SLUG_REALIA_BROWSE)
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)
        # it would be good to make a mock of the repository and test if links are generated ok

    def test_realia_search(self):
        url = '/{}/'.format(config.SLUG_REALIA_SEARCH)
        response = self.app.get(url)
        # the search page should load the django-selectable javascript
        self.assertContains(response, 'jquery.dj.selectable.js')

    def test_realia_admin(self):

        url = '/admin/dasa/resolution/'
        response = self.app.get(url, user=self.superuser.username)
        self.assertEqual(response.status_code, 200)

        url = '/admin/dasa/resolution/{self.resolution1.id}/'.format(**locals())
        response = self.app.get(url, user=self.superuser.username)
        self.assertEqual(response.status_code, 200)

    def test_selected_parameter(self):
        url = '/{}/'.format(config.SLUG_REALIA_BROWSE)

        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.app.get(url, {'selected': '1'})
        self.assertEqual(response.status_code, 200)
        response = self.app.get(url, {'selected': ''})
        self.assertEqual(response.status_code, 200)
        response = self.app.get(url, {'selected': 'xxx'}, expect_errors=True)
        self.assertEqual(response.status_code, 404)

    def _get_scans_with_resolution(self, resolution):
        realia_item = resolution
        if not realia_item.date:
            return []
        timeFrames = [realia_item.date]
        timeFrames = filter(None, timeFrames)
        timeFrames = list(set(timeFrames))
        scans_in_timeframe = self.repository.get_scans_in_timeframe(timeFrame=timeFrames)
#         realia_item_date = realia_item.date.isoformat().split()[0]
        return scans_in_timeframe

    def test_link_to_pagebrowser(self):
        resolution = models.Resolution.objects.all()[0]
        expected_result = '<a href="#" onClick="return openPageBrowser(\'http://dasa.localhost/pagebrowser/icaatom-dasa-anri-go-id_339-ead-xml-1-853?page_number=888\')">file 853, folio 888</a>'
        link_to_pagebrowser = utils.print_link_to_pagebrowser(self._get_scans_with_resolution(resolution))
        self.assertEqual(link_to_pagebrowser, expected_result)

        resolution = models.Resolution.objects.all()[4]
        template = '<a href="#" onClick="return openPageBrowser(\'http://dasa.localhost/pagebrowser/icaatom-dasa-anri-go-id_339-ead-xml-1-{file}?page_number={pagenumber}\')">{text}</a>'
                   # '<a href="#" onClick="return openPageBrowser(\'http://dasa.localhost/pagebrowser/icaatom-dasa-anri-go-id_339-ead-xml-1-851   ?page_number=          11\')">file 851, folio 11</a>
        l1 = template.format(file='851', pagenumber=11, text='file 851, folio 11')
        l2 = template.format(file='853', pagenumber=11, text='file 853, folio 11')
        l3 = template.format(file='853', pagenumber=111, text='111-112')
        expected_result = ', '.join([l1, l2, l3])
        link_to_pagebrowser = utils.print_link_to_pagebrowser(self._get_scans_with_resolution(resolution))
        self.assertEqual(link_to_pagebrowser, expected_result)

        resolution = models.Resolution.objects.all()[10]
        expected_result = ''
        link_to_pagebrowser = utils.print_link_to_pagebrowser(self._get_scans_with_resolution(resolution))
        self.assertEqual(link_to_pagebrowser, expected_result)

        # in thoery it happens that some scans have no folioNumber
        resolution = models.Resolution.objects.all()[4]
        scans = self._get_scans_with_resolution(resolution)
        del scans[1]['folioNumber']
        link_to_pagebrowser = utils.print_link_to_pagebrowser(scans)
        l3 = template.format(file='853', pagenumber=112, text='112')
        expected_result = ', '.join([l1, l2, l3])
        self.assertEqual(link_to_pagebrowser, expected_result)

    def test_search_form(self):
        self.resolution1.file = '1585'
        self.resolution1.save()

        view = RealiaSearch()
        form_class = view.form_class
        form = form_class()
        self.assertEqual(form.search()[0].model, models.Resolution)
        self.assertEqual(form.search().count(), models.Resolution.objects.count())

        # now search for an archiveFile  in different ways
        self.assertEqual(self.resolution1.date, datetime.date(1801, 2, 3))

        # searching for achivefiles is complex with realia
#         form = form_class(data={'archiveFile': '1585'})
#         results = form.search()
#         self.assertEqual(results.count(), len([obj for obj in models.Resolution.objects.filter(file='1585')]))
#         self.assertTrue(results.count() > 0)

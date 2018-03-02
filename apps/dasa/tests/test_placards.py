# encoding=utf-8
#
# copyright Gerbrandy SRL
# www.gerbrandy.com
# 2013
#

from dasa import config

from basic_tests import BaseTestCase

from dasa import models


class PlacardsTestCase(BaseTestCase):

    def setUp(self):
        # add some brieven
        super(PlacardsTestCase, self).setUp()

        self.placard1 = models.Placard(
            volume_number='101',
            page_number_from='1',
            page_number_to='1',
            governor='xxx',
            issued_date_d='1',
            issued_date_m='1',
            issued_date_y='1701',
            published_date_d='11',
            published_date_m='11',
            published_date_y='1711',
            text='text for placard1',
#             next='1',
            order='1',
            )
        self.placard1.save()

        self.placard2 = models.Placard(
            volume_number='234',
            page_number_from='2',
            page_number_to='2',
            governor='antohergovernor',
            issued_date_d='2',
            issued_date_m='2',
            issued_date_y='1812',
            published_date_d='13',
            published_date_m='10',
            published_date_y='1812',
            text='text for placard2',
            order='2',
            )
        self.placard2.save()
        self.placard1.next = self.placard2
        self.placard1.save()

    def test_sanity(self):
        # check that we have some diplomatieke brieven
        self.assertEqual(models.Placard.objects.count(), 2)

    def test_browse(self):
        url = '/{}/'.format(config.SLUG_PLACARD_BROWSE)
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)
        object_list = response.context['paginator_page'].object_list

        # check if we find our archiveFile fields in the browse page
        self.assertEqual(len(object_list), models.Placard.objects.count())
        self.assertContains(response, self.placard1.volume_number)
        self.assertContains(response, self.placard2.volume_number)
        # destination
#         self.assertContains(response, self.placard1.issued_date_m)
        self.assertContains(response, self.placard1.issued_date_d)
        self.assertContains(response, self.placard1.issued_date_y)
        self.assertContains(response, self.placard2.text)
        self.assertContains(response, self.placard2.published_date_y)
        self.assertContains(response, self.placard2.governor)

    def test_search(self):
        url = '/{}/'.format(config.SLUG_PLACARD_SEARCH)
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)

        # the search page should load the django-selectable javascript
        self.assertContains(response, 'jquery.dj.selectable.js')

        response = self.app.get(url, {'governor': self.placard1.governor})
        self.assertContains(response, self.placard1.governor)
        self.assertContains(response, self.placard1.text)
        self.assertNotContains(response, self.placard2.text)

        response = self.app.get(url, {'description': 'placard1'})
        self.assertContains(response, self.placard1.text)
        self.assertNotContains(response, self.placard2.text)

    def test_placard_governors(self):
        url = '/{}/'.format(config.SLUG_PLACARD_GOVERNORS)
        response = self.app.get(url)

    def test_admin(self):

        url = '/admin/dasa/placard/'
        response = self.app.get(url, user=self.superuser.username)
        self.assertEqual(response.status_code, 200)

    def test_page_navigation(self):
        url = '/' + config.SLUG_PLACARD_BROWSE + '/'
        response = self.app.get(url)
        self.assertEqual(response.context['paginator_page'].number, 1)
        response = self.app.get(url, {'page': '1'})
        self.assertEqual(response.context['paginator_page'].number, 1)
        response = self.app.get(url, {'page': '100'})
        self.assertEqual(response.context['paginator_page'].number, 1)
        response = self.app.get(url, {'page': 'xx'})
        self.assertEqual(response.context['paginator_page'].number, 1)
        response = self.app.get(url, {'page': '0'})
        self.assertEqual(response.context['paginator_page'].number, 1)



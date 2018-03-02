#
# copyright Gerbrandy SRL
# www.gerbrandy.com
# 2013
#


import datetime

from basic_tests import BaseTestCase
from dasa import config
from dasa import models
from django.core.urlresolvers import reverse


class HartaKarunTestCase(BaseTestCase):
    def test_release_of_hk_items(self):
        # check if hk item page titles show up in category page

        # get a category and, for senity, ensure it has some items
        hk_category = models.HartaKarunCategory.objects.all()[3]
        hk_items = hk_category.hartakarun_items.all()
        hk_item = hk_items[1]

        hk_item.release_date = None
        hk_item.save()

        self.assertEqual(hk_category.number_of_articles, 8)
        response = self.client.get(reverse(config.SLUG_HARTAKARUN_SUBCATEGORY, args=[hk_category.id]))
        self.assertNotContains(response, hk_item.title)

        hk_item.release_date = datetime.date(2000, 12, 1)
        hk_item.save()

        self.assertEqual(hk_category.number_of_articles, 9)
        response = self.client.get(reverse(config.SLUG_HARTAKARUN_SUBCATEGORY, args=[hk_category.id]))
        self.assertContains(response, hk_item.title)

        hk_item.release_date = datetime.date(2020, 12, 1)
        hk_item.save()

        self.assertEqual(hk_category.number_of_articles, 8)
        response = self.client.get(reverse(config.SLUG_HARTAKARUN_SUBCATEGORY, args=[hk_category.id]))
        self.assertNotContains(response, hk_item.title)

        url_of_hk_item = reverse('hartakarunitem', args=[hk_item.id])
        response = self.app.get(url_of_hk_item)

    def test_description_and_content(self):
        self.assert_description_and_content_on_page(config.SLUG_HARTAKARUN_SUBCATEGORY)
        self.assert_description_and_content_on_page(config.SLUG_HARTAKARUN_MAIN_CATEGORY)
        self.assert_description_and_content_on_page(config.SLUG_HARTAKARUN_ALL_ARTICLES)
        self.assert_description_and_content_on_page(config.SLUG_HARTAKARUN)

    def test_parameters(self):
        url = '/{0}/category/'.format(config.SLUG_HARTAKARUN)
        category = models.HartaKarunCategory.objects.all()[0]

        response = self.app.get(url + str(category.id))
        self.assertEqual(response.status_code, 301)
        response = self.app.get(url + str(category.id) + '/')
        self.assertEqual(response.status_code, 200)
        response = self.app.get(url + str(category.id) + '/xxx/', expect_errors=True)
        self.assertEqual(response.status_code, 404)
        response = self.app.get(url + '/xxx/', expect_errors=True)
        self.assertEqual(response.status_code, 404)
        response = self.app.get(url + '/xxx', expect_errors=True)
        self.assertEqual(response.status_code, 301)
        response = self.app.get(url + '/12345/', expect_errors=True)
        self.assertEqual(response.status_code, 404)

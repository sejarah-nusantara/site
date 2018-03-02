#
# copyright Gerbrandy SRL
# www.gerbrandy.com
# 2013
#

# encoding=utf-8

from basic_tests import BaseTestCase
from dasa import models
from dasa.forms import DasaQuery
from haystack.forms import SearchQuerySet


class SearchTestCase(BaseTestCase):
    # this list of fixtures will be loaded before testing
    def test_search_url(self):
        """functional test for search"""
        response = self.client.get('/search/?q=+&models=hartakarun_items')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/search/?q=')
        self.assertContains(response, 'You did not provide a search term')

    def test_indexing(self):
        """test if pages with the right release date are indexed (or not): NOT WRITTEN"""
        # unfortunately, we cannot test this because
        #   - the dummy backend does not do anything
        #   - the 'simple_backend' does not support searchign by date
        # if not using the 'realtimesearchindex', saving will not lead to indexing

        return False

        hk_category = models.HartaKarunCategory.objects.all()[3]
        hk_items = hk_category.hartakarun_items.all()
        hk_item = hk_items[1]
        search_term = hk_item.title.split()[1]
#
#         hk_item.release_date = datetime.date(2000, 12, 1)
        hk_item.save()
        response = self.client.get('/search/?q={search_term}&models=hartakarun_items'.format(search_term=search_term))
        self.assertContains(response, hk_item.title)

        #
        # check if news items are indexed
        news_item, _created = models.News.object.get_or_create(title='news item 1', text='one two three text is here')
        news_item.save()
        response = self.client.get('/search/?q={search_term}'.format(search_term='three'))
        self.assertContains(response, news_item.title)

    def test_dasa_query(self):
        sqs = SearchQuerySet().query
        self.assertEqual(DasaQuery('x').prepare(sqs), 'x')
        self.assertEqual(DasaQuery('-x').prepare(sqs), 'NOT x')
        self.assertEqual(DasaQuery('x AND y').prepare(sqs), 'x AND y')
        self.assertEqual(DasaQuery('x OR y').prepare(sqs), 'x OR y')
        self.assertEqual(DasaQuery('x NOT y').prepare(sqs), 'x NOT y')

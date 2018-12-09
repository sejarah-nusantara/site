# encoding=utf-8
#
# copyright Gerbrandy SRL
# www.gerbrandy.com
# 2013ff
#

from dasa import config

from basic_tests import BaseTestCase

from dasa.models import Appendix
from dasa.views.appendix import AppendixSearch
from dasa import queries


class AppendixTestCase(BaseTestCase):

    def setUp(self):
        super(AppendixTestCase, self).setUp()

        self.appendix1 = Appendix(
            title_nl='keyword1 keyword2 keyword3',
            doc_y=1683,
            archiveFile='1585',
            document_type_nl='Document Type',
            vessel_names='Anna, Bolle',
            )
        self.appendix1.save()
        self.appendix2 = Appendix(
            title_nl='keyword4',
            doc_y=1630,
            archiveFile='1586',
            document_type_nl='Another Document Type',
            vessel_names='Claes',
            )
        self.appendix2.save()

    def test_sanity(self):
        self.assertEqual(Appendix.objects.count(), 2)

    def test_appendix_browse(self):
        url = '/{}/'.format(config.SLUG_APPENDIX_BROWSE)
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context['paginator_page'].object_list), 2)

    def test_appendix_search(self):
        url = '/{}/'.format(config.SLUG_MARGINALIA_SEARCH)
        response = self.app.get(url)
        # the search page should load the django-selectable javascript
        self.assertContains(response, 'jquery.dj.selectable.js')

    def test_appendix_admin(self):

        url = '/admin/dasa/journalentry/'
        response = self.app.get(url, user=self.superuser.username)
        self.assertEqual(response.status_code, 200)

        url = '/admin/dasa/journalentry/{self.appendix1.id}/'.format(**locals())
        response = self.app.get(url, user=self.superuser.username)
        self.assertEqual(response.status_code, 200)

    def test_description_and_content(self):
        self.assert_description_and_content_on_page(config.SLUG_APPENDIX_BROWSE)
        self.assert_description_and_content_on_page(config.SLUG_APPENDIX_SEARCH)

    def test_selected_parameter(self):
        url = '/{}/'.format(config.SLUG_APPENDIX_BROWSE)

        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.app.get(url, {'selected': '1'})
        self.assertEqual(response.status_code, 200)
        response = self.app.get(url, {'selected': ''})
        self.assertEqual(response.status_code, 200)
        response = self.app.get(url, {'selected': 'xxx'}, expect_errors=True)
        self.assertEqual(response.status_code, 404)

    def test_appendix_form(self):
        view = AppendixSearch()
        form_class = view.form_class
        form = form_class()

        # test some precondition for the test
        self.assertEqual(self.appendix1.doc_y, 1683)
        self.assertEqual(self.appendix2.doc_y, 1630)
        self.assertEqual(self.appendix1.archiveFile, '1585')

        # calling the form without parameters finds all objects
        results = form.search()
        self.assertEqual(results[0].model, Appendix)
        self.assertEqual(results.count(), Appendix.objects.count())
        self.assertEqual(results[0].archiveFile, self.appendix1.archiveFile)

        self.assertEqual(results[0].title_nl, self.appendix1.title_nl)
        self.assertEqual(results[0].vessel_names, self.appendix1.vessel_names)
        self.assertEqual(results[0].doc_y, self.appendix1.doc_y)
        # TODO: we cannot really test searching without a proper SOLR instance
        return

        form = form_class(data={'doc_date_to': '1650-01-01'})
        results = form.search()
        self.assertEqual(results, [self.appendix2])

        form = form_class(data={'doc_date_from': '1650-01-01'})
        results = form.search()
        self.assertEqual([r.object for r in results], [self.appendix1])
        assert False, 'xx'
        return

        form = form_class(data={'archiveFile': '1585'})
        results = form.search()
        self.assertEqual(results.count(), len([obj for obj in Appendix.objects.filter(archiveFile='1585')]))
        self.assertTrue(results.count() > 0)

        form = form_class(data={'doc_date_from': '1650-01-01'})
        results = form.search()
        self.assertEqual([r.object for r in results], [self.appendix1])

        form = form_class(data={'doc_date_to': '1650-01-01'})
        results = form.search()
        self.assertEqual(results, [self.appendix2])

        form = form_class(data={'res_date_from': '1650-01-01'})
        results = form.search()
        self.assertEqual(results, [self.appendix1])

        form = form_class(data={'res_date_to': '1650-01-01'})
        results = form.search()
        self.assertEqual(results, [self.appendix1])

        form = form_class(data={'keyword': 'keyword1'})
        results = form.search()
        self.assertEqual(results, [self.appendix1])

    def test_vesselnames_index(self):
        def new_get_appendix_vesselnames():
            vessel_names = self.appendix1.vessel_names_as_list() + self.appendix2.vessel_names_as_list()
            return [(n, 1) for n in vessel_names]
        queries.get_appendix_vesselnames = new_get_appendix_vesselnames

        url = '/{}/'.format(config.SLUG_APPENDIX_VESSELNAMES)
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.appendix1.vessel_names_as_list()[0])
        # self.assertContains(response, self.appendix1.vessel_names_as_list()[1])
        self.assertContains(response, self.appendix2.vessel_names_as_list()[0])

        response = self.app.get(url, {'first_letter': 'A'})
        self.assertContains(response, self.appendix1.vessel_names_as_list()[0])
        self.assertNotContains(response, self.appendix2.vessel_names_as_list()[0])

    def test_documenttypes_index(self):
        # patch queries
        def new_get_documenttypes_appendix():
            return [
                (self.appendix1.document_type_nl, 1),
                (self.appendix2.document_type_nl, 1),
            ]
        queries.get_documenttypes_appendix = new_get_documenttypes_appendix

        url = '/{}/'.format(config.SLUG_APPENDIX_DOCUMENTTYPES)
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.app.get(url, {'first_letter': 'D'})
        # appendix1.document_type_nl starts with a 'D'
        self.assertContains(response, self.appendix1.document_type_nl)
        # appendix2.document_type_nl does not start with a 'D'
        self.assertNotContains(response, self.appendix2.document_type_nl)

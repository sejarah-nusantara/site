#
# copyright Gerbrandy SRL
# www.gerbrandy.com
# 2013
#

from django.conf import settings

from basic_tests import BaseTestCase
from dasa import config
from dasa import models
from dasa.utils import get_page


class PagesTestCase(BaseTestCase):

    def setUp(self):
        super(PagesTestCase, self).setUp()
        self.add_page('hathi31')

    def test_if_pages_are_there(self):
        TYPICAL_MENU_ENTRY = self.menuitem4.page.title

        self.assertContains(self.client.get('/'), 'Arsip Nasional Republik Indonesia')
        self.assertContains(self.client.get('/%s/1/' % config.SLUG_HARTAKARUN_MAIN_CATEGORY), 'Malay Indonesian')

        # the name of the main categories should occur twice (oncein the menu, once in the body
        self.assertContains(self.client.get('/hartakarun/'), 'Malay Indonesian', count=2)
        # the name of each subcategory should occur as well

        self.assertContains(self.client.get('/hartakarun/'), 'Malay Indonesian', count=2)

        self.assertContains(self.client.get('/hartakarun/item/1/'), 'Thomas Dias')

        resolutions_page = models.BasicPage.objects.get(slug=config.SLUG_ARCHIVE_GENERALRESOLUTIONS)
        self.assertContains(self.client.get('/%s/' % config.SLUG_ARCHIVE_GENERALRESOLUTIONS), resolutions_page.title)
        self.assertContains(self.client.get('/%s/' % config.SLUG_ARCHIVE_GENERALRESOLUTIONS), TYPICAL_MENU_ENTRY)
        self.assertContains(self.client.get('/%s/' % config.SLUG_REALIA_SUBJECTS), 'Realia Subjects')

        self.assertContains(self.client.get('/%s/' % config.SLUG_SEARCH), TYPICAL_MENU_ENTRY)

    def test_realia_browse(self):
        """TODO: write this test for the Realia page (make it work with haystack)..."""
        response = self.client.get('/realia-browse/')
        # the response must contain the first data among the realia
#         first_realia = models.Resolution.objects.all()[0]
        return

        self.assertContains(response, 'Feb. 3, 1801')

    def test_appendices_resolution(self):
        test_content = 'SOME TEST CONTENT'
        self.add_page(config.SLUG_APPENDICES_RESOLUTIONS, title=test_content)
        TYPICAL_MENU_ENTRY = self.menuitem4.page.title
        resolutions_page = models.BasicPage.objects.get(slug=config.SLUG_APPENDICES_RESOLUTIONS)
        self.assertContains(self.client.get('/%s/' % config.SLUG_APPENDICES_RESOLUTIONS), resolutions_page.title)
        self.assertContains(self.client.get('/%s/' % config.SLUG_APPENDICES_RESOLUTIONS), TYPICAL_MENU_ENTRY)
#         self.assertContains(self.client.get('/%s/' % json.SLUG_APPENDICES_RESOLUTIONS), test_content)

    def test_foreword(self):
        p = self.add_page('foreword-2')
        p.content = 'content of foreword-2'
        p.save()
        response = self.client.get('/foreword/')
        self.assertContains(response, p.content)

    def test_breadcrumbs(self):
        response = self.app.get('/{}/'.format(config.SLUG_MARGINALIA_BROWSE))
        self.assert_crumbs_are_sane(response)
        breadcrumbs = response.context['breadcrumbs']
        self.assertEqual(breadcrumbs[0][1], '/{}/'.format(config.SLUG_ARCHIVE))

        # see if breadcrubms are translated
        response = self.app.get('/id/{}/'.format(config.SLUG_MARGINALIA_BROWSE))
        self.assert_crumbs_are_sane(response)
        breadcrumbs = response.context['breadcrumbs']
        self.assertEqual(breadcrumbs[0][1], '/id/{}/'.format(config.SLUG_ARCHIVE))

#         1) http://www.sejarah-nusantara.anri.go.id/id/search/
#
# ... the laatste breadcrum gaat weer naar de engelse zoekpagina
        response = self.app.get('/id/search/')
        self.assert_crumbs_are_sane(response)
#
# 2) http://www.sejarah-nusantara.anri.go.id/id/marginalia-ships/
#
#  ... heeft een dubbele breadcrum op het eind
        response = self.app.get('/id/marginalia-ships/')
        self.assert_crumbs_are_sane(response)
#
# 3) http://www.sejarah-nusantara.anri.go.id/id/hathi1/
# ...
# http://www.sejarah-nusantara.anri.go.id/id/hathi31/
# ... the laatste breadcrum gaat weer naar de engelse hathi pagina

        response = self.app.get('/id/hathi31/')
        self.assert_crumbs_are_sane(response)
#
        response = self.app.get('/id/{}/1/'.format(config.SLUG_NEWS))
        self.assert_crumbs_are_sane(response)
        breadcrumbs = response.context['breadcrumbs']
        self.assertEqual(breadcrumbs[0][1], '/id/{}/'.format(config.SLUG_NEWS))

    def test_404(self):
        # we expect a 404 if we pass a parameters that we would not expect otherwise

        # news items
        response = self.app.get('/id/{0}/xxx/1/'.format(config.SLUG_NEWS), expect_errors=True)
        self.assertEqual(response.status_code, 404)
        response = self.app.get('/id/{}/10000/'.format(config.SLUG_NEWS), expect_errors=True)
        self.assertEqual(response.status_code, 404)
        response = self.app.get('/id/1/10000/'.format(config.SLUG_NEWS), expect_errors=True)
        self.assertEqual(response.status_code, 404)

        # hk categories
        response = self.app.get('/{0}/{1}/class=/'.format(config.SLUG_HARTAKARUN_MAIN_CATEGORY, models.HartaKarunCategory.objects.all()[0].id), expect_errors=True)
        self.assertEqual(response.status_code, 404)
        response = self.app.get('/{0}/1234/'.format(config.SLUG_HARTAKARUN_MAIN_CATEGORY, models.HartaKarunCategory.objects.all()[0].id), expect_errors=True)
        self.assertEqual(response.status_code, 404)
        response = self.app.get('/{0}/xxxxx/'.format(config.SLUG_HARTAKARUN_SUBCATEGORY), expect_errors=True)
        self.assertEqual(response.status_code, 404)

    def assert_crumbs_are_sane(self, response):
        breadcrumbs = response.context['breadcrumbs']
        if breadcrumbs:
            self.assertNotEqual(breadcrumbs[-1][1], response.request.path)

        # no duplicates
        self.assertEqual(len([b[0] for b in breadcrumbs]), len(set([b[0] for b in breadcrumbs])), breadcrumbs)
        self.assertEqual(len([b[1] for b in breadcrumbs]), len(set([b[1] for b in breadcrumbs])), breadcrumbs)
        if response.request.path.startswith('/id/'):
            for breadcrumb in breadcrumbs:
                self.assertTrue(breadcrumb[1].startswith('/id/'), breadcrumbs)

    def test_image(self):
        # TODO: write test for self.app.get('image/myimage/?size=200x200')
        pass

    def test_google_analytics(self):
        # depending on the settings, google analytics should be included or not
        settings.GOOGLE_ANALYTICS_ID = '12345678'
        response = self.app.get('/')
        self.assertContains(response, 'analytics.js')
        self.assertContains(response, settings.GOOGLE_ANALYTICS_ID)

        settings.GOOGLE_ANALYTICS_ID = None
        response = self.app.get('/')
        self.assertNotContains(response, 'analytics.js')

    def test_signin_page_update(self):
        # we had a problem that page objects were cached
        slug = config.SLUG_ACCOUNTS_SIGNIN
        page = get_page(slug=slug)

        page.content = 'ZZZ'
        page.save()
        response = self.app.get('/accounts/signin/')
        self.assertContains(response, 'ZZZ')

        page.content = 'YYY'
        page.save()
        response = self.app.get('/accounts/signin/')
        self.assertContains(response, 'YYY')

    def test_description_and_content(self):
        slug = 'some_page'
        self.add_page(slug)
        page = models.BasicPage.objects.get(slug=slug)
        page.description = 'description_en'
        page.content_en = 'content_en'
        page.save()
        response = self.app.get('/{}/'.format(slug))
        self.assertContains(response, 'description_en')
        self.assertContains(response, 'content_en')

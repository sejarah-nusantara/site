# encoding=utf-8
#
# copyright Gerbrandy SRL
# www.gerbrandy.com
# 2013
#

from django.contrib.auth.models import User, Group
from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse

from dasa import models
from basic_tests import BaseTestCase


class MetaTagsTestCase(BaseTestCase):

    def test_admin_links(self):
        """test seome basic facts about the admin interface"""

        url = reverse('admin:index')
        response = self.app.get(url, user=self.superuser)

        self.assertContains(response, reverse('admin:dasa_basicpage_changelist'))
        self.assertContains(response, reverse('admin:dasa_metatags_changelist'))

        # we now add a metatags
        response = self.app.get(reverse('admin:dasa_metatags_add'))

        # in our form, we should have tags in english and bahasa
        self.assertTrue('keywords_en' in response.form.fields, response.form.fields.keys())
        self.assertTrue('keywords_id' in response.form.fields, response.form.fields.keys())
        # the original fields should not be visible on the form, however
        self.assertFalse('keywords' in response.form.fields, response.form.fields.keys())

        # we add some data
        response.form['object_type'] = 'all'
        keywords = 'key1 and key2'
        response.form['keywords_id'] = keywords
        response.form['description_en'] = 'descritpio in en'
        response = response.form.submit().maybe_follow()
        # now we visit the list of metatags
        response = self.app.get(reverse('admin:dasa_metatags_changelist'))
        # we should now find our keywords on this page
        self.assertContains(response, keywords)

        # we should also find (translated) keywords and description fields in BasicPage edit pages
        page = self.add_page('testpage')
        response = self.app.get(reverse('admin:dasa_basicpage_change', args=(str(page.id),)), user=self.superuser)
        # in our form, we should have tags in english and bahasa
        self.assertTrue('meta_keywords_en' in response.form.fields, response.form.fields.keys())
        self.assertTrue('meta_keywords_id' in response.form.fields, response.form.fields.keys())
        # the original fields should not be visible on the form, however
        self.assertFalse('meta_keywords' in response.form.fields, response.form.fields.keys())

    def test_metatags_on_pages(self):
        page_description_en = 'afsdlskadj'
        page_keywords_en = 'dfsalkjfdasl;j '
        keywords_all_en = 'lakdsfj;dflsakj dsfakj'
        keywords_basicpage_en = 'en_dhdsfac'
        description_all_en = 'enl;jkjdflsakj dsfakj'
        description_basicpage_en = 'en_l;ljdhdsfac'

        page_description_id = 'asdldfkasjlkajf '
        page_keywords_id = 'adsflkxvcnm'
        keywords_all_id = 'lkajfsdl; fdsa'
        keywords_basicpage_id = 'idafsdkljkasdjfxx'
        description_all_id = 'l;jkidjdflsakj dsfakj'
        description_basicpage_id = 'idl;ljdhdsfac'

        page = self.add_page('a page')
        page.meta_description_en = page_description_en
        page.meta_keywords_en = page_keywords_en
        page.meta_description_id = page_description_id
        page.meta_keywords_id = page_keywords_id
        page.save()

        models.MetaTags.objects.create(
            object_type='all',
            keywords_en=keywords_all_en,
            keywords_id=keywords_all_id,
            description_id=description_all_id,
            description_en=description_all_en,
            )
        models.MetaTags.objects.create(
            object_type='BasicPage',
            keywords_en=keywords_basicpage_en,
            keywords_id=keywords_basicpage_id,
            description_id=description_basicpage_id,
            description_en=description_basicpage_en,
            )

        # now get the page
        response = self.app.get('/en/{page.slug}/'.format(page=page)).maybe_follow()

        self.assertContains(response, page_description_en)
        self.assertContains(response, page_keywords_en)
        self.assertContains(response, keywords_all_en)
        self.assertContains(response, description_all_en)
        self.assertContains(response, description_basicpage_en)
        self.assertContains(response, keywords_all_en)

        self.assertNotContains(response, page_description_id)
        self.assertNotContains(response, page_keywords_id)
        self.assertNotContains(response, keywords_all_id)
        self.assertNotContains(response, description_all_id)
        self.assertNotContains(response, description_basicpage_id)
        self.assertNotContains(response, keywords_all_id)
        # now get the indonesian version of the page
        response = self.app.get('/id/{page.slug}/'.format(page=page)).maybe_follow()

        self.assertContains(response, page_description_id)
        self.assertContains(response, page_keywords_id)
        self.assertContains(response, keywords_all_id)
        self.assertContains(response, description_all_id)
        self.assertContains(response, description_basicpage_id)
        self.assertContains(response, keywords_all_id)

        self.assertNotContains(response, page_description_en)
        self.assertNotContains(response, page_keywords_en)
        self.assertNotContains(response, keywords_all_en)
        self.assertNotContains(response, description_all_en)
        self.assertNotContains(response, description_basicpage_en)
        self.assertNotContains(response, keywords_all_en)

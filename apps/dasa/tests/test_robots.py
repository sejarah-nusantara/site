#
# copyright Gerbrandy SRL
# www.gerbrandy.com
# 2013
#

from django.conf import settings

from basic_tests import BaseTestCase
from dasa import config


class RobotsTestCase(BaseTestCase):

    def setUp(self):
        super(RobotsTestCase, self).setUp()

    def test_robots_txt(self):
        url = '/robots.txt'
        settings.DEBUG = False
        response = self.app.get(url)
        host_url = response.request.host_url + ':80'
        self.assertContains(response, 'User-agent: *')
        self.assertContains(response, 'Disallow: /admin/')
        self.assertContains(response, 'Disallow: /static/')
        self.assertEqual(response.content_type, 'text/plain')
        self.assertContains(response, 'Sitemap: {host_url}/sitemap.xml'.format(host_url=host_url))

        # if debug is True, all pages should be disallowed
        settings.DEBUG = True
        response = self.app.get(url)
        self.assertContains(response, 'Disallow: /')

    def test_sitemap(self):
        url = '/sitemap.xml'
        response = self.app.get(url)
        host_url = response.request.host_url + ':80'
        self.assertEqual(response.content_type, 'application/xml')
        self.assertContains(response, '<?xml version="1.0" encoding="UTF-8"?>')
        self.assertContains(response, '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n    xmlns:xhtml="http://www.w3.org/1999/xhtml"')
        self.assertContains(response, '/' + config.SLUG_FOREWORD)
        self.assertContains(response, '/id/' + config.SLUG_FOREWORD)
        self.assertContains(response, 'href="{host_url}/id/{slug}'.format(host_url=host_url, slug=config.SLUG_FOREWORD))

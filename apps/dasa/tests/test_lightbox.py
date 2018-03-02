#
# copyright Gerbrandy SRL
# www.gerbrandy.com
# 2013
#

from basic_tests import BaseTestCase
from dasa import models


class HartaKarunTestCase(BaseTestCase):
    def test_ligthbox_items(self):
        # add some ligthbox items
        lightboxitem1 = models.LightBoxItem(title='title1', url='url1', visible=True)
        lightboxitem1.save()
        lightboxitem2 = models.LightBoxItem(title='title2', url='url2', visible=False)
        lightboxitem2.save()

        # we should only see item 1 on the homeapge, as 2 is not visible
        response = self.app.get('/')
        self.assertContains(response, lightboxitem1.url)
        self.assertNotContains(response, lightboxitem2.url)

        # also test the ordering
        lightboxitem1.order = 1
        lightboxitem1.save()
        lightboxitem2.order = 2
        lightboxitem2.visible = True
        lightboxitem2.save()
        response = self.app.get('/')
        lightbox_items = list(response.context['lightbox_items'])
        self.assertTrue(lightbox_items.index(lightboxitem1) < lightbox_items.index(lightboxitem2))

        lightboxitem1.order = 3
        lightboxitem1.save()
        response = self.app.get('/')
        lightbox_items = list(response.context['lightbox_items'])
        self.assertTrue(lightbox_items.index(lightboxitem1) > lightbox_items.index(lightboxitem2))

# create_pagebrowser_books
from optparse import make_option
import sys
from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
    help = "Creates (or initializes) pagebrowser books for the data in the database."
    base_options = (
        make_option("-f", "--filename", action="store", type="string", dest="filename",
                    help='If provided, directs output to a file instead of stdout.'),
    )
    option_list = BaseCommand.option_list + base_options

    def handle(self, **options):
        """create (or update) books in the pagebrowser"""
        from dasa import models

        def fixup_path(img_url):
            print img_url
            if not img_url:
                return

            if '/user_media/' in img_url:
                img_url = os.path.join('.', img_url[img_url.find('/user_media/') + len('/user_media/'):])
            if '/media/' in img_url:
                img_url = os.path.join('.', img_url[img_url.find('/media/') + len('/user_media/'):])
            if not img_url.startswith('uploads'):
                img_url = os.path.join('uploads', img_url)
            img_url = img_url.replace('/./', '/')
            return img_url

        for scan in models.Scan.objects.all():
            img_url = scan.image.name
            scan.image = fixup_path(img_url)
            scan.save()

        for hk in models.LightBoxItem.objects.all():
            hk.image = fixup_path(hk.image.name)
            hk.save()

        for hk in models.HartaKarunMainCategory.objects.all():
            hk.image = fixup_path(hk.image.name)
            hk.image_intro = fixup_path(hk.image_intro.name)
            hk.save()
        for hk in models.HartaKarunCategory.objects.all():
            hk.image = fixup_path(hk.image.name)
            hk.image_intro = fixup_path(hk.image_intro.name)
            hk.save()
        for hk in models.HartaKarunItem.objects.all():
            hk.image = fixup_path(hk.image.name)
            hk.save()
        for hk in models.BasicPage.objects.all():
            hk.image = fixup_path(hk.image.name)
            hk.image_description = fixup_path(hk.image_description.name)
            hk.save()
        for hk in models.News.objects.all():
            hk.image = fixup_path(hk.image.name)
            hk.image_description = fixup_path(hk.image_description.name)
            hk.save()

#         for hk in models.RetroBookScan.objects.all():
#             hk.image = fixup_path(hk.image.name)
#             hk.save()


        return


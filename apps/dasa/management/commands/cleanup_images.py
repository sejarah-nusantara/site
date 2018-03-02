import os
import re
import glob
from shutil import copyfile
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "remove unused images, move images in 'uploads' folder to new locations"

    def handle(self, **options):
        """create (or update) books in the pagebrowser"""
        def fixup_path(img_url):
            print 'fixing up img_url'
#             if not img_url:
#                 return
#
#             if '/user_media/' in img_url:
#                 img_url = os.path.join('.', img_url[img_url.find('/user_media/') + len('/user_media/'):])
#             if '/media/' in img_url:
#                 img_url = os.path.join('.', img_url[img_url.find('/media/') + len('/user_media/'):])
#             if img_url.startswith('uploads/'):
#                 img_url = img_url[len('uploads/'):]
#
#             return img_url
        from dasa import models
        # make a list of images used on the site
        # (the list contsist of (obj, attribute) tuples)
        used_images = []
        IMAGE_FIELDS = dict(settings.IMAGE_FIELDS)

        for klass in IMAGE_FIELDS:

            for obj in eval(klass).objects.all():
                for attr_name in IMAGE_FIELDS[klass]:
                    used_images.append((obj, attr_name))
#         for obj in models.BasicPage.objects.all():
#             used_images.append((obj, 'image'))
#             used_images.append((obj, 'image_description'))
#
#         for obj in models.HartaKarunCategory.objects.all():
#             used_images.append((obj, 'image'))
#             used_images.append((obj, 'image_intro'))
#
#         for obj in models.HartaKarunMainCategory.objects.all():
#             used_images.append((obj, 'image'))
#             used_images.append((obj, 'image_intro'))
#
#         for obj in models.HartaKarunItem.objects.all():
#             used_images.append((obj, 'image'))
#             used_images.append((obj, 'pdf'))
#             used_images.append((obj, 'pdf_id'))
#
#         for obj in models.LightBoxItem.objects.all():
#             used_images.append((obj, 'image'))
#
#         for obj in models.News.objects.all():
#             used_images.append((obj, 'image'))
#             used_images.append((obj, 'image_description'))
#
#         for obj in models.Scan.objects.all():
#             used_images.append((obj, 'image'))

        used_images = [(obj, getattr(obj, attr_name), attr_name) for obj, attr_name in used_images if getattr(obj, attr_name)]

        used_images_full_paths = [os.path.abspath(os.path.join(settings.MEDIA_ROOT, attr.name)) for obj, attr, attr_name in used_images]

        # list images linked in pages
        TEXT_FIELDS = dict(settings.TEXT_FIELDS)
        for klass in TEXT_FIELDS:
            for obj in eval(klass).objects.all():
                for attr_name in TEXT_FIELDS[klass]:
                    for lang_suffix in ['', '_en', '_id']:
                        s = getattr(obj, attr_name + lang_suffix)
                        if s:
#                             for link in re.findall('<img src=".*?"', s):
                            for link in re.findall('/media/.*?"', s):
                                link = link[len('/media/'):-len('"')]

                                full_path1 = os.path.abspath(os.path.join(settings.MEDIA_ROOT, link))
                                used_images_full_paths.append(full_path1)
                                if not 'uploads' in link:
                                    full_path2 = os.path.abspath(os.path.join(settings.MEDIA_ROOT, 'uploads', link))
                                    used_images_full_paths.append(full_path2)
                                if not os.path.exists(full_path1) and not os.path.exists(full_path2):
                                    print 'WARNING: file {full_path} is referenced by {obj} in {attr_name}{lang_suffix}, but cannot be found'.format(**locals())
                                if '/_versions/' in full_path1:
                                    used_images_full_paths.append(full_path1.replace('/_versions/', '/'))

        # list images in uploads
        images_in_uploads = glob.glob(os.path.join(settings.MEDIA_ROOT, 'uploads/*'))
        images_in_uploads += glob.glob(os.path.join(settings.MEDIA_ROOT, 'uploads/*/*'))
        images_in_uploads += glob.glob(os.path.join(settings.MEDIA_ROOT, 'uploads/*/*/*'))
        images_in_uploads += glob.glob(os.path.join(settings.MEDIA_ROOT, 'uploads/*/*/*/*'))
        images_in_uploads = [fn for fn in images_in_uploads if os.path.isfile(fn)]


#         for fn in images_in_uploads:
#             print fn
        unused_images = [fn for fn in images_in_uploads if fn not in used_images_full_paths]

        print 'TOTAL IMAGES USED IN CRM: ', len(used_images)
        print 'TOTAL IMAGES IN UPLOADS DIR: ', len(images_in_uploads)
        print 'TO DELETE', len(unused_images), 'images'
        for fn in unused_images:
            print fn
        return
        if unused_images:
            print 'deleting unused images...'
            for fn in unused_images:
                os.remove(fn)

        move_to = {
            models.HartaKarunItem: 'dasadefined/HartaKarunArticles',
            models.HartaKarunCategory: 'dasadefined/HartaKarunCategories',
            models.HartaKarunMainCategory: 'dasadefined/HartaKarunMainCategories',
            models.LightBoxItem: 'dasadefined/Lightbox',
            models.News: 'dasadefined/News',
            models.BasicPage: 'dasadefined/Pages',
            models.Scan: 'dasadefined/Images',
        }

        for dirname in move_to.values():

            if not os.path.exists(os.path.join(settings.MEDIA_ROOT, dirname)):
                os.mkdir(os.path.join(settings.MEDIA_ROOT, dirname))

        print 'moving images'
        for obj, img, attr_name in used_images:
            if img.name.startswith('uploads/'):
                origin = os.path.join(settings.MEDIA_ROOT, img.name)
                if not os.path.exists(origin):
                    print 'WARNING: file {origin} does not exist (used in {obj} - {obj.id})'.format(**locals())
                    continue
                destination_dir = move_to[obj.__class__]
                fn = img.name[len('uploads/'):]
                destination_candidate = os.path.join(settings.MEDIA_ROOT, destination_dir, fn)
                destination = destination_candidate
                i = 0

                while os.path.exists(destination):
                    f1 = open(origin)
                    f2 = open(destination)
                    if f1.read() == f2.read():
                        # they are the same
                        break
#                         continue

                    i += 1
                    destination = '{destination_candidate}_{i}'.format(**locals())

                print 'moving {img.name} to {destination}'.format(**locals())
                setattr(obj, attr_name, destination)
                obj.save()
                copyfile(origin, destination[len(settings.MEDIA_ROOT) + 1:])
                os.remove(origin)

        print 'cleaning up'

        for obj, attr, attr_name in used_images:
            fn = attr.name
            if fn.startswith(settings.MEDIA_ROOT):
                fn = fn[len(settings.MEDIA_ROOT):]
                if fn.startswith('/'):
                    fn = fn[1:]
                setattr(obj, attr_name, fn)
                obj.save()

        print 'done'
        return

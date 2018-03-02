#
# copyright Gerbrandy SRL
# www.gerbrandy.com
# 2013
#


from modeltranslation.translator import translator, TranslationOptions
from dasa import models


class PageTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'content', 'image_caption', 'image_description_caption', 'meta_keywords', 'meta_description',)

translator.register(models.BasicPage, PageTranslationOptions)


class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'content', 'image_caption', 'image_description_caption',)

translator.register(models.News, NewsTranslationOptions)


class HartaKarunMainCategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'shortIntroText', 'longIntroText', 'image_description_caption', 'image_caption',)
translator.register(models.HartaKarunMainCategory, HartaKarunMainCategoryTranslationOptions)


class HartaKarunCategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'shortIntroText', 'longIntroText', 'image_caption', 'image_description_caption',)
translator.register(models.HartaKarunCategory, HartaKarunCategoryTranslationOptions)


class HartaKarunItemTranslationOptions(TranslationOptions):
    fields = ('short_title', 'long_title', 'introduction', 'citation',
        'comment', 'image_caption',)

translator.register(models.HartaKarunItem, HartaKarunItemTranslationOptions)


class ScanTranslationOptions(TranslationOptions):
    fields = ['image_caption']

translator.register(models.Scan, ScanTranslationOptions)


class ResolutionTranslationOptions(TranslationOptions):
    fields = []
translator.register(models.Resolution, ResolutionTranslationOptions)


class JournalEntryTranslationOptions(TranslationOptions):
    fields = []
translator.register(models.JournalEntry, JournalEntryTranslationOptions)


class TimeLineItemTranslationOptions(TranslationOptions):
    fields = ['caption', ]
translator.register(models.TimeLineItem, TimeLineItemTranslationOptions)


class LightBoxItemTranslationOptions(TranslationOptions):
    fields = ['title', 'url']

translator.register(models.LightBoxItem, LightBoxItemTranslationOptions)


class MetaTagsTranslationonOptions(TranslationOptions):
    fields = ['keywords', 'description']

translator.register(models.MetaTags, MetaTagsTranslationonOptions)
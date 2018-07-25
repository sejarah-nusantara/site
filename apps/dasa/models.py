#
# copyright Gerbrandy SRL
# www.gerbrandy.com
# 2013
#

import datetime
import os
import re

from django.db import models
# from django.utils.translation import ugettext as _
# don't translate the backend
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.defaultfilters import date as format_date
from django.contrib.auth.models import User
from django.utils import translation
from django.utils.safestring import mark_safe

from userena.models import UserenaBaseProfile

from south.modelsinspector import add_introspection_rules

from filebrowser.fields import FileBrowseField
from filebrowser.base import FileObject

from tinymce import models as tinymce_models

from haystack.query import SearchQuerySet

from dasa.utils import first_words, format_date_for_timeglider, sluggify
from dasa.utils import pagebrowser_id
from dasa.repository import repository
from dasa import config
from dasa import utils

_ = lambda x: x  # @IgnorePep8


IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff']


class FileBrowseField(FileBrowseField):
    # patch filebrowsefield

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        if not value or not isinstance(value, FileObject):
            return value
        return value.path

    def get_prep_value(self, value):
        if not value or not isinstance(value, FileObject):
            return value
        return value.path


class ImageFieldMainText(FileBrowseField):
    def __init__(self, directory=settings.UPLOAD_TO, max_length=255, null=True, blank=True, extensions=IMAGE_EXTENSIONS):
        return super(ImageFieldMainText, self).__init__(
            _('Image (main text)'),
            directory=directory,
            blank=blank,
            null=null,
            max_length=255,
            extensions=IMAGE_EXTENSIONS,
            )


class ImageFieldIntro(FileBrowseField):
    def __init__(self, directory=settings.UPLOAD_TO, max_length=255, null=True, blank=True, extensions=IMAGE_EXTENSIONS):
        return super(ImageFieldIntro, self).__init__(
            _('Image (description)'),
            directory=directory,
            max_length=255,
            blank=blank,
            null=null,
            extensions=IMAGE_EXTENSIONS,
            )


# these 'introspection rules' are used by South in creating the migrations
add_introspection_rules([], ["^dasa\.models\.FileBrowseField"])
add_introspection_rules([], ["^dasa\.models\.ImageFieldIntro"])
add_introspection_rules([], ["^dasa\.models\.ImageFieldMainText"])


def CaptionField(image_field):
    return models.CharField(_('Caption for ') + image_field.verbose_name, max_length=255, blank=True, null=True)


class DasaWrapper(object):
    """provides some general functionality shared by all Dasa objects"""
    def __unicode__(self):
        if hasattr(self, 'title'):
            if callable(self.title):
                return self.title()
            elif self.title:
                return self.title
        return unicode(super(DasaWrapper, self))

    def admin_link(self):
        """a link to the admin page - used in admin inline forms"""
        link = '<a href="%s">%s</a>' % (reverse("admin:dasa_%s_change" % self._meta.module_name, args=(self.id,)), unicode(self))
        return link

    admin_link.allow_tags = True
    admin_link.short_description = _('Title')

    def get_field(self, name):
        d = dict([(x.name, x) for x in self._meta.fields])
        try:
            return d[name]
        except KeyError:
            raise KeyError('No field with name %s' % name)

    def get_value(self, field_name):
        return getattr(self, field_name, None)

    def get_fields(self, include=[], exclude=[], exclude_values=[]):
        """list all fields defined for this model

        arguments:
            include, exclude: lists of attribute names
            exclude_values: if the value of a field is in this list, it will be excluded from the result
        returns:
            a list of pairs (instance_of_Field, value)
        """
        ls = self._meta.fields
        ls = [x for x in ls if x.attname[-3:] not in ['_id', '_en']]
        if include:
            ls = [self.get_field(x) for x in include]
        if exclude:
            ls = [x for x in ls if x.attname not in exclude]
        items = [(x, getattr(self, x.attname)) for x in ls]
        items = [item for item in items if item[1] not in exclude_values]
        return items

    def repr_for_search_result(self):
        """return a nice representation for search results"""
        return u'<span class="searchresult_title">%s</span> <span class="searchresult_type">(%s)</span>' % (self, self._meta.verbose_name)

    def solr_index(self):
        """Return a string that serves as the basis of full-text search

        we put the values of *all* fields in the sorl index

        returns:
            a string
        """
        STOPWORDS = [
            'not applicable',
            'not available',
            'not translated',
            'ID_ANRI',
            'HR',
            'Y',
            'N'
        ]
        ls = [v for _k, v in self.get_solr_fields()]
        ls = [v for v in ls if v]
        ls = [unicode(v) for v in ls]
        ls = [v for v in ls if v not in STOPWORDS]
        ls = [v for v in ls if not v.isdigit()]
        ls = [v for v in ls if not v.endswith('.png')]
        return '\n'.join(ls)

    def get_solr_fields(self):
        return self.get_fields(exclude=['type'])

    @models.permalink
    def get_absolute_url(self):
        """return an url of a representation of this object"""
        return ('%s' % self.__class__.__name__.lower(), (), {'path': self.id})

    def fields(self):
        """a helper, so we do this in a template: "item.fields.<field_name>.verbose_name"
        """
        def _setval(field, value):
            field.value = value
            return field
        return dict((field.name, _setval(field, value)) for field, value in self.get_fields())


class Appendix(DasaWrapper, models.Model):
    """This is a Appendix to the Resolution books
    """
    class Meta:
        db_table = 'dasa_appendix'
        verbose_name = _('Appendix to general resolutions')
        verbose_name_plural = _('Appendices to general resolutions')
        ordering = ('order',)

    archiveFile = models.TextField(_('Filenumber'), blank=True)
    folio_number_from = models.CharField('%s (%s)' % (_('Folionumber'), _('from')), max_length=255, blank=True)
    folio_number_to = models.CharField('%s (%s)' % (_('Folionumber'), _('to')), max_length=255, blank=True)
    folio_number_extra = models.CharField('%s (%s)' % (_('Folionumber'), _('extra')), max_length=255, blank=True)

    document_type_nl = models.TextField(blank=True, max_length=255)
    title_nl = models.TextField(blank=True, max_length=255)

    doc_y = models.IntegerField(blank=True, null=True)
    doc_m = models.IntegerField(blank=True, null=True)
    doc_d = models.IntegerField(blank=True, null=True)
    res_y = models.IntegerField(blank=True, null=True)
    res_m = models.IntegerField(blank=True, null=True)
    res_d = models.IntegerField(blank=True, null=True)

    vessel_names = models.TextField(_('Ship Names'), blank=True)
    person_names_asian = models.TextField(_('Asian names'), blank=True)
    person_names_european = models.TextField(_('European names'), blank=True)
    place_names = models.TextField(_('Place names'), blank=True)

    notes = models.TextField(blank=True, null=True)

    order = models.PositiveIntegerField(_("Order"), blank=True, null=True)

    def __unicode__(self):
        return u'<Appendix to the resolution books - {self.pk} - {self.title_nl}>'.format(self=self)

    def __str__(self):
        return self.__unicode__()

    def archive_reference(self):
        folio_number_to = self.folio_number_to
        if self.folio_number_extra:
            folio_number_to += ', ' + self.folio_number_extra
        return archive_reference(self.archiveFile, self.folio_number_from, folio_number_to)

    def link_to_pagebrowser(self):
        return link_to_pagebrowser(self.archiveFile, self.folio_number_from)

    def doc_date(self):
        return utils.prettyprint_date(self.doc_y, self.doc_m, self.doc_d)

    def res_date(self):
        return utils.prettyprint_date(self.res_y, self.res_m, self.res_d)

    def vessel_names_as_list(self):
        s = self.vessel_names
        if s:
            ls = s.split(';')
            ls = [x.strip(';,. \n') for x in ls]
            return ls
        else:
            return []

    def person_names_european_list(self):
        s = self.person_names_european
        if s:
            ls = s.split(';')
            ls = [x.strip(';,. \n') for x in ls]
            return ls
        else:
            return []

    def person_names_asian_list(self):
        s = self.person_names_asian
        if s:
            ls = s.split(';')
            ls = [x.strip(';,. \n') for x in ls]
            return ls
        else:
            return []

    def place_names_list(self):
        s = self.place_names
        if s:
            ls = s.split(';')
            ls = [x.strip(';,. \n') for x in ls]
            return ls
        else:
            return []

    def get_absolute_url(self):
        return reverse(config.SLUG_APPENDIX_BROWSE) + '?selected=%s' % self.id

    def repr_for_search_result(self):
        return '<span class="searchresult_title">%s</span> <span class="searchresult_type">(%s)</span>' % (self.title_nl, self._meta.verbose_name)


class BasicPage(DasaWrapper, models.Model):
    """A page on the website
    """
    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")
        ordering = ['title', 'slug']

    title = models.CharField(_('Title'), max_length=255)
    description = models.TextField(_('Description'), blank=True)
    image_description = ImageFieldIntro()
    image_description_caption = CaptionField(image_description)
    content = models.TextField(_('Content'), blank=True)
    image = ImageFieldMainText()
    image_caption = CaptionField(image)

    slug = models.CharField(_('Slug'), max_length=100, blank=True)  # defined the URL where this page can be found

    meta_keywords = models.TextField(
        ('Keywords'),
        help_text=('The "keywords" are used by search engines.'),
        null=True,
        blank=True,
        )
    meta_description = models.TextField(
        ('Description'),
        help_text=('The "description" is used by search engines and other web services'),
        null=True,
        blank=True,
        )

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        # before saving, make sure we have a sensible slug
        if not self.slug:
            self.slug = self.title
        existing_slugs = [x.slug for x in BasicPage.objects.all() if x != self]
        self.slug = sluggify(self.slug)
        _slug = self.slug  # strip trailing /
        i = 1
        while self.slug in existing_slugs:
            self.slug = '%s_%s' % (_slug, i)
            i += 1
        self.slug = sluggify(self.slug)

        super(BasicPage, self).save(*args, **kwargs)

    def first_paragraphs(self):
        return '\n'.join(self.split_paragraphs()[:2])

    def other_paragraphs(self):
        """return that part of self.content that is not returned by self.first_paragraphs"""
        return '\n'.join(self.split_paragraphs()[2:])

    def split_paragraphs(self):
        """separate the first paragraph in self.content from the following paragraphs

        return a list of paragraphs
        """
        s = self.content
        boundary = '</p>'
        matches = list(re.finditer(boundary, s))
        paragraphs = []
        start = 0
        for m in matches:
            paragraphs.append(s[start:m.end()])
            start = m.end()
        paragraphs.append(s[start:])
        paragraphs = [x for x in paragraphs if x]
        return paragraphs

    @models.permalink
    def get_absolute_url(self):
        """return an url of a representation of this object"""
        return ('%s' % self.__class__.__name__.lower(), (), {'path': self.slug})


class News(DasaWrapper, models.Model):
    """a News item is just like a Page, but with a date attribute"""
    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'
        ordering = ['-date']

    title = models.CharField(_('Title'), max_length=255)
    date = models.DateField(_('Date'), default=datetime.date.today())
    description = models.TextField(_('Description'), blank=True)
    image_description = ImageFieldIntro()
    image_description_caption = CaptionField(image_description)
    content = tinymce_models.HTMLField(_('Content'), blank=True)
    image = ImageFieldMainText()
    image_caption = CaptionField(image)


class HartaKarunMainCategory(DasaWrapper, models.Model):
    """A collection of HataKarunCategory objects"""
    class Meta:
        verbose_name = 'Harta Karun Main Category'
        verbose_name_plural = 'Harta Karun Main Categories'
        ordering = ['position']

    name = models.CharField(_('Title'), max_length=255)
    shortIntroText = models.TextField(_('Description'), blank=True)
    image_intro = ImageFieldIntro()
    image_description_caption = CaptionField(image_intro)
    longIntroText = tinymce_models.HTMLField(_('Main Text'), blank=True)
    image = ImageFieldMainText()
    image_caption = CaptionField(image)
    position = models.IntegerField(_('Position'), blank=True,)

    def save(self, *args, **kwargs):
        if not self.position:
            self.position = 1
        super(HartaKarunMainCategory, self).save(*args, **kwargs)

    @property
    def title(self):
        return self.name

    @property
    def description(self):
        return self.shortIntroText

    @property
    def image_description(self):
        return self.image_intro

    @property
    def content(self):
        return self.longIntroText


class HartaKarunCategory(DasaWrapper, models.Model):
    """The main category for hartakarun items

    """
    class Meta:
        verbose_name = 'Harta Karun Category'
        verbose_name_plural = 'Harta Karun Categories'
        ordering = ['name']

    name = models.CharField(_('Title'), max_length=255)
    shortIntroText = models.TextField(_('Description'), blank=True,
        help_text="This information will appear on the page below the title")
    image_intro = ImageFieldIntro()
    image_description_caption = CaptionField(image_intro)

    longIntroText = tinymce_models.HTMLField(_('Introduction'), blank=True,)
    image = ImageFieldMainText()
    image_caption = CaptionField(image)

    hartakarun_main_category = models.ForeignKey(
        'dasa.HartaKarunMainCategory',
        null=True,
        related_name='subcategories',
        verbose_name='Harta Karun Main Category',
        )

    @property
    def image_description(self):
        # this property serves to make the model compatible with page ...
        return self.image_intro

    @property
    def content(self):
        return self.longIntroText

    def __unicode__(self):
        return self.name

    @property
    def title(self):
        return self.name

    @property
    def published_hartakarun_items(self):
        return self.hartakarun_items.filter(release_date__lte=datetime.datetime.now())

    @property
    def number_of_articles(self):
        number_of_articles = self.published_hartakarun_items.count()
        return number_of_articles

    def print_number_of_articles(self):
        number_of_articles = self.number_of_articles
        if number_of_articles == 1:
            noun = _('article')
        else:
            noun = _('articles')
        return '%s %s' % (number_of_articles, noun)

    @property
    def extended_title(self):
        """return title with number of articles"""
        return '%s (%s)' % (self.title, self.print_number_of_articles())

    @property
    def description(self):
        return self.shortIntroText

    @property
    def hartakarun_parent_position(self):
        """
        ??
        """
        return self.hartakarun_parent.position

    def _all_hk_categories(self):
        """return all HartaKarun objects in correct order (i.e. ordered by position of parent and own position)
        """
        ls = HartaKarunCategory.objects.all()
        ls = [(x.hartakarun_parent and x.hartakarun_parent.position or x.position, x.position, x) for x in ls]
        ls.sort()
        ls = [x[-1] for x in ls]
        return ls

    def next(self):
        """return the next category"""
        ls = self._all_hk_categories()
        idx = ls.index(self)
        if idx < len(ls) - 1:
            return ls[idx + 1]

    def previous(self):
        """return the previous category"""
        ls = self._all_hk_categories()
        idx = ls.index(self)
        if idx > 0:
            return ls[idx - 1]


class HartaKarunItem(DasaWrapper, models.Model):
    """

    for translation options cf: HartaKarunItemTranslationOptions
    """
    class Meta:
        verbose_name = _('Harta Karun Article')
        verbose_name_plural = _('Harta Karun Articles')

    # short_title is registered for translation
    number = models.CharField(
        _('Number'),
        max_length=50,
        null=True,
        unique=True,
        )

    short_title = models.CharField(
        _('Title'),
        max_length=255,
        )

    long_title = models.TextField(
        _('Description'),
        blank=True,
        help_text="This text will appear on the HartaKarun web page below the title",
        )

    title_nl = models.CharField(
        _('Original title'),
        blank=True,
        help_text='Original title',
        max_length=255,
        )

    release_date = models.DateField(
        _('Release Date'),
        max_length=255,
        blank=True,
        null=True,
        help_text='date on which the HK item is released (the item will be visible on the site only after this date)',
        )

    hartakaruncategory = models.ForeignKey(
        HartaKarunCategory,
        related_name='hartakarun_items',
        verbose_name=HartaKarunCategory._meta.verbose_name
        )

    # citation is registred for translation
    citation = tinymce_models.HTMLField(
        _('Citation'),
        blank=True,
        help_text="A textual string that can be used when referring to this HK item in a publication",
        )

    introduction = tinymce_models.HTMLField(
        _('Introduction'),
        blank=True,
        help_text=_("a scientific introduction to the Harta Karun document."),
        )

    edited_by = models.CharField(
        _('Editing'),
        max_length=255,
        blank=True,
        )

    introduced_by = models.CharField(
        _('Introduced'),
        max_length=255,
        blank=True,
        )

    selected_by = models.CharField(
        _('Document selection'),
        max_length=255,
        blank=True,
        )

    transcription = tinymce_models.HTMLField(
        _('Transcription'),
        blank=True,
        null=True,
        )

    transcribed_by = models.CharField(
        _('Dutch Text Transcription'),
        max_length=255,
        blank=True,
        )

    translation_id = tinymce_models.HTMLField(
        _('Translation in Indonesian'),
        blank=True,
        null=True,
        )

    translation_en = tinymce_models.HTMLField(
        _('Translation in English'),
        blank=True,
        null=True,
        )

    translated_en_by = models.CharField(
        _('English translation'),
        max_length=255,
        blank=True,
        help_text="name of person responsible for the translation of the Harta Karun document transcription to English",
    )

    translated_id_by = models.CharField(
        _('Indonesian translation'),
        blank=True,
        max_length=255,
        help_text="name of person responsible for the translation of the Harta Karun document transcription to Indonesian",
        )

    image = ImageFieldIntro()
    image_caption = CaptionField(image)

    date_on_timeline = models.DateField(
        _('Historical Date'),
        blank=True,
        null=True,
        help_text="Please fill in a date in the format yyyy-mm-dd",
        )

    ISBN = models.CharField(
        _('Publication Reference'),
        max_length=100,
        blank=True,
        help_text=_('ISBN number or DOI number'),
        )

    archivalSourceReference = models.CharField(
        _('Archival Source'),
        max_length=1000,
        blank=True,
        help_text='an archival reference to the archive file and folio numbers that apply to the article',
        )

    # comment is registered for translation
    comment = models.TextField(
        _('Comments'),
        blank=True,
        help_text="Not visible on the website",
        )

    pdf = FileBrowseField(
        _('PDF with full text [en]'),
        directory=settings.UPLOAD_TO,
        blank=True,
        null=True,
        max_length=255,
        extensions=[".pdf", ".doc"],
    )

    pdf_id = FileBrowseField(
        _('PDF with full text [id]'),
        directory=settings.UPLOAD_TO,
        blank=True,
        null=True,
        max_length=255,
        extensions=[".pdf", ".doc"],
    )

    @property
    def title(self):
        return self.short_title

    def description(self):
        return self.long_title

    def __unicode__(self):
        return unicode(self.short_title)

    def slug(self):
        """used to identify this thing"""
        return self.short_title_en

    def repr_for_timeglider(self):
        """returns a dictionary that will be used as the json source for the timeglider widget"""
        startdate = self.date_on_timeline
        d = {
            'id': self.pk,
            'title': '%s' % self.short_title,
            'description': self.long_title,
            "startdate": format_date_for_timeglider(startdate),
            'importance': 50,  # required
            "icon": "/static/images/icons/circle_red.png",
            "link": self.get_absolute_url(),
        }
        return d

    def pages(self):
        return self.scans.all()

    def get_absolute_url(self):
        return reverse('hartakarunitem', args=(self.number,))

    def link_to_pdf(self):
        # return a link to the pdf file with an indication of its size
        page = self
        if translation.get_language() == 'id':
            page_pdf = page.pdf_id or page.pdf
        else:
            page_pdf = page.pdf
        if page_pdf:
#            # TODO: make filesize work again
#             pdf_link = '<a href="{url}">{text} ({size} kB)</a>'.format(
#                 url=page_pdf.url,
#                 size=filesize,
#                 text=_("Download the full article in PDF"),
#                 )
            pdf_link = '<a href="{url}">{text}</a>'.format(
                url=page_pdf.url,
                text=_("Download the full article in PDF"),
                )
        else:
            pdf_link = ''
        return pdf_link


class Scan(DasaWrapper, models.Model):
    """An image belowing to a HartaKarun Item"""
    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')
        ordering = ['position']

    reference = models.CharField(('Reference [??]'), max_length=255, blank=True)
    hartakarun_item = models.ForeignKey(HartaKarunItem, null=True, related_name="scans")
    institution = models.CharField(('InstitutionID [??]'), max_length=255, blank=True)
    fonds = models.CharField(('FondsID [??]'), max_length=255, blank=True)
    file_id = models.CharField(('File Identifier'), max_length=255, blank=True)
    position = models.PositiveSmallIntegerField("Position", blank=True, null=True)
    image = FileBrowseField(_('Image'), directory=settings.UPLOAD_TO, blank=True, null=True, max_length=255,
        extensions=IMAGE_EXTENSIONS,)
    image_caption = CaptionField(image)

    def __unicode__(self):
        return u'%s-%s-%s-%s' % (self.hartakarun_item, self.reference, self.file_id, self.position)

    def get_pagenumber(self):
        return self.position


def archive_reference(archiveFile, folio_number_from, folio_number_to=None):
    result = ''
    if archiveFile:
        result += 'file %s' % utils.to_integer(archiveFile)
        result += ', folio '
        result += folio_number_from
        if folio_number_to:
            result += '-'
            result += folio_number_to

    return result


def link_to_pagebrowser(archiveFile, folio_number, archive='K66a'):
    archive_id = settings.ARCHIVE_IDS[archive]
    language_code = translation.get_language()
    if archive == 'CorpusDipl':
        ead_id = 'CorpusDiplomaticum'
    elif archive == 'DeHaan':
        ead_id = 'DeHaan'
    else:
        ead_id = settings.LANGUAGE2EAD.get(language_code, settings.LANGUAGE_CODE)
    pb_url = os.path.join(settings.PAGEBROWSER_PUBLIC_URL, pagebrowser_id(ead_id=ead_id, archive_id=archive_id, archiveFile=archiveFile))
    pb_url += '?page_number=%s' % folio_number
    return pb_url


class Placard(DasaWrapper, models.Model):
    """Placard

    """
    class Meta:
        verbose_name = _("Placard")
        verbose_name_plural = _("Placards")

    def __unicode__(self):
        return u'Placard issued on {self.issued_date_d}-{self.issued_date_m}-{self.issued_date_y}'.format(self=self)

    volume_number = models.CharField(max_length=255, blank=True)
    page_number_from = models.CharField('%s (%s)' % (('Pagenumber'), _('from')), max_length=255, blank=True)
    page_number_to = models.CharField('%s (%s)' % (('Pagenumber'), _('from')), max_length=255, blank=True, null=True)
    governor = models.CharField(max_length=255, blank=True, null=True)
    issued_date_d = models.IntegerField(blank=True, null=True)
    issued_date_m = models.IntegerField(blank=True, null=True)
    issued_date_y = models.IntegerField(blank=True, null=True)
    published_date_d = models.IntegerField(blank=True, null=True)
    published_date_m = models.IntegerField(blank=True, null=True)
    published_date_y = models.IntegerField(blank=True, null=True)
    text = models.TextField()
    next = models.ForeignKey('Placard', blank=True, null=True, related_name='previous')
    order = models.PositiveIntegerField(_("Order"), blank=True, null=True)

    @property
    def governors(self):
        return filter(None, [self.governor])

    def issued_date(self):
        return utils.prettyprint_date(self.issued_date_y, self.issued_date_m, self.issued_date_d)

    @property
    def issued_date_as_date(self):
        return utils.to_date(self.issued_date_y, self.issued_date_m, self.issued_date_d)

    def published_date(self):
        return utils.prettyprint_date(self.published_date_y, self.published_date_m, self.published_date_d)

    def get_absolute_url(self):
        return reverse(config.SLUG_PLACARD_BROWSE) + '?selected=%s' % self.id


class DiplomaticLetter(DasaWrapper, models.Model):
    """Diplomatieke Brief

    """
    class Meta:
        verbose_name = _("Diplomatic Letter")
        verbose_name_plural = _("Diplomatic Letters")
        ordering = ['insertion_date']

    volume = models.CharField(blank=True, max_length=255)
    pagePubFirst = models.CharField(blank=True, max_length=255)
    pagePubLast = models.CharField(blank=True, max_length=255)

    archiveFile = models.TextField(_('Filenumber'), blank=True)
    folio_number_from = models.CharField('%s (%s)' % (_('Folionumber'), _('from')), max_length=255, blank=True)
    folio_number_to = models.CharField('%s (%s)' % (_('Folionumber'), _('to')), max_length=255, blank=True)
    insertion_y = models.IntegerField(blank=True, null=True)
    insertion_m = models.IntegerField(blank=True, null=True)
    insertion_d = models.IntegerField(blank=True, null=True)
    insertion_date = models.DateField(blank=True, null=True)
    original_y = models.IntegerField(blank=True, null=True)
    original_m = models.IntegerField(blank=True, null=True)
    original_d = models.IntegerField(blank=True, null=True)

    originalLetterAvailableYN = models.CharField(blank=True, max_length=1)
    sealedYN = models.CharField(blank=True, max_length=1)
    originalLanguage = models.CharField(blank=True, max_length=255)
    translatedInto = models.CharField(blank=True, max_length=255)

    notes = models.TextField(blank=True, null=True)
    rulers = models.ManyToManyField('DiplomaticLetterRuler', related_name='letters')
    sources = models.ManyToManyField('DiplomaticLetterLocation', related_name='letters_from')
    destinations = models.ManyToManyField('DiplomaticLetterLocation', related_name='letters_to')

    order = models.PositiveIntegerField(_("Order"), blank=True, null=True)
    next = models.ForeignKey('DiplomaticLetter', blank=True, null=True, related_name='previous')

    def title(self):
        return u'Diplomatic Letter {insertion_date}'.format(**self.__dict__)

    def locations(self):
        return list(set(self.destinations() + self.sources()))

    def get_source_names(self):
        return [location.city for location in self.sources.all()]

    def get_destination_names(self):
        return [location.city for location in self.destinations.all()]

    def get_location_names(self):
        return list(set(self.get_destination_names() + self.get_source_names()))

    def get_ruler_names(self):
        return [ruler.name_modern for ruler in self.rulers.all()]

    def archive_reference(self):
        return archive_reference(self.archiveFile, self.folio_number_from, self.folio_number_to)

    def link_to_pagebrowser(self):
        return link_to_pagebrowser(self.archiveFile, self.folio_number_from)

    def link_to_hathitrust(self):
        return '/hathi{volume}'.format(volume=utils.to_integer(self.volume))

    def hathitrust_reference(self):
        result = ''
        if self.volume:
            result += _('volume') + ' ' + utils.to_integer(self.volume)
            result += ', ' + _('page') + ' ' + utils.to_integer(self.pagePubFirst)
            if self.pagePubLast:
                result += '-'
                result += utils.to_integer(self.pagePubLast)
        return result

    def print_original_date(self):
        return utils.prettyprint_date(self.original_y, self.original_m, self.original_d)

    def get_absolute_url(self):
        return reverse(config.SLUG_DIPLOMATICLETTERS_BROWSE) + '?selected=%s' % self.id

    def repr_for_search_result(self):
        """return a nice representation for search results"""
        return u'<span class="searchresult_title">%s</span> <span class="searchresult_type">(%s)</span>' % (self, self._meta.verbose_name)

    def solr_index(self):
        result = super(DiplomaticLetter, self).solr_index()
        if self.originalLetterAvailableYN == "Y":
            result += "\nOriginal letter available"
        if self.sealedYN == "Y":
            result += "\nSealed"
        return result


class DiplomaticLetterRuler(DasaWrapper, models.Model):
    class Meta:
        verbose_name = _("Diplomatic Letter - Ruler")
        verbose_name_plural = _("Diplomatic Letter - Rulers")

    name_modern = models.CharField(max_length=255)
    period_start = models.CharField(max_length=255, null=True)
    period_end = models.CharField(max_length=255, null=True)
    location = models.CharField(max_length=255, null=True)
    alternative_name1 = models.CharField(max_length=255, null=True)
    alternative_name2 = models.CharField(max_length=255, null=True)
    alternative_name3 = models.CharField(max_length=255, null=True)
    alternative_name4 = models.CharField(max_length=255, null=True)
    alternative_name5 = models.CharField(max_length=255, null=True)
    alternative_name6 = models.CharField(max_length=255, null=True)
    alternative_name7 = models.CharField(max_length=255, null=True)
    alternative_name8 = models.CharField(max_length=255, null=True)
    reference = models.TextField(null=True)

    def title(self):
        return self.name_modern

    def period(self):
        period_end = self.period_end or ''
        period_end = period_end.strip()
        if period_end.endswith('.0'):
            period_end = period_end[:-2]

        period_start = self.period_start or ''
        period_start = period_start.strip()
        if period_start.endswith('.0'):
            period_start = period_start[:-2]

        if period_start or period_end:
            return '({period_start}-{period_end})'.format(period_end=period_end, period_start=period_start)
        else:
            return ''

    def alternativenames(self):
        ls = [
            self.alternative_name1,
            self.alternative_name2,
            self.alternative_name3,
            self.alternative_name4,
            self.alternative_name5,
            self.alternative_name6,
            self.alternative_name7,
            self.alternative_name8,
            ]
        ls = filter(None, ls)
        return ls

    @property
    def number_of_letters(self):
        return self.letters.count()

    def get_absolute_url(self):
        return reverse(config.SLUG_DIPLOMATICLETTERS_RULERS) + '?selected=%s' % self.id

    def repr_for_search_result(self):
        """return a nice representation for search results"""
        return u'<span class="searchresult_title">%s</span> <span class="searchresult_type">(%s)</span>' % (self, self._meta.verbose_name)

    def get_solr_fields(self):
        return self.get_fields(exclude=['type', 'reference'])


class DiplomaticLetterLocation(DasaWrapper, models.Model):

    class Meta:
        verbose_name = _("Diplomatic Letter - Location")
        verbose_name_plural = _("Diplomatic Letter - Locations")

    continent = models.CharField(max_length=255, null=True)
    region = models.CharField(max_length=255, null=True)
    region_altenative_name = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    city_alternative_name = models.CharField(max_length=255, null=True)
    city_alternative_name2 = models.CharField(max_length=255, null=True)
    city_alternative_name3 = models.CharField(max_length=255, null=True)
    exact = models.CharField(max_length=1, null=True)
    place = models.TextField(null=True)
    reference = models.TextField(null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    def title(self):
        s = ''
        if self.city:
            s += self.city
        s += ' -- ' + self.specifications_without_city()
        return s

    def order(self):
        return self.pk

    def specifications_without_city(self):
        specs = [
            self.place,
            ', '.join(filter(None, [self.city_alternative_name, self.city_alternative_name2, self.city_alternative_name3])),
            self.region,
            self.region_altenative_name,
            self.continent,
            ]
        specs = filter(None, specs)
        return ' > '.join(specs)

    @property
    def number_of_letters(self):
        sqs = SearchQuerySet().models(DiplomaticLetter)
        sqs = sqs.filter(locations__exact=self.city)
        return sqs.count()

    def get_absolute_url(self):
        return reverse(config.SLUG_DIPLOMATICLETTERS_LOCATIONS) + '?selected=%s' % self.id

    def repr_for_search_result(self):
        """return a nice representation for search results"""
        return u'<span class="searchresult_title">%s</span> <span class="searchresult_type">(%s)</span>' % (self, self._meta.verbose_name)

    def latitude_as_string(self):
        # return non-localized string for use with googel maps api
        return unicode(self.latitude).replace(',', '.')

    def longitude_as_string(self):
        # return non-localized string for use with googel maps api
        return unicode(self.longitude).replace(',', '.')


class JournalEntry(DasaWrapper, models.Model):
    """Marginalia

    An entry in the daily journal

    [this class is a bit of a misnomer - it should have been called Marginalia]
    """
    class Meta:
        verbose_name = _("Marginalia to the Daily Journals")
        verbose_name_plural = _("Marginalia to the Daily Journals")

    description = models.TextField(_('Description'), blank=True)
    date = models.DateField(_('Date'), blank=True)
    priority = models.CharField(_('Priority'), max_length=255, blank=True)
    folio_number_from = models.CharField('%s (%s)' % (_('Folionumber'), _('from')), max_length=255, blank=True)
    folio_number_to = models.CharField('%s (%s)' % (_('Folionumber'), _('to')), max_length=255, blank=True)
    annotation = models.TextField(_('Annotation'), blank=True)
    vessel_names = models.TextField(_('Ship Names'), blank=True)
    order = models.PositiveIntegerField(_("Order"), blank=True, null=True)
    next = models.ForeignKey('JournalEntry', blank=True, null=True, related_name='previous')
    archiveFile = models.CharField(_('File'), max_length=255, blank=True)
    person_names_asian = models.TextField(_('Asian names'), blank=True)
    person_names_european = models.TextField(_('European names'), blank=True)
    place_names = models.TextField(_('Place names'), blank=True)

    @property
    def title(self):
        return self.description

    def archive_reference(self):
        return archive_reference(self.archiveFile, self.folio_number_from, self.folio_number_to)

    def link_to_pagebrowser(self):
        return link_to_pagebrowser(self.archiveFile, self.folio_number_from)

    def get_absolute_url(self):
        return reverse(config.SLUG_MARGINALIA_BROWSE) + '?selected=%s' % self.id

    def repr_for_search_result(self):
        return '<span class="searchresult_title">%s: %s</span> <span class="searchresult_type">(%s)</span>' % (format_date(self.date), self.description, self._meta.verbose_name)

# class MarginaliaPersonNamesAsian(DasaWrapper, models.Model):
#     class Meta:
#         verbose_name = _("Asian name")
#         verbose_name_plural = _("Asian names")
#     name = models.TextField(_('Name'))

class TimeLineItem(DasaWrapper, models.Model):

    class Meta:
        verbose_name = 'Timeline Item'
        verbose_name_plural = 'Timeline Items'
    year = models.IntegerField(_('Year'))
    month = models.IntegerField(_('Month'), blank=True, null=True)
    day = models.IntegerField(_('Day'), blank=True, null=True)
    caption = models.CharField(_('Fonds'), max_length=1000, blank=True)

    def repr_for_timeglider(self):
        """returns a dictionary that will be used as the json source for the timeglider widget"""
        if self.month and self.day:
            startdate = datetime.date(self.year, self.month, self.day)
            date_display = ''
        else:
            startdate = datetime.date(self.year, 1, 1)
            date_display = 'year'

        d = {
            'id': self.pk,
            'title': self.caption,
            'description': self.caption,  # not requires
            'startdate': format_date_for_timeglider(startdate),
            'date_display': date_display,
            'importance': 40,  # required
            "icon": "/static/images/icons/flag_black.png",
        }
        return d


class LightBoxItem(models.Model):
    """These items are shown on the lightbox on the home page"""
    class Meta:
        verbose_name = _("Lightbox item (for home page)")
        verbose_name_plural = _("Lightbox items (for home page)")

    title = models.CharField(_('Title'), max_length=255, null=True)
    url = models.CharField(_('URL to the page'), max_length=255, null=True, blank=True)
    image = FileBrowseField(
        _('Image'),
        directory=settings.UPLOAD_TO,
        blank=False,
        null=True,
        max_length=255,
        extensions=IMAGE_EXTENSIONS,
    )
    visible = models.BooleanField(_('Visible?'), default=True)
    order = models.IntegerField(_('Order'), null=True, blank=True)


class UserProfile(UserenaBaseProfile):
    """userprofile for Userena"""
    user = models.OneToOneField(User,
        unique=True,
        verbose_name=_('user'),
        related_name='userprofile',
        )
    country = models.CharField(_('Country'), max_length=255, null=True,)


class MenuItem(models.Model):
    parent = models.ForeignKey('self', verbose_name=('parent'), null=True, blank=True,)
    page = models.ForeignKey('BasicPage', verbose_name=('page'), null=True, blank=True)
    function_call = models.CharField(('Function (only use if you know waht you are doing)'), null=True, blank=True, max_length=255)
    # order in the whole list of all menu items (mostly to make them show correctly in hte admin interface)
    order = models.IntegerField(blank=True, null=True)
    # position within within its context
    position = models.IntegerField(blank=True)
    level = models.IntegerField(blank=True)

    class Meta:
        ordering = ['order']

    def __init__(self, *args, **kwargs):
        result = super(MenuItem, self).__init__(*args, **kwargs)
        self.__original_parent_id = self.parent_id
        return result

    def get_level(self):
        if self.parent:
            return self.parent.level + 1
        else:
            return 1

    def caption_with_spacer(self):
        spacer = ''
        for _i in range(0, self.level):
            spacer += '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
        if self.level > 0:
            spacer += '|-&nbsp;'
        return mark_safe('%s%s' % (spacer, self.page.title))

    def __unicode__(self):
        return self.page.title

    def save(self, force_insert=False, **kwargs):
        # determine where to show this menuitem
        self.level = self.get_level()

        # make sure that we do not make a circular reference
        # XXX: should be checked recursively
        menuitem = self
        while menuitem.parent:
            assert menuitem.parent != self, 'A menuitem cannot be a child of itself'
            menuitem = menuitem.parent

        # if we changed the parent, we reset the order and position
        if self.parent_id != self.__original_parent_id:
            self.position = MenuItem.objects.filter(parent=self.parent).count() + 1
            self.order = None

        if not self.position:
            self.position = MenuItem.objects.filter(parent=self.parent).count() + 1

        result = super(MenuItem, self).save(force_insert, **kwargs)

        if not self.order:
            # reorder all menuitems
            MenuItem.reorder_menuitems()
            # need this, for reasons undiscovered, to make sure that we save 'self' correctly
            self.order = MenuItem.objects.get(id=self.id).order
            super(MenuItem, self).save(force_insert, **kwargs)

        self.__original = self.__dict__
        return result

    def children(self):
        children = MenuItem.objects.filter(parent=self).order_by('position').select_related('page').all()
        for child in children:
            child.parent = self  # Hack to avoid unnecessary DB queries further down the track.
        return list(children)

    def move_menuitem(self, vector):
        """
        move the menuitem one position (forwards or backwards) below the current parent

            menuitem: a MenuItem instance
            vector: a integer, typically -1 or +1, the number of positions to move
        """
        assert vector in [-1, 1]
        menuitem = self
        old_position = menuitem.position
        new_position = old_position + vector
        try:
            next_menuitem = MenuItem.objects.get(position=new_position, parent=menuitem.parent)
        except self.DoesNotExist:
            # if there is no item at the new position, we fail quietely
            return

        # switch position and order between menuitem and next_menuitem
        # the call to 'save' will fix order of the children
        next_menuitem.position = old_position
        menuitem.position = new_position
        menuitem.save()
        next_menuitem.save()
        self.reorder_menuitems()

    @classmethod
    def reorder_menuitems(cls, parent=None, offset=None):
        """set the 'order' attribute correctly for each menuitem that is a child of parent, on the basis of the 'position' property

        returns a new offset - which is the old offset increment by the number of children (and grandchildren, ecc) of the parent
        """
        if not offset:
            if parent:
                offset = parent.order
            else:
                offset = 0

        menuitems = MenuItem.objects.filter(parent=parent).order_by('position').all()

        for i, menuitem in enumerate(menuitems):
            new_order = offset + 1
            if menuitem.order != new_order:
                menuitem.order = new_order
                menuitem.position = i + 1
                menuitem.save()
            offset = cls.reorder_menuitems(parent=menuitem, offset=offset + 1)

        return offset


class MetaTags(models.Model):
    """An object to define 'keywords' and 'description' fields on the site
    """
    class Meta:
        verbose_name = ("Meta Tags")
        verbose_name_plural = ("Meta Tags")

    object_type_choices = [
        ('all', 'All pages'),
        (BasicPage.__name__, BasicPage._meta.verbose_name),
        (News.__name__, News._meta.verbose_name),
        (HartaKarunItem.__name__, HartaKarunItem._meta.verbose_name),
        (HartaKarunCategory.__name__, HartaKarunCategory._meta.verbose_name),
        (HartaKarunMainCategory.__name__, HartaKarunMainCategory._meta.verbose_name),
        ]
    object_type = models.CharField(
        ('Type of object'),
        choices=object_type_choices,
        max_length=255,
        )
    keywords = models.TextField(
        ('Keywords'),
        help_text=('The "keywords" field will consist of these keywords, together with any keywords defined on the page.'),
        null=True,
        blank=True,
        )
    description = models.TextField(
        ('Description'),
        help_text=('The "description" tag will consist of the contents of this, together with the title of the page'),
        null=True,
        blank=True,
        )


class Resolution(DasaWrapper, models.Model):
    """This is a Realia Item

    """
    class Meta:
        db_table = 'dasa_resolution'
        verbose_name = _('Realia')
        verbose_name_plural = _('Realia')
        # ordering will (of course) be ignored by haystack/solr.
        ordering = ('order',)

    date = models.DateField(_('Date'), blank=True, null=True)
    subject = models.CharField(_('Subject'), max_length=255, null=True, blank=True, db_index=True)
    type = models.CharField(_('Type'), max_length=255, null=True, blank=True, db_index=True)
    description = models.TextField(_('Description'), null=True, blank=True)
    priority = models.CharField(_('Priority'), max_length=255, null=True, blank=True)
    source = models.CharField(_('Source'), max_length=255, null=True, blank=True, db_index=True)
    register_folionumber = models.CharField('%s %s' % (_('Register'), _('folionumber')), max_length=255, null=True, blank=True)
    resolution_folionumber = models.CharField('%s %s' % (_('Resolution'), _('folionumber')), max_length=255, null=True, blank=True)
    institution = models.CharField(_('Institution'), max_length=255, null=True, blank=True)
    fonds = models.CharField(('fonds'), max_length=255, null=True, blank=True)
    file = models.CharField(('Archive file'), max_length=255, null=True, blank=True)
    comment = models.TextField(_('Comment'), blank=True)
    next_resolution = models.ForeignKey('Resolution', blank=True, null=True, related_name='_previous_resolution')
    order = models.PositiveIntegerField(_('Order'), blank=True)

    def __str__(self):
        return unicode(self)

    def __unicode__(self):
        return u'%s: %s' % (self.id, self.title)

    @property
    def previous_resolution(self):
        ls = self._previous_resolution.all()
        if ls:
            return ls[0]

    def get_public_fields(self):
        flds = ['date', 'subject', 'description', 'source']
        return ((fld, val) for fld, val in self.get_fields() if fld.name in flds)

    @property
    def title(self):
        return self.description

    def description_first_words(self):
        return first_words(self.description, 50)

    def _is_realia(self):
        # TODO: check if this is always True (I think it is)
        return not self._is_register()

    def _is_register(self):
        return 'register' in self.source

    def _is_besogne(self):
        return False  # not in dasa10 data

    def get_absolute_url(self):
        return reverse(config.SLUG_REALIA_BROWSE) + '?selected=%s' % self.id

    def repr_for_search_result(self):
        return '<span class="searchresult_title">%s: %s</span> <span class="searchresult_type">(%s)</span>' % (format_date(self.date), self.description, self._meta.verbose_name)

    def repr_for_timeglider(self):
        """returns a dictionary that will be used as the json source for the timeglider widget"""
        startdate = self.date
        d = {
            'id': self.pk,
            'title': '%s: %s' % (self.date, self.description),
            'startdate': format_date_for_timeglider(startdate),
            'importance': 50,  # required
            "icon": "/static/images/icons/triangle_orange.png",
            "link": "/resolution/%s" % self.pk,
        }
        return d


def prettyprint_volumePage(volumePage):
    links = []
    volumePage = unicode(volumePage)
    volumePages = volumePage.split(';')
    for volume_page in volumePages:
        if '-' in volume_page:
            volume, page = volume_page.split('-')
            href = link_to_pagebrowser(volume, page, archive='CorpusDipl')
            s = u'<a href="{href}" target="_pagebrowser">{volume_page}</a>'.format(href=href, volume_page=volume_page)
            links.append(s)
        else:
            links.append(volume_page)

    return mark_safe(u'; '.join(links))


class CorpusDiplomaticumPersoon(DasaWrapper, models.Model):
    """A person from the Corpus Diplomaticum
    """
    class Meta:
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")

    name = models.CharField(_('Name'), max_length=255, blank=False)
    ref = models.CharField(max_length=255, blank=False)
    volumePage = models.TextField(blank=True)

    def prettyprint_volumePage(self):
        return prettyprint_volumePage(self.volumePage)


class CorpusDiplomaticumPlaats(DasaWrapper, models.Model):
    """A Plaats from the Corpus Diplomaticum
    """
    class Meta:
        verbose_name = _("Place")
        verbose_name_plural = _("Places")

    name = models.CharField(max_length=255, blank=False)
    ref = models.CharField(max_length=255, blank=False)
    volumePage = models.TextField(blank=True)

    def prettyprint_volumePage(self):
        return prettyprint_volumePage(self.volumePage)


class CorpusDiplomaticumContract(DasaWrapper, models.Model):
    """A Plaats from the Corpus Diplomaticum
    """
    class Meta:
        verbose_name = _("Corpus Diplomaticum Contract")
        verbose_name_plural = _("Corpus Diplomaticum Contracts")

    order = models.IntegerField(db_index=True)
    volumeNumber = models.CharField(max_length=255, db_index=True)
    pageFrom = models.CharField(max_length=255)
    pageTo = models.CharField(max_length=255)
    pageSupp = models.CharField(max_length=255)
    numberRoman = models.CharField(max_length=255)
    numberDigits = models.CharField(max_length=255)
    areaName = models.CharField(max_length=255, db_index=True)
    dayFrom = models.IntegerField(db_index=True, null=True)
    monthFrom = models.IntegerField(db_index=True, null=True)
    yearFrom = models.IntegerField(db_index=True, null=True)
    dayTo = models.IntegerField(db_index=True, null=True)
    monthTo = models.IntegerField(db_index=True, null=True)
    yearTo = models.IntegerField(db_index=True, null=True)
    kingdomName = models.CharField(max_length=255)
    contractSourceDescription = models.TextField()
    signedPlace = models.CharField(max_length=255)
    signedAsians = models.TextField()
    signedEuropeans = models.TextField()

    def dateFrom(self):
        if self.yearFrom and self.monthFrom and self.dayFrom:
            return datetime.date(self.yearFrom, self.monthFrom, self.dayFrom)
        else:
            return

    @property
    def print_dateFrom(self):
        return utils.prettyprint_date(self.yearFrom, self.monthFrom, self.dayFrom)

    @property
    def print_dateTo(self):
        return utils.prettyprint_date(self.yearTo, self.monthTo, self.dayTo)

    @property
    def link_to_pagebrowser(self):
        return link_to_pagebrowser(self.volumeNumber, self.pageFrom, archive='CorpusDipl')

    @property
    def link_to_pagebrowser_pageSupp(self):
        if self.pageSupp:
            return link_to_pagebrowser(self.volumeNumber, self.pageSupp, archive='CorpusDipl')

    def get_absolute_url(self):
        return reverse(config.SLUG_CORPUSDIPLOMATICUM_CONTRACTS_BROWSE) + '?selected=%s' % self.id

    def repr_for_search_result(self):
        return '<span class="searchresult_title">%s - %s</span> <span class="searchresult_type">(%s)</span>' % (
            self.numberRoman, self.numberDigits, self._meta.verbose_name)


class DeHaan(DasaWrapper, models.Model):
    """DeHaan

    """
    class Meta:
        verbose_name = _("DeHaan")
        verbose_name_plural = _("DeHaan")

    def __unicode__(self):
        return u'Map from collection DeHaan with ID {self.IDSource}'.format(self=self)

    IDSource = models.CharField(max_length=6)
    originalMissingYN = models.CharField(max_length=1)
    scanMissingYN = models.CharField(max_length=1)
    refScanFrontImage = models.CharField(max_length=255, blank=True)
    refScanBackImage = models.CharField(max_length=255, blank=True)
    descriptionByDeHaanNL = models.CharField(max_length=2000, blank=True)
    descriptionOnMapNL = models.CharField(max_length=2000, blank=True)
    titleNL = models.CharField(max_length=1000, blank=True)
    titleEN = models.CharField(max_length=1000, blank=True)
    typeMap = models.CharField(max_length=255, blank=True)
    scale = models.CharField(max_length=255, blank=True)
    locationEN	= models.CharField(max_length=255, blank=True)
    dimensionHWinCM	= models.CharField(max_length=255, blank=True)
    Color	= models.CharField(max_length=255, blank=True)
    typeGraphics	= models.CharField(max_length=255, blank=True)
    Blurred	= models.CharField(max_length=255, blank=True)
    maker	= models.CharField(max_length=255, blank=True)
    date	= models.CharField(max_length=255, blank=True)
    commentsEN	= models.CharField(max_length=1000, blank=True)
    refOtherMaps = models.CharField(max_length=255, blank=True)
    refOriginalEN = models.CharField(max_length=1000, blank=True)
    refArchiveFile = models.CharField(max_length=255, blank=True)
    refArchiveDateBijlagen = models.CharField(max_length=255, blank=True)
    refArchiveDescription = models.CharField(max_length=255, blank=True)
    indexTerms = models.CharField(max_length=1000, blank=True)
    numIndexTerms = models.CharField(max_length=255, blank=True)

    order = models.PositiveIntegerField(_("Order"), blank=True, null=True)

    @property
    def description(self):
        return ' '.join([self.descriptionByDeHaanNL, self.descriptionOnMapNL, self.titleNL, self.titleEN])

    @property
    def otherMaps(self):
        ls = self.refOtherMaps.split(';')
        ls = [s.strip() for s in ls]
        return ls

    @property
    def indexTermsSplitted(self):
        ls = self.indexTerms.split(';')
        ls = [s.strip() for s in ls]
        return ls

    def _splitCode(self, s):
        code = s.split('_')[-1]
        archiveFile, folioNumber = code.split('-')
        return archiveFile, folioNumber

    @property
    def linkToPagebrowserFrontImage(self):
        archiveFile, folio_number = self._splitCode(self.refScanFrontImage)
        return link_to_pagebrowser(archiveFile, folio_number, archive='DeHaan')

    @property
    def linkToPagebrowserBackImage(self):
        archiveFile, folio_number = self._splitCode(self.refScanBackImage)
        return link_to_pagebrowser(archiveFile, folio_number, archive='DeHaan')

    @property
    def refScanFrontImageThumb(self):
        # return a link to the thubmail
        if self.refScanFrontImage:
            archiveFile, folio_number = self._splitCode(self.refScanFrontImage)
            params = {
                'folioNumber': folio_number,
                'archiveFile': archiveFile
            }
            result = repository.open_url('scans', **params)
            url = self.linkToPagebrowserFrontImage
            if result['total_results'] == 1:
                image_url = result['results'][0]['URL'] + '/image'
                image_url = image_url.replace('http://localhost:5000', settings.REPOSITORY_PUBLIC_URL)
                return '<a href="{url}" target="_pagebrowser"><img src="{image_url}?size=200x300"></img></a>'.format(url=url, image_url=image_url)
            else:
                print 'WARNING: No scan found for {self.refScanFrontImage}'.format(self=self)
                return '<a href="{url}" target="_pagebrowser">Image not found</a>'.format(url=url)
        else:
            print 'This record has no refScanFrontImage defined'
            return ''

    @property
    def refScanBackImageThumb(self):
        if self.refScanBackImage:
            archiveFile, folio_number = self._splitCode(self.refScanBackImage)
            params = {
                'folioNumber': folio_number,
                'archiveFile': archiveFile
            }
            result = repository.open_url('scans', **params)
            url = self.linkToPagebrowserBackImage
            if result['total_results'] == 1:
                image_url = result['results'][0]['URL'] + '/image'
                image_url = image_url.replace('http://localhost:5000', settings.REPOSITORY_PUBLIC_URL)
                return '<a href="{url}" target="_pagebrowser"><img src="{image_url}?size=200x300"></img></a>'.format(url=url, image_url=image_url)
            else:
                print 'WARNING: No scan found for {self.refScanBackImage}'.format(self=self)
                return '<a href="{url}" target="_pagebrowser">Image not found</a>'.format(url=url)
        else:
            print 'This record has no refScanBackImage defined'
            return ''
            # repository.open_url('/scans?folioNumber=0006A1&archiveFile=E')

    @property
    def refArchiveFileAsString(self):
        s = self.refArchiveFile
        if s.endswith('.0'):
            s = s[:-len('.0')]
        return s

    def link_to_pagebrowser(self):
        return link_to_pagebrowser(self.archiveFile, self.folio_number_from)

    # @property
        # def governors(self):
    #     return filter(None, [self.governor])
    #
    # def issued_date(self):
    #     return utils.prettyprint_date(self.issued_date_y, self.issued_date_m, self.issued_date_d)
    #
    # @property
    # def issued_date_as_date(self):
    #     return utils.to_date(self.issued_date_y, self.issued_date_m, self.issued_date_d)
    #
    # def published_date(self):
    #     return utils.prettyprint_date(self.published_date_y, self.published_date_m, self.published_date_d)

    def get_absolute_url(self):
        return reverse(config.SLUG_DEHAAN_BROWSE) + '?selected=%s' % self.id

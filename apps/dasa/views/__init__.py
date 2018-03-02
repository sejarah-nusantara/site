#
# copyright Gerbrandy SRL
# www.gerbrandy.com
# 2013-
#


import copy
import os
import random
import json
import types
from datetime import datetime
import logging
from textwrap import dedent

from django.core.paginator import Page as PaginatorPage, Paginator, InvalidPage
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.views.generic.base import RedirectView
from django.core import urlresolvers
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout as Signout
from django.views.generic import TemplateView
from django.views.generic import View
from django.conf import settings

from haystack.query import SearchQuerySet
from haystack.views import SearchView

from sorl.thumbnail import get_thumbnail

import userena
from userena.decorators import secure_required
from userena.utils import get_profile_model, get_user_model
from userena.views import ExtraContextTemplateView, userena_settings
from userena.models import UserenaSignup

from guardian.decorators import permission_required

import dasa
from dasa import config, models
from dasa import forms
from dasa import queries
from dasa.utils import sluggify, urlencode
from dasa.pagebrowser import PageBrowserBook
from dasa.repository import repository
from dasa.utils import get_page
from dasa.menu import get_menu
from dasa import utils

from common import DasaSearchView, Page, translate, admin_link, prettyprint_query, _tagcloud
from common import repository_logger
import corpusdiplomaticum
import appendix



LENGTH_OF_RESULTS_LIST = 4


class Home(Page):
    slug = 'home'
    template_name = 'index.html'

    def get_context_data(self):
        context = Page.get_context_data(self)
        menuitems = [
            config.SLUG_FOREWORD,
            config.SLUG_HARTAKARUN,
            config.SLUG_NEWS,
            config.SLUG_SEARCH,
            ]
        menuitems = [dasa.menu.MenuItem(page=dasa.menu.get_page(x)) for x in menuitems]
        menuitems2 = [
            config.SLUG_INTRODUCTION,
            config.SLUG_ARCHIVE,
            config.SLUG_CONTACT,
            config.SLUG_ORGANIZATION,
            ]
        menuitems2 = [dasa.menu.MenuItem(page=dasa.menu.get_page(x)) for x in menuitems2]
        context['home_menuitems'] = menuitems
        context['home_menuitems2'] = menuitems2
        context['lightbox_items'] = models.LightBoxItem.objects.filter(visible=True).order_by('order').all()

        return context


class Foreword(Page):
    slug = 'foreword'
    template_name = 'pages/foreword.html'

    def get_context_data(self):
        context = Page.get_context_data(self)
        context['page_foreword_2'] = get_page('foreword-2', default='')
        return context


class HartaKarunIndex(Page):
    slug = config.SLUG_HARTAKARUN

    def get_context_data(self):
        context = super(HartaKarunIndex, self).get_context_data(self)
        page = self.get_page()
        categories = models.HartaKarunCategory.objects.all()
        main_categories = models.HartaKarunMainCategory.objects.all()

        categories_grid = [cat.subcategories.all() for cat in main_categories]
        categories_grid = zip(*categories_grid)
        context.update({
            'page': page,
            'admin_link': admin_link(page),
            'categories': categories,
            'main_categories': main_categories,
            'categories_grid': categories_grid,
            'submenu': main_categories,
        })
        return context


class HartakarunMainCategoryView(Page):

    slug = config.SLUG_HARTAKARUN_MAIN_CATEGORY

    def get_page(self, path):
        return self._get_category(path)

    def _get_category(self, path):
        try:
            return models.HartaKarunMainCategory.objects.get(pk=path)
        except ValueError:
            raise Http404
        except models.HartaKarunMainCategory.DoesNotExist:
            raise Http404

    def breadcrumbs(self):
        breadcrumbs = [(_('Harta Karun'), urlresolvers.reverse(config.SLUG_HARTAKARUN))]
        return breadcrumbs

    def get_context_data(self, path=config.SLUG_HARTAKARUN_MAIN_CATEGORY):
        context = super(HartakarunMainCategoryView, self).get_context_data(path)
        category = self._get_category(path)
        subcategories = category.subcategories.all()
        context.update({
            'category_shown': subcategories[0],
            'main_category': category,
            'subcategories': subcategories,
            'selected_category': category,
        })
        return context


class HartakarunCategoryView(Page):
    template_name = 'hartakarun_category.html'

    def get_page(self, path):
        if path and path.isdigit():
            page = models.HartaKarunCategory.objects.get(pk=path)
        else:
            raise Http404
        return page

    def get_context_data(self, path):
        context = Page.get_context_data(self, path)
        page = context.get('page')
        main_category = page.hartakarun_main_category
        subcategories = main_category.subcategories.all()
        breadcrumbs = [(_('Harta Karun'), urlresolvers.reverse(config.SLUG_HARTAKARUN)),
                       (main_category.title, urlresolvers.reverse(config.SLUG_HARTAKARUN_MAIN_CATEGORY, args=[main_category.pk])),
                       ]

        hartakarun_items = page.published_hartakarun_items.all()

        context.update({
            'hartakarun_items': hartakarun_items,
            'main_category': main_category,
            'subcategories': subcategories,
            'selected_category': page,
            'category_shown': page,
            'breadcrumbs': breadcrumbs,
        })
        return context


class HartaKarunItemView(Page):
    template_name = 'hartakarun_item.html'

    def get_page(self, path, section=None):
        try:
            return models.HartaKarunItem.objects.get(number=path)
        except models.HartaKarunItem.DoesNotExist:
            raise Http404

    def get_context_data(self, path, section='introduction'):
        context = super(HartaKarunItemView, self).get_context_data()
        pk = path

        page = self.get_page(pk)
        category = page.hartakaruncategory
        main_category = category.hartakarun_main_category
        pagebrowser_url = os.path.join(settings.PAGEBROWSER_URL, sluggify(unicode(page.slug())))
        breadcrumbs = [
            (_('Harta Karun'), urlresolvers.reverse(config.SLUG_HARTAKARUN)),
            (main_category.title, urlresolvers.reverse(config.SLUG_HARTAKARUN_MAIN_CATEGORY, args=[main_category.pk])),
            (category.title, urlresolvers.reverse(config.SLUG_HARTAKARUN_SUBCATEGORY, args=[category.pk])),
        ]

        pdf_link = page.link_to_pdf()

        hartakarun_fields = page.get_fields([
            'introduced_by',
            'selected_by',
            'transcribed_by',
            'translated_id_by',
            'translated_en_by',
            'edited_by',
            'archivalSourceReference',
            'title_nl',  # (= original title)
            'citation',
            'ISBN',  # ( = publication reference)
            'release_date',
        ])

        hartakarun_fields = [(_(field.verbose_name), value) for field, value in hartakarun_fields]

        if pdf_link:
            hartakarun_fields.append((_('PDF'), pdf_link))
        hartakarun_fields.append((_('Harta Karun Category'), '<a href="%s">%s</a>' % (urlresolvers.reverse(config.SLUG_HARTAKARUN_SUBCATEGORY, args=[category.pk]), category.title)))

        context.update({
            'page': page,
            'pdf_link': pdf_link,
            'hartakarun_fields': hartakarun_fields,
            'pagebrowser_url': pagebrowser_url,
            'section': section,
            'admin_link': admin_link(page),
            'breadcrumbs': breadcrumbs,
            'menuitems': self.get_menu().menuitems(path=breadcrumbs[-1][1])
        })
        return context


class HartaKarunArticles(Page):
    slug = config.SLUG_HARTAKARUN_ALL_ARTICLES
    results_per_page = 20

    def get_context_data(self):
        context = super(HartaKarunArticles, self).get_context_data()

        articles = models.HartaKarunItem.objects
        context.update(self.get_context_order_by(['number', 'short_title', 'hartakaruncategory__name', 'date_on_timeline', 'release_date'],
            default=['-release_date', 'number']))

        order_by = context.get('order_by', None)
        if 'number' in order_by or '-number' in order_by:
            if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
                # (check that we are not using sqllite3, which we use for testing, and which does not like lpad
                pass
            else:
                articles = articles.extra(select={'padded_number': "lpad(number, 200, '0')"})
                if 'number' in order_by:
                    order_by.remove('number')
                    order_by.append('padded_number')
                elif '-number' in order_by:
                    order_by.remove('-number')
                    order_by.append('-padded_number')

        articles = articles.order_by(*order_by)

        # show only articles that have a release date, and that release date should be in teh past
        articles = articles.filter(release_date__lte=datetime.now())
        articles = articles.all()
        paginator = Paginator(articles, self.results_per_page)
        page_no = self.request.GET.get('page', 1)
        try:
            page = paginator.page(page_no)
        except InvalidPage:
            page = paginator.page(1)
#             raise Http404("No such page!")

        context.update({
            'articles': articles.all(),
        })

        for fld_name in ['release_date', 'date_on_timeline', 'long_title', 'hartakaruncategory']:
            context['field_%s' % fld_name] = models.HartaKarunItem._meta.get_field(fld_name)

        context.update(self.navigation_context(paginator, page))

        return context


class RetrobookIndex(Page):
    # based on page with slug 'retrobook'
    # template in pages/retrobook.html
    def get_context_data(self, path):
        context = Page.get_context_data(self, path)
        retrobooks = repository.get_retro_books()
        context['retrobooks'] = retrobooks
        return context


class Archive(Page):
    slug = config.SLUG_ARCHIVE

    def get_context_data(self):
        context = Page.get_context_data(self)
        context['archive_sections'] = [
            self.get_page(config.SLUG_INVENTORY),
            self.get_page(config.SLUG_DAILY_JOURNALS),
            self.get_page(config.SLUG_GENERALRESOLUTIONS),
            self.get_page(config.SLUG_DIGITAL_PRESERVATION),
        ]
        return context


class Inventory(Page):
    slug = config.SLUG_INVENTORY

    def get_context_data(self):
        context = Page.get_context_data(self)
        context['inventories'] = [
            self.get_page('%s_id' % config.SLUG_INVENTORY),
            self.get_page('%s_en' % config.SLUG_INVENTORY),
            self.get_page('%s_nl' % config.SLUG_INVENTORY),
        ]
        return context


class InventoryTree(Page):

    template_name = 'pages/inventory_tree.html'

    def get_page(self, path):
        """try to find a BasicPage object with a slug corresponding to path or self.slug"""
        language = self._kwargs['language']
        slug = '%s_%s' % (config.SLUG_INVENTORY, language)

        try:
            page = models.BasicPage.objects.get(slug=slug)
        except models.BasicPage.DoesNotExist:
            msg = 'Could not find BasicPage with slug "%s"' % slug
            raise Exception(msg)
            raise Http404(msg)
        return page

    def get_context_data(self, language):
        context = Page.get_context_data(self)
        language = self._kwargs['language']
        view_archivefile_text = translate('view_the_archive_file', language)
        custodhist_header = translate('custodhist_header', language)

        pagebrowser_url = settings.PAGEBROWSER_PUBLIC_URL
        repository_url = settings.REPOSITORY_PUBLIC_URL
        if not repository_url.endswith('/'):
            repository_url += '/'

        context.update({
            'ead_id': settings.LANGUAGE2EAD[language],
            'pagebrowser_url': pagebrowser_url,
            'repository_url': repository_url,
            'view_archivefile_text': view_archivefile_text,
            'custodhist_header': custodhist_header,
        })
        return context


class MarginaliaVessels(Page):
    slug = config.SLUG_MARGINALIA_SHIPS
    template_name = 'pages/marginalia-vessels.html'

    def get_context_data(self, **kwargs):
        context = super(MarginaliaVessels, self).get_context_data()
        first_letter = self.request.REQUEST.get('first_letter')
        vessel_names = queries.get_marginalia_vesselnames()

        def _sort_string(vessel_name):
            """a string used for sorting
            """
            s = vessel_name
            s = s.strip()
            for prefix in ['de ', "'t ", "l'", "'s "]:
                if s.startswith(prefix):
                    s = s[len(prefix):]
            s = s + vessel_name
            return s.lower().strip()

        vessel_names = [(_sort_string(name), name, count) for name, count in vessel_names]

        letters_and_counts = [
            (letter, len([s for s in vessel_names if s[0].upper().startswith(letter)])) for letter in 'abcdefghijklmnopqrstuvwxyz'.upper()
        ]
        letters_and_counts = [(x, c) for x, c in letters_and_counts if c > 0]

        letters_and_counts.append(('All', len(vessel_names)))

        if first_letter and first_letter.lower() != 'all':
            vessel_names = [(sort_string, name, c) for sort_string, name, c in vessel_names if sort_string.startswith(first_letter.lower())]
        vessel_names.sort()
        vessel_names = [('%s' % name, c) for _sort_string, name, c in vessel_names]

        # make three columns
        col_length = len(vessel_names) / 3 + 1
        vessel_names = [vessel_names[:col_length], vessel_names[col_length: 2 * col_length], vessel_names[2 * col_length:]]

        context.update({
            'vessel_names': vessel_names,
            'letters': letters_and_counts,
        })
        return context

class MarginaliaAsianNames(Page):
    slug = config.SLUG_MARGINALIA_ASIANNAMES
    template_name = 'pages/marginalia-asian-names.html'

    def get_context_data(self, **kwargs):
        context = super(MarginaliaAsianNames, self).get_context_data()
        first_letter = self.request.REQUEST.get('first_letter')
        names = queries.get_marginalia_asiannames()

        def _sort_string(vessel_name):
            """a string used for sorting
            """
            s = vessel_name
            s = s.strip()
            for prefix in ['de ', "'t ", "l'", "'s "]:
                if s.startswith(prefix):
                    s = s[len(prefix):]
            s = s + vessel_name
            return s.lower().strip()

        names = [(_sort_string(name), name, count) for name, count in names]

        letters_and_counts = [
            (letter, len([s for s in names if s[0].upper().startswith(letter)])) for letter in 'abcdefghijklmnopqrstuvwxyz'.upper()
        ]
        letters_and_counts = [(x, c) for x, c in letters_and_counts if c > 0]

        letters_and_counts.append(('All', len(names)))

        if first_letter and first_letter.lower() != 'all':
            names = [(sort_string, name, c) for sort_string, name, c in names if sort_string.startswith(first_letter.lower())]
        names.sort()
        names = [('%s' % name, c) for _sort_string, name, c in names]

        # make three columns
        col_length = len(names) / 3 + 1
        names = [names[:col_length], names[col_length: 2 * col_length], names[2 * col_length:]]

        context.update({
            'names': names,
            'letters': letters_and_counts,
        })
        return context

class MarginaliaEuropeanNames(Page):
    slug = config.SLUG_MARGINALIA_EUROPEANNAMES
    template_name = 'pages/marginalia-european-names.html'

    def get_context_data(self, **kwargs):
        context = super(MarginaliaEuropeanNames, self).get_context_data()
        first_letter = self.request.REQUEST.get('first_letter')
        names = queries.get_marginalia_europeannames()

        def _sort_string(vessel_name):
            """a string used for sorting
            """
            s = vessel_name
            s = s.strip()
            for prefix in ['de ', "'t ", "l'", "'s "]:
                if s.startswith(prefix):
                    s = s[len(prefix):]
            s = s + vessel_name
            return s.lower().strip()

        names = [(_sort_string(name), name, count) for name, count in names]

        letters_and_counts = [
            (letter, len([s for s in names if s[0].upper().startswith(letter)])) for letter in 'abcdefghijklmnopqrstuvwxyz'.upper()
        ]
        letters_and_counts = [(x, c) for x, c in letters_and_counts if c > 0]

        letters_and_counts.append(('All', len(names)))

        if first_letter and first_letter.lower() != 'all':
            names = [(sort_string, name, c) for sort_string, name, c in names if sort_string.startswith(first_letter.lower())]
        names.sort()
        names = [('%s' % name, c) for _sort_string, name, c in names]

        # make three columns
        col_length = len(names) / 3 + 1
        names = [names[:col_length], names[col_length: 2 * col_length], names[2 * col_length:]]

        context.update({
            'names': names,
            'letters': letters_and_counts,
        })
        return context

class MarginaliaPlaceNames(Page):
    slug = config.SLUG_MARGINALIA_PLACENAMES
    template_name = 'pages/marginalia-place-names.html'

    def get_context_data(self, **kwargs):
        context = super(MarginaliaPlaceNames, self).get_context_data()
        first_letter = self.request.REQUEST.get('first_letter')
        names = queries.get_marginalia_placenames()

        def _sort_string(vessel_name):
            """a string used for sorting
            """
            s = vessel_name
            s = s.strip()
            for prefix in ['de ', "'t ", "l'", "'s "]:
                if s.startswith(prefix):
                    s = s[len(prefix):]
            s = s + vessel_name
            return s.lower().strip()

        names = [(_sort_string(name), name, count) for name, count in names]

        letters_and_counts = [
            (letter, len([s for s in names if s[0].upper().startswith(letter)])) for letter in 'abcdefghijklmnopqrstuvwxyz'.upper()
        ]
        letters_and_counts = [(x, c) for x, c in letters_and_counts if c > 0]

        letters_and_counts.append(('All', len(names)))

        if first_letter and first_letter.lower() != 'all':
            names = [(sort_string, name, c) for sort_string, name, c in names if sort_string.startswith(first_letter.lower())]
        names.sort()
        names = [('%s' % name, c) for _sort_string, name, c in names]

        # make three columns
        col_length = len(names) / 3 + 1
        names = [names[:col_length], names[col_length: 2 * col_length], names[2 * col_length:]]

        context.update({
            'names': names,
            'letters': letters_and_counts,
        })
        return context

class RealiaSubjects(Page):
    """a list of subjects of resolutions"""
    slug = config.SLUG_REALIA_SUBJECTS
    template_name = 'pages/realia-subjects.html'

    def get_context_data(self, **kwargs):
        context = super(RealiaSubjects, self).get_context_data()
        request = self.request
        first_letter = request.REQUEST.get('first_letter')
        subjects = queries.get_subjects()
        letters_and_counts = [
            (x, len([s for s, _count in subjects if s.upper().startswith(x)])) for x in 'abcdefghijklmnopqrstuvwxyz'.upper()
        ]
        letters_and_counts = [(x, c) for x, c in letters_and_counts if c > 0]
        letters_and_counts.append(('All', len(subjects)))

        if first_letter:
            subjects = [(x, c) for x, c in subjects if x.upper().startswith(first_letter)]
        subjects.sort()
        # make three columns
        col_length = len(subjects) / 3 + 1
        subjects = [subjects[:col_length], subjects[col_length: 2 * col_length], subjects[2 * col_length:]]

        context.update({
            'subjects': subjects,
            'letters': letters_and_counts,
        })
        return context


class HartaKarunTimeLine(TemplateView):
    template_name = 'hartakarun_timeline.html'


class Book(Page):
    template_name = 'book.html'


class BookShelveIndex(Page):
    template_name = 'pages/collections.html'
    slug = config.SLUG_COLLECTIONS

    def get_context_data(self, path=config.SLUG_COLLECTIONS):
        context = Page.get_context_data(self)
        books = repository.get_daily_journal_books()
        context.update(dict(books=books))
        return context

    def breadcrumbs(self):
        ls = ['archive', 'collections']
        return utils.slugs2breadcrumbs(ls)


class NewsIndex(Page):
    template_name = 'news_index.html'
    slug = config.SLUG_NEWS

    def get_context_data(self):
        context = super(NewsIndex, self).get_context_data(self)
        items = models.News.objects.all()
        context['items'] = items
        return context


class News(Page):
    """A news Item"""

    def get_page(self, path):
        if not path.isdigit():
            raise Http404
        try:
            page = models.News.objects.get(pk=path)
        except models.News.DoesNotExist:
            raise Http404
        return page


class SiteSearch(DasaSearchView):
    slug = config.SLUG_SEARCH

    def extra_context(self):
        context = Page.get_context_data(self)

        request = self.request
        query = request.REQUEST

        # create a pretty-printed version of the query string
        query_prettyprinted = ''
        if query.get('q'):
            query_prettyprinted += '<em>%s</em>\n' % query.get('q')
            search_models = query.getlist('models')
            model2names = dict(forms.SiteSearchForm().choices)
            modelnames = [model2names[m] for m in search_models]
            if modelnames:
                query_prettyprinted += 'in <em>%s</em>\n' % ' and '.join([unicode(x) for x in modelnames])

        context.update({
            'query_prettyprinted': mark_safe(query_prettyprinted.strip()),
        })

        return context

    def get_results(self):
        results = super(SiteSearch, self).get_results()
        # HK items have a releaste date that needs to be respected
        if isinstance(results, type([])):
            results = [x for x in results if x.release_date <= datetime.now()]
        else:
            results = results.filter(release_date__lte=datetime.now())
        return results


class DiplomaticLettersBrowse(DasaSearchView):
    slug = config.SLUG_DIPLOMATICLETTERS_BROWSE
    template_name = 'pages/diplomaticletters-browse.html'
    readmore_buttons = False

    def __init__(self, *args, **kwargs):
        super(DiplomaticLettersBrowse, self).__init__(*args, **kwargs)
        self.form_class = forms.DiplomaticLettersSearchForm

    def extra_context(self):
        context = super(DiplomaticLettersBrowse, self).extra_context()
        context.update(self.get_context_order_by(['date', 'archive_reference'], default='date'))

        published_archivefiles = repository.get_archivefiles(status=config.STATUS_PUBLISHED)
        context['published_archivefiles'] = [x.archiveFile for x in published_archivefiles]

        return context


class DiplomaticLettersSearch(DiplomaticLettersBrowse):
    slug = config.SLUG_DIPLOMATICLETTERS_SEARCH
    template_name = 'pages/diplomaticletters-search.html'

    def extra_context(self):
        context = super(DiplomaticLettersSearch, self).extra_context()
        context['tags_locations'] = _tagcloud(queries.get_diplomaticletter_locations(), 50)
        context['tags_rulers'] = _tagcloud(queries.get_diplomaticletter_rulers(), 15)

        # get mininal and maximal dates
        min_date, max_date = queries.get_min_max_dates(models.DiplomaticLetter)
        context['min_year'], context['max_year'] = min_date.year, max_date.year
        # javascript months start counting at 0 (so january = 0, ecc)
        context['min_month'], context['max_month'] = min_date.month - 1, max_date.month - 1
        context['min_day'], context['max_day'] = min_date.day, max_date.day

        query = dict(self.request.REQUEST)
        form = self.form_class
        query_prettyprinted = prettyprint_query(query, form)
        context['query_prettyprinted'] = query_prettyprinted
        return context


class DiplomaticLettersRulers(DasaSearchView):
    slug = config.SLUG_DIPLOMATICLETTERS_RULERS
    template_name = 'pages/diplomaticletters-rulers.html'
    readmore_buttons = False

    def __init__(self, *args, **kwargs):
        super(DiplomaticLettersRulers, self).__init__(*args, **kwargs)
        self.searchqueryset = SearchQuerySet().models(models.DiplomaticLetterRuler)  # .order_by('name_modern')
        self.form_class = forms.DiplomaticLetterRulerSearchForm
        # because we need to access all objects to crate the alfabet, we optimize (a facet on first_letter would be more efficient...)

    def extra_context(self):
        context = super(DiplomaticLettersRulers, self).extra_context()
        context.update(self.get_context_order_by(['name_modern_exact', 'location', 'number_of_letters']))

        results = self.searchqueryset
        letters_and_counts = [
            (letter, len([obj for obj in results if obj.name_modern and obj.name_modern.upper().startswith(letter)]))
            for letter in 'abcdefghijklmnopqrstuvwxyz'.upper()
        ]
        letters_and_counts = [(x, c) for x, c in letters_and_counts if c > 0]
        letters_and_counts.append(('All', results.count()))
        context['letters'] = letters_and_counts
        return context


class DiplomaticLettersLocations(DasaSearchView):
    slug = config.SLUG_DIPLOMATICLETTERS_LOCATIONS
    template_name = 'pages/diplomaticletters-locations.html'
    readmore_buttons = False

    def __init__(self, *args, **kwargs):
        super(DiplomaticLettersLocations, self).__init__(*args, **kwargs)
        self.searchqueryset = SearchQuerySet().models(models.DiplomaticLetterLocation)
        # because we need to access all objects to crate the alfabet, we optimize (a facet on first_letter would be more efficient...)
        self.searchqueryset = self.searchqueryset.load_all()
        self.form_class = forms.DiplomaticLettersLocationsSearchForm

    def extra_context(self, **kwargs):
        context = super(DiplomaticLettersLocations, self).extra_context(**kwargs)

        context.update(self.get_context_order_by(['city_exact', 'number_of_letters']))

        results = self.searchqueryset

        letters_and_counts = [
            (letter, len([obj for obj in results if obj.object.city and obj.object.city.upper().startswith(letter)]))
            for letter in 'abcdefghijklmnopqrstuvwxyz'.upper()
        ]
        letters_and_counts = [(x, c) for x, c in letters_and_counts if c > 0]
        letters_and_counts.append(('All', results.count()))
        context['letters'] = letters_and_counts
        context['page'] = self.get_page(self.slug)
        return context


class MarginaliaBrowse(DasaSearchView):
    slug = config.SLUG_MARGINALIA_BROWSE
    template_name = 'pages/marginalia-browse.html'

    def __init__(self, *args, **kwargs):
        DasaSearchView.__init__(self, *args, **kwargs)
        self.form_class = forms.MarginaliaSearchForm

    def extra_context(self):
        context = super(MarginaliaBrowse, self).extra_context()
        context.update(self.get_context_order_by(['date', 'description', 'vessel_names', 'archive_reference'], default='date'))
        published_archivefiles = repository.get_archivefiles(status=config.STATUS_PUBLISHED)
        context['published_archivefiles'] = [x.archiveFile for x in published_archivefiles]
        return context


class MarginaliaSearch(MarginaliaBrowse):
    slug = config.SLUG_MARGINALIA_SEARCH
    template_name = 'pages/marginalia-search.html'

    def extra_context(self):

        context = super(MarginaliaSearch, self).extra_context()

        context['tags_vessels'] = _tagcloud(queries.get_marginalia_vesselnames())
        context['tags_europeannames'] = _tagcloud(queries.get_marginalia_europeannames())
        context['tags_asiannames'] = _tagcloud(queries.get_marginalia_asiannames())
        context['tags_placenames'] = _tagcloud(queries.get_marginalia_placenames())

        # get mininal and maximal dates
        min_date, max_date = queries.get_min_max_dates(models.JournalEntry)
        context['min_year'], context['max_year'] = min_date.year, max_date.year
        # javascript months start counting at 0 (so january = 0, ecc)
        context['min_month'], context['max_month'] = min_date.month - 1, max_date.month - 1
        context['min_day'], context['max_day'] = min_date.day, max_date.day

        query = dict(self.request.REQUEST)
        query_prettyprinted = prettyprint_query(query=query, form=self.form_class)
        context['query_prettyprinted'] = query_prettyprinted
        return context


class PlacardsBrowse(DasaSearchView):
    slug = config.SLUG_PLACARD_BROWSE
    template_name = 'pages/placards-browse.html'
    readmore_buttons = False

    def __init__(self, *args, **kwargs):
        super(PlacardsBrowse, self).__init__(*args, **kwargs)
        self.searchqueryset = SearchQuerySet().models(models.Placard)
        self.form_class = forms.PlacardsSearchForm

    def extra_context(self, **kwargs):
        context = super(PlacardsBrowse, self).extra_context(**kwargs)

        context.update(self.get_context_order_by(['location', 'date']))

        return context


class PlacardsSearch(PlacardsBrowse):
    slug = config.SLUG_PLACARD_SEARCH
    template_name = 'pages/placards-search.html'

    def __init__(self, *args, **kwargs):
        super(PlacardsSearch, self).__init__(*args, **kwargs)
        self.searchqueryset = SearchQuerySet().models(models.Placard)
        self.form_class = forms.PlacardsSearchForm

    def extra_context(self):
        context = super(PlacardsSearch, self).extra_context()
        context['tags_governors'] = _tagcloud(queries.get_placard_governors(), 50)

        # get mininal and maximal dates
        min_date, max_date = queries.get_min_max_dates(models.Placard)
        context['min_year'], context['max_year'] = min_date.year, max_date.year
        # javascript months start counting at 0 (so january = 0, ecc)
        context['min_month'], context['max_month'] = min_date.month - 1, max_date.month - 1
        context['min_day'], context['max_day'] = min_date.day, max_date.day

        query = dict(self.request.REQUEST)
        form = self.form_class
        query_prettyprinted = prettyprint_query(query, form)
        context['query_prettyprinted'] = query_prettyprinted
        return context


class PlacardGovernors(Page):
    slug = config.SLUG_PLACARD_GOVERNORS
    template_name = 'pages/placards-governors.html'

    def get_context_data(self, **kwargs):
        context = super(PlacardGovernors, self).get_context_data()
        first_letter = self.request.REQUEST.get('first_letter')
        governors = queries.get_placard_governors()

        def _sort_string(governor):
            """a string used for sorting
            """
            s = governor
            s = s.strip()
            for prefix in ['de ', "'t ", "l'", "'s "]:
                if s.startswith(prefix):
                    s = s[len(prefix):]
            s = s + governor
            return s.lower().strip()

        governors = [(_sort_string(name), name, count) for name, count in governors]

        letters_and_counts = [
            (letter, len([s for s in governors if s[0].upper().startswith(letter)])) for letter in 'abcdefghijklmnopqrstuvwxyz'.upper()
        ]
        letters_and_counts = [(x, c) for x, c in letters_and_counts if c > 0]

        letters_and_counts.append(('All', len(governors)))

        if first_letter:
            governors = [(sort_string, name, c) for sort_string, name, c in governors if sort_string.startswith(first_letter.lower())]
        governors.sort()
        governors = [('%s' % name, c) for _sort_string, name, c in governors]
        # make three columns

        col_length = len(governors) / 3 + 1
        governors = [governors[:col_length], governors[col_length: 2 * col_length], governors[2 * col_length:]]

        context.update({
            'governors': governors,
            'letters': letters_and_counts,
        })
        return context


class RealiaBrowse(DasaSearchView):
    """View to browse models.Resolution objects"""
    slug = config.SLUG_REALIA_BROWSE
    template_name = 'pages/realia-browse.html'

    def __init__(self, *args, **kwargs):
        DasaSearchView.__init__(self, *args, **kwargs)
        self.form_class = forms.RealiaSearchForm

    def extra_context(self):
        context = super(RealiaBrowse, self).extra_context()
        context.update(self.get_context_order_by(['date', 'description', 'subject'], default='date'))
        return context

    def build_page(self):
        paginator, page = super(RealiaBrowse, self).build_page()

        timeFrames = [realia_item.date for realia_item in page.object_list]
        timeFrames = filter(None, timeFrames)
        timeFrames = list(set(timeFrames))

        published_archivefiles = [arch['archiveFile'] for arch in repository.get_archivefiles_json()]
        scans_in_timeframe = repository.get_scans_in_timeframe(timeFrame=timeFrames, published_archivefiles=published_archivefiles)

        for realia_item in page.object_list:
            if realia_item.date:

                # strftime does not work on dates before 1900
                # realia_item_date = realia_item.date.strftime('%Y-%m-%d')
                realia_item_date = realia_item.date.isoformat().split()[0]
                scans = (
                    [scan for scan in scans_in_timeframe if scan['timeFrameFrom'] == realia_item_date] +
                    [scan for scan in scans_in_timeframe if scan['timeFrameFrom'] < realia_item_date and scan.get('timeFrameTo') and scan['timeFrameTo'] >= realia_item_date]
                    )
                realia_item.link_to_pagebrowser = utils.print_link_to_pagebrowser(scans)
            else:
                realia_item.link_to_pagebrowser = ''

        return (paginator, page)


class RealiaSearch(RealiaBrowse):
    """View to search models.Resolution objects"""
    slug = config.SLUG_REALIA_SEARCH
    template_name = 'pages/realia-search.html'

    def extra_context(self):
        context = super(RealiaSearch, self).extra_context()
        context['tags'] = _tagcloud(queries.get_subjects())

        # get mininal and maximal dates
        min_date, max_date = queries.get_min_max_dates(models.Resolution)
        context['min_year'], context['max_year'] = min_date.year, max_date.year
        # javascript months start counting at 0 (so january = 0, ecc)
        context['min_month'], context['max_month'] = min_date.month - 1, max_date.month - 1
        context['min_day'], context['max_day'] = min_date.day, max_date.day

        query = dict(self.request.REQUEST)
        form = self.form_class
        query_prettyprinted = prettyprint_query(query, form)
        context['query_prettyprinted'] = query_prettyprinted

        return context

def timeglider_json(request, path):
    events = []
    if path == 'resolution':
        ls = models.Resolution.objects.order_by('?')[:100]
        events += [x.repr_for_timeglider() for x in ls]
    elif path == 'hartakaruncategory':
        # show timeline options
        ls = models.TimeLineItem.objects.all()
        events += [x.repr_for_timeglider() for x in ls]
        # XXX show hartakarun items
        ls = models.HartaKarunItem.objects.all()
        events += [x.repr_for_timeglider() for x in ls]

    random.shuffle(events)
    timeline = {
        'id': 'dasa_timeline',
        "title": "DASA Timeline",
        #        'description': '',
        #        "timezone": "-07:00",
        'events': events,
        "focus_date": '1685-01-01 00:00:00',
        "initial_zoom": 53,
    }

    content = json.dumps([timeline])
    return HttpResponse(
        content,
        content_type='application/javascript; charset=utf8'
    )


class CollectionsDailyJournals(Page):
    slug = config.SLUG_ARCHIVE_DAILY_JOURNALS
    template_name = 'pages/collections.html'

    def get_context_data(self):
        context = super(CollectionsDailyJournals, self).get_context_data()
        context['books'] = repository.get_daily_journal_books()
        for book in context['books']:
            if book.titles:
                book.title = book.titles.get(self.request.LANGUAGE_CODE, book.title)
        return context


class CollectionsResolution(Page):
    slug = config.SLUG_ARCHIVE_GENERALRESOLUTIONS
    template_name = 'pages/collections.html'

    def get_context_data(self):
        context = super(CollectionsResolution, self).get_context_data()
        context['books'] = repository.get_resolution_books()
        for book in context['books']:
            if book.titles:
                book.title = book.titles.get(self.request.LANGUAGE_CODE, book.title)
        return context


class AppendicesResolution(Page):
    slug = config.SLUG_APPENDICES_RESOLUTIONS
    template_name = 'pages/collections.html'

    def get_context_data(self):
        context = super(AppendicesResolution, self).get_context_data()
        context['books'] = repository.get_appendices_resolutions()
        for book in context['books']:
            if book.titles:
                book.title = book.titles.get(self.request.LANGUAGE_CODE, book.title)
        return context


class CollectionsBesognes(Page):
    slug = config.SLUG_COLLECTIONS_BESOGNES
    template_name = 'pages/collections.html'

    def get_context_data(self):
        context = super(CollectionsBesognes, self).get_context_data()
        context['books'] = repository.get_besogne_books()
        return context


class RedirectAccountsUrlView(RedirectView):

    permanent = True
    query_string = False

    # any url starting with 'accounts_..' will be redirected to 'accounts/..'
    def get_redirect_url(self, slug):
        return 'accounts/{0}'.format(slug)


@secure_required
def signup(
    request,
    signup_form=forms.SignupForm,
    template_name='userena/signup_form.html',
    success_url=None,
    extra_context={},
):
    path = 'signup'
    context = {
        'path': path,
    }
    extra_context.update(context)
    if not success_url:
        success_url = urlresolvers.reverse('userena_signup_complete')
    return userena.views.signup(request, signup_form, template_name, success_url, extra_context)


#
# lifted from userena.views
#
@secure_required
@permission_required('change_profile', (get_profile_model(), 'user__username', 'username'))
def profile_edit(request, username, edit_profile_form=forms.EditProfileForm,
                 template_name='userena/profile_form.html', success_url=None,
                 extra_context=None, **kwargs):
    """
    Edit profile.

    Edits a profile selected by the supplied username. First checks
    permissions if the user is allowed to edit this profile, if denied will
    show a 404. When the profile is successfully edited will redirect to
    ``success_url``.

    :param username:
        Username of the user which profile should be edited.

    :param edit_profile_form:

        Form that is used to edit the profile. The :func:`EditProfileForm.save`
        method of this form will be called when the form
        :func:`EditProfileForm.is_valid`.  Defaults to :class:`EditProfileForm`
        from userena.

    :param template_name:
        String of the template that is used to render this view. Defaults to
        ``userena/edit_profile_form.html``.

    :param success_url:
        Named URL which will be passed on to a django ``reverse`` function after
        the form is successfully saved. Defaults to the ``userena_detail`` url.

    :param extra_context:
        Dictionary containing variables that are passed on to the
        ``template_name`` template.  ``form`` key will always be the form used
        to edit the profile, and the ``profile`` key is always the edited
        profile.

    **Context**

    ``form``
        Form that is used to alter the profile.

    ``profile``
        Instance of the ``Profile`` that is edited.

    """
    user = get_object_or_404(get_user_model(),
                             username__iexact=username)

    profile = user.get_profile()

    user_initial = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'country': profile.country or 'ID',
    }

    form = edit_profile_form(instance=profile, initial=user_initial)

    if request.method == 'POST':
        form = edit_profile_form(request.POST, request.FILES, instance=profile,
                                 initial=user_initial)

        if form.is_valid():
            profile = form.save()
            if userena_settings.USERENA_USE_MESSAGES:
                messages.success(request, _('Your profile has been updated.'), fail_silently=True)

            if success_url:
                redirect_to = success_url
            else:
                redirect_to = urlresolvers.reverse('userena_profile_detail', kwargs={'username': username})
            return redirect(redirect_to)

    if not extra_context:
        extra_context = dict()

    extra_context['form'] = form
    extra_context['profile'] = profile
    return ExtraContextTemplateView.as_view(template_name=template_name,
                                            extra_context=extra_context)(request)


def profile_detail(request, username):
    return redirect(urlresolvers.reverse('userena_profile_edit', args=[username]))


class ProtectedPage(TemplateView):
    template_name = 'test_protected_page.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedPage, self).dispatch(*args, **kwargs)


@secure_required
def signout(request, next_page=userena_settings.USERENA_REDIRECT_ON_SIGNOUT,
            template_name='userena/signout.html', *args, **kwargs):
    """
    Signs out the user and adds a success message ``You have been signed
    out.`` If next_page is defined you will be redirected to the URI. If
    not the template in template_name is used.

    :param next_page:
        A string which specifies the URI to redirect to.

    :param template_name:
        String defining the name of the template to use. Defaults to
        ``userena/signout.html``.

    """
    if request.user.is_authenticated() and userena_settings.USERENA_USE_MESSAGES:  # pragma: no cover
        messages.success(request, _('You have been signed out.'), fail_silently=True)
    next_url = request.GET.get('next')
    if next_url and next_url.startswith('accounts/'):
        request.GET.set('next', ['/'])
    return Signout(request, next_page, template_name, *args, **kwargs)


class HathiTrust(Page):
    template_name = 'hathitrust.html'


class ImageViewer(Page):
    """A bare page with an image viewer, to be used in a popup

    request parameters are:
        image : the URL of an image
    """
#     template_name = 'imageviewer.html'
    @property
    def template_name(self):
        language_code = self.kwargs['language_code']
        return 'imageviewer_{language_code}.html'.format(**locals())

    def get_context_data(self, language_code):
        context = super(ImageViewer, self).get_context_data()
        context['image_url'] = self.request.REQUEST.get('image')
        context['language_code'] = language_code
        return context


class BareImage(View):
    def dispatch(self, request, image_path):
        f = open(os.path.join(settings.MEDIA_ROOT, image_path))
        if request.GET.get('size'):
            thumbnail = get_thumbnail(f, request.GET['size'])
        else:
            thumbnail = f
        return HttpResponse(thumbnail.read(), mimetype="image/jpg")


def is_authenticated(request):
    user = request.user
    if user.is_active:
        return HttpResponse('1')
    else:
        return HttpResponse('')


def password_reset_confirm(*args, **kwargs):
    response = auth_views.password_reset_confirm(
        post_reset_redirect=urlresolvers.reverse('django.contrib.auth.views.password_reset_complete'), *args, **kwargs
    )
    if response.status_code == 200 and response.context_data.get('form') is None:
        return redirect(urlresolvers.reverse('accounts_password_reset_failed'))
    else:
        return response


def password_reset(*args, **kwargs):
    # generate post_reset_redirect url on request, so that the currentlanguage is taken into account
    response = auth_views.password_reset(
        post_reset_redirect=urlresolvers.reverse('userena_password_reset_done'), *args, **kwargs
    )
    return response


class DirectTemplateView(TemplateView):
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        if self.extra_context is not None:
            for key, value in self.extra_context.items():
                if callable(value):
                    context[key] = value()
                else:
                    context[key] = value
        return context


@secure_required
def activate(request, activation_key,
             template_name='userena/activate_fail.html',
             retry_template_name='userena/activate_retry.html',
             success_url=None, extra_context=None):
    """
    Activate a user with an activation key.

    The key is a SHA1 string. When the SHA1 is found with an
    :class:`UserenaSignup`, the :class:`User` of that account will be
    activated.  After a successful activation the view will redirect to
    ``success_url``.  If the SHA1 is not found, the user will be shown the
    ``template_name`` template displaying a fail message.
    If the SHA1 is found but expired, ``retry_template_name`` is used instead,
    so the user can proceed to :func:`activate_retry` to get a new actvation key.

    :param activation_key:
        String of a SHA1 string of 40 characters long. A SHA1 is always 160bit
        long, with 4 bits per character this makes it --160/4-- 40 characters
        long.

    :param template_name:
        String containing the template name that is used when the
        ``activation_key`` is invalid and the activation fails. Defaults to
        ``userena/activate_fail.html``.

    :param retry_template_name:
        String containing the template name that is used when the
        ``activation_key`` is expired. Defaults to
        ``userena/activate_retry.html``.

    :param success_url:
        String containing the URL where the user should be redirected to after
        a successful activation. Will replace ``%(username)s`` with string
        formatting if supplied. If ``success_url`` is left empty, will direct
        to ``userena_profile_detail`` view.

    :param extra_context:
        Dictionary containing variables which could be added to the template
        context. Default to an empty dictionary.

    """
    try:
        if (not UserenaSignup.objects.check_expired_activation(activation_key) or not userena_settings.USERENA_ACTIVATION_RETRY):
            user = UserenaSignup.objects.activate_user(activation_key)
            if user:
                # Sign the user in.
                auth_user = authenticate(identification=user.email,
                                         check_password=False)
                login(request, auth_user)

#                 if userena_settings.USERENA_USE_MESSAGES:
#                     messages.success(request, _('Your account has been activated and you have been signed in.'),
#                                      fail_silently=True)

                if success_url:
                    redirect_to = success_url % {'username': user.username}
                else:
                    redirect_to = urlresolvers.reverse('userena_profile_detail',
                                            kwargs={'username': user.username})

                return redirect(redirect_to)
            else:
                if not extra_context:
                    extra_context = dict()
                return ExtraContextTemplateView.as_view(template_name=template_name,
                                                        extra_context=extra_context)(request)
        else:
            if not extra_context:
                extra_context = dict()
            extra_context['activation_key'] = activation_key
            return ExtraContextTemplateView.as_view(template_name=retry_template_name,
                                                extra_context=extra_context)(request)
    except UserenaSignup.DoesNotExist:
        if not extra_context:
            extra_context = dict()
        return ExtraContextTemplateView.as_view(template_name=template_name,
                                                extra_context=extra_context)(request)


def robots_txt(request):
    host_url = 'http://{host}'.format(host=request.get_host())

    # only allow if DEBUG is False
    if settings.DEBUG:
        content = dedent("""\
            User-agent: *
            Disallow: /
            """.format(host_url=host_url))

    else:
        content = dedent("""\
            User-agent: *
            Disallow: /admin/
            Disallow: /static/
            Sitemap: {host_url}/sitemap.xml

            User-agent: Yandex
            Disallow: /
            """.format(host_url=host_url))
    return HttpResponse(content, content_type='text/plain')


def sitemap_xml(request):
    host_url = 'http://{host}'.format(host=request.get_host())
    content = dedent("""\
        <?xml version="1.0" encoding="UTF-8"?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
            xmlns:xhtml="http://www.w3.org/1999/xhtml"
            >
        """.format(host_url=host_url))

    slugs_in_sitemap = []

    def url_code(slug, host_url=host_url):
        slug = slug.strip('/')
        if slug in slugs_in_sitemap:
            return ''
        slugs_in_sitemap.append(slug)
        content = dedent("""\
            <url>
                <loc>{host_url}/{slug}/</loc>
                <xhtml:link
                    rel="alternate"
                    hreflang="id"
                    href="{host_url}/id/{slug}/" />
                <xhtml:link
                    rel="alternate"
                    hreflang="en"
                    href="{host_url}/{slug}/" />

            </url>
            """.format(slug=slug, host_url=host_url))
        return content

    for menuitem in models.MenuItem.objects.prefetch_related('page').all():
        slug = menuitem.page.slug
        content += url_code(slug)

    for item in models.HartaKarunMainCategory.objects.all():
        slug = item.get_absolute_url()
        content += url_code(slug)

    for item in models.HartaKarunCategory.objects.all():
        slug = item.get_absolute_url()
        content += url_code(slug)

    for item in models.HartaKarunItem.objects.all():
        slug = item.get_absolute_url()
        content += url_code(slug)

    for item in models.News.objects.all():
        slug = item.get_absolute_url()
        content += url_code(slug)

    for key in config.__dict__:
        if key.startswith('SLUG_'):
            slug = config.__dict__[key]
            if slug.startswith('accounts_'):
                continue
            content += url_code(slug)
    content += '</urlset>'
    return HttpResponse(content, content_type='application/xml')


class ErrorView(TemplateView):
    def dispatch(self, *args, **kwargs):
        msg = 'This exception is raised intentionally, for debugging purposes'
        raise Exception(msg)

        def raise_404(error):
                repository_logger.error('[{0}] ERROR: {1}'.format('1234', unicode(error)))
                response = HttpResponse('Error: ' + unicode(error))
                response.status_code = 404
                return response
        return raise_404('ConflictError')
        return raise_404(msg)

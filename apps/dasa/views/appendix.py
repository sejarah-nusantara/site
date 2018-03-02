
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

class AppendixBrowse(DasaSearchView):
    slug = config.SLUG_APPENDIX_BROWSE
    template_name = 'pages/appendix-browse.html'
    orderable_fields = ['archive_reference', 'date', 'title', 'vessel_names', ]

    def __init__(self, *args, **kwargs):
        DasaSearchView.__init__(self, *args, **kwargs)
        self.form_class = forms.AppendixSearchForm

    def extra_context(self):
        context = super(AppendixBrowse, self).extra_context()
        context.update(self.get_context_order_by(self.orderable_fields, default='archive_reference'))
        published_archivefiles = repository.get_archivefiles(status=config.STATUS_PUBLISHED)
        context['published_archivefiles'] = [x.archiveFile for x in published_archivefiles]
        return context

    def build_page(self):
        paginator, page = super(AppendixBrowse, self).build_page()

        def get_res_date(appendix_item):
            appendix_item_date = utils.to_date(appendix_item.res_y, appendix_item.res_m or 1, appendix_item.res_d or 1)
            return appendix_item_date

        timeFrames = [get_res_date(appendix_item) for appendix_item in page.object_list]
        timeFrames = filter(None, timeFrames)
        timeFrames = list(set(timeFrames))

        published_archivefiles = [arch['archiveFile'] for arch in repository.get_archivefiles_json()]
        scans_in_timeframe = repository.get_scans_in_timeframe(timeFrame=timeFrames, published_archivefiles=published_archivefiles)

        for appendix_item in page.object_list:
            appendix_item_date = get_res_date(appendix_item)
            if appendix_item_date:
                appendix_item_date = appendix_item_date.isoformat().split()[0]
                scans = (
                    [scan for scan in scans_in_timeframe if scan.get('timeFrameFrom') and scan.get('timeFrameFrom') == appendix_item_date] +
                    [scan for scan in scans_in_timeframe if
                        scan.get('timeFrameFrom') and scan.get('timeFrameFrom') < appendix_item_date and
                        scan.get('timeFrameTo') and scan['timeFrameTo'] >= appendix_item_date]
                    )
                appendix_item.resolution_reference = utils.print_link_to_pagebrowser(scans)
            else:
                appendix_item.resolution_reference = ''

        return (paginator, page)


class AppendixSearch(AppendixBrowse):
    slug = config.SLUG_APPENDIX_SEARCH
    template_name = 'pages/appendix-search.html'

    def extra_context(self):

        context = super(AppendixSearch, self).extra_context()

        context['tags_documenttypes'] = _tagcloud(queries.get_documenttypes_appendix())
        context['tags_vessels'] = _tagcloud(queries.get_appendix_vesselnames())
        context['tags_europeannames'] = _tagcloud(queries.get_appendix_europeannames())
        context['tags_asiannames'] = _tagcloud(queries.get_appendix_asiannames())
        context['tags_placenames'] = _tagcloud(queries.get_appendix_placenames())



        # get mininal and maximal dates
        context['doc_min_year'], context['doc_max_year'] = queries.get_min_max_values(models.Appendix, 'doc_y')
        context['res_min_year'], context['res_max_year'] = queries.get_min_max_values(models.Appendix, 'res_y')
        # javascript months start counting at 0 (so january = 0, ecc)
        context['doc_min_month'] = '0'
        context['doc_min_day'] = '1'
        context['doc_max_month'] = '11'
        context['doc_max_day'] = '31'
        context['res_min_month'] = '0'
        context['res_min_day'] = '1'
        context['res_max_month'] = '11'
        context['res_max_day'] = '31'

        query = dict(self.request.REQUEST)
        query_prettyprinted = prettyprint_query(query=query, form=self.form_class)
        context['query_prettyprinted'] = query_prettyprinted
        return context


class AppendixVesselNames(Page):
    slug = config.SLUG_APPENDIX_VESSELNAMES
    template_name = 'pages/appendix-vessels.html'
    readmore_buttons = False

    def get_context_data(self, **kwargs):
        context = super(AppendixVesselNames, self).get_context_data()
        first_letter = self.request.REQUEST.get('first_letter')
        vessel_names = queries.get_appendix_vesselnames()

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


class AppendixDocumentTypes(Page):
    slug = config.SLUG_APPENDIX_DOCUMENTTYPES
    template_name = 'pages/appendix-documenttypes.html'
    readmore_buttons = False

    def get_context_data(self, **kwargs):
        context = super(AppendixDocumentTypes, self).get_context_data()
        first_letter = self.request.REQUEST.get('first_letter')
        records = queries.get_documenttypes_appendix()

        def _sort_string(record):
            """a string used for sorting
            """
            s = record
            s = s.strip()
            for prefix in ['de ', "'t ", "l'", "'s "]:
                if s.startswith(prefix):
                    s = s[len(prefix):]
            s = s + record
            return s.lower().strip()

        records = [(_sort_string(name), name, count) for name, count in records]

        letters_and_counts = [
            (letter, len([s for s in records if s[0].upper().startswith(letter)])) for letter in 'abcdefghijklmnopqrstuvwxyz'.upper()
        ]
        letters_and_counts = [(x, c) for x, c in letters_and_counts if c > 0]

        letters_and_counts.append(('All', len(records)))

        if first_letter and first_letter.lower() != 'all':
            records = [(sort_string, name, c) for sort_string, name, c in records if sort_string.startswith(first_letter.lower())]
        records.sort()
        records = [('%s' % name, c) for _sort_string, name, c in records]

        # make three columns
        col_length = len(records) / 3 + 1
        records = [records[:col_length], records[col_length: 2 * col_length], records[2 * col_length:]]

        context.update({
            'records': records,
            'letters': letters_and_counts,
        })
        return context

class AppendixAsianNames(Page):
    slug = config.SLUG_APPENDIX_ASIANNAMES
    template_name = 'pages/appendix-asian-names.html'

    def get_context_data(self, **kwargs):
        context = super(AppendixAsianNames, self).get_context_data()
        first_letter = self.request.REQUEST.get('first_letter')
        names = queries.get_appendix_asiannames()

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

class AppendixEuropeanNames(Page):
    slug = config.SLUG_APPENDIX_EUROPEANNAMES
    template_name = 'pages/appendix-european-names.html'

    def get_context_data(self, **kwargs):
        context = super(AppendixEuropeanNames, self).get_context_data()
        first_letter = self.request.REQUEST.get('first_letter')
        names = queries.get_appendix_europeannames()

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

class AppendixPlaceNames(Page):
    slug = config.SLUG_APPENDIX_PLACENAMES
    template_name = 'pages/appendix-place-names.html'

    def get_context_data(self, **kwargs):
        context = super(AppendixPlaceNames, self).get_context_data()
        first_letter = self.request.REQUEST.get('first_letter')
        names = queries.get_appendix_placenames()

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

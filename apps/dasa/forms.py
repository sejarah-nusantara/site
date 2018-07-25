# encoding=utf-8
#
# copyright Gerbrandy SRL
# www.gerbrandy.com
# 2013
#


import random
import re

try:
    from hashlib import sha1 as sha_constructor
except ImportError:
    from django.utils.hashcompat import sha_constructor

from django.db import models as django_models
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate

from haystack.forms import model_choices, SearchQuerySet, EmptySearchQuerySet
from haystack.inputs import BaseInput, Clean, Exact, Not
from haystack.query import SQ

from userena.forms import SignupFormOnlyEmail
from userena.utils import get_profile_model, get_user_model
from userena import settings as userena_settings
from userena.models import UserenaSignup
from userena import forms as userena_forms

from django_countries import countries

from dasa import lookups
from dasa import models

import selectable

INPUT_FORMATS = [
    '%d-%m-%y',
    '%d/%m/%y',
    '%d-%m-%Y',
    '%d/%m/%Y',
    '%d %b %Y',
    '%d %B %Y',
    '%Y-%m-%d',
    '%Y-%m-%d',
    '%m/%d/%Y',
    '%m/%d/%y',
]

JQUERY_UI_ATTRS = {'class': 'ui-widget ui-widget-content ui-corner-all'}


class DasaQuery(BaseInput):
    """
    A convenience class that handles common user queries.

    In addition to cleaning all tokens, it handles double quote bits as
    exact matches & terms with '-' in front as NOT queries.
    """
    input_type_name = 'auto_query'
    post_process = False
    exact_match_re = re.compile(r'"(?P<phrase>.*?)"')
    boolean_operators = ['AND', 'OR', 'NOT']

    def prepare(self, query_obj):
        query_string = super(DasaQuery, self).prepare(query_obj)
        exacts = self.exact_match_re.findall(query_string)
        tokens = []
        query_bits = []

        for rough_token in self.exact_match_re.split(query_string):
            if not rough_token:
                continue
            elif rough_token not in exacts:
                # We have something that's not an exact match but may have more
                # than on word in it.
                tokens.extend(rough_token.split(' '))
            else:
                tokens.append(rough_token)

        for token in tokens:
            if not token:
                continue
            elif token in self.boolean_operators:
                query_bits.append(token)
            elif token in exacts:
                query_bits.append(Exact(token, clean=True).prepare(query_obj))
            elif token.startswith('-') and len(token) > 1:
                # This might break Xapian. Check on this.
                query_bits.append(Not(token[1:]).prepare(query_obj))
            else:
                query_bits.append(Clean(token).prepare(query_obj))

        return u' '.join(query_bits)


class SearchForm(forms.Form):
    """adapted from haystack.forms.SearchForm"""

    searchqueryset = None

    def __init__(self, *args, **kwargs):

        if not self.searchqueryset:
            self.searchqueryset = kwargs.pop('searchqueryset', None)
        self.load_all = kwargs.pop('load_all', False)

        if self.searchqueryset is None:
            self.searchqueryset = SearchQuerySet()

        super(SearchForm, self).__init__(*args, **kwargs)

    def no_query_found(self):
        """
        Determines the behavior when no query was found.

        By default, no results are returned (``EmptySearchQuerySet``).

        Should you want to show all results, override this method in your
        own ``SearchForm`` subclass and do ``return self.searchqueryset.all()``.
        """
        return EmptySearchQuerySet()

    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        if not self.cleaned_data.get('q'):
            return self.no_query_found()

        if self.cleaned_data['q']:
            sqs = self.searchqueryset.filter(content=DasaQuery(self.cleaned_data['q']))

        if self.load_all:
            sqs = sqs.load_all()

        return sqs

    def get_suggestion(self):
        if not self.is_valid():
            return None

        return self.searchqueryset.spelling_suggestion(self.cleaned_data['q'])


class SiteSearchForm(SearchForm):
    """Form for site-wide search"""

    attrs = {'type': 'search'}
    attrs.update(JQUERY_UI_ATTRS)
    q = forms.CharField(required=False, label=_('Search'), widget=forms.TextInput(attrs=attrs))

    mapchoice2models = {
        'all': [x[0] for x in model_choices() if x[0] not in ['dasa.journalentryclass', 'dasa.resolutionclass']],
        'hartakarun': ['dasa.hartakaruncategory', 'dasa.hartakarunmaincategory', 'dasa.hartakarunitem'],
        'journalentries': ['dasa.journalentry', ],
        'resolutions': ['dasa.resolution'],
        'diplomaticletters': ['dasa.diplomaticletter', 'dasa.diplomaticletterlocation', 'dasa.diplomaticletterruler'],
        'retrobooks': ['dasa.retrobookscan', 'dasa.retrobook'],
        'hartakarun_items': ['dasa.hartakarunitem'],
        'placards': ['dasa.placard'],
        'appendices': ['dasa.appendix'],
        'corpusdiplomaticumcontracts': ['dasa.corpusdiplomaticumcontract'],
        'maps': ['dasa.dehaan'],
    }

    def __init__(self, *args, **kwargs):

        super(SiteSearchForm, self).__init__(*args, label_suffix='', **kwargs)
        self.choices = [
            ('all', _('Entire site')),
            ('hartakarun', _('Harta Karun Categories')),
            ('hartakarun_items', _('Harta Karun Articles')),
            ('journalentries', _('Marginalia to the Daily Journals')),
            ('resolutions', _('Realia to the Resolutions and Besognes')),
            ('diplomaticletters', _('Diplomatic Letters')),
            ('placards', _('Placards')),
            ('appendices', _('Appendices Resolutions')),
            ('corpusdiplomaticumcontracts', _('Corpus Diplomaticum Contracts')),
            ('maps', _('Maps')),
            ]
        choices = self.choices
        self.fields['models'] = forms.MultipleChoiceField(
            choices=choices, required=False, label=_('Search In'),
            widget=forms.CheckboxSelectMultiple(),
            )

    def get_models(self):
        """Return an alphabetical list of model classes in the index."""
        search_models = []
        if self.is_valid():
            choices = self.cleaned_data['models']
            if not choices:
                choices = ['all']
            if not isinstance(choices, type([])):
                choices = [choices]
            for choice in choices:
                for model in self.mapchoice2models[choice]:
                    search_models.append(django_models.get_model(*model.split('.')))

        return list(set(search_models))

    def search(self):
        sqs = super(SiteSearchForm, self).search()
        sqs = sqs.models(*self.get_models())
        return sqs


class MarginaliaSearchForm(SearchForm):
    searchqueryset = SearchQuerySet().models(models.JournalEntry)

    def __init__(self, *args, **kwargs):
        super(MarginaliaSearchForm, self).__init__(*args, label_suffix='', **kwargs)

    description = forms.CharField(
        label=_('Description'),
        widget=forms.TextInput(attrs=JQUERY_UI_ATTRS),
        required=False,
    )

    date_from = forms.DateField(
        required=False,
        label=_('Date from'),
        widget=forms.widgets.DateInput(attrs=JQUERY_UI_ATTRS),
        )

    date_to = forms.DateField(
        label=_('Date to'),
        required=False,
        widget=forms.widgets.DateInput(attrs=JQUERY_UI_ATTRS),
        )

    vessel_name = forms.CharField(
        label=_('Ship name'),
        widget=selectable.forms.AutoCompleteWidget(lookups.VesselNameLookup, allow_new=True),
        required=False,
    )

    european_name = forms.CharField(
        label=_('European name'),
        widget=selectable.forms.AutoCompleteWidget(lookups.MarginaliaEuropeanNameLookup, allow_new=True),
        required=False,
    )

    asian_name = forms.CharField(
        label=_('Asian name'),
        widget=selectable.forms.AutoCompleteWidget(lookups.MarginaliaAsianNameLookup, allow_new=True),
        required=False,
    )

    place_name = forms.CharField(
        label=_('Place name'),
        widget=selectable.forms.AutoCompleteWidget(lookups.MarginaliaPlaceNameLookup, allow_new=True),
        required=False,
    )

    archiveFile = forms.CharField(
        label=_('Archive file'),
        widget=forms.widgets.TextInput(attrs=JQUERY_UI_ATTRS),
        required=False,
    )

    order_by = forms.CharField(required=False, widget=forms.HiddenInput())

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(MarginaliaSearchForm, self).search()
        if self.is_valid():
            if self.cleaned_data.get('description'):
                sqs = sqs.filter(description=DasaQuery(self.cleaned_data['description']))
            if self.cleaned_data.get('date_from'):
                sqs = sqs.filter(date__gte=self.cleaned_data['date_from'])
            if self.cleaned_data.get('date_to'):
                sqs = sqs.filter(date__lte=self.cleaned_data['date_to'])
            if self.cleaned_data.get('vessel_name'):
                sqs = sqs.filter(vessel_names_list__exact=DasaQuery(self.cleaned_data['vessel_name']))
            if self.cleaned_data.get('asian_name'):
                sqs = sqs.filter(person_names_asian_list__exact=DasaQuery(self.cleaned_data['asian_name']))
            if self.cleaned_data.get('european_name'):
                sqs = sqs.filter(person_names_european_list__exact=DasaQuery(self.cleaned_data['european_name']))
            if self.cleaned_data.get('place_name'):
                sqs = sqs.filter(place_names_list__exact=DasaQuery(self.cleaned_data['place_name']))
            if self.cleaned_data.get('archiveFile'):
                sqs = sqs.filter(archiveFile=self.cleaned_data['archiveFile'])
            if self.cleaned_data.get('order_by'):
                order_by = self.cleaned_data.get('order_by')
                if order_by == 'archive_reference':
                    sqs = sqs.order_by('archiveFile').order_by('folio_number_from')
                elif order_by == '-archive_reference':
                    sqs = sqs.order_by('-archiveFile').order_by('-folio_number_from')
                else:
                    sqs = sqs.order_by(order_by)
            else:
                sqs = sqs.order_by('order')

            if self.cleaned_data.get('vessel_name'):  # and self.cleaned_data['vessel_name'] not in [',']:
                # exact filtering on tags does not work, so we do it by hand
                # (WHICH IS VERY EXPENSIVE)
                sqs = [x for x in sqs if self.cleaned_data.get('vessel_name') in (x.vessel_names_list or '')]
            if self.cleaned_data.get('asian_name'):  # and self.cleaned_data['vessel_name'] not in [',']:
                # exact filtering on tags does not work, so we do it by hand
                # (WHICH IS VERY EXPENSIVE)
                sqs = [x for x in sqs if self.cleaned_data.get('asian_name') in (x.person_names_asian_list or '')]
            if self.cleaned_data.get('european_name'):  # and self.cleaned_data['vessel_name'] not in [',']:
                # exact filtering on tags does not work, so we do it by hand
                # (WHICH IS VERY EXPENSIVE)
                sqs = [x for x in sqs if self.cleaned_data.get('european_name') in (x.person_names_european_list or '')]
            # if self.cleaned_data.get('place_name'):
            #     # exact filtering on tags does not work, so we do it by hand
            #     # (WHICH IS VERY EXPENSIVE)
            #     sqs = [x for x in sqs if self.cleaned_data.get('place_name') in (x.place_name_list or '')]
        else:
            sqs = sqs.order_by('order')
        return sqs

    def no_query_found(self):
        """
        Determines the behavior when no query was found.

        By default, no results are returned (``EmptySearchQuerySet``).

        Should you want to show all results, override this method in your
        own ``SearchForm`` subclass and do ``return self.searchqueryset.all()``.
        """
        return self.searchqueryset  # .all()


class AppendixSearchForm(SearchForm):
    searchqueryset = SearchQuerySet().models(models.Appendix)

    def __init__(self, *args, **kwargs):
        super(AppendixSearchForm, self).__init__(*args, label_suffix='', **kwargs)

    doc_date_from = forms.DateField(
        required=False,
        label=_('Document date from'),
        widget=forms.widgets.DateInput(attrs=JQUERY_UI_ATTRS),
        )

    doc_date_to = forms.DateField(
        label=_('Document date to'),
        required=False,
        widget=forms.widgets.DateInput(attrs=JQUERY_UI_ATTRS),
        )

    res_date_from = forms.DateField(
        required=False,
        label=_('Resolution date from'),
        widget=forms.widgets.DateInput(attrs=JQUERY_UI_ATTRS),
        )

    res_date_to = forms.DateField(
        label=_('Resolution date to'),
        required=False,
        widget=forms.widgets.DateInput(attrs=JQUERY_UI_ATTRS),
        )

    document_type = forms.CharField(
        label=_('Document type'),
        widget=selectable.forms.AutoCompleteWidget(lookups.DocumentTypeAppendixLookup, allow_new=True, attrs=JQUERY_UI_ATTRS),
        required=False,
    )

    vessel_name = forms.CharField(
        label=_('Ship name'),
        widget=selectable.forms.AutoCompleteWidget(lookups.VesselNameAppendixLookup, allow_new=True, attrs=JQUERY_UI_ATTRS),
        required=False,
    )

    european_name = forms.CharField(
        label=_('European name'),
        widget=selectable.forms.AutoCompleteWidget(lookups.AppendixEuropeanNameLookup, allow_new=True),
        required=False,
    )

    asian_name = forms.CharField(
        label=_('Asian name'),
        widget=selectable.forms.AutoCompleteWidget(lookups.AppendixAsianNameLookup, allow_new=True),
        required=False,
    )

    place_name = forms.CharField(
        label=_('Place name'),
        widget=selectable.forms.AutoCompleteWidget(lookups.AppendixPlaceNameLookup, allow_new=True),
        required=False,
    )


    archiveFile = forms.CharField(
        label=_('Archive file'),
        required=False,
        widget=forms.widgets.TextInput(attrs=JQUERY_UI_ATTRS),
    )

    text = forms.CharField(
        label=_('Search in text'),
        required=False,
        widget=forms.widgets.TextInput(attrs=JQUERY_UI_ATTRS),
    )

    order_by = forms.CharField(required=False, widget=forms.HiddenInput())

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(AppendixSearchForm, self).search()
        if self.is_valid():
            if self.cleaned_data.get('description'):
                sqs = sqs.filter(description=DasaQuery(self.cleaned_data['description']))

            doc_date_from = self.cleaned_data.get('doc_date_from')
            if doc_date_from:
                sqs = sqs.filter(doc_y__gte=doc_date_from.year)
                sqs = sqs.filter(SQ(doc_m__gte=doc_date_from.month) | SQ(doc_m=0))
                sqs = sqs.filter(SQ(doc_d__gte=doc_date_from.day) | SQ(doc_d=0))

            doc_date_to = self.cleaned_data.get('doc_date_to')
            if doc_date_to:
                sqs = sqs.filter(doc_y__lte=doc_date_to.year)
                sqs = sqs.filter(doc_m__lte=doc_date_to.month)
                sqs = sqs.filter(doc_d__lte=doc_date_to.day)

            res_date_from = self.cleaned_data.get('res_date_from')
            if res_date_from:
                sqs = sqs.filter(res_y__gte=res_date_from.year)
                sqs = sqs.filter(SQ(res_m__gte=res_date_from.month) | SQ(res_m=0))
                sqs = sqs.filter(SQ(res_d__gte=res_date_from.day) | SQ(res_d=0))

            res_date_to = self.cleaned_data.get('res_date_to')
            if res_date_to:
                sqs = sqs.filter(res_y__lte=res_date_to.year)
                sqs = sqs.filter(doc_m__lte=res_date_to.month)
                sqs = sqs.filter(res_d__lte=res_date_to.day)

            if self.cleaned_data.get('vessel_name'):
                sqs = sqs.filter(vessel_names_list__exact=DasaQuery(self.cleaned_data['vessel_name']))
            if self.cleaned_data.get('asian_name'):
                sqs = sqs.filter(person_names_asian_list__exact=DasaQuery(self.cleaned_data['asian_name']))
            if self.cleaned_data.get('european_name'):
                sqs = sqs.filter(person_names_european_list__exact=DasaQuery(self.cleaned_data['european_name']))
            if self.cleaned_data.get('place_name'):
                sqs = sqs.filter(place_names_list__exact=DasaQuery(self.cleaned_data['place_name']))

            if self.cleaned_data.get('document_type'):
                sqs = sqs.filter(document_type=self.cleaned_data['document_type'])
            if self.cleaned_data.get('archiveFile'):
                sqs = sqs.filter(archiveFile=self.cleaned_data['archiveFile'])
            if self.cleaned_data.get('order_by'):
                order_by = self.cleaned_data.get('order_by')
                if order_by == 'archive_reference':
                    sqs = sqs.order_by('archiveFile').order_by('folio_number_from')
                elif order_by == '-archive_reference':
                    sqs = sqs.order_by('-archiveFile').order_by('-folio_number_from')
                elif order_by == 'date':
                    sqs = sqs.order_by('doc_y').order_by('doc_m').order_by('doc_d')
                elif order_by == '-date':
                    sqs = sqs.order_by('-doc_y').order_by('-doc_m').order_by('-doc_d')
#                 elif order_by == 'title':
                else:
                    sqs = sqs.order_by(order_by)
            else:
                # by default, we order by archive reference
                sqs = sqs.order_by('archiveFile').order_by('folio_number_from')

            if self.cleaned_data.get('vessel_name'):  # and self.cleaned_data['vessel_name'] not in [',']:
                # exact filtering on tags does not work, so we do it by hand
                # (WHICH IS VERY EXPENSIVE)
                sqs = [x for x in sqs if self.cleaned_data.get('vessel_name') in (x.vessel_names_list or '')]
            if self.cleaned_data.get('text'):
                sqs = sqs.filter(text=self.cleaned_data['text'])
        else:
            sqs = sqs.order_by('order')
        return sqs

    def no_query_found(self):
        """
        Determines the behavior when no query was found.

        By default, no results are returned (``EmptySearchQuerySet``).

        Should you want to show all results, override this method in your
        own ``SearchForm`` subclass and do ``return self.searchqueryset.all()``.
        """
        return self.searchqueryset  # .all()


class RealiaSearchForm(SearchForm):
    """A form for searching for resolutions"""
    searchqueryset = SearchQuerySet().models(models.Resolution)

    def __init__(self, *args, **kwargs):
        super(RealiaSearchForm, self).__init__(*args, label_suffix='', **kwargs)

    description = forms.CharField(
        label=_('Description'),
        widget=forms.widgets.TextInput(attrs=JQUERY_UI_ATTRS),
        required=False,
    )

    subject = forms.CharField(
        label=_('Subject'),
        widget=selectable.forms.AutoCompleteWidget(lookups.SubjectLookup, allow_new=True, attrs=JQUERY_UI_ATTRS),
        required=False,
    )

    date_from = forms.DateField(
        required=False,
        label=_('Date from'),
        input_formats=INPUT_FORMATS,
        widget=forms.widgets.DateInput(attrs=JQUERY_UI_ATTRS),
        )

    date_to = forms.DateField(required=False, label=_('Date to'), input_formats=INPUT_FORMATS,
        widget=forms.widgets.DateInput(attrs=JQUERY_UI_ATTRS),)

    #  archiveFile is a relatively complex case -
    # cf. views.RealiaSearch.print_link_to_pagebrowser
    #     archiveFile = forms.CharField(
    #         label=_('Archive file'),
    #         required=False,
    #     )

    order_by = forms.CharField(required=False, widget=forms.HiddenInput())

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(RealiaSearchForm, self).search()
        if self.is_valid():
            if self.cleaned_data['description']:
                sqs = sqs.filter(description=DasaQuery(self.cleaned_data['description']))
            if self.cleaned_data['subject']:
                sqs = sqs.filter(subject=DasaQuery(self.cleaned_data['subject']))
            if self.cleaned_data.get('source'):
                sqs = sqs.filter(source=DasaQuery(self.cleaned_data['source']))
            if self.cleaned_data.get('date_from'):
                sqs = sqs.filter(date__gte=self.cleaned_data['date_from'])
            if self.cleaned_data.get('date_to'):
                sqs = sqs.filter(date__lte=self.cleaned_data['date_to'])
            if self.cleaned_data.get('order_by'):
                sqs = sqs.order_by(self.cleaned_data['order_by'])
            else:
                sqs = sqs.order_by('order')
        else:
            sqs = sqs.order_by('order')

        return sqs

    def no_query_found(self):
        """
        Determines the behavior when no query was found.

        By default, no results are returned (``EmptySearchQuerySet``).

        Should you want to show all results, override this method in your
        own ``SearchForm`` subclass and do ``return self.searchqueryset.all()``.
        """
        return self.searchqueryset  # .all()


class PlacardsSearchForm(SearchForm):

    # this field is named 'location' because that is the index in which it is stored in solr
    description = forms.CharField(
        label=_('Description'),
        widget=forms.widgets.TextInput(attrs=JQUERY_UI_ATTRS),
        required=False,
    )
    date_from = forms.DateField(
        required=False, label=_('Date from'), input_formats=INPUT_FORMATS,
        widget=forms.widgets.DateInput(attrs=JQUERY_UI_ATTRS),
    )

    date_to = forms.DateField(
        required=False, label=_('Date to'), input_formats=INPUT_FORMATS,
        widget=forms.widgets.DateInput(attrs=JQUERY_UI_ATTRS),
        )
    governor = forms.CharField(
        label=_('Governor'),
        widget=selectable.forms.AutoCompleteWidget(lookups.PlacardGovernorLookup, allow_new=True),
        required=False,
    )
    order_by = forms.CharField(required=False, widget=forms.HiddenInput())

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(PlacardsSearchForm, self).search()
        if self.is_valid():
            if self.cleaned_data.get('description'):
                sqs = sqs.filter(description=DasaQuery(self.cleaned_data['description']))
            if self.cleaned_data.get('governor'):
                sqs = sqs.filter(location__exact=DasaQuery(self.cleaned_data['governor']))
            if self.cleaned_data.get('date_from'):
                sqs = sqs.filter(date__gte=self.cleaned_data['date_from'])
            if self.cleaned_data.get('date_to'):
                sqs = sqs.filter(date__lte=self.cleaned_data['date_to'])
            if self.cleaned_data.get('order_by'):
                order_by = self.cleaned_data.get('order_by')
                if order_by == 'archive_reference':
                    sqs = sqs.order_by('archiveFile').order_by('folio_number_from')
                elif order_by == '-archive_reference':
                    sqs = sqs.order_by('-archiveFile').order_by('-folio_number_from')
                elif order_by == 'description':
                    pass
                elif order_by == '-description':
                    pass
                else:
                    sqs = sqs.order_by(order_by)
            else:
                sqs = sqs.order_by('order')

        else:
            sqs = sqs.order_by('order')
        return sqs

    def no_query_found(self):
        """ """
        return self.searchqueryset


class CorpusDiplomaticumContractsSearchForm(SearchForm):

    searchqueryset = SearchQuerySet().models(models.CorpusDiplomaticumContract)

    date_from = forms.DateField(
        required=False,
        label=_('Date from'),
        input_formats=INPUT_FORMATS,
        widget=forms.widgets.DateInput(attrs=JQUERY_UI_ATTRS),
    )

    date_to = forms.DateField(
        required=False, label=_('Date to'), input_formats=INPUT_FORMATS,
        widget=forms.widgets.DateInput(attrs=JQUERY_UI_ATTRS),
        )

    areaName = forms.CharField(
        label=_('Area'),
        widget=selectable.forms.AutoCompleteWidget(lookups.CorpusDiplomaticumAreaNameLookup, allow_new=True, attrs=JQUERY_UI_ATTRS),
        required=False,
    )

    text = forms.CharField(
        label=_('Search in text'),
        required=False,
        widget=forms.widgets.TextInput(attrs=JQUERY_UI_ATTRS),
    )

    order_by = forms.CharField(required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(CorpusDiplomaticumContractsSearchForm, self).__init__(label_suffix='', *args, **kwargs)

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(CorpusDiplomaticumContractsSearchForm, self).search()
        if self.is_valid():
            date_from = self.cleaned_data.get('date_from')
            if date_from:
                sqs = sqs.filter(dateFrom__gte=date_from)

            date_to = self.cleaned_data.get('date_to')
            if date_to:
                sqs = sqs.filter(dateFrom__lte=date_to)

            text = self.cleaned_data.get('text')
            if text:
                sqs = sqs.filter(text=DasaQuery(text))

            if self.cleaned_data.get('areaName'):
                sqs = sqs.filter(areaName=self.cleaned_data['areaName'])

            if self.cleaned_data.get('order_by'):
                order_by = self.cleaned_data.get('order_by')
                if order_by == 'volume':
                    sqs = sqs.order_by('volumeNumber').order_by('pageFromInt')
                elif order_by == '-volume':
                    sqs = sqs.order_by('-volumeNumber').order_by('-pageFromInt')
                elif order_by == 'dateFrom':
                    sqs = sqs.order_by('yearFrom').order_by('monthFrom').order_by('dayFrom')
                elif order_by == '-dateFrom':
                    sqs = sqs.order_by('-yearFrom').order_by('-monthFrom').order_by('-dayFrom')
                else:
                    sqs = sqs.order_by(order_by)
            else:
                # sqs = sqs.order_by('order')
                sqs = sqs.order_by('volumeNumber').order_by('pageFromInt')

        else:
            sqs = sqs.order_by('volumeNumber').order_by('pageFromInt')
            # sqs = sqs.order_by('order')
        return sqs

    def no_query_found(self):
        """
        Determines the behavior when no query was found.

        By default, no results are returned (``EmptySearchQuerySet``).

        Should you want to show all results, override this method in your
        own ``SearchForm`` subclass and do ``return self.searchqueryset.all()``.
        """
        return self.searchqueryset


class DiplomaticLettersSearchForm(SearchForm):

    searchqueryset = SearchQuerySet().models(models.DiplomaticLetter)

    date_from = forms.DateField(
        required=False,
        label=_('Date from'),
        input_formats=INPUT_FORMATS,
        widget=forms.widgets.DateInput(attrs=JQUERY_UI_ATTRS),
    )

    date_to = forms.DateField(
        required=False, label=_('Date to'), input_formats=INPUT_FORMATS,
        widget=forms.widgets.DateInput(attrs=JQUERY_UI_ATTRS),
        )

    source = forms.CharField(
        label=_('Source'),
        widget=selectable.forms.AutoCompleteWidget(lookups.DiplomaticLetterLocationLookup, allow_new=True, attrs=JQUERY_UI_ATTRS),
        required=False,
    )

    destination = forms.CharField(
        label=_('Destination'),
        widget=selectable.forms.AutoCompleteWidget(lookups.DiplomaticLetterLocationLookup, allow_new=True, attrs=JQUERY_UI_ATTRS),
        required=False,
    )

    location = forms.CharField(
        label=_('Location'),
        widget=selectable.forms.AutoCompleteWidget(lookups.DiplomaticLetterLocationLookup, allow_new=True, attrs=JQUERY_UI_ATTRS),
        required=False,
    )
    ruler = forms.CharField(
        label=_('Ruler'),
        widget=selectable.forms.AutoCompleteWidget(lookups.DiplomaticLetterRulerLookup, allow_new=True, attrs=JQUERY_UI_ATTRS),
        required=False,
    )

    archiveFile = forms.CharField(
        label=_('Archive file'),
        required=False,
        widget=forms.widgets.TextInput(attrs=JQUERY_UI_ATTRS),
    )

    volume = forms.CharField(
        label=_('Volume'),
        required=False,
        widget=forms.widgets.TextInput(attrs=JQUERY_UI_ATTRS),
    )

    text = forms.CharField(
        label=_('Search in text'),
        required=False,
        widget=forms.widgets.TextInput(attrs=JQUERY_UI_ATTRS),
    )

    order_by = forms.CharField(required=False, widget=forms.HiddenInput())
    ruler_id = forms.IntegerField(label=_('Ruler'), required=False, widget=forms.HiddenInput())
    destination_id = forms.IntegerField(label=_('Destination'), required=False, widget=forms.HiddenInput())
    source_id = forms.IntegerField(label=_('Source'), required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(DiplomaticLettersSearchForm, self).__init__(label_suffix='', *args, **kwargs)

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(DiplomaticLettersSearchForm, self).search()
        if self.is_valid():
            if self.cleaned_data.get('date_from'):
                sqs = sqs.filter(date__gte=self.cleaned_data['date_from'])
            if self.cleaned_data.get('date_to'):
                sqs = sqs.filter(date__lte=self.cleaned_data['date_to'])
            if self.cleaned_data.get('location'):
                sqs = sqs.filter(locations__exact=self.cleaned_data['location'])
            if self.cleaned_data.get('source'):
                sqs = sqs.filter(sources__exact=self.cleaned_data['source'])
            if self.cleaned_data.get('destination'):
                sqs = sqs.filter(destinations_exact=self.cleaned_data['destination'])
            if self.cleaned_data.get('ruler'):
                sqs = sqs.filter(rulers__exact=self.cleaned_data['ruler'])

            if self.cleaned_data.get('text'):
                sqs = sqs.filter(text=self.cleaned_data['text'])
            if self.cleaned_data.get('archiveFile'):
                sqs = sqs.filter(archiveFile=self.cleaned_data['archiveFile'])
            if self.cleaned_data.get('volume'):
                sqs = sqs.filter(source=self.cleaned_data['volume'])
            if self.cleaned_data.get('order_by'):
                order_by = self.cleaned_data.get('order_by')
                if order_by == 'archive_reference':
                    sqs = sqs.order_by('archiveFile').order_by('folio_number_from')
                elif order_by == '-archive_reference':
                    sqs = sqs.order_by('-archiveFile').order_by('-folio_number_from')
                elif order_by == 'description':
                    pass
                elif order_by == '-description':
                    pass
                else:
                    sqs = sqs.order_by(order_by)
            else:
                sqs = sqs.order_by('date')

        else:
            sqs = sqs.order_by('date')
        return sqs

    def no_query_found(self):
        """
        Determines the behavior when no query was found.

        By default, no results are returned (``EmptySearchQuerySet``).

        Should you want to show all results, override this method in your
        own ``SearchForm`` subclass and do ``return self.searchqueryset.all()``.
        """
        return self.searchqueryset  # .all()


class DiplomaticLetterRulerSearchForm(SearchForm):

    description = forms.CharField(
        label=_('Search keyword'),
        widget=selectable.forms.AutoCompleteWidget(lookups.SubjectLookup, allow_new=True, attrs=JQUERY_UI_ATTRS),
        required=False,
    )

    first_letter = forms.CharField(required=False, widget=forms.HiddenInput())

    order_by = forms.CharField(required=False, widget=forms.HiddenInput())

    def no_query_found(self):
        """
        Determines the behavior when no query was found.

        By default, no results are returned (``EmptySearchQuerySet``).

        Should you want to show all results, override this method in your
        own ``SearchForm`` subclass and do ``return self.searchqueryset.all()``.
        """
        return self.searchqueryset  # .all()

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(DiplomaticLetterRulerSearchForm, self).search()
        if self.is_valid():
            if self.cleaned_data.get('description'):
                sqs = sqs.filter(text=self.cleaned_data['description'])
            if self.cleaned_data.get('order_by'):
                # TODO: implement ordering args
                order_by = self.cleaned_data.get('order_by')
                sqs = sqs.order_by(order_by)
            else:
                sqs = sqs.order_by('name_modern_exact')

            first_letter = self.cleaned_data.get('first_letter')
            if first_letter and first_letter.lower() != 'all':

                # filtering by __startswith does not seem to work well with SOLR
                # because we will access all objects, we 'load_all' for effeciency reasons
                sqs = sqs.load_all()
                sqs = [obj for obj in sqs if obj.object.name_modern and obj.object.name_modern[0].lower() == first_letter.lower()]
        else:
            sqs = sqs.order_by('name_modern_exact')
        return sqs


class DiplomaticLettersLocationsSearchForm(SearchForm):
    description = forms.CharField(
        label=_('Search keyword'),
        required=False,
        widget=forms.TextInput(attrs=JQUERY_UI_ATTRS),
    )

    first_letter = forms.CharField(required=False, widget=forms.HiddenInput())

    order_by = forms.CharField(required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(DiplomaticLettersLocationsSearchForm, self).__init__(label_suffix='', *args, **kwargs)

    def no_query_found(self):
        """
        Determines the behavior when no query was found.

        By default, no results are returned (``EmptySearchQuerySet``).

        Should you want to show all results, override this method in your
        own ``SearchForm`` subclass and do ``return self.searchqueryset.all()``.
        """
        return self.searchqueryset

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(DiplomaticLettersLocationsSearchForm, self).search()
        if self.is_valid():
            if self.cleaned_data.get('description'):
                sqs = sqs.filter(text=self.cleaned_data['description'])
            if self.cleaned_data.get('order_by'):
                order_by = self.cleaned_data.get('order_by')
                sqs = sqs.order_by(order_by)
            else:
                sqs = sqs.order_by('city_exact')

            first_letter = self.cleaned_data.get('first_letter')
            if first_letter and first_letter.lower() != 'all':
                # filtering by __startswith does not seem to work well with SOLR
                # because we will access all objects, we 'load_all' for effeciency reasons
                sqs = sqs.load_all()
                sqs = [obj for obj in sqs if obj.object.city and obj.object.city[0].lower() == first_letter.lower()]
        else:
            sqs = sqs.order_by('city_exact')
        return sqs


class AppendixShipsSearchForm(SearchForm):
    description = forms.CharField(
        label=_('Search keyword'),
        required=False,
        widget=forms.TextInput(attrs=JQUERY_UI_ATTRS),
    )

    first_letter = forms.CharField(required=False, widget=forms.HiddenInput())

    order_by = forms.CharField(required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(DiplomaticLettersLocationsSearchForm, self).__init__(label_suffix='', *args, **kwargs)

    def no_query_found(self):
        """
        Determines the behavior when no query was found.

        By default, no results are returned (``EmptySearchQuerySet``).

        Should you want to show all results, override this method in your
        own ``SearchForm`` subclass and do ``return self.searchqueryset.all()``.
        """
        return self.searchqueryset

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(DiplomaticLettersLocationsSearchForm, self).search()
        if self.is_valid():
            if self.cleaned_data.get('description'):
                sqs = sqs.filter(text=self.cleaned_data['description'])
            if self.cleaned_data.get('order_by'):
                order_by = self.cleaned_data.get('order_by')
                sqs = sqs.order_by(order_by)
            else:
                sqs = sqs.order_by('city_exact')

            first_letter = self.cleaned_data.get('first_letter')
            if first_letter and first_letter.lower() != 'all':
                # filtering by __startswith does not seem to work well with SOLR
                # because we will access all objects, we 'load_all' for effeciency reasons
                sqs = sqs.load_all()
                sqs = [obj for obj in sqs if obj.object.city and obj.object.city[0].lower() == first_letter.lower()]
        else:
            sqs = sqs.order_by('city_exact')
        return sqs


class AppendixDocumentTypesSearchForm(SearchForm):
    description = forms.CharField(
        label=_('Search keyword'),
        required=False,
        widget=forms.TextInput(attrs=JQUERY_UI_ATTRS),
    )

    first_letter = forms.CharField(required=False, widget=forms.HiddenInput())

    order_by = forms.CharField(required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(DiplomaticLettersLocationsSearchForm, self).__init__(label_suffix='', *args, **kwargs)

    def no_query_found(self):
        """
        Determines the behavior when no query was found.

        By default, no results are returned (``EmptySearchQuerySet``).

        Should you want to show all results, override this method in your
        own ``SearchForm`` subclass and do ``return self.searchqueryset.all()``.
        """
        return self.searchqueryset

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(DiplomaticLettersLocationsSearchForm, self).search()
        if self.is_valid():
            if self.cleaned_data.get('description'):
                sqs = sqs.filter(text=self.cleaned_data['description'])
            if self.cleaned_data.get('order_by'):
                order_by = self.cleaned_data.get('order_by')
                sqs = sqs.order_by(order_by)
            else:
                sqs = sqs.order_by('city_exact')

            first_letter = self.cleaned_data.get('first_letter')
            if first_letter and first_letter.lower() != 'all':
                # filtering by __startswith does not seem to work well with SOLR
                # because we will access all objects, we 'load_all' for effeciency reasons
                sqs = sqs.load_all()
                sqs = [obj for obj in sqs if obj.object.city and obj.object.city[0].lower() == first_letter.lower()]
        else:
            sqs = sqs.order_by('city_exact')
        return sqs


#
# code based on http://docs.django-userena.org/en/latest/faq.html
#
class SignupForm(SignupFormOnlyEmail):
    """
    A form to demonstrate how to add extra fields to the signup form, in this
    case adding the first and last name.


    """
#     full_name = forms.CharField(label=_('Your name'), max_length=100, required=True)
    first_name = forms.CharField(label=_(u'First name'), max_length=30, required=False)
    last_name = forms.CharField(label=_(u'Last name'), max_length=30, required=False)
    _('Repeat password')
    _('Country')
    _('Signup')
    country = forms.ChoiceField(choices=countries.COUNTRIES, initial='ID')
    _('This email is already in use. Please supply a different email.')

    def __init__(self, *args, **kw):
        """

        A bit of hackery to get the first name and last name at the top of the
        form instead at the end.

        """
        super(SignupForm, self).__init__(*args, **kw)
        self.base_fields['password1'].label = _('Password')

    def save(self):
        """
        Override the save method to save the first and last name to the user
        field.

        """
        """ Generate a random username before falling back to parent signup form """
        while True:
            username = sha_constructor(str(random.random())).hexdigest()[:5]
            try:
                get_user_model().objects.get(username__iexact=username)
            except get_user_model().DoesNotExist:
                break

        self.cleaned_data['username'] = username

        username, email, password = (self.cleaned_data['username'],
                                     self.cleaned_data['email'],
                                     self.cleaned_data['password1'])

        # creat the user, but dont send an email yet
        new_user = UserenaSignup.objects.create_user(
            username,
            email,
            password,
            not userena_settings.USERENA_ACTIVATION_REQUIRED,
            send_email=False,
        )

        new_user.first_name = self.cleaned_data['first_name']
        new_user.last_name = self.cleaned_data['last_name']
        new_user.userprofile.country = self.cleaned_data['country']
        new_user.save()
        new_user.userprofile.save()

        # send the activation mail after having saved first and last name
        new_user.userena_signup.send_activation_email()

        # Userena expects to get the new user from this form, so return the new
        # user.
        return new_user


class EditProfileForm(forms.ModelForm):
    """ Base form used for fields that are always required """
    first_name = forms.CharField(label=_(u'First name'), max_length=30, required=False)
    last_name = forms.CharField(label=_(u'Last name'), max_length=30, required=False)
    country = forms.ChoiceField(choices=countries.COUNTRIES)
    email = forms.EmailField(widget=forms.TextInput(attrs=dict({'class': 'required'}, maxlength=75)), label=_(u"Email"))
    _('Save changes')

    def __init__(self, *args, **kwargs):
        """
        The current ``user`` is needed for initialisation of this form so
        that we can check if the email address is still free and not always
        returning ``True`` for this query because it's the users own e-mail
        address.

        """
        user = kwargs['instance'].user
        super(EditProfileForm, self).__init__(*args, **kwargs)

        self.fields.keyOrder = ['first_name', 'last_name', 'country', 'email']
        if not isinstance(user, get_user_model()):
            raise TypeError("user must be an instance of %s" % get_user_model().__name__)
        else:
            self.user = user

    def clean_email(self):
        """ Validate that the email is not already registered with another user """
        if get_user_model().objects.filter(email__iexact=self.cleaned_data['email']).exclude(email__iexact=self.user.email):
            raise forms.ValidationError(_(u'This email is already in use. Please supply a different email.'))
        return self.cleaned_data['email']

    class Meta:
        model = get_profile_model()
        exclude = ['user', 'mugshot', 'privacy', ]

    def save(self, force_insert=False, force_update=False, commit=True):
        profile = super(EditProfileForm, self).save(commit=commit)
        # Save first and last name
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        profile.country = self.cleaned_data['country']

        if user.email != self.cleaned_data['email']:
            user.email = self.cleaned_data['email']

        user.save()

        return profile


class AuthenticationForm(userena_forms.AuthenticationForm):
    identification = userena_forms.identification_field_factory(_(u"Email address"), _(u"Please supply us with your email address."))
    #
    # for the translation machinery we just register some keywords used in teh form
    _('Password')
    _(u'Remember me for %(days)s')
    _('Signin')

    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)

    def clean(self):
        """
        Checks for the identification and password.

        If the combination can't be found will raise an invalid sign in error.

        """
        identification = self.cleaned_data.get('identification')
        password = self.cleaned_data.get('password')

        if identification and password:
            user = authenticate(identification=identification, password=password)
            if user is None:
                raise forms.ValidationError(_(u"Please enter a correct email and password. Note that both fields are case-sensitive."))
        return self.cleaned_data


class DeHaanSearchForm(SearchForm):
    searchqueryset = SearchQuerySet().models(models.DeHaan)

    def __init__(self, *args, **kwargs):
        super(DeHaanSearchForm, self).__init__(*args, label_suffix='', **kwargs)

    ID = forms.CharField(
        label=_('ID'),
        # widget=selectable.forms.AutoCompleteWidget(lookups.DocumentTypeAppendixLookup, allow_new=True, attrs=JQUERY_UI_ATTRS),
        required=False,
    )

    description = forms.CharField(
        label=_('Description'),
        required=False,
        widget=forms.widgets.TextInput(attrs=JQUERY_UI_ATTRS),
    )

    index_term = forms.CharField(
        label=_('Index Term'),
        # widget=selectable.forms.AutoCompleteWidget(lookups.VesselNameAppendixLookup, allow_new=True, attrs=JQUERY_UI_ATTRS),
        required=False,
    )

    text = forms.CharField(
        label=_('Search in text'),
        required=False,
        widget=forms.widgets.TextInput(attrs=JQUERY_UI_ATTRS),
    )

    order_by = forms.CharField(required=False, widget=forms.HiddenInput())

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        # import ipdb; ipdb.set_trace()
        sqs = super(DeHaanSearchForm, self).search()
        if self.is_valid():
            IDOrig = self.cleaned_data.get('ID')
            sqs = sqs.order_by('order')
            if IDOrig:
                sqs = sqs.filter(type=IDOrig)
            if self.cleaned_data.get('description'):
                sqs = sqs.filter(description=DasaQuery(self.cleaned_data['description']))

            if self.cleaned_data.get('index_term'):  # and self.cleaned_data['vessel_name'] not in [',']:
                # exact filtering on tags does not work, so we do it by hand
                # (WHICH IS VERY EXPENSIVE)
                sqs = [x for x in sqs if self.cleaned_data.get('index_term') in (x.vessel_names_list or '')]
            if self.cleaned_data.get('text'):
                sqs = sqs.filter(text=self.cleaned_data['text'])
        else:
            sqs = sqs.order_by('order')
        return sqs

    def no_query_found(self):
        """
        Determines the behavior when no query was found.

        By default, no results are returned (``EmptySearchQuerySet``).

        Should you want to show all results, override this method in your
        own ``SearchForm`` subclass and do ``return self.searchqueryset.all()``.
        """
        return self.searchqueryset  # .all()


_('Send password')

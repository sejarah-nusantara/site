from dasa import config, models, forms
from dasa import queries, utils
from common import DasaSearchView, _tagcloud, Page


class CorpusDiplomaticumContractsBrowse(DasaSearchView):
    slug = config.SLUG_CORPUSDIPLOMATICUM_CONTRACTS_BROWSE
    template_name = 'pages/corpusdiplomaticum-contracts-browse.html'

    def __init__(self, *args, **kwargs):
        super(CorpusDiplomaticumContractsBrowse, self).__init__(*args, **kwargs)
        self.form_class = forms.CorpusDiplomaticumContractsSearchForm

    def extra_context(self):
        context = super(CorpusDiplomaticumContractsBrowse, self).extra_context()
        # context.update(self.get_context_order_by(['date', 'archive_reference'], default='date'))

        # published_archivefiles = repository.get_archivefiles(status=config.STATUS_PUBLISHED)
        # context['published_archivefiles'] = [x.archiveFile for x in published_archivefiles]
        # get mininal and maximal dates
        # get mininal and maximal dates
        # min_date, max_date = queries.get_min_max_dates(models.CorpusDiplomaticumContract)
        # context['min_year'], context['max_year'] = min_date.year, max_date.year
        # # javascript months start counting at 0 (so january = 0, ecc)
        # context['min_month'], context['max_month'] = min_date.month - 1, max_date.month - 1
        # context['min_day'], context['max_day'] = min_date.day, max_date.day
        context['min_year'], context['max_year'] = queries.get_min_max_values(models.CorpusDiplomaticumContract, 'yearFrom')
        # javascript months start counting at 0 (so january = 0, ecc)
        context['min_month'] = '0'
        context['min_day'] = '1'
        context['max_month'] = '11'
        context['max_day'] = '31'

        context['tags_areaNames'] = _tagcloud(queries.get_corpusdiplomaticum_areanames(), 50)
        context.update(self.get_context_order_by(['dateFrom', 'areaName', 'volume'], default='volume'))
        return context


class CorpusDiplomaticumContractsSearch(CorpusDiplomaticumContractsBrowse):
    slug = config.SLUG_CORPUSDIPLOMATICUM_CONTRACTS_SEARCH
    template_name = 'pages/corpusdiplomaticum-contracts-search.html'


class CorpusDiplomaticumContractsAreas(Page):
    slug = config.SLUG_CORPUSDIPLOMATICUM_CONTRACTS_AREAS
    template_name = 'pages/corpusdiplomaticum-contracts-areas.html'

    def get_context_data(self, **kwargs):
        context = super(CorpusDiplomaticumContractsAreas, self).get_context_data()
        first_letter = self.request.REQUEST.get('first_letter')
        names = queries.get_corpusdiplomaticum_areanames()

        names = [(utils.sort_string(name), name, count) for name, count in names]

        letters_and_counts = [
            (letter, len([s for s in names if s[0].upper().startswith(letter)])) for letter in 'abcdefghijklmnopqrstuvwxyz'.upper()
        ]
        letters_and_counts = [(x, c) for x, c in letters_and_counts if c > 0]

        letters_and_counts.append(('All', len(names)))

        if first_letter and first_letter.lower() != 'all':
            names = [(sort_string, name, c) for sort_string, name, c in names if sort_string.startswith(first_letter.lower())]
        names.sort()
        names = [('%s' % name, c) for _dummy, name, c in names]

        # make three columns
        col_length = len(names) / 2 + 1
        names = [names[:col_length], names[col_length:]]
        context.update({
            'areas': names,
            'letters': letters_and_counts,
        })
        return context


class CorpusDiplomaticumPersons(Page):
    slug = config.SLUG_CORPUSDIPLOMATICUM_PERSONS
    template_name = 'pages/corpusdiplomaticum-persons.html'

    def get_context_data(self, **kwargs):
        context = super(CorpusDiplomaticumPersons, self).get_context_data()
        first_letter = self.request.REQUEST.get('first_letter')
        persons = [p for p in models.CorpusDiplomaticumPersoon.objects.all()]

        persons = [(utils.sort_string(p.name), p) for p in persons]

        letters_and_counts = [
            (letter, len([p for p in persons if p[0].startswith(letter)])) for letter in 'abcdefghijklmnopqrstuvwxyz'
        ]
        letters_and_counts = [(x, c) for x, c in letters_and_counts if c > 0]

        letters_and_counts.append(('All', len(persons)))

        if first_letter and first_letter.lower() != 'all':
            persons = [(sort_string, name) for sort_string, name in persons if sort_string.startswith(first_letter.lower())]
        persons.sort()
        persons = [p for _dummy, p in persons]

        # make two columns
        col_length = len(persons) / 2 + 1
        persons = [persons[:col_length], persons[col_length:]]

        context.update({
            'persons': persons,
            'letters': letters_and_counts,
        })
        return context


class CorpusDiplomaticumPlaces(Page):
    slug = config.SLUG_CORPUSDIPLOMATICUM_PLACES
    template_name = 'pages/corpusdiplomaticum-places.html'

    def get_context_data(self, **kwargs):
        context = super(CorpusDiplomaticumPlaces, self).get_context_data()
        first_letter = self.request.REQUEST.get('first_letter')
        persons = [p for p in models.CorpusDiplomaticumPlaats.objects.all()]

        persons = [(utils.sort_string(p.name), p) for p in persons]

        letters_and_counts = [
            (letter, len([p for p in persons if p[0].startswith(letter)])) for letter in 'abcdefghijklmnopqrstuvwxyz'
        ]
        letters_and_counts = [(x, c) for x, c in letters_and_counts if c > 0]

        letters_and_counts.append(('All', len(persons)))

        if first_letter and first_letter.lower() != 'all':
            persons = [(sort_string, name) for sort_string, name in persons if sort_string.startswith(first_letter.lower())]
        persons.sort()
        persons = [p for _dummy, p in persons]

        # make two columns
        col_length = len(persons) / 2 + 1
        persons = [persons[:col_length], persons[col_length:]]

        context.update({
            'persons': persons,
            'letters': letters_and_counts,
        })
        return context

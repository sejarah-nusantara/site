#
# copyright Gerbrandy SRL
# www.gerbrandy.com
# 2013
#


from haystack.query import SearchQuerySet
from dasa import models
import datetime


def get_subjects(firstletter=None):
    """returns a list of pairs ('subject', number_of_resolutions)"""
    try:
        qry = SearchQuerySet().models(models.Resolution).facet('subject', limit=10000, mincount=1)
        subjects = qry.facet_counts()['fields']['subject']
        if firstletter:
            subjects = [x for x in subjects if x.lower().startswith(firstletter)]
        return subjects
    except KeyError:
        return []


def get_marginalia_vesselnames():
    qry = SearchQuerySet().models(models.JournalEntry).facet('vessel_names_list', limit=10000, mincount=1)
    try:
        vessel_names = qry.facet_counts()['fields']['vessel_names_list']
        return vessel_names
    except KeyError:
        return []

def get_marginalia_asiannames():
    qry = SearchQuerySet().models(models.JournalEntry).facet('person_names_asian_list', limit=10000, mincount=1)
    try:
        vessel_names = qry.facet_counts()['fields']['person_names_asian_list']
        return vessel_names
    except KeyError:
        return []

def get_marginalia_europeannames():
    qry = SearchQuerySet().models(models.JournalEntry).facet('person_names_european_list', limit=10000, mincount=1)
    try:
        vessel_names = qry.facet_counts()['fields']['person_names_european_list']
        return vessel_names
    except KeyError:
        return []

def get_marginalia_placenames():
    qry = SearchQuerySet().models(models.JournalEntry).facet('place_names_list', limit=10000, mincount=1)
    try:
        vessel_names = qry.facet_counts()['fields']['place_names_list']
        return vessel_names
    except KeyError:
        return []


def get_appendix_vesselnames():
    qry = SearchQuerySet().models(models.Appendix).facet('vessel_names_list', limit=10000, mincount=1)
    try:
        vessel_names = qry.facet_counts()['fields']['vessel_names_list']
        return vessel_names
    except KeyError:
        return []

def get_appendix_asiannames():
    qry = SearchQuerySet().models(models.Appendix).facet('person_names_asian_list', limit=10000, mincount=1)
    try:
        vessel_names = qry.facet_counts()['fields']['person_names_asian_list']
        return vessel_names
    except KeyError:
        return []

def get_appendix_europeannames():
    qry = SearchQuerySet().models(models.Appendix).facet('person_names_european_list', limit=10000, mincount=1)
    try:
        vessel_names = qry.facet_counts()['fields']['person_names_european_list']
        return vessel_names
    except KeyError:
        return []

def get_appendix_placenames():
    qry = SearchQuerySet().models(models.Appendix).facet('place_names_list', limit=10000, mincount=1)
    try:
        vessel_names = qry.facet_counts()['fields']['place_names_list']
        return vessel_names
    except KeyError:
        return []


def get_documenttypes_appendix():
    qry = SearchQuerySet().models(models.Appendix).facet('documenttypes_list', limit=10000, mincount=1)
    try:
        vessel_names = qry.facet_counts()['fields']['documenttypes_list']
        return vessel_names
    except KeyError:
        return []

def get_dehaan_indexTerms():
    # the indexMaps index is called vessle_names_list (for reasons of quick coding)
    qry = SearchQuerySet().models(models.DeHaan).facet('vessel_names_list', limit=10000, mincount=1)
    try:
        vessel_names = qry.facet_counts()['fields']['vessel_names_list']
        return vessel_names
    except KeyError:
        return []


def get_min_max_dates(model, fld='date'):
    # given a model, get minimal and maximal values for the date field from solr
    qry = SearchQuerySet().models(model).stats(fld)
    results = qry.stats_results()
    if not results:
        # fail silently
        return datetime.date.today(), datetime.date.today()
    min_date = results[fld]['min']
    max_date = results[fld]['max']
    min_date = min_date.split('T')[0]
    min_date = datetime.datetime.strptime(min_date, '%Y-%m-%d')
    max_date = max_date.split('T')[0]
    max_date = datetime.datetime.strptime(max_date, '%Y-%m-%d')

    return min_date, max_date


def get_min_max_values(model, fld):
    # given a model, get minimal and maximal values for the date field from solr
    qry = SearchQuerySet().models(model).stats(fld)
    results = qry.stats_results()
    if not results:
        return (None, None)
        raise Exception('??')
    min_val = results[fld]['min']
    max_val = results[fld]['max']

    return min_val, max_val


def get_diplomaticletter_rulers():
    qry = SearchQuerySet().models(models.DiplomaticLetter).facet('rulers', limit=10000, mincount=1)
    try:
        result = qry.facet_counts()['fields']['rulers']
        return result
    except KeyError:
        return []


def get_diplomaticletter_locations():
    qry = SearchQuerySet().models(models.DiplomaticLetter).facet('locations', limit=10000, mincount=1)
    try:
        result = qry.facet_counts()['fields']['locations']
        return result
    except KeyError:
        return []


def get_placard_governors():
    qry = SearchQuerySet().models(models.Placard).facet('locations', limit=10000, mincount=1)
    try:
        result = qry.facet_counts()['fields']['locations']
        return result
    except KeyError:
        return []


def get_resolution_sources():
    qry = SearchQuerySet().models(models.Resolution).facet('source')
    try:
        return qry.facet_counts()['fields']['source']
    except KeyError, error:
        from django.conf import settings
        solr_url = settings.HAYSTACK_SOLR_URL
        raise Exception('%(error)s\n Check if solr is running on %(solr_url)s; try "fab build_solr_schema"' % locals())


def choices_resolution_subject():
    ls = [(subject, '%s (%s)' % (subject, count)) for subject, count in get_subjects()]
    ls.sort()
    return ls


def choices_resolution_source():
    ls = [(subject, '%s (%s)' % (subject, count)) for subject, count in get_resolution_sources()]
    ls.sort()
    return [('', '')] + ls


def get_corpusdiplomaticum_areanames():
    qry = SearchQuerySet().models(models.CorpusDiplomaticumContract).facet('areaName', limit=10000, mincount=1)
    try:
        result = qry.facet_counts()['fields']['areaName']
        return result
    except KeyError:
        return []

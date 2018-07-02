# encoding=utf-8

#
# this file defines which elements are indexed by solr (and how)
#
#
import datetime
from haystack import indexes
from django.conf import settings
import models

# TODO: this not very elegant, mixing test code with production code
TEST_ENVIRONMENT = getattr(settings, 'TEST_ENVIRONMENT', False)

class SiteSearchIndex(indexes.SearchIndex, indexes.Indexable):
    """

    """
    text = indexes.CharField(model_attr='solr_index', document=True)
    release_date = indexes.DateField(null=True)

    def get_model(self):
        return models.BasicPage

    def prepare_release_date(self, obj):
        # only hk items have a release date, but we include them for all objects
        if isinstance(obj, models.HartaKarunItem):
            return obj.release_date
        else:
            # return some date in the past
            return datetime.datetime(2000, 1, 1)



class DeHaanIndex(SiteSearchIndex):
    #     The following search fields are shown and can be used:
    #  Map ID (searches in: ID)
    #  Description (searches in fields: descriptionByDeHaanNL, descriptionOnMapNL, titleEN
    #  Index term (searches in: indexTerms)
    #  Search in text (means search in all fields)

    # abusing the 'type' index for storing the IDSource
    type = indexes.CharField(model_attr='IDSource', faceted=False)
    description = indexes.CharField(model_attr='description', faceted=False)
    # abusing the 'vessel_names' index to also store the indexTerms
    vessel_names = indexes.CharField(model_attr='indexTerms', faceted=True)
    vessel_names_list = indexes.MultiValueField(model_attr='indexTermsSplitted', faceted=True)
    locations = indexes.MultiValueField(model_attr='indexTerms', faceted=True)
    vessel_names_list = indexes.MultiValueField(faceted=True)
    text = indexes.CharField(model_attr='solr_index', document=True)
    order = indexes.IntegerField(model_attr='order', faceted=False, null=True)

    def get_model(self):
        return models.DeHaan

    def prepare_vessel_names_list(self, obj):
        s = obj.indexTerms
        if s:
            ls = s.split(';')
            ls = [x.strip(',. \n') for x in ls]
            return ls
        else:
            return []



class ResolutionIndex(SiteSearchIndex):
    # put facets on all the fields that are used for sorting in the overview
    order = indexes.IntegerField(model_attr='order', faceted=True, null=True)
    date = indexes.DateField(model_attr='date', faceted=True, null=True)
    subject = indexes.CharField(model_attr='subject', faceted=True)
    type = indexes.CharField(model_attr='type', faceted=True)
    description = indexes.CharField(model_attr='description', faceted=True)

    source = indexes.CharField(model_attr='source', faceted=True)

    def get_model(self):
        return models.Resolution


class JournalEntryIndex(SiteSearchIndex):
    """indexes for Marginalia"""
    order = indexes.IntegerField(model_attr='order', faceted=True, null=True)
    date = indexes.DateField(model_attr='date', faceted=True, null=True)
    description = indexes.CharField(model_attr='description', faceted=True)
    vessel_names = indexes.CharField(model_attr='vessel_names', faceted=True)
    vessel_names_list = indexes.MultiValueField(faceted=True)
    annotation = indexes.CharField(model_attr='annotation', faceted=True)
    archiveFile = indexes.CharField(model_attr='archiveFile', faceted=True)
    folio_number_from = indexes.IntegerField(faceted=True)
    person_names_asian = indexes.CharField(model_attr='person_names_asian', faceted=True)
    person_names_asian_list = indexes.MultiValueField(faceted=True)
    person_names_european = indexes.CharField(model_attr='person_names_european', faceted=True)
    person_names_european_list = indexes.MultiValueField(faceted=True)
    place_names = indexes.CharField(model_attr='place_names', faceted=True)
    place_names_list = indexes.MultiValueField(faceted=True)

    def get_model(self):
        return models.JournalEntry

    def prepare_vessel_names_list(self, obj):
        s = obj.vessel_names
        if s:
            ls = s.split(';')
            ls = [x.strip(',. \n') for x in ls]
            return ls
        else:
            return []

    def prepare_person_names_asian_list(self, obj):
        s = obj.person_names_asian
        if s:
            ls = s.split(';')
            ls = [x.strip(',. \n') for x in ls]
            ls = [x for x in ls if x]
            return ls
        else:
            return []

    def prepare_person_names_european_list(self, obj):
        s = obj.person_names_european
        if s:
            ls = s.split(';')
            ls = [x.strip(',. \n') for x in ls]
            ls = [x for x in ls if x]
            return ls
        else:
            return []

    def prepare_place_names_list(self, obj):
        s = obj.place_names
        if s:
            ls = s.split(';')
            ls = [x.strip(',. \n') for x in ls]
            ls = [x for x in ls if x]
            return ls
        else:
            return []

    def prepare_folio_number_from(self, obj):
        if obj.folio_number_from and obj.folio_number_from.isdigit():
            return int(obj.folio_number_from)
        else:
            return 0


class AppendixIndex(SiteSearchIndex):
    """indexes for Appendices to the resolution books"""
    order = indexes.IntegerField(model_attr='order', faceted=True, null=True)
    vessel_names = indexes.CharField(model_attr='vessel_names', faceted=True)
    vessel_names_list = indexes.MultiValueField(faceted=True)
    person_names_asian = indexes.CharField(model_attr='person_names_asian', faceted=True)
    person_names_asian_list = indexes.MultiValueField(faceted=True)
    person_names_european = indexes.CharField(model_attr='person_names_european', faceted=True)
    person_names_european_list = indexes.MultiValueField(faceted=True)
    place_names = indexes.CharField(model_attr='place_names', faceted=True)
    place_names_list = indexes.MultiValueField(faceted=True)

    document_type = indexes.CharField(model_attr='document_type_nl', faceted=True)
    documenttypes_list = indexes.MultiValueField(faceted=True)
    archiveFile = indexes.CharField(model_attr='archiveFile', faceted=True)
    title = indexes.CharField(model_attr='title_nl', null=True)
    folio_number_from = indexes.IntegerField(faceted=True)
    doc_y = indexes.IntegerField(null=True, model_attr='doc_y')
    doc_m = indexes.IntegerField(null=True, model_attr='doc_m')
    doc_d = indexes.IntegerField(null=True, model_attr='doc_d')
    res_y = indexes.IntegerField(null=True, model_attr='res_y')
    res_m = indexes.IntegerField(null=True, model_attr='res_m')
    res_d = indexes.IntegerField(null=True, model_attr='res_d')

    def get_model(self):
        return models.Appendix

    def prepare_vessel_names_list(self, obj):
        return obj.vessel_names_as_list()

    def prepare_person_names_asian_list(self, obj):
        s = obj.person_names_asian
        if s:
            ls = s.split(';')
            ls = [x.strip(',. \n') for x in ls]
            ls = [x for x in ls if x]
            return ls
        else:
            return []

    def prepare_person_names_european_list(self, obj):
        s = obj.person_names_european
        if s:
            ls = s.split(';')
            ls = [x.strip(',. \n') for x in ls]
            ls = [x for x in ls if x]
            return ls
        else:
            return []

    def prepare_place_names_list(self, obj):
        s = obj.place_names
        if s:
            ls = s.split(';')
            ls = [x.strip(',. \n') for x in ls]
            ls = [x for x in ls if x]
            return ls
        else:
            return []


    def prepare_documenttypes_list(self, obj):
        s = obj.document_type_nl
        if s:
            return [s]
        else:
            return []

    def prepare_folio_number_from(self, obj):
        if obj.folio_number_from and obj.folio_number_from.isdigit():
            return int(obj.folio_number_from)
        else:
            return

    def prepare_doc_m(self, obj):
        return obj.doc_m or 0

    def prepare_doc_d(self, obj):
        return obj.doc_d or 0

    def prepare_res_m(self, obj):
        return obj.res_m or 0

    def prepare_res_d(self, obj):
        return obj.res_d or 0


class CorpusDiplomaticumContractIndex(SiteSearchIndex):
    """indexes for Diplomatieke Brieven"""
    text = indexes.CharField(model_attr='solr_index', document=True)
    # order = indexes.IntegerField(model_attr='order', faceted=True, null=True)
    yearFrom = indexes.IntegerField(model_attr='yearFrom', faceted=True, null=True)
    monthFrom = indexes.IntegerField(model_attr='monthFrom', faceted=True, null=True)
    dayFrom = indexes.IntegerField(model_attr='dayFrom', faceted=True, null=True)
    dateFrom = indexes.DateField(model_attr='dateFrom', faceted=True, null=True)
    areaName = indexes.CharField(model_attr='areaName', faceted=True)
    volumeNumber = indexes.CharField(model_attr='volumeNumber')
    pageFrom = indexes.CharField(model_attr='pageFrom')
    pageFromInt = indexes.IntegerField(model_attr='pageFrom')

    def get_model(self):
        return models.CorpusDiplomaticumContract


class DiplomaticLetterIndex(SiteSearchIndex):
    """indexes for Diplomatieke Brieven"""
    text = indexes.CharField(model_attr='solr_index', document=True)
    order = indexes.IntegerField(model_attr='order', faceted=True, null=True)
    date = indexes.DateField(model_attr='insertion_date', faceted=True, null=True)
    # have some problems with deployment
    #     insertion_date = indexes.DateField(model_attr='insertion_date', faceted=True, null=True)
    archiveFile = indexes.CharField(model_attr='archiveFile', faceted=True)
    folio_number_from = indexes.IntegerField(faceted=True)
    locations = indexes.MultiValueField(model_attr='get_location_names', faceted=True)
    sources = indexes.MultiValueField(model_attr='get_source_names', faceted=True)
    destinations = indexes.MultiValueField(model_attr='get_destination_names', faceted=True)
    rulers = indexes.MultiValueField(model_attr='get_ruler_names', faceted=True)
    # we abuse the 'source' index to index the 'volume' field, as a quick shortcut
    source = indexes.CharField(model_attr='volume', faceted=True)

    def get_model(self):
        return models.DiplomaticLetter


class DiplomaticLetterRulerIndex(SiteSearchIndex):
    name_modern = indexes.CharField(model_attr='name_modern', faceted=True)
    location = indexes.CharField(model_attr='location', faceted=False)
    number_of_letters = indexes.IntegerField(model_attr='number_of_letters', faceted=False)

    def get_model(self):
        return models.DiplomaticLetterRuler


class DiplomaticLetterLocationIndex(SiteSearchIndex):
    city = indexes.CharField(model_attr='city', faceted=True)
    number_of_letters = indexes.IntegerField(model_attr='number_of_letters', faceted=False)

    def get_model(self):
        return models.DiplomaticLetterLocation


class PlacardIndex(SiteSearchIndex):
    # we abuse the 'location' index field to store the 'governor' value
    # (to avoid defining yet another extra index)
    description = indexes.CharField(model_attr='text', faceted=False)
    date = indexes.DateField(model_attr='issued_date_as_date', faceted=False, null=True)
    location = indexes.CharField(model_attr='governor', faceted=False, null=True)
    locations = indexes.MultiValueField(model_attr='governors', faceted=True)
    order = indexes.IntegerField(model_attr='order', faceted=False, null=True)

    def get_model(self):
        return models.Placard


class HartaKarunMainCategoryIndex(SiteSearchIndex):

    def get_model(self):
        return models.HartaKarunMainCategory


class HartaKarunCategoryIndex(SiteSearchIndex):

    def get_model(self):
        return models.HartaKarunCategory


class HartaKarunItemIndex(SiteSearchIndex):

    def get_model(self):
        return models.HartaKarunItem


class ScanIndex(SiteSearchIndex):

    def get_model(self):
        return models.Scan


class NewsIndex(SiteSearchIndex):

    def get_model(self):
        return models.News

"""lookup classes used by django-selectable"""

from selectable.base import LookupBase
from selectable.registry import registry

from dasa import queries


class DasaLookup(LookupBase):
    base_query = None

    def get_query(self, request, term):
        data = [x[0] for x in self.base_query()]
        data = filter(lambda x: x.lower().startswith(term.lower()), data)
        data.sort()
        return data


class SubjectLookup(DasaLookup):
    def base_query(self):
        return queries.get_subjects()

registry.register(SubjectLookup)


class VesselNameLookup(DasaLookup):
    def base_query(self):
        return queries.get_marginalia_vesselnames()

registry.register(VesselNameLookup)

class MarginaliaAsianNameLookup(DasaLookup):
    def base_query(self):
        return queries.get_marginalia_asiannames()

registry.register(MarginaliaAsianNameLookup)

class MarginaliaEuropeanNameLookup(DasaLookup):
    def base_query(self):
        return queries.get_marginalia_europeannames()

registry.register(MarginaliaEuropeanNameLookup)

class MarginaliaPlaceNameLookup(DasaLookup):
    def base_query(self):
        return queries.get_marginalia_placenames()

registry.register(MarginaliaPlaceNameLookup)


class VesselNameAppendixLookup(DasaLookup):
    def base_query(self):
        return queries.get_appendix_vesselnames()

registry.register(VesselNameAppendixLookup)

class AppendixAsianNameLookup(DasaLookup):
    def base_query(self):
        return queries.get_appendix_asiannames()

registry.register(AppendixAsianNameLookup)

class AppendixEuropeanNameLookup(DasaLookup):
    def base_query(self):
        return queries.get_appendix_europeannames()

registry.register(AppendixEuropeanNameLookup)

class AppendixPlaceNameLookup(DasaLookup):
    def base_query(self):
        return queries.get_appendix_placenames()

registry.register(AppendixPlaceNameLookup)




class DocumentTypeAppendixLookup(DasaLookup):
    def base_query(self):
        return queries.get_documenttypes_appendix()

registry.register(DocumentTypeAppendixLookup)


class DiplomaticLetterLocationLookup(DasaLookup):
    def base_query(self):
        return queries.get_diplomaticletter_locations()

registry.register(DiplomaticLetterLocationLookup)


class DiplomaticLetterRulerLookup(DasaLookup):
    def base_query(self):
        return queries.get_diplomaticletter_rulers()

registry.register(DiplomaticLetterRulerLookup)


class PlacardGovernorLookup(DasaLookup):
    def base_query(self):
        return queries.get_placard_governors()

registry.register(PlacardGovernorLookup)

class CorpusDiplomaticumAreaNameLookup(DasaLookup):
    def base_query(self):
        return queries.get_corpusdiplomaticum_areanames()

registry.register(CorpusDiplomaticumAreaNameLookup)

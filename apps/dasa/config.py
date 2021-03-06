
# the SLUG_* constants connect the BasicPage objects in the db with the urls and views

SLUG_ARCHIVE = 'archive'
SLUG_ARCHIVE_DAILY_JOURNALS = 'archive_daily_journals'
SLUG_ARCHIVE_GENERALRESOLUTIONS = 'archive_generalresolutions'
SLUG_APPENDICES_RESOLUTIONS = 'appendices-resolutions'
SLUG_APPENDIX_BROWSE = 'browse-appendices'
SLUG_APPENDIX_SEARCH = 'search-appendices'
SLUG_APPENDIX_VESSELNAMES = 'appendices_resolutions_ships'
SLUG_APPENDIX_ASIANNAMES = 'appendices-resolutions-asian-names'
SLUG_APPENDIX_EUROPEANNAMES = 'appendices-resolutions-european-names'
SLUG_APPENDIX_PLACENAMES = 'appendices-resolutions-place-names'
SLUG_APPENDIX_DOCUMENTTYPES = 'appendices-resolutions-documenttypes'
SLUG_COLLECTIONS_RESOLUTION = 'collections-resolutions'
SLUG_CONTACT = 'contact'
SLUG_COPYRIGHT = 'copyright'
SLUG_CORPUSDIPLOMATICUM_CONTRACTS_BROWSE = 'corpusdiplomaticum_contracts_browse'
SLUG_CORPUSDIPLOMATICUM_CONTRACTS_SEARCH = 'corpusdiplomaticum_contracts_search'
SLUG_CORPUSDIPLOMATICUM_CONTRACTS_AREAS = 'corpusdiplomaticum_contracts_areas'
SLUG_CORPUSDIPLOMATICUM_PERSONS = 'corpusdiplomaticum_persons'
SLUG_CORPUSDIPLOMATICUM_PLACES = 'corpusdiplomaticum_places'
SLUG_DISCLAIMER = 'disclaimer'
SLUG_DEHAAN_BROWSE = 'browse-maps'
SLUG_DEHAAN_SEARCH = 'search-maps'
SLUG_DEHAAN_INDEXTERMS = 'index-maps'
SLUG_DAILY_JOURNALS = 'daily_journals'
SLUG_DAILY_JOURNALS_VOLUMES = 'daily_journals_volumes'
SLUG_DIGITAL_PRESERVATION = 'digital_preservation'
SLUG_DIPLOMATICLETTERS_BROWSE = 'browse_letters'
SLUG_DIPLOMATICLETTERS_SEARCH = 'search_letters'
SLUG_DIPLOMATICLETTERS_RULERS = 'rulers_index'
SLUG_DIPLOMATICLETTERS_LOCATIONS = 'locations_index'
SLUG_ENTRIES = 'entries'
SLUG_FOREWORD = 'foreword'
SLUG_GENERALRESOLUTIONS = 'generalresolutions'
SLUG_HARTAKARUN = 'hartakarun'
SLUG_HARTAKARUN_ALL_ARTICLES = 'hartakarun-all-articles'
SLUG_HARTAKARUN_MAIN_CATEGORY = 'hartakarunmaincategory'  # MUST COINCIDE WITH HartaKarunMainCategory.lower()
SLUG_HARTAKARUN_SUBCATEGORY = 'hartakaruncategory'  # MUST COINCIDE WITH HartaKarunCategory.lower()
SLUG_INTRODUCTION = 'introduction'
SLUG_INVENTORY = 'inventory'
SLUG_MARGINALIA_BROWSE = 'marginalia_browse'
SLUG_MARGINALIA_SEARCH = 'marginalia_search'
SLUG_MARGINALIA_SHIPS = 'marginalia_ships'
SLUG_MARGINALIA_ASIANNAMES = 'marginalia-asian-names'
SLUG_MARGINALIA_EUROPEANNAMES = 'marginalia-european-names'
SLUG_MARGINALIA_PLACENAMES = 'marginalia-place-names'
SLUG_NEWS = 'berita'
SLUG_ORGANIZATION = 'organization'
SLUG_PRIVACY = 'privacy'
SLUG_PLACARD_BROWSE = 'browse-placards'
SLUG_PLACARD_SEARCH = 'search-placards'
SLUG_PLACARD_GOVERNORS = 'placard-governors'
SLUG_REALIA_BROWSE = 'realia_browse'
SLUG_REALIA_SEARCH = 'realia_search'
SLUG_REALIA_SUBJECTS = 'realia_subjects'
SLUG_SEARCH = 'search'
SLUG_SITE_POLICY = 'site_policy'
STATUS_PUBLISHED = 2

# TODO: refactor: this seems to not be really used in production
SLUG_COLLECTIONS = 'collections'
SLUG_COLLECTIONS_BESOGNES = 'collections_besognes'

SLUG_ACCOUNTS_PROFILE_PASSWORD = 'accounts_profile_password'
SLUG_ACCOUNTS_SIGNIN = 'accounts_signin'
SLUG_ACCOUNTS_SIGNUP = 'accounts_signup'
SLUG_ACCOUNTS_ACTIVATE_FAIL = 'accounts_activate_fail'
SLUG_ACCOUNTS_PASSWORD_COMPLETE = 'accounts_password_complete'
SLUG_ACCOUNTS_PASSWORD_RESET = 'accounts_password_reset'
SLUG_ACCOUNTS_PASSWORD_RESET_DONE = 'accounts_password_reset_done'
SLUG_ACCOUNTS_PASSWORD_RESET_CONFIRM = 'accounts_password_reset_confirm'
SLUG_ACCOUNTS_PASSWORD_RESET_COMPLETE = 'accounts_password_reset_complete'
SLUG_ACCOUNTS_PASSWORD_RESET_FAILED = 'accounts_password_reset_failed'
SLUG_ACCOUNTS_PROFILE_EDIT = 'accounts_profile_edit'
SLUG_ACCOUNTS_PROFILE_PASSWORD = 'accounts_profile_password'
SLUG_ACCOUNTS_SIGNUP_COMPLETE = 'accounts_signup_complete'


def get_slugs_in_use():
    # return a dictionary with slugs that are defined by constants
    slugs = [(k, v) for k, v in globals().items() if k.startswith('SLUG_')]
    return dict(slugs)

SLUGS_IN_USE = get_slugs_in_use()

import logging

from django.conf.urls import include, patterns, url
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.http import Http404
from django.core import urlresolvers

from django.contrib import admin
admin.autodiscover()

from dasa.filebrowser_site import site as filebrowser_site

from userena import views as userena_views
from userena import settings as userena_settings

from dasa import views as views
# need "unused" imports on next line to keep them availabe
from dasa.views import get_page, corpusdiplomaticum, syncarchivefiles
from dasa import forms
from dasa import config
from dasa import menu

menuitems = menu.Menu().menuitems()
logger = logging.getLogger('django')
c = config.__dict__
# handler403 = 'dasa.views.signin'
#


def extra_context(slug=None, **kwargs):
    context = {'menuitems': menuitems, 'home_page': get_page('home')}
    context.update(kwargs)
    if slug:
        try:
            page = get_page(slug)
            context.update({'page': page})
            context.update({'show_admin_link': '1'})
        except Http404:
            logger.warn('Could not find a BasicPage with slug {slug}'.format(slug=slug))
    return context


def dasa_view_wrapper(view, slug=None, **wrapper_kwargs):
    """wrap a view function and add some dasa context variables"""

    def new_view(*args, **kwargs):
        context = kwargs.get('extra_context', {})
        context.update(extra_context(slug, **wrapper_kwargs))
        kwargs['extra_context'] = context
        return view(*args, **kwargs)
    return new_view


def signin_redirect(redirect=None, user=None):
    """where do we go after signin?"""
    if redirect:
        return redirect
    elif user is not None:
        return urlresolvers.reverse('userena_profile_detail', args=[user.username])
    else:
        return settings.LOGIN_REDIRECT_URL


urlpatterns = patterns('',
    #
    url(r'^robots.txt$', views.robots_txt, name='robots_txt'),
    url(r'^sitemap.xml$', views.sitemap_xml, name='sitemap_xml'),
    (r'^admin/filebrowser/', include(filebrowser_site.urls)),
    (r'^admin/', include(admin.site.urls)),
    #
    # URLs for accounts
    #
    url(r'^is_authenticated/$', views.is_authenticated, name='is_authenticated'),
    url(
        r'^accounts/signin/$',
        dasa_view_wrapper(userena_views.signin, slug=config.SLUG_ACCOUNTS_SIGNIN),
        {
            'auth_form': forms.AuthenticationForm,
            'redirect_signin_function': signin_redirect,
        },
        name='userena_signin'),
    url(
        r'^accounts/signup/$',
        dasa_view_wrapper(views.signup, slug=config.SLUG_ACCOUNTS_SIGNUP),
        name='userena_signup'),
    url(
        r'^accounts/signout/$',
        dasa_view_wrapper(userena_views.signout),
        name='userena_signout',),
    # View profiles
    # views.profile_detail redirects to the edit account
    url(r'^accounts/(?P<username>(?!signout|signup|signin)[\.\w-]+)/$', views.profile_detail, name='userena_profile_detail'),
    # any url starting with 'accounts_..' will be redirected to 'accounts/..'
    url(r'^accounts_(?P<slug>[\.\w-]+)/$', views.RedirectAccountsUrlView.as_view()),

    url(r'^accounts/(?P<username>[\.\w-]+)/edit/$',
        dasa_view_wrapper(views.profile_edit, slug=config.SLUG_ACCOUNTS_PROFILE_EDIT),
        name='userena_profile_edit',
        ),  # Edit profile

    # Reset password
    url(r'^accounts/password/reset/$',
        dasa_view_wrapper(views.password_reset, slug=config.SLUG_ACCOUNTS_PASSWORD_RESET),
        {
            'template_name': 'userena/password_reset_form.html',
            'email_template_name': 'userena/emails/password_reset_message.txt',
        },
       name='userena_password_reset'),
    url(
        r'^accounts/password/reset/done/$',
        dasa_view_wrapper(auth_views.password_reset_done, slug=config.SLUG_ACCOUNTS_PASSWORD_RESET_DONE),
        {
            'template_name': 'userena/password_reset_done.html',
        },
        name='userena_password_reset_done',
    ),
    url(
        r'^accounts/password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        dasa_view_wrapper(views.password_reset_confirm, slug=config.SLUG_ACCOUNTS_PASSWORD_RESET_CONFIRM),
        {
            'template_name': 'userena/password_reset_confirm_form.html',
        },
        name='userena_password_reset_confirm',
    ),
    url(r'^accounts/password/reset/confirm/complete/$',
        dasa_view_wrapper(auth_views.password_reset_complete, slug=config.SLUG_ACCOUNTS_PASSWORD_RESET_COMPLETE),
        {'template_name': 'userena/password_reset_complete.html', },
        name='userena_password_reset_complete',),

    url(r'^accounts/password/reset/failed/$',
       views.DirectTemplateView.as_view(
           template_name='userena/accounts_password_reset_failed.html',
           extra_context=extra_context(slug=config.SLUG_ACCOUNTS_PASSWORD_RESET_FAILED),
           ),
        name='accounts_password_reset_failed'),

    # Change password
    url(r'^accounts/(?P<username>[\.\w-]+)/password/$',
        dasa_view_wrapper(userena_views.password_change, slug=config.SLUG_ACCOUNTS_PROFILE_PASSWORD),
        name='userena_password_change'),

    url(r'^accounts/(?P<username>[\.\w-]+)/password/complete/$',
       dasa_view_wrapper(userena_views.direct_to_user_template, slug=config.SLUG_ACCOUNTS_PASSWORD_COMPLETE),
       {'template_name': 'userena/password_complete.html'},
       name='userena_password_change_complete'),

    # Signup
    url(
        #         r'^accounts/(?P<username>[\.\w-]+)/signup/complete/$',
        r'^accounts/signup/complete/$',
        #        userena_views.direct_to_user_template,
        views.DirectTemplateView.as_view(**{'template_name': 'userena/signup_complete.html',
        'extra_context': extra_context(
            slug=config.SLUG_ACCOUNTS_SIGNUP_COMPLETE,
            userena_activation_required=userena_settings.USERENA_ACTIVATION_REQUIRED,
            userena_activation_days=userena_settings.USERENA_ACTIVATION_DAYS,
            )}),
        name='userena_signup_complete'),
    # Activate
    url(r'^accounts/activate/(?P<activation_key>\w+)/$',
       dasa_view_wrapper(views.activate, slug=config.SLUG_ACCOUNTS_ACTIVATE_FAIL),
       name='userena_activate'),

    # Retry activation
    url(r'^accounts/activate/retry/(?P<activation_key>\w+)/$',
        userena_views.activate_retry,
        name='userena_activate_retry'),

    (r'^accounts/', include('userena.urls')),

    url(r'^admin/sync_archivefiles$', syncarchivefiles.SyncArchiveFiles.as_view(), name='sync_archivefiles'),

    url(r'^$', views.Home.as_view(), name="home"),

    url(r'^%(SLUG_HARTAKARUN)s/$' % c, views.HartaKarunIndex.as_view(), name=config.SLUG_HARTAKARUN),
    url(r'^%(SLUG_HARTAKARUN)s/timeline$' % c, views.HartaKarunTimeLine.as_view(), name='hartakarun_timeline'),
    # the names of these url patterns should be like model.lowercase() so they get picked up by DasaWrapper.absolute_url()
    url(r'^%(SLUG_HARTAKARUN)s/item/(?P<path>.*)/$' % c, views.HartaKarunItemView.as_view(), name='hartakarunitem'),
    url(r'^%(SLUG_HARTAKARUN)s/item/(?P<path>.*)/(?P<section>.*)$' % c, views.HartaKarunItemView.as_view(), name='hartakarunitem'),
    url(r'^%(SLUG_HARTAKARUN_MAIN_CATEGORY)s/(?P<path>.*)/$' % c, views.HartakarunMainCategoryView.as_view(), name=config.SLUG_HARTAKARUN_MAIN_CATEGORY),
    url(r'^%(SLUG_HARTAKARUN)s/category/(?P<path>.*)/$' % c, views.HartakarunCategoryView.as_view(), name='hartakaruncategory'),
    url(r'^%(SLUG_HARTAKARUN_ALL_ARTICLES)s/$' % c, views.HartaKarunArticles.as_view(), name=config.SLUG_HARTAKARUN_ALL_ARTICLES),

    url(r'^%(SLUG_ARCHIVE)s/$' % c, views.Archive.as_view(), name='archive'),

    url(r'^%(SLUG_INVENTORY)s/$' % c, views.Inventory.as_view(), name='inventory'),
    url(r'^%(SLUG_INVENTORY)s_(?P<language>..)/$' % c, views.InventoryTree.as_view(), name='inventory_tree'),

    url(r'^%(SLUG_MARGINALIA_BROWSE)s/$' % c, views.MarginaliaBrowse(), name=config.SLUG_MARGINALIA_BROWSE),
    url(r'^%(SLUG_MARGINALIA_SEARCH)s/$' % c, views.MarginaliaSearch(), name=config.SLUG_MARGINALIA_SEARCH),
    url(r'^%(SLUG_MARGINALIA_SHIPS)s/$' % c, views.MarginaliaVessels.as_view(), name=config.SLUG_MARGINALIA_SHIPS),
    url(r'^%(SLUG_MARGINALIA_ASIANNAMES)s/$' % c, views.MarginaliaAsianNames.as_view(), name=config.SLUG_MARGINALIA_ASIANNAMES),
    url(r'^%(SLUG_MARGINALIA_EUROPEANNAMES)s/$' % c, views.MarginaliaEuropeanNames.as_view(), name=config.SLUG_MARGINALIA_EUROPEANNAMES),
    url(r'^%(SLUG_MARGINALIA_PLACENAMES)s/$' % c, views.MarginaliaPlaceNames.as_view(), name=config.SLUG_MARGINALIA_PLACENAMES),

    url(r'^%(SLUG_APPENDIX_BROWSE)s/$' % c, views.appendix.AppendixBrowse(), name=config.SLUG_APPENDIX_BROWSE),
    url(r'^%(SLUG_APPENDIX_SEARCH)s/$' % c, views.appendix.AppendixSearch(), name=config.SLUG_APPENDIX_SEARCH),
    url(r'^%(SLUG_APPENDIX_VESSELNAMES)s/$' % c, views.appendix.AppendixVesselNames.as_view(), name=config.SLUG_APPENDIX_VESSELNAMES),
    url(r'^%(SLUG_APPENDIX_DOCUMENTTYPES)s/$' % c, views.appendix.AppendixDocumentTypes.as_view(), name=config.SLUG_APPENDIX_DOCUMENTTYPES),
    url(r'^%(SLUG_APPENDIX_ASIANNAMES)s/$' % c, views.appendix.AppendixAsianNames.as_view(), name=config.SLUG_APPENDIX_ASIANNAMES),
    url(r'^%(SLUG_APPENDIX_EUROPEANNAMES)s/$' % c, views.appendix.AppendixEuropeanNames.as_view(), name=config.SLUG_APPENDIX_EUROPEANNAMES),
    url(r'^%(SLUG_APPENDIX_PLACENAMES)s/$' % c, views.appendix.AppendixPlaceNames.as_view(), name=config.SLUG_APPENDIX_PLACENAMES),

    url(r'^%(SLUG_DEHAAN_BROWSE)s/$' % c, views.dehaan.DeHaanBrowse(), name=config.SLUG_DEHAAN_BROWSE),
    url(r'^%(SLUG_DEHAAN_SEARCH)s/$' % c, views.dehaan.DeHaanSearch(), name=config.SLUG_DEHAAN_SEARCH),
    url(r'^%(SLUG_DEHAAN_INDEXTERMS)s/$' % c, views.DeHaanIndexMap.as_view(), name=config.SLUG_DEHAAN_INDEXTERMS),

    url(r'^%(SLUG_PLACARD_BROWSE)s/$' % c, views.PlacardsBrowse(), name=config.SLUG_PLACARD_BROWSE),
    url(r'^%(SLUG_PLACARD_SEARCH)s/$' % c, views.PlacardsSearch(), name=config.SLUG_PLACARD_SEARCH),
    url(r'^%(SLUG_PLACARD_GOVERNORS)s/$' % c, views.PlacardGovernors.as_view(), name=config.SLUG_PLACARD_GOVERNORS),

    url(r'^%(SLUG_REALIA_BROWSE)s/$' % c, views.RealiaBrowse(), name=config.SLUG_REALIA_BROWSE),
    url(r'^%(SLUG_REALIA_SEARCH)s/$' % c, views.RealiaSearch(), name=config.SLUG_REALIA_SEARCH),
    url(r'^%(SLUG_REALIA_SUBJECTS)s/$' % c, views.RealiaSubjects.as_view(), name=config.SLUG_REALIA_SUBJECTS),

    url(r'^%(SLUG_CORPUSDIPLOMATICUM_CONTRACTS_BROWSE)s/$' % c, corpusdiplomaticum.CorpusDiplomaticumContractsBrowse(), name=config.SLUG_CORPUSDIPLOMATICUM_CONTRACTS_BROWSE),
    url(r'^%(SLUG_CORPUSDIPLOMATICUM_CONTRACTS_SEARCH)s/$' % c, corpusdiplomaticum.CorpusDiplomaticumContractsSearch(), name=config.SLUG_CORPUSDIPLOMATICUM_CONTRACTS_SEARCH),
    url(r'^%(SLUG_CORPUSDIPLOMATICUM_CONTRACTS_AREAS)s/$' % c, corpusdiplomaticum.CorpusDiplomaticumContractsAreas.as_view(), name=config.SLUG_CORPUSDIPLOMATICUM_CONTRACTS_AREAS),
    url(r'^%(SLUG_CORPUSDIPLOMATICUM_PERSONS)s/$' % c, corpusdiplomaticum.CorpusDiplomaticumPersons.as_view(), name=config.SLUG_CORPUSDIPLOMATICUM_PERSONS),
    url(r'^%(SLUG_CORPUSDIPLOMATICUM_PLACES)s/$' % c, corpusdiplomaticum.CorpusDiplomaticumPlaces.as_view(), name=config.SLUG_CORPUSDIPLOMATICUM_PLACES),

    url(r'^%(SLUG_DIPLOMATICLETTERS_BROWSE)s/$' % c, views.DiplomaticLettersBrowse(), name=config.SLUG_DIPLOMATICLETTERS_BROWSE),
    url(r'^%(SLUG_DIPLOMATICLETTERS_SEARCH)s/$' % c, views.DiplomaticLettersSearch(), name=config.SLUG_DIPLOMATICLETTERS_SEARCH),
    url(r'^%(SLUG_DIPLOMATICLETTERS_LOCATIONS)s/$' % c, views.DiplomaticLettersLocations(), name=config.SLUG_DIPLOMATICLETTERS_LOCATIONS),
    url(r'^%(SLUG_DIPLOMATICLETTERS_RULERS)s/$' % c, views.DiplomaticLettersRulers(), name=config.SLUG_DIPLOMATICLETTERS_RULERS),

    url(r'^%(SLUG_ARCHIVE_DAILY_JOURNALS)s/$' % config.__dict__, views.CollectionsDailyJournals.as_view(), name=config.SLUG_COLLECTIONS),
    url(r'^%(SLUG_ARCHIVE_GENERALRESOLUTIONS)s/$' % config.__dict__, views.CollectionsResolution.as_view(), name=config.SLUG_ARCHIVE_GENERALRESOLUTIONS),
    url(r'^%(SLUG_APPENDICES_RESOLUTIONS)s/$' % config.__dict__, views.AppendicesResolution.as_view(), name=config.SLUG_APPENDICES_RESOLUTIONS),
    # TODO: refactor: this view seems not be used in production
    url(r'^%(SLUG_COLLECTIONS)s/$' % config.__dict__, views.BookShelveIndex.as_view(), name=config.SLUG_COLLECTIONS),
    # TODO: refactor: this view seems not be used in production
    url(r'^%(SLUG_COLLECTIONS_BESOGNES)s/$' % config.__dict__, views.CollectionsBesognes.as_view(), name=config.SLUG_COLLECTIONS),

    url(r'^book/$', views.Book.as_view(), name='book'),

    url(r'^%(SLUG_NEWS)s/$' % c, views.NewsIndex.as_view(), name='news_index'),
    url(r'^%(SLUG_NEWS)s/(?P<path>.*)/$' % c, views.News.as_view(), name='news'),

    (r'^tinymce/', include('tinymce.urls')),
    (r'^mce_filebrowser/', include('mce_filebrowser.urls')),
    (r'^localeurl/', include('localeurl.urls')),
    (r'^grappelli/', include('grappelli.urls')),

    url(r'^%(SLUG_SEARCH)s/$' % c, views.SiteSearch(), name='search'),

    (r'^selectable/', include('selectable.urls')),

    (r'^json/timeglider_(?P<path>.*).json/$', 'dasa.views.timeglider_json'),

    url(r'^hathitrust_example/$' % c, views.HathiTrust.as_view()),

    url(r'^imageviewer_(?P<language_code>..)/$' % c, views.ImageViewer.as_view()),
    url(r'^image/(?P<image_path>.*)$' % c, views.BareImage.as_view()),
    url(r'^error$' % c, views.ErrorView.as_view()),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )

urlpatterns += patterns('',
    # this line should be last in the urls list - we send all unmatched urls to dasa.views.page
    url(r'^foreword/$', views.Foreword.as_view(), name='foreword'),
    url(r'^(?P<path>.*)/$', views.Page.as_view(), name='basicpage'),
    )

#
# copyright Gerbrandy SRL
# www.gerbrandy.com
# 2013
#


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.conf.urls import patterns
from django.http import HttpResponseRedirect

from sorl.thumbnail.admin import AdminImageMixin

from modeltranslation.admin import TranslationAdmin

from tinymce.widgets import TinyMCE

from mce_filebrowser.admin import MCEFilebrowserAdmin

from utils import fix_date

from django_countries import countries

from guardian.admin import GuardedModelAdmin

from userena.models import UserenaSignup
from userena.utils import get_user_model

from dasa import models
from dasa import config
from models import HartaKarunCategory, HartaKarunItem, Scan, HartaKarunMainCategory


class BasicPageForm(
    forms.ModelForm
    ):
    class Meta:
        model = models.BasicPage

    description_en = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}), required=False)
    description_id = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}), required=False)

    content_en = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}), required=False)
    content_id = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}), required=False)


class BasicPageAdmin(
    MCEFilebrowserAdmin,
    AdminImageMixin,
    TranslationAdmin,
    ):
    """
    Admin class for BasicPage.
    """
    form = BasicPageForm
    list_display = ['title_id', 'title_en', 'slug']
    list_display_links = ['title_id', 'title_en', 'slug']
    search_fields = ['title']

    def get_form(self, request, obj=None, **kwargs):
        form = super(BasicPageAdmin, self).get_form(request, obj=obj, **kwargs)
        if obj and obj.slug in config.SLUGS_IN_USE.values():
            help_text = mark_safe('<span style="font-weight:bold; color: black">PLEASE DO NOT CHANGE THIS SLUG</span> - it\'s value is used by the system')
            form.base_fields['slug'].help_text = help_text

        return form
admin.site.register(models.BasicPage, BasicPageAdmin)


class NewsAdmin(
    AdminImageMixin,
    TranslationAdmin,
    MCEFilebrowserAdmin,
    ):
    list_display = ['date', 'title_id', 'title_en']
    pass
admin.site.register(models.News, NewsAdmin)


class HartaKarunCategoryInline(AdminImageMixin, admin.TabularInline):
    model = HartaKarunCategory
    fields = ['admin_link']
    readonly_fields = fields
    max_num = 0  # remove add link
    can_delete = False


class HartaKarunItemInline(admin.TabularInline):
    model = HartaKarunItem
    fields = ['admin_link']
    readonly_fields = fields
    max_num = 0  # remove add link
    can_delete = False


class HartaKarunMainCategoryAdmin(AdminImageMixin, TranslationAdmin):
    actions = None  # no actions, hides the checkboxes in the list view

    inlines = [HartaKarunCategoryInline]
admin.site.register(HartaKarunMainCategory, HartaKarunMainCategoryAdmin)


class HartaKarunCategoryAdmin(AdminImageMixin, TranslationAdmin):

    actions = None  # no actions, hides the checkboxes in the list view
    list_display = ['name', 'hartakarun_main_category', ]

    inlines = [HartaKarunItemInline]


admin.site.register(HartaKarunCategory, HartaKarunCategoryAdmin)


class HartaKarunScansInlineForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(HartaKarunScansInlineForm, self).__init__(*args, **kwargs)
        self.fields['position'].widget = forms.HiddenInput()

    class Meta:
        model = Scan


class HartaKarunScansInline(AdminImageMixin, admin.TabularInline):

    model = Scan
    fields = ['image', 'position', 'image_caption_en', 'image_caption_id', 'selflink']
    readonly_fields = ['selflink']
    sortable_field_name = "position"
#    max_num = 1 #remove add link
#    can_delete = False
    fk_name = 'hartakarun_item'
    form = HartaKarunScansInlineForm

    class Media:
        css = {
            "all": ("css/dasa_admin.css",)
        }

    def selflink(self, obj):
        if obj.id:
            return '<a href="%s">edit</a>' % reverse('admin:dasa_scan_change', args=[obj.id])
        else:
            return ''
    selflink.allow_tags = True


class HartaKarunItemAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            data = args[0]
        elif 'data' in kwargs:
            data = kwargs['data']
        else:
            data = None
        if data is not None:
            data['date_on_timeline'] = fix_date(data['date_on_timeline'])
        super(HartaKarunItemAdminForm, self).__init__(*args, **kwargs)


class HartaKarunItemAdmin(AdminImageMixin, TranslationAdmin):

    form = HartaKarunItemAdminForm

    actions = None  # no actions, hides the checkboxes in the list view
    list_display = ['list_display_number', 'short_title', 'hartakaruncategory']
    list_display_links = ['list_display_number', 'short_title']
    list_select_related = True  # because we show the hartakaruncategory title, we select all related items to save on db queries

    def list_display_number(self, obj):
        return obj.number

    list_display_number.admin_order_field = 'number'

    inlines = [HartaKarunScansInline]

admin.site.register(HartaKarunItem, HartaKarunItemAdmin)


class ScanAdmin(AdminImageMixin, TranslationAdmin):
    exclude = ['reference', 'institution', 'fonds', 'file_id']

admin.site.register(Scan, ScanAdmin)


class ResolutionAdmin(AdminImageMixin, TranslationAdmin):
    list_display = ['description', 'order', 'subject', 'date']

admin.site.register(models.Resolution, ResolutionAdmin)


class JournalEntryAdmin(AdminImageMixin, TranslationAdmin):
    list_display = ['description', 'date', 'folio_number_from', 'folio_number_to']
#    inlines = [RetroBookScanInline]
admin.site.register(models.JournalEntry, JournalEntryAdmin)


class LightBoxItemAdmin(AdminImageMixin, TranslationAdmin):
    list_display = ['title', 'order']

admin.site.register(models.LightBoxItem, LightBoxItemAdmin)


class UserenaSignupInline(admin.StackedInline):
    model = UserenaSignup
    max_num = 1


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile

    country = forms.ChoiceField(choices=[('', '')] + list(countries.COUNTRIES))


class UserProfileInline(admin.StackedInline):
    model = models.UserProfile
    max_num = 1
    fields = ['country']
    form = UserProfileForm


class UserenaAdmin(UserAdmin, GuardedModelAdmin):
    inlines = [UserProfileInline, UserenaSignupInline, ]
    list_display = ('username',
                    'email',
                    'first_name', 'last_name',
                    'country',
                    'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active')

    countries = dict(countries.COUNTRIES)

    def __init__(self, *args, **kwargs):
        super(UserenaAdmin, self).__init__(*args, **kwargs)
#         self.fieldsets[1][1]['fields'] = list(self.fieldsets[1][1]['fields']) + ['country']

    def country(self, obj):
        country_code = obj.userprofile.country
        if country_code:
            return unicode(self.countries.get(country_code, ''))
        else:
            return ''
try:
    admin.site.unregister(get_user_model())
except admin.sites.NotRegistered:
    pass

admin.site.register(get_user_model(), UserenaAdmin)


class MenuAdmin(admin.ModelAdmin):
    list_display = [
        'caption_with_spacer',
        'move_down_link',
        'move_up_link',
    ]
    actions = None
    exclude = ['order', 'position', 'level', 'function_call']

    def get_form(self, request, obj=None, **kwargs):
        # get base form object
        form = super(MenuAdmin, self).get_form(request, obj, **kwargs)

        # remove the "+" signs
        form.base_fields['parent'].widget.can_add_related = False
        form.base_fields['page'].widget.can_add_related = False
        return form

    def move_down_link(self, instance):
        return mark_safe('<a href="./move_down?id={instance.id}">move down</a>'.format(**locals()))
    move_down_link.short_description = 'move down'

    def move_up_link(self, instance):
        return mark_safe('<a href="./move_up?id={instance.id}">move up</a>'.format(**locals()))
    move_up_link.short_description = 'move up'

    def get_urls(self):
        urls = super(MenuAdmin, self).get_urls()
        my_urls = patterns('',
               (r'^move_up/$', self.admin_site.admin_view(self.move_up_item)),
               (r'^move_down/$', self.admin_site.admin_view(self.move_down_item)),
            )

        return my_urls + urls

    def move_up_item(self, request):
        menuitem_id = request.REQUEST.get('id')
        menuitem = models.MenuItem.objects.get(id=menuitem_id)
        menuitem.move_menuitem(-1)
        return HttpResponseRedirect('../')

    def move_down_item(self, request):
        menuitem_id = request.REQUEST.get('id')
        menuitem = models.MenuItem.objects.get(id=menuitem_id)
        menuitem.move_menuitem(+1)
        return HttpResponseRedirect('../')


admin.site.register(models.MenuItem, MenuAdmin)


class MetaTagsAdmin(TranslationAdmin):
    list_display = [
        'object_type',
        'keywords_id',
        'description_id',
        'keywords_en',
        'description_en',
    ]
    actions = None

admin.site.register(models.MetaTags, MetaTagsAdmin)

admin.site.register(models.DiplomaticLetter)
admin.site.register(models.DiplomaticLetterRuler)
admin.site.register(models.DiplomaticLetterLocation)
admin.site.register(models.DeHaan)
admin.site.register(models.Placard)
admin.site.register(models.Appendix)

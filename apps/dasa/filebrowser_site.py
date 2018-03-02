import os

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render_to_response, HttpResponse
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext as Context
from django import forms

from filebrowser.sites import get_breadcrumbs
from filebrowser.sites import get_settings_var
from filebrowser.sites import storage
from filebrowser.sites import FileBrowserSite
from filebrowser.templatetags.fb_tags import query_helper
from filebrowser.actions import flip_horizontal
from filebrowser.actions import flip_vertical
from filebrowser.actions import rotate_90_clockwise
from filebrowser.actions import rotate_90_counterclockwise
from filebrowser.actions import rotate_180
from filebrowser.base import FileObject
from filebrowser import signals

from dasa import models


class FileBrowserSite(FileBrowserSite):
    #
    # function class was copied verbatim from filebrowser.sites - we only added 'used_by' to the context
    #
    def detail(self, request):
        """
        Show detail page for a file.

        Rename existing File/Directory (deletes existing Image Versions/Thumbnails).
        """
        from filebrowser.forms import ChangeForm
        query = request.GET
        path = u'%s' % os.path.join(self.directory, query.get('dir', ''))
        fileobject = FileObject(os.path.join(path, query.get('filename', '')), site=self)

        if request.method == 'POST':
            form = ChangeForm(request.POST, path=path, fileobject=fileobject, filebrowser_site=self)
            if form.is_valid():
                new_name = form.cleaned_data['name']
                action_name = form.cleaned_data['custom_action']
                try:
                    action_response = None
                    if action_name:
                        action = self.get_action(action_name)
                        # Pre-action signal
                        signals.filebrowser_actions_pre_apply.send(sender=request, action_name=action_name, fileobject=[fileobject], site=self)
                        # Call the action to action
                        action_response = action(request=request, fileobjects=[fileobject])
                        # Post-action signal
                        signals.filebrowser_actions_post_apply.send(sender=request, action_name=action_name, fileobject=[fileobject], result=action_response, site=self)
                    if new_name != fileobject.filename:
                        signals.filebrowser_pre_rename.send(sender=request, path=fileobject.path, name=fileobject.filename, new_name=new_name, site=self)
                        fileobject.delete_versions()
                        self.storage.move(fileobject.path, os.path.join(fileobject.head, new_name))
                        signals.filebrowser_post_rename.send(sender=request, path=fileobject.path, name=fileobject.filename, new_name=new_name, site=self)
                        messages.add_message(request, messages.SUCCESS, ('Renaming was successful.'))
                    if isinstance(action_response, HttpResponse):
                        return action_response
                    if "_continue" in request.POST:
                        redirect_url = reverse("filebrowser:fb_detail", current_app=self.name) + query_helper(query, "filename=" + new_name, "filename")
                    else:
                        redirect_url = reverse("filebrowser:fb_browse", current_app=self.name) + query_helper(query, "", "filename")
                    return HttpResponseRedirect(redirect_url)
                except OSError, (_errno, _strerror):
                    form.errors['name'] = forms.util.ErrorList([('Error.')])
        else:
            form = ChangeForm(initial={"name": fileobject.filename}, path=path, fileobject=fileobject, filebrowser_site=self)

        return render_to_response('filebrowser/detail.html', {
            'form': form,
            'fileobject': fileobject,
            'query': query,
            'title': u'%s' % fileobject.filename,
            'settings_var': get_settings_var(directory=self.directory),
            'breadcrumbs': get_breadcrumbs(query, query.get('dir', '')),
            'breadcrumbs_title': u'%s' % fileobject.filename,
            'filebrowser_site': self,
            'used_by': self.fileobject_is_used_by(fileobject)
        }, context_instance=Context(request, current_app=self.name))

    def fileobject_is_used_by(self, fileobject):
        if fileobject.filetype == 'Folder':
            return []
        filename = fileobject.name
        used_by = []
        for classname, attr_names in settings.IMAGE_FIELDS:
            for attr_name in attr_names:
                used_by += eval(classname).objects.filter(**{attr_name: filename}).all()
        # the image can also be used by one of the text fields
        for classname, attr_names in settings.TEXT_FIELDS:
            for attr_name in attr_names:
                used_by += eval(classname).objects.filter(**{attr_name + '__icontains': filename}).all()

        return used_by


site = FileBrowserSite(name='filebrowser', storage=storage)

# Default actions
site.add_action(flip_horizontal)
site.add_action(flip_vertical)
site.add_action(rotate_90_clockwise)
site.add_action(rotate_90_counterclockwise)
site.add_action(rotate_180)

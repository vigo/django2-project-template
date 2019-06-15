import logging

from django.contrib import admin
from django.contrib.admin import helpers
from django.contrib.admin.utils import model_ngettext
from django.core.exceptions import PermissionDenied
from django.db import models
from django.forms import TextInput
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _

from ..utils import console
from ..widgets import AdminImageFileWidget

__all__ = ['CustomBaseModelAdmin', 'CustomBaseModelAdminWithSoftDelete']

console = console(source=__name__)
logger = logging.getLogger('app')


class CustomBaseModelAdmin(admin.ModelAdmin):
    """

    Base admin for BaseModel

    """

    sticky_list_filter = ('status',)

    formfield_overrides = {
        models.ImageField: {'widget': AdminImageFileWidget},
        models.CharField: {'widget': TextInput(attrs={'size': 100})},
    }

    def get_list_filter(self, request):
        list_filter = list(super().get_list_filter(request))
        if self.sticky_list_filter:
            list_filter = list(self.sticky_list_filter) + list(list_filter)
        return list_filter


def recover_selected(modeladmin, request, queryset):
    number_of_rows_recovered, __ = queryset.undelete()  # __ = recovered_items
    if number_of_rows_recovered == 1:
        message_bit = _('1 record was')
    else:
        message_bit = _('%(number_of_rows)s records were') % dict(number_of_rows=number_of_rows_recovered)
    message = _('%(message_bit)s successfully marked as active') % dict(message_bit=message_bit)
    modeladmin.message_user(request, message)


def hard_delete_selected(modeladmin, request, queryset):
    opts = modeladmin.model._meta  # # pylint: disable=W0212

    deletable_objects, model_count, perms_needed, protected = modeladmin.get_deleted_objects(queryset, request)

    if request.POST.get('post') and not protected:
        if perms_needed:
            raise PermissionDenied
        if queryset.count():
            number_of_rows_deleted, __ = queryset.hard_delete()  # __ = deleted_items
            if number_of_rows_deleted == 1:
                message_bit = _('1 record was')
            else:
                message_bit = _('%(number_of_rows)s records were') % dict(number_of_rows=number_of_rows_deleted)
            message = _('%(message_bit)s deleted') % dict(message_bit=message_bit)
            modeladmin.message_user(request, message)
        return None

    objects_name = model_ngettext(queryset)
    if perms_needed or protected:
        title = _('Cannot delete %(name)s') % {'name': objects_name}
    else:
        title = _('Are you sure?')

    context = {
        **modeladmin.admin_site.each_context(request),
        'title': title,
        'objects_name': str(objects_name),
        'deletable_objects': [deletable_objects],
        'model_count': dict(model_count).items(),
        'queryset': queryset,
        'perms_lacking': perms_needed,
        'protected': protected,
        'opts': opts,
        'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
        'media': modeladmin.media,
    }

    request.current_app = modeladmin.admin_site.name

    return TemplateResponse(request, 'admin/hard_delete_selected_confirmation.html', context)


class CustomBaseModelAdminWithSoftDelete(CustomBaseModelAdmin):

    hide_deleted_at = True

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.GET:
            return queryset
        return queryset.all()

    def get_exclude(self, request, obj=None):
        excluded = super().get_exclude(request, obj=obj)
        exclude = [] if excluded is None else list(excluded)
        if self.hide_deleted_at:
            exclude.append('deleted_at')
        return exclude

    def get_actions(self, request):
        existing_actions = super().get_actions(request)
        existing_actions.update(
            dict(
                recover_selected=(recover_selected, 'recover_selected', _('Recover selected %(verbose_name_plural)s'))
            )
        )
        existing_actions.update(
            dict(
                hard_delete_selected=(
                    hard_delete_selected,
                    'hard_delete_selected',
                    _('Hard delete selected %(verbose_name_plural)s'),
                )
            )
        )
        return existing_actions

from django.contrib import admin
from django.contrib.admin import helpers
from django.contrib.admin.utils import model_ngettext
from django.core.exceptions import PermissionDenied
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _

from ..models import BaseModel
from ..utils import console, numerify

__all__ = ['BaseAdmin', 'BaseAdminWithSoftDelete']

console = console(source=__name__)


class BaseAdmin(admin.ModelAdmin):

    sticky_list_filter = ('status',)

    def get_list_filter(self, request):
        list_filter = list(super().get_list_filter(request))
        if self.sticky_list_filter:
            list_filter = list(self.sticky_list_filter) + list(list_filter)
        return list_filter


def recover_selected(modeladmin, request, queryset):
    number_of_rows_recovered, recovered_items = queryset.undelete()
    if number_of_rows_recovered == 1:
        message_bit = _('1 record was')
    else:
        message_bit = _('%(number_of_rows)s records were') % dict(
            number_of_rows=number_of_rows_recovered
        )
    message = _('%(message_bit)s successfully marked as active') % dict(
        message_bit=message_bit
    )
    modeladmin.message_user(request, message)
    return None


def hard_delete_selected(modeladmin, request, queryset):
    opts = modeladmin.model._meta

    deletable_objects, model_count, perms_needed, protected = modeladmin.get_deleted_objects(
        queryset, request
    )

    if request.POST.get('post') and not protected:
        if perms_needed:
            raise PermissionDenied
        n = queryset.count()
        if n:
            number_of_rows_deleted, deleted_items = queryset.hard_delete()
            if number_of_rows_deleted == 1:
                message_bit = _('1 record was')
            else:
                message_bit = _('%(number_of_rows)s records were') % dict(
                    number_of_rows=number_of_rows_deleted
                )
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

    return TemplateResponse(
        request, 'admin/hard_delete_selected_confirmation.html', context
    )


class BaseAdminWithSoftDelete(BaseAdmin):

    hide_deleted_at = True

    def get_queryset(self, request):
        qs = self.model.objects.get_queryset()
        if request.GET.get('status__exact', None):
            if numerify(request.GET.get('status__exact')) == BaseModel.STATUS_DELETED:
                return qs.deleted()
        return qs.all()

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
                recover_selected=(
                    recover_selected,
                    'recover_selected',
                    _('Recover selected %(verbose_name_plural)s'),
                )
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

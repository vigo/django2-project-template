from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from ..utils import numerify
from ..models import BaseModel


__all__ = [
    'BaseAdmin',
    'BaseAdminWithSoftDelete',
]


class BaseAdmin(admin.ModelAdmin):
    sticky_list_filter = ('status',)

    def get_list_filter(self, request):
        list_filter = list(super().get_list_filter(request))
        if self.sticky_list_filter:
            list_filter = list(self.sticky_list_filter) + list(list_filter)
        return list_filter


def recover_deleted(modeladmin, request, queryset):
    number_of_rows_recovered, recovered_items = queryset.undelete()
    if number_of_rows_recovered == 1:
        message_bit = _('1 record was')
    else:
        message_bit = _('%(number_of_rows)s records were') % dict(number_of_rows=number_of_rows_recovered)
    message = _('%(message_bit)s successfully marked as active') % dict(message_bit=message_bit)
    modeladmin.message_user(request, message)
    return None


class BaseAdminWithSoftDelete(BaseAdmin):
    hide_deleted_at = True

    def get_queryset(self, request):
        qs = self.model.objects_bm.get_queryset()
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
        existing_actions.update(dict(
            recover_deleted=(
                recover_deleted,
                'recover_deleted',
                _('Recover selected %(verbose_name_plural)s'),
            )
        ))
        return existing_actions

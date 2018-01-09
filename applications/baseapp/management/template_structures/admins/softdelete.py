TEMPLATE_ADMIN_SOFTDELETEMODEL = """from django.contrib import admin

from baseapp.admin import BaseAdminWithSoftDelete

from ..models import {model_name}


__all__ = [
    '{model_name}',
]


class {model_name}Admin(BaseAdminWithSoftDelete):
    # sticky_list_filter = None
    # hide_deleted_at = False
    pass


admin.site.register({model_name}, {model_name}Admin)

"""


__all__ = [
    'TEMPLATE_ADMIN_SOFTDELETEMODEL',
]
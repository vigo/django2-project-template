TEMPLATE_ADMIN_BASEMODEL = """from django.contrib import admin

from baseapp.admin import BaseAdmin

from ..models import {model_name}


__all__ = [
    '{model_name}Admin',
]


@admin.register({model_name})
class {model_name}Admin(BaseAdmin):
    # sticky_list_filter = None
    pass

"""


__all__ = ['TEMPLATE_ADMIN_BASEMODEL']

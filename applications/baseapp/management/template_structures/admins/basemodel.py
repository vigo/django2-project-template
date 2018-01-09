TEMPLATE_ADMIN_BASEMODEL = """from django.contrib import admin

from baseapp.admin import BaseAdmin

from ..models import {model_name}


__all__ = [
    '{model_name}',
]


class {model_name}Admin(BaseAdmin):
    # sticky_list_filter = None
    pass


admin.site.register({model_name}, {model_name}Admin)

"""


__all__ = [
    'TEMPLATE_ADMIN_BASEMODEL',
]

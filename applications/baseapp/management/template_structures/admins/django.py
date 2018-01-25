TEMPLATE_ADMIN_DJANGO = """from django.contrib import admin

from ..models import {model_name}


__all__ = [
    '{model_name}Admin',
]


class {model_name}Admin(admin.ModelAdmin):
    pass


admin.site.register({model_name}, {model_name}Admin)

"""


__all__ = [
    'TEMPLATE_ADMIN_DJANGO',
]

TEMPLATE_ADMIN_DJANGO = """from django.contrib import admin

from ..models import {model_name}


__all__ = [
    '{model_name}Admin',
]


@admin.register({model_name})
class {model_name}Admin(admin.ModelAdmin):
    pass

"""


__all__ = ['TEMPLATE_ADMIN_DJANGO']

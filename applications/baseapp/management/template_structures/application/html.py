"""
HTML template for app generator
"""

TEMPLATE_HTML = """{{% extends "base.html" %}}
{{% load static i18n %}}

{{% block title %}}{app_name_title} Application{{% endblock %}}

{{% block body %}}
<section class="section">
    <div class="container">
        <h1 class="title">Hello from {app_name_title}</h1>
    </div>
</section>
{{% endblock %}}

"""


__all__ = ['TEMPLATE_HTML']

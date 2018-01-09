TEMPLATE_HTML = """{{% extends "baseapp/base.html" %}}
{{% load static %}}
{{% load i18n %}}

{{% block page_title %}}{app_name_title} Application{{% endblock %}}

{{% block page_body %}}
<div class="container">
    <div class="row">
        <div class="twelve columns">
            <h1>Hello from {app_name_title}</h1>

            {{% hdbg %}}
        </div>
    </div>

</div>
{{% endblock %}}

"""


__all__ = [
    'TEMPLATE_HTML',
]
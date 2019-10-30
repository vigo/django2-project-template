[![Build Status](https://travis-ci.org/vigo/django2-project-template.svg?branch=master)](https://travis-ci.org/vigo/django2-project-template)
![Python](https://img.shields.io/badge/python-3.7.4-green.svg)
![Django](https://img.shields.io/badge/django-2.2.6-green.svg)
![Version](https://img.shields.io/badge/version-3.5.1-yellow.svg)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/c73fb40b38f5455abd34d496bbc52b9b)](https://www.codacy.com/app/vigo/django2-project-template?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=vigo/django2-project-template&amp;utm_campaign=Badge_Grade)

# Django Project Starter Template

My custom project starter for Django! I’ll try to support every upcoming
Django releases as much as I can!

## Requirements

- Latest `Python 3.7.4` runtime environment.
- `PostgreSQL`
- `pip`, `virtualenv`, `virtualenvwrapper`
- If you like to run Rake Tasks, you need `Ruby` too...

## Installation

macOS user can install `PostgreSQL` from [Homebrew](https://brew.sh):

```bash
$ brew install postgres  # if you need to
```

Don’t forget to start your database server before continue. Now create your
database:

```bash
$ createdb -E UTF8 -T template0 my_project_dev

# or createdb with locale
$ createdb -E UTF8 -T template0 --lc-collate=tr_TR.UTF-8 --lc-ctype=tr_TR.UTF-8 my_project_dev

# or postgres from docker
$ PGPASSWORD=YOUR-POSTGRES-PASSWORD createdb -h localhost -U postgres -E UTF8 -T template0 my_project_dev

# grant privileges
$ PGPASSWORD=YOUR-POSTGRES-PASSWORD psql -h localhost -U postgres -d my_project_dev -c "GRANT ALL PRIVILEGES ON DATABASE my_project_dev TO postgres;"

# check
$ PGPASSWORD=YOUR-POSTGRES-PASSWORD psql -h localhost -U postgres -l
```

Please use `virtualenvwrapper` and create your environment and activate it.
With Python 3.3+, you don’t need to install `virtualenv`. You can create your
environment via; `python -m venv /path/to/your/environment`

```bash
# example
$ mkvirtualenv my_projects_env

# or make it active:
$ workon my_projects_env
```

You need to declare `DATABASE_URL` for postgres connection and `DJANGO_SECRET`
for settings. I always put my project specific environment variables under
`virtualenvwrapper`’s `postactivate` file. Open your
`~/.virtualenvs/my_projects_env/bin/postactivate` and add (*or set it
manually*):

```bash
# docker/postgres usage;
export DATABASE_URL="postgres://postgres:YOUR-POSTGRES-PASSWORD@localhost:5432/my_project_dev"

# or for osx/homebrew postgres usage;
export DATABASE_URL="postgres://localhost:5432/my_project_dev"
export DJANGO_SECRET=$(head -c 75 /dev/random | base64 | tr -dc 'a-zA-Z0-9' | head -c 50)
```

By default, `DJANGO_ENV` environment variable is set to `development` via
`manage.py`. For production usage, `DJANGO_ENV` environment variable is set to
`production` via `wsgi.py`. This means, if you don’t set `DJANGO_ENV` variable,
app sets it for you. 

Now trigger `workon my_projects_env`, this reloads environment variables.
then;

```bash
# for django X.Y.Z
# check https://github.com/vigo/django2-project-template/releases

$ curl -L https://github.com/vigo/django2-project-template/archive/django-X.Y.Z.zip > template.zip
$ unzip template.zip
$ mv django2-project-template-django-X.Y.Z my_project && rm template.zip
$ cd my_project/
$ cp config/settings/development.example.py config/settings/development.py
$ cp config/settings/test.example.py config/settings/test.py
# development.py is not under revison control
# test.py is not under revison control
$ pip install -r requirements/development.pip
$ git init # now you can start your own repo!
```

or, you can use installer script:

```bash
$ bash <(curl -fsSL https://raw.githubusercontent.com/vigo/django2-project-template/master/install.sh)
$ cd YOUR_PROJECT/
$ pip install -r requirements/development.pip
$ git init # now you can start your own repo!
```

This template comes with custom **User** model. Please take a look at it. If you
need to add/change fields, please do so. Default app language is set to `en-us` and
timezone is set to `UTC`. I use:

```python
# config/settings/base.py

LANGUAGE_CODE = 'tr'
TIME_ZONE = 'Europe/Istanbul'
```

If you change anything, please run `makemigrations` to keep track of your db.
Then continue to work:

```bash
$ python manage.py migrate
$ python manage.py createsuperuser

# enter: Email, First Name, Last Name and password
$ python manage.py runserver_plus # or
$ rake
```

You can fix your Django Admin titles now. Go to `config/urls.py` and fix:

```python
admin.site.index_title = _('Your admin index title')
admin.site.site_title = _('Your site title')
admin.site.site_header = _('Your site header')
```

Do not forget to compile your locale messages files.

---

## Features

- Custom `User` Model
- Custom `BaseModel`
- Custom `BaseModelWithSoftDelete`
- Custom manager for `BaseModel` and `BaseModelWithSoftDelete`
- Better Django Application structure! (*imho*)
- Settings abstraction: Development / Production / Heroku / Test
- Requirements abstraction depending on your environment!
- Custom logger and log formatters for development server
- Basic logging configuration for production server
- App and Model creator management commands
- Custom Locale middleware
- Debug Mixin for your HTML templates
- Handy utils: `console`, `console.dir()`, `numerify`, `save_file`
- File widget for Django Admin: `AdminImageFileWidget`
- Easy naming for your admin site!
- `DJANGO_ENV` indicator for your admin site!
- Custom and configurable error pages: `400`, `403`, `404`, `500`
- `OverwriteStorage` for overwriting file uploads
- Custom file storage for missing files for development environment: `FileNotFoundFileSystemStorage`
- Report errors to Slack: `SlackExceptionHandler`

---

## Quick Start

Let’s create `blog` application. We’ll have two models. `Post` and `Category`.
First, create application:

```bash
$ python manage.py create_app blog

# or

$ rake new:application[blog]

"blog" application created.

    - Do not forget to add your `blog` to `INSTALLED_APPS` under `config/settings/base.py`:

    INSTALLED_APPS += [
        'blog.apps.BlogConfig',
    ]

    - Do not forget to fix your `config/urls.py`:
    
    # ...
    urlpatterns = [
        # ...
        # this is just an example!
        path('__blog__/', include('blog.urls', namespace='blog')),
        # ..
    ]
    # ...
```

Fix your `config/settings/base.py`, add this newly created app to your `INSTALLED_APPS`:

```python
# config/settings/base.py
:
:
AUTH_USER_MODEL = 'baseapp.User'

INSTALLED_APPS += [
    'blog.apps.BlogConfig',
]
```

Now, if you fix your `config/urls.py` you’ll be able to see demo
pages for your app:

```python
# config/urls.py
:
:
urlpatterns = [
    # ...
    path('__blog__/', include('blog.urls', namespace='blog')),
    # ..
]
```

Now run server and call `http://127.0.0.1:8000/__blog__/`:

```bash
$ python manage.py runserver

# or

$ rake
```

You’ll see `Hello from Blog` page and If you check `blog/views/index.py` you’ll see
and example usage of `HtmlDebugMixin` and `console` util. 

```python
import logging

from django.views.generic.base import TemplateView

from baseapp.mixins import HtmlDebugMixin
from baseapp.utils import console

__all__ = ['BlogView']

logger = logging.getLogger('app')
console = console(source=__name__)


class BlogView(HtmlDebugMixin, TemplateView):
    template_name = 'blog/index.html'

    def get_context_data(self, **kwargs):
        self.hdbg('Hello from hdbg')
        kwargs = super().get_context_data(**kwargs)
        console.dir(self.request.user)
        return kwargs
```

Let’s look at our `blog` application structure:

```bash
    applications/blog/
    ├── admin
    │   └── __init__.py
    ├── migrations
    │   └── __init__.py
    ├── models
    │   └── __init__.py
    ├── tests
    │   ├── __init__.py
    │   └── index.py
    ├── views
    │   ├── __init__.py
    │   └── index.py
    ├── __init__.py
    ├── apps.py
    └── urls.py
```

Now lets add `Post` model with **soft-delete** feature!

```bash
$ python manage.py create_model blog Post softdelete

# or

$ rake new:model[blog,Post,softdelete]

models/post.py created.
admin/post.py created.
Post model added to models/__init__.py
Post model added to admin/__init__.py


    `Post` related files created successfully:

    - `blog/models/post.py`
    - `blog/admin/post.py`

    Please check your models before running `makemigrations` ok?
```

This creates `blog/models/post.py` and `blog/admin/post.py` files:

```python
# blog/models/post.py

import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _

from baseapp.models import BaseModelWithSoftDelete
from baseapp.utils import console

__all__ = ['Post']

logger = logging.getLogger('app')
console = console(source=__name__)


class Post(BaseModelWithSoftDelete):
    title = models.CharField(max_length=255, verbose_name=_('title'))

    class Meta:
        app_label = 'blog'
        verbose_name = _('post')
        verbose_name_plural = _('posts')
    
    def __str__(self):
        return self.title
```

and `Category` model:

```bash
$ python manage.py create_model blog Category softdelete

# or

$ rake new:model[blog,Category,softdelete]

models/category.py created.
admin/category.py created.
Category model added to models/__init__.py
Category model added to admin/__init__.py


    `Category` related files created successfully:

    - `blog/models/category.py`
    - `blog/admin/category.py`

    Please check your models before running `makemigrations` ok?
```

Now It’s time to fix our models by hand!

```python
# blog/models/post.py

import logging

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from baseapp.models import BaseModelWithSoftDelete
from baseapp.utils import console

__all__ = ['Post']

logger = logging.getLogger('app')
console = console(source=__name__)


class Post(BaseModelWithSoftDelete):
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name=_('author'),
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name=_('category'),
    )
    title = models.CharField(max_length=255, verbose_name=_('title'))
    body = models.TextField(verbose_name=_('body'))

    class Meta:
        app_label = 'blog'
        verbose_name = _('post')
        verbose_name_plural = _('posts')  # check pluralization

    def __str__(self):
        return self.title
```

We’ll keep `blog/models/category.py` same, `Category` will have only `title`
field:

```python
# blog/models/category.py

import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _

from baseapp.models import BaseModelWithSoftDelete
from baseapp.utils import console

__all__ = ['Category']

logger = logging.getLogger('app')
console = console(source=__name__)


class Category(BaseModelWithSoftDelete):
    title = models.CharField(max_length=255, verbose_name=_('title'))

    class Meta:
        app_label = 'blog'
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.title
```


Now It’s time to create migrations:

```bash
$ python manage.py makemigrations --name create_post_and_category

# or

$ rake db:update[blog,create_post_and_category]

Migrations for 'blog':
  applications/blog/migrations/0001_create_post_and_category.py
    - Create model Category
    - Create model Post
```

Now migrate!

```bash
$ python manage.py migrate

# or

$ rake db:migrate

Operations to perform:
  Apply all migrations: admin, auth, baseapp, blog, contenttypes, sessions
Running migrations:
  Applying blog.0001_create_post_and_category... OK
```

Now time to run server and dive in to admin page!

```bash
$ python manage.py runserver

# or

$ rake

Performing system checks...

System check identified no issues (0 silenced).
XXXXXX YY, ZZZZ - AA:BB:CC
Django version X.Y.Z, using settings 'config.settings.development'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

Open `http://127.0.0.1:8000/admin/` and use your superuser credentials.

---

## Project File/Folder Structure

What I’ve changed ?

- All Django apps live under `applications/` folder.
- All of the models live under generated app’s `models/` folder.
- All of the views live under generated app’s `views/` folder.
- All of the tests live under generated app’s `tests/` folder.
- All of the admin files live under generated app’s `admin/` folder.
- Every app should contain It’s own `urls.py`.
- All settings related files will live under `config/settings/` folder.
- Every environment has It’s own setting such as `config/settings/development.py`.
- Every environment/settings can have It’s own package/module requirements.
- All of the templates live under basedir’s `templates/APP_NAME` folder.
- All of the locales live under basedir’s `locale/LANG/...` folder.
- Lastly, Ruby and Python can be friends in a Django Project!

Here is directory/file structure:

```bash
.
├── applications
│   └── baseapp
├── config
│   ├── settings
│   ├── __init__.py
│   ├── urls.py
│   └── wsgi.py
├── db
├── locale
│   └── tr
├── requirements
│   ├── base.pip
│   ├── development.pip
│   └── heroku.pip
├── static
│   └── css
├── templates
│   ├── admin
│   ├── baseapp
│   └── base.html
├── Procfile
├── Rakefile
├── manage.py
├── requirements.txt
└── runtime.txt
```

---

## Settings and Requirements Abstraction

By default, `manage.py` looks for `DJANGO_ENV` environment variable. Builds 
`DJANGO_SETTINGS_MODULE` environment variable according to `DJANGO_ENV` variable.
If your `DJANGO_ENV` environment variable is set to `production`, this means that
you are running `config/settings/production.py`.

Also `config/wsgi.py` looks for `DJANGO_ENV` environment variable too. For
example, If you want to deploy this application to **HEROKU**, you need
`config/settings/heroku.py` and must add config variable `DJANGO_ENV` and set
it to `heroku` on HEROKU site. (*You’ll find more information further below*)

All the other settings files (*according to environment*) imports
`config/settings/base.py` and gets everything from it. `development.py` is
un-tracked/git-ignored file. Original file is `development.example.py`. You
need to create a copy of it! (*if you follow along from the beginning, you’ve already did this*)

All the base/common required Python packages/modules are defined under `requirements/base.pip`:

```bash
Django==2.2.6
Pillow==6.2.1
django-extensions==2.2.5
python-slugify==4.0.0
psycopg2-binary==2.8.4
dj-database-url==0.5.0
```

### `base.py`

This is the main settings file. All other settings will extend this one. By
default, we have [Django Extensions][01] installed as 3^rd party app.

Available installed apps are:

```python
# base apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'baseapp.apps.BaseappConfig',  # our helper app
]
```

Extras are:

```python
# add your newly created apps here!
INSTALLED_APPS += [
    'django_extensions',
]
```

Django Extension adds great functionalities:

```bash
admin_generator
clean_pyc
clear_cache
compile_pyc
create_command
create_jobs
create_template_tags
delete_squashed_migrations
describe_form
drop_test_database
dumpscript
export_emails
find_template
generate_password
generate_secret_key
graph_models
mail_debug
merge_model_instances
notes
passwd
pipchecker
print_settings
print_user_for_session
reset_db
reset_schema
runjob
runjobs
runprofileserver
runscript
runserver_plus
set_default_site
set_fake_emails
set_fake_passwords
shell_plus
show_template_tags
show_templatetags
show_urls
sqlcreate
sqldiff
sqldsn
sync_s3
syncdata
unreferenced_files
update_permissions
validate_templates
```

One of my favorite: `python manage.py show_urls` :)

### `development.py`

Logging is enabled only in development mode. Our development server
uses [Werkzeug][03] and we have special filter which is defined in `LOGGIN_SKIP_THESE_EXTENSIONS`.
You can skip displaying specified extensions from development server logs.

You can un-comment `django.db.backends` if you want to see the SQL queries.
Example:

```python
LOGGING = {
    :
    :
    'loggers': {
        'app': {'handlers': ['console'], 'level': 'DEBUG'},
        'werkzeug': {'handlers': ['console'], 'level': 'DEBUG', 'propagate': True},
        'django.db.backends': {'handlers': ['console_sql'], 'level': 'DEBUG'},  # un-comment
    },
}
```

By default, this template ships with [Django Debug Toolbar][02] in development
mode.

`AUTH_PASSWORD_VALIDATORS` are removed for development purposes. You can enter
simple passwords such as `1234`. `MEDIA_ROOT` is set to basedir’s `media` folder,
`STATICFILES_DIRS` includes basedir’s `static` folder.

All the required modules are defined under `requirements/development.pip`:

```bash
-r base.pip
ipython==7.9.0
bpython==0.18
ptpython==2.0.6
Werkzeug==0.16.0
django-debug-toolbar==2.0
coverage==4.5.4
isort==4.3.21
black==19.10b0
flake8==3.7.9
flake8-bandit==2.1.2
flake8-blind-except==0.1.1
flake8-bugbear==19.8.0
flake8-builtins==1.4.1
flake8-polyfill==1.0.2
flake8-print==3.1.1
flake8-quotes==2.1.0
flake8-string-format==0.2.3
pylint==2.4.3
```

### `test.example.py`

Basic settings for running tests. 

### `heroku.py`

You can deploy your app to HEROKU super easy. Just set your `ALLOWED_HOSTS`.
Add your heroku domain here:

```python
ALLOWED_HOSTS = [
    'lit-eyrie-63238.herokuapp.com',  # example heroku domain
]
```

All the required modules are defined under `requirements/heroku.pip`:

```bash
-r base.pip
gunicorn==19.9.0
whitenoise==4.1.4
```

By default, Heroku requires `requirements.txt`. Therefore we have it too :)

```python
-r requirements/heroku.pip
```

Heroku also requires `Procfile` and `runtime.txt`. Both provided in the basedir.
Don’t forget to create heroku config variables:

```bash
$ heroku login
$ heroku apps:create
$ heroku addons:create heroku-postgresql:hobby-dev
$ heroku config:set DJANGO_ENV="heroku"
$ heroku config:set DJANGO_SECRET='YOUR_GENERATED_RANDOM_SECRET'
$ heroku config:set WEB_CONCURRENCY=3
$ git push heroku master
$ heroku run python manage.py migrate
$ heroku run python manage.py createsuperuser
```

### Others

If you are using different platform or OS, such as Ubuntu or your custom
servers, you can follow the settings and requirements conventions. If you name
it `production`, create your `config/settings/production.py` and
`requirements/production.pip`. 

You need to set these environment variables in to your production server
environment:

- `DJANGO_ENV` to `production`
- `DATABASE_URL` to your PostgreSQL’s url
- `DJANGO_SECRET` to more securly generated secret.

---

## `User` model

This is custom model which uses `AbstractBaseUser` and `PermissionsMixin`.
Fields are:

- `created_at`
- `updated_at`
- `email`
- `first_name`
- `middle_name` (optional)
- `last_name`
- `avatar` (optional)
- `is_active`
- `is_staff`
- `is_superuser`

Username field is set to: `email`. Your users will login using their email’s
and password’s by default. You can modify everything if you like to. This also
mimics like default User model of Django. Available methods are:

- `get_short_name`
- `get_full_name`

---

## `BaseModel`

This is a common model. By default, `BaseModel` contains these fields:

- `created_at`
- `updated_at`
- `status`

We are overriding the default manager. `BaseModel` uses `BaseModelQuerySet` as
manager, `BaseModelWithSoftDelete` uses `BaseModelWithSoftDeleteManager`.
There are 4 basic status types:

```python
STATUS_OFFLINE = 0
STATUS_ONLINE = 1
STATUS_DELETED = 2
STATUS_DRAFT = 3
```

You can make these queries:

```python
>>> Post.objects.deleted()  # filters: status = STATUS_DELETED
>>> Post.objects.actives()  # filters: status = STATUS_ONLINE
>>> Post.objects.offlines() # filters: status = STATUS_OFFLINE
>>> Post.objects.drafts()   # filters: status = STATUS_DRAFT
```

## `BaseModelWithSoftDelete`

This model inherits from `BaseModel` and provides fake deletion which is
probably called **SOFT DELETE**. This means, when you call model’s `delete()`
method or QuerySet’s `delete()` method, it acts like delete action but never
deletes the data.

Just sets the status field to `STATUS_DELETED` and sets `deleted_at` field to
**NOW**.

This works exactly like Django’s `delete()`. Broadcasts `pre_delete` and
`post_delete` signals and returns the number of objects marked as deleted and
a dictionary with the number of deletion-marks per object type.

You can call `hard_delete()` method to delete an instance or a queryset
actually.

```python
>>> Post.objects.all()

SELECT "blog_post"."id",
       "blog_post"."created_at",
       "blog_post"."updated_at",
       "blog_post"."status",
       "blog_post"."deleted_at",
       "blog_post"."author_id",
       "blog_post"."category_id",
       "blog_post"."title",
       "blog_post"."body"
  FROM "blog_post"
 LIMIT 21

Execution time: 0.000135s [Database: default]

<BaseModelWithSoftDeleteQuerySet [<Post: Python post 1>, <Post: Python post 2>, <Post: Python post 3>]>

>>> Category.objects.all()

SELECT "blog_category"."id",
       "blog_category"."created_at",
       "blog_category"."updated_at",
       "blog_category"."status",
       "blog_category"."deleted_at",
       "blog_category"."title"
  FROM "blog_category"
 WHERE "blog_category"."deleted_at" IS NULL
 LIMIT 21

<BaseModelWithSoftDeleteQuerySet [<Category: Python>]>

>>> Category.objects.delete()
(4, {'blog.Category': 1, 'blog.Post': 3})

>>> Category.objects.all()
<BaseModelWithSoftDeleteQuerySet []>       # rows are still there! don’t panic!

>>> Category.objects.deleted()
<BaseModelWithSoftDeleteQuerySet [<Category: Python>]>
```

`BaseModelWithSoftDeleteQuerySet` has these query options according to
`status` field:

- `.all()`
- `.offlines()` : filters if `BaseModel.STATUS_OFFLINE` is set
- `.actives()` : filters if `BaseModel.STATUS_ONLINE` is set
- `.deleted()` : filters if `BaseModel.STATUS_DELETED` is set and `deleted_at` is not `NULL`
- `.drafts()` : filters if `BaseModel.STATUS_DRAFT` is set
- `.delete()` : soft delete on given object.
- `.undelete()` : recover soft deleted on given object.
- `.hard_delete()` : this is real delete. this method erases given object.


When soft-delete enabled (*during model creation*), Django admin will
automatically use `CustomBaseModelAdminWithSoftDelete` which is inherited from:
 `CustomBaseModelAdmin` <- `admin.ModelAdmin`.

---

## `CustomBaseModelAdmin`, `CustomBaseModelAdminWithSoftDelete`

Inherits from `admin.ModelAdmin`. By default, adds `status` to `list_filter`.
You can disable this via setting `sticky_list_filter = None`. When model is
created with `rake new:model...` or from management command, admin file is
automatically generated. 

Example for `Post` model admin.

```python
import logging

from django.contrib import admin

from baseapp.admin import CustomBaseModelAdminWithSoftDelete
from baseapp.utils import console

from ..models import Post

__all__ = ['PostAdmin']

logger = logging.getLogger('app')
console = console(source=__name__)

@admin.register(Post)
class PostAdmin(CustomBaseModelAdminWithSoftDelete):
    # sticky_list_filter = None
    # hide_deleted_at = False
    pass
```

By default, `deleted_at` excluded from admin form like `created_at` and
`updated_at` fields. You can also override this via `hide_deleted_at` attribute.
Comment/Uncomment lines according to your needs! This works only in `CustomBaseModelAdminWithSoftDelete`.

`CustomBaseModelAdminWithSoftDelete` also comes with special admin action. You can
recover/make active (*undelete*) multiple objects like deleting items.

---

## `CustomLocaleMiddleware`

This is mostly used for our custom projects. Injects `LANGUAGE_CODE` variable to
`request` object. `/en/path/to/page/` sets `request.LANGUAGE_CODE` to `en` otherwise `tr`.

```python
# add this to your settings/base.py
MIDDLEWARE += ['baseapp.middlewares.CustomLocaleMiddleware']
```

---

## Custom Error Pages

You have browsable (only in development mode) and customizable error handler
functions and html templates now!. Templates are under `templates/custom_errors/`
folder. Handlers are under `baseapp/views/http_errors.py`

---

## `HtmlDebugMixin`

![Example baseapp view](screenshots/example-baseapp-view.png "Debug on view layer")

---

`HtmlDebugMixin` injects `{{ IS_DEBUG }}` and `{{ LANG }}` template variables
to context. Also with `self.hdbg(arg, arg, arg)` method, you can debug
anything from view to html template...

```python
# example: views.py

import logging

from django.views.generic.base import TemplateView

from baseapp.mixins import HtmlDebugMixin
from baseapp.utils import console

__all__ = ['IndexView']

logger = logging.getLogger('app')
console = console(source=__name__)


class IndexView(HtmlDebugMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        self.hdbg('This', 'is', 'an', 'example', 'of')
        self.hdbg('self.hdbg', 'usage')
        self.hdbg(self.request.__dict__)
        return kwargs
```

`{% hdbg %}` tag added by default in to your `templates/base.html`:

```django
{% load static %}
{% load i18n %}

<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}Baseapp{% endblock %}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.8.0/css/bulma.min.css">
    <script defer src="https://use.fontawesome.com/releases/v5.3.1/js/all.js"></script>
    <link rel="stylesheet" href="{% static 'css/baseapp.css' %}">
    <link rel="stylesheet" href="{% static 'css/application.css' %}">
    {% block extra_css %}{% endblock %}
</head>
<body>
    {% hdbg %}
    {% block body %}{% endblock %}
    {% block extra_js %}{% endblock %}
</body>
</html>
```

If you don’t want to extend from `templates/base.html` you can use your
own template. You just need to add `{% hdbg %}` tag in to your template.

---

## `baseapp.utils.console`

Do you need to debug an object from the View or anywhere from your Python
script? Sometimes you need to print out some variable(s) or values to console
and you want to keep it safe right? `print()` is very dangerous if you forget
on production server.

`console()`, `console.dir()` they both work only under `DEBUG = True` mode.

```python
# example: views.py

from baseapp.utils import console

class IndexView(TemplateView):
    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        console('Hello', 'World')
        console.dir(self.request.user)
        return kwargs
```

Now `console.dir()` outputs to terminal:

```bash
instance of AnonymousUser | <class 'django.utils.functional.SimpleLazyObject'>**
(   {   'arg': (   <SimpleLazyObject: <django.contrib.auth.models.AnonymousUser object at 0x10c3229e8>>,),
        'instance_attributes': ['_setupfunc', '_wrapped'],
        'internal_methods': [   '__class__', '__delattr__', '__dict__',
                                '__dir__', '__doc__', '__eq__', '__format__',
                                '__ge__', '__getattribute__', '__gt__',
                                '__hash__', '__init__', '__init_subclass__',
                                '__le__', '__lt__', '__module__', '__ne__',
                                '__new__', '__reduce__', '__reduce_ex__',
                                '__repr__', '__setattr__', '__sizeof__',
                                '__str__', '__subclasshook__', '__weakref__'],
        'private_methods': ['_groups', '_user_permissions'],
        'public_attributes': [   'check_password', 'delete',
                                 'get_all_permissions',
                                 'get_group_permissions', 'get_username',
                                 'groups', 'has_module_perms', 'has_perm',
                                 'has_perms', 'id', 'is_active',
                                 'is_anonymous', 'is_authenticated',
                                 'is_staff', 'is_superuser', 'pk', 'save',
                                 'set_password', 'user_permissions',
                                 'username'],
        'public_methods': ['_setupfunc']},)
********************************************************************************
```

You can set defaults for `console`:

```python
from baseapp.utils import console

console = console(
    source='console.py', # banner title will be `console.py`
    width=8,             # output width will wrap to 8 chars (demo purpose)
    indent=8,            # 8 characters will be userd for indention (demo purpose)
    color='white',       # banner color will be: white
)

console('Hello again...')
```

There are few basic color options available:

- black
- red
- green
- yellow
- blue
- magenta
- cyan
- white
- default

---

## `baseapp.utils.numerify`

Little helper for catching **QUERY_STRING** parameters for numerical values:

```python
from baseapp.utils import numerify

>>> numerify("1")
1
>>> numerify("1a")
-1
>>> numerify("ab")
-1
>>> numerify("abc", default=44)
44
```

---

## `baseapp.utils.save_file`

While using `FileField`, sometimes you need to handle uploaded files. In this
case, you need to use `upload_to` attribute. Take a look at the example in `baseapp/models/user.py`:

```python
from baseapp.utils import save_file as custom_save_file
:
:
:
class User(AbstractBaseUser, PermissionsMixin):
    :
    :
    avatar = models.FileField(
        upload_to=save_user_avatar,
        verbose_name=_('Profile Image'),
        null=True,
        blank=True,
    )
    :
    :
```

`save_user_avatar` returns `custom_save_file`’s return value. Default
configuration of for `custom_save_file` is 
`save_file(instance, filename, upload_to='upload/%Y/%m/%d/')`. Uploads are go to
such as `MEDIA_ROOT/upload/2017/09/21/`...

Make your custom uploads like:

```python
from baseapp.utils import save_file as custom_save_file

def my_custom_uploader(instance, filename):
    # do your stuff
    # at the end, call:
    return custom_save_file(instance, filename, upload_to='images/%Y/')


class MyModel(models.Model):
    image = models.FileField(
        upload_to='my_custom_uploader',
        verbose_name=_('Profile Image'),
    )
```

## `baseapp.storage`

### `FileNotFoundFileSystemStorage`

![FileNotFoundFileSystemStorage handles non existing images](screenshots/django-admin-storage.png "Django admin")

---

After shipping/deploying Django app, users start to upload files, right ?
Then you need to implement new features etc. You can get the dump of the
database but what about uploaded files ? Sometimes files are too much or
too big. If you call, let’s say, a model’s `ImageField`’s `url` property,
local dev server logs lot’s of **file not found** errors to console.

Also breaks the look of application via broken image signs in browser.

Now, you won’t see any errors... `FileNotFoundFileSystemStorage` is a
fake storage that handles non existing files. Returns `file-not-found.jpg`
from `static/` folder.

This is **development purposes** only! Do not use in the production!

You don’t need to change/add anything to your code...

### `OverwriteStorage`

`OverwriteStorage` helps you to overwrite file when uploading from django
admin. Example usage:

```python
# in a model
from baseapp.utils.storage image OverwriteStorage

class MyModel(models.Model):
    :
    :
    photo = models.ImageField(
        upload_to=save_media_photo,
        storage=OverwriteStorage(),
    )
    :
    :
```

Add `storage` option in you file related fields.

---

## `AdminImageFileWidget`

Use this widget in your admin forms:

```python
from baseapp.widgets import AdminImageFileWidget

class MyAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.FileField: {'widget': AdminImageFileWidget},
    }
```

This widget uses `Pillow` (*Python Image Library*) which ships with your `base.pip`
requirements file. Show image preview, width x height if the file is image.

---

## `context_processors.py`

Currently, there is only one template variable available: `{{ DJANGO_ENVIRONMENT_NAME }}`.
This is used for indicating the current environment in django admin site. You
can customize look and feel here:

```django
<!-- templates/admin/base_site.html -->

{% extends "admin/base_site.html" %}

{% load i18n %}

{% block title %}{{ title }} | {{ site_title|default:_('Django site admin') }}{% endblock %}

{% block branding %}
<h1 id="site-name">
    <a href="{% url 'admin:index' %}">{{ site_header|default:_('Django administration') }}</a>
</h1>
{% endblock %}


{% block welcome-msg %}
    {% trans 'Welcome,' %}
    <strong>{{ user.get_full_name }}</strong>.
{% endblock %}

{% block extrastyle %}
<style type="text/css">
    body:before {
        display: block;
        width: 100%;
        position: fixed;
        top: 0;
        z-index: 9999;
        line-height: 35px;
        text-align: center;
        font-weight: bold;
        text-transform: uppercase;
        color: white;
        content: "{{ DJANGO_ENVIRONMENT_NAME }}";
        background-color: red;
    }
    body {
        padding-top: 35px !important;
    }
</style>
{% endblock %}
```

This adds a basic HTML element via CSS to the `<body>` tag.

---

## Rakefile

If you have Ruby installed, you’ll have lots of handy tasks for the project.
Type `rake -T` for list of tasks:

```bash
$ rake -T

rake db:migrate[database]                                        # Run migration for given database (default: 'default')
rake db:roll_back[name_of_application,name_of_migration]         # Roll-back (name of application, name of migration)
rake db:shell                                                    # run database shell ..
rake db:show[name_of_application]                                # Show migrations for an application (default: 'all')
rake db:update[name_of_application,name_of_migration,is_empty]   # Update migration (name of application, name of migration?, is empty?)
rake locale:compile                                              # Compile locale dictionary
rake locale:update                                               # Update locale dictionary
rake new:application[name_of_application]                        # Create new Django application
rake new:model[name_of_application,name_of_model,type_of_model]  # Create new Model for given application: django,basemodel,softdelete
rake run_server                                                  # Run server
rake shell[repl]                                                 # Run shell+ avail: ptpython,ipython,bpython default: ptpython
rake test:browse_coverage[port]                                  # Browse test coverage
rake test:coverage[cli_args]                                     # Show test coverage (default: '--show-missing --ignore-errors --skip-covered')
rake test:run[name_of_application,verbose]                       # Run tests for given application
```

Default task is `run_server`. Just type `rake` that’s it! `runserver` uses
`runserver_plus`. This means you have lots of debugging options!

### `rake db:migrate[database]`

Migrates database with given database name. Default is `default`. If you like
to work multiple databases:

```python
# example
# config/settings/development.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db', 'development.sqlite3'),
    },
    'my_database': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db', 'my_database.sqlite3'),
    }
}
```

You can just call `rake db:migrate` or specify different database like: 
`rake db:migrate[my_database]` :)

### `rake db:roll_back[name_of_application,name_of_migration]`

Your database must be rollable :) To see available migrations: 
`rake db:roll_back[NAME_OF_YOUR_APPLICATION]`. Look at the list and choose your
target migration (*example*): `rake db:roll_back[baseapp,1]`.

```bash
# example scenario
$ rake db:roll_back[baseapp]
Please select your migration:
baseapp
 [X] 0001_create_custom_user
 [X] 0002_post_model

$ rake db:roll_back[baseapp,1]
$ rake db:show[baseapp]
baseapp
 [X] 0001_create_custom_user
 [ ] 0002_post_model
```

### `rake db:shell`

Runs default database client.

### `rake db:show[name_of_application]`

Show migrations. Examples:

```bash
$ rake db:show # shows everything
admin
 [X] 0001_initial
 [X] 0002_logentry_remove_auto_add
auth
 [X] 0001_initial
 [X] 0002_alter_permission_name_max_length
 [X] 0003_alter_user_email_max_length
 [X] 0004_alter_user_username_opts
 [X] 0005_alter_user_last_login_null
 [X] 0006_require_contenttypes_0002
 [X] 0007_alter_validators_add_error_messages
 [X] 0008_alter_user_username_max_length
baseapp
 [X] 0001_create_custom_user
blog
 [X] 0001_create_post_and_category
contenttypes
 [X] 0001_initial
 [X] 0002_remove_content_type_name
sessions
 [X] 0001_initial
```

or just a specific app:

```bash
$ rake db:show[blog]
blog
 [X] 0001_create_post_and_category
```

### `rake db:update[name_of_application,name_of_migration,is_empty]`

When you add/change something in the model, you need to create migrations. Use
this task. Let’s say you have added new field to `Post` model in your `blog`
app:

```bash
$ rake db:update[blog]                           # automatic migration (example)
Migrations for 'blog':
  applications/blog/migrations/0003_auto_20170921_1357.py
    - Alter field category on post
    - Alter field title on post

$ rake db:update[blog,add_new_field_to_post]     # migration with name (example)
Migrations for 'blog':
  applications/blog/migrations/0002_add_new_field_to_post.py

$ rake db:update[blog,add_new_field_to_post,yes] # migration with name (example)
Migrations for 'blog':
  applications/blog/migrations/0002_empty_mig.py
```

### `rake locale:compile` and `rake locale:update`

When you make changes in your application related to locales, run: `rake locale:update`.
When you finish editing your `django.po` file, run `rake locale:compile`.

### `rake new:application[name_of_application]`

Creates new application!

```bash
$ rake new:application[blog]
```

### `rake new:model[name_of_application,name_of_model,type_of_model]`

Creates new model! Available model types are: `django` (default), `basemodel`
and `softdelete`.

```bash
$ rake new:model[blog,Post]                # will create model using Django’s `models.Model`
$ rake new:model[blog,Post,basemodel]      # will create model using our `BaseModel`
$ rake new:model[blog,Post,softdelete]     # will create model using our `BaseModelWithSoftDelete`
```

### `rake shell[repl]`

Runs Django repl/shell with use `shell_plus` of [django-extensions][01].
 `rake shell`. This loads everything to your shell! Also you can see the
SQL statements while playing in shell. We have couple different repls:

1. `ptpython`
1. `bpython`
1. `ipython`

Default repl is: `ptpython`

```bash
$ rake shell
$ rake shell[bpython]
$ rake shell[ipython]
```

### `rake test:run[name_of_application,verbose]`

If you don’t provide `name_of_application` default value will be `applications`. 
`verbose` is `1` by default.

Examples:

```bash
$ rake test:run
$ rake test:run[baseapp,2]
```

### `rake test:coverage[cli_args]`

Get the test report. Default is `--show-missing --ignore-errors --skip-covered` for
`cli_args` parameter.

```bash
$ rake test:coverage
```

### `rake test:browse_coverage[port]`

Serves generated html coverages under `htmlcov` folder via `python`. Default port
is `9001`

---

## Run Tests Manually

```bash
$ DJANGO_ENV=test python manage.py test baseapp -v 2                                 # or
$ DJANGO_ENV=test python manage.py test baseapp.tests.test_user.CustomUserTestCase   # run single unit
$ rake test:run[baseapp]
```

---

## Manual Usage

Let’s assume you need a model called: `Page`. Create a file under `YOUR_APP/models/page.py`:

```python
# YOUR_APP/models/page.py

from django.db import models


__all__ = [
    'Page',
]

class Page(models.Model):
    # define your fields here...
    pass

# YOUR_APP/models/__init__.py
# append:
from .page import *
```

Now make migrations etc... Use it as `from YOUR_APP.models import Page` :)

---

## New Features

### SlackExceptionHandler

`baseapp.utils.log.SlackExceptionHandler`

You can send errors/exceptions to [slack](https://api.slack.com) channel.
Just create a slack app, get the webhook URL and set as `SLACK_HOOK`
environment variable. Due to slack message size limitation, `traceback`
is disabled.

Example message contains:

- http status
- error message
- exception message
- user.id or None
- full path

```bash
http status: 500
ERROR (internal IP): Internal Server Error: /__baseapp__/
Exception: User matching query does not exist.
user_id: anonymous (None)
full path: /__baseapp__/?foo=!
```

You can enable/disable in `config/settings/production.py` / `config/settings/heroku.py`:

```python
:
:
    'loggers': {
        'django.request': {'handlers': ['mail_admins', 'slack'], 'level': 'ERROR', 'propagate': False},  # remove 'slack'
    }
:
:
```

---

## Contributer(s)

- [Uğur "vigo" Özyılmazel](https://github.com/vigo) - Creator, maintainer

---

## Contribute

All PR’s are welcome!

1. `fork` (https://github.com/vigo/django2-project-template/fork)
1. Create your `branch` (`git checkout -b my-features`)
1. `commit` yours (`git commit -am 'added killer options'`)
1. `push` your `branch` (`git push origin my-features`)
1. Than create a new **Pull Request**!

---

## License

This project is licensed under MIT


[01]: https://github.com/django-extensions/django-extensions "Django Extensions"
[02]: https://django-debug-toolbar.readthedocs.io/en/stable/ "Django Debug Toolbar"
[03]: http://werkzeug.pocoo.org "Werkzeug"

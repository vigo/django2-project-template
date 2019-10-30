## Change Log

**2019-10-30**

- Change log is now individual file `CHANGELOG.md` 
- Upgrade to Django 2.2.6
- Now using Python 3.7.4
- Upgrade bulma to 0.8.0
- Upgrade packages
- Fix admin list filter for soft deleted objects
- New Version: 3.5.1


**2019-09-30**

- Fix `console` function.
- New Version: 3.4.4

**2019-09-19**

- New Version: 3.4.3
- Remove `urlify`, using `from slugify import slugify` instead
- New Version: 3.4.2
- Remove `baseapp/utils/storage.py`, now using only `baseapp/storage.py`

**2019-09-10**

- Django 2.2.5
- Fix Turkish locales
- Fix password validations for custom user

**2019-07-10**

- New Version: 3.2.2
- Enhance `FileSystemStorage` (#26)
- Add example screenshots
- Upgrade python packages
- Django 2.2.3

**2019-07-04**

- New Version: 3.3.1
- New package for Python 3.7.3
- Upgrade dependencies (`base.pip`, `development.pip`)
- Add `production.pip`
- Add `ptpython` as default repl

**2019-06-23**

- New Version: 3.2.1
- Fix `production` and `heroku` logging options
- Update security related config variables
- Add Slack error reporter

**2019-06-15**

- New Version: 3.2.0
- Fixed and improved AdminImageFileWidget (#25)
- Fixed logging config for Heroku (#24)
- Fixed settings for production and Heroku (#23, #22)
- Fixed base admin model (BaseAdmin) -> CustomBaseModelAdmin and CustomBaseModelAdminWithSoftDelete (#21)
- Add FileNotFoundFileSystemStorage (#9)

**2019-05-19**

- Fix: Soft-deleted items are now editable (Issue #19)
- Remove `TEST_DATABASE_URL`, It was useless :)
- Add custom error pages (Issue #10)

**2019-05-13**

- New Version: 3.0
- Fix soft-deletion feature
- `DJANGO_ENV` variable usage enhanced.
- Integrate `dj_database_url` to development/test environments too...
- Use `TEST_DATABASE_URL` for testing database.
- Additional information for PostgreSQL via Docker usage.

**2019-04-11** 

- New Version: 2.0
- Django upgrade: Django 2.2-LTS
- New development settings and logging features
- Default language is set to `en-us`, timezone is set to `UTC`
- PostgreSQL is default database now!
- Python packages are upgraded
- New REPL support: `bpython`
- BaseModelWithSoftDelete now supports `keep_parents`
- `pre_undelete` and `post_undelete` signals are welcome

**2019-03-22**

- Line width fixed to 88 chars
- All code generators now inject `console` and `logger` (model, admin, view, test)
- Fix: `BaseModelWithSoftDelete` relation with standard model
- Upgrade: Django 2.1.7 and other packages

**2019-01-13**

- Fix: Recovers related model items. Now works 100% correct.
- Add: Hard Delete feature. (*for BaseModelWithSoftDelete usage*)
- Fix: Wrong translations

**2019-01-12**

- Django version upgrade to: 2.1.5
- Upgrade: required python packages for dev, test, prod etc...
- Fix: Missing locale generator for JavaScript
- Add: Production logging configuration

**2018-12-04**

- Update: `BaseModel` and `BaseModelWithSoftDelete` now override `objects` via
  their own managers.

**2018-11-30**

- Update: flake8 ignores configured
- Removed: `flake8-import-order` using `isort` already...

**2018-11-19**

- Linters and formatters added.

**2018-11-16**

- Update: New version with new features.

**2018-05-08**

- Fix: `application/__init__.py`

**2018-05-07**

- Automatic Django Admin registration changed to: `@admin.register({model_name})` style.

**2018-05-02**

- Django 2.0.5 and related changes.
- Django Admin site titles are easy editable.
- Django Admin site indicator.

**2018-01-09**

- Django 2.0.1 and related changes.


# pylint: disable=W0212,W0143,R0201

import logging
from collections import Counter

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from ..utils import console
from .signals import post_undelete, pre_undelete

__all__ = ['BaseModel', 'BaseModelWithSoftDelete']

console = console(source=__name__)
logger = logging.getLogger('app')


class BaseModelQuerySet(models.QuerySet):
    """
    Common QuerySet for BaseModel and BaseModelWithSoftDelete.

    Available methods are:

    - `.actives()` : filters `status` is `STATUS_ONLINE`
    - `.deleted()` : filters `status` is `STATUS_DELETED`
    - `.offlines()`: filters `status` is `STATUS_OFFLINE`
    - `.drafts()`  : filters `status` is `STATUS_DRAFT`

    """

    def actives(self):
        return self.filter(status=BaseModel.STATUS_ONLINE)

    def deleted(self):
        return self.filter(status=BaseModel.STATUS_DELETED)

    def offlines(self):
        return self.filter(status=BaseModel.STATUS_OFFLINE)

    def drafts(self):
        return self.filter(status=BaseModel.STATUS_DRAFT)


class BaseModelWithSoftDeleteQuerySet(BaseModelQuerySet):
    """
    Available methods are:

    - `.all()`        : mimics deleted records.
    - `.actives()`    : filters `status` is `STATUS_ONLINE`
    - `.offlines()`   : filters `status` is `STATUS_OFFLINE`
    - `.drafts()`     : filters `status` is `STATUS_DRAFT`
    - `.deleted()`    : returns soft deleted objects.
    - `.delete()`     : soft deletes given objects.
    - `.undelete()`   : recovers given soft deleted object. fixes status and deleted_at values.
    - `.hard_delete()`: real delete method. no turning back!

    """

    def all(self):  # noqa: A003
        return self.filter(deleted_at__isnull=True).exclude(status=BaseModel.STATUS_DELETED)

    def actives(self):
        return self.all().filter(status=BaseModel.STATUS_ONLINE)

    def offlines(self):
        return self.all().filter(status=BaseModel.STATUS_OFFLINE)

    def drafts(self):
        return self.all().filter(status=BaseModel.STATUS_DRAFT)

    def delete(self):
        return self._delete_or_undelete()

    def undelete(self):
        return self._delete_or_undelete(True)

    def hard_delete(self):
        return super().delete()

    def _delete_or_undelete(self, undelete=False):
        processed_instances = {}
        call_method = 'undelete' if undelete else 'delete'

        for model_instance in self:
            _count, model_information = getattr(model_instance, call_method)()
            for (app_label, row_amount) in model_information.items():
                processed_instances.setdefault(app_label, 0)
                processed_instances[app_label] = processed_instances[app_label] + row_amount
        return (sum(processed_instances.values()), processed_instances)


class BaseModelManager(models.Manager):
    def get_queryset(self):
        return BaseModelQuerySet(self.model, using=self._db)

    def actives(self):
        return self.get_queryset().actives()

    def deleted(self):
        return self.get_queryset().deleted()

    def offlines(self):
        return self.get_queryset().offlines()

    def drafts(self):
        return self.get_queryset().drafts()


class BaseModelWithSoftDeleteManager(BaseModelManager):
    """
    This is a manager for `BaseModelWithSoftDelete` instances.
    """

    def get_queryset(self):
        return BaseModelWithSoftDeleteQuerySet(self.model, using=self._db)

    def all(self):  # noqa: A003
        return self.get_queryset().all()

    def delete(self):
        return self.get_queryset().delete()

    def undelete(self):
        return self.get_queryset().undelete()

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class BaseModel(models.Model):
    """
    Use this model for common functionality
    """

    STATUS_OFFLINE = 0
    STATUS_ONLINE = 1
    STATUS_DELETED = 2
    STATUS_DRAFT = 3

    STATUS_CHOICES = (
        (STATUS_OFFLINE, _('Offline')),
        (STATUS_ONLINE, _('Online')),
        (STATUS_DELETED, _('Deleted')),
        (STATUS_DRAFT, _('Draft')),
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_ONLINE, verbose_name=_('Status'))

    objects = BaseModelManager()

    class Meta:
        abstract = True


class BaseModelWithSoftDelete(BaseModel):

    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Deleted At'))

    objects = BaseModelWithSoftDeleteManager()

    class Meta:
        abstract = True

    def hard_delete(self):
        super().delete()

    def delete(self, using=None, keep_parents=False):
        return self._delete_or_undelete(using, keep_parents)

    def undelete(self, using=None, keep_parents=False):
        return self._delete_or_undelete(using, keep_parents, undelete=True)

    def _delete_or_undelete_instance(self, instance, method='delete'):
        if method == 'delete':
            models.signals.pre_delete.send(sender=instance.__class__, instance=instance)
            if issubclass(type(instance), BaseModel):
                instance.status = instance.STATUS_DELETED
                instance.deleted_at = timezone.now()
                instance.save()
            else:
                instance.delete()
            models.signals.post_delete.send(sender=instance.__class__, instance=instance)
            return instance._meta.label

        pre_undelete.send(sender=instance.__class__, instance=instance)
        undelete_label = None
        if issubclass(type(instance), BaseModel):
            instance.status = instance.STATUS_ONLINE
            instance.deleted_at = None
            instance.save()
            undelete_label = instance._meta.label
        post_undelete.send(sender=instance.__class__, instance=instance)
        return undelete_label

    def _get_instances(self, obj, method):
        manager_or_model = obj
        if hasattr(obj, 'get_accessor_name'):
            manager_or_model = getattr(self, obj.get_accessor_name())

        if not issubclass(type(manager_or_model), models.Manager):
            return [manager_or_model]

        if getattr(obj, 'on_delete', None):
            if obj.on_delete.__name__ != 'CASCADE':
                return []
            if not hasattr(manager_or_model, 'undelete'):
                return manager_or_model.all()
            if method == 'undelete':
                return manager_or_model.deleted()
            return manager_or_model.actives()

        if hasattr(manager_or_model, 'undelete'):
            if method == 'undelete':
                return manager_or_model.deleted()
            return manager_or_model.actives()
        return manager_or_model.all()

    def _delete_or_undelete(self, using=None, keep_parents=False, undelete=False):
        using = using or 'default'
        processed_instances = Counter()
        method = 'undelete' if undelete else 'delete'
        processed_label = self._delete_or_undelete_instance(self, method=method)
        if processed_label is not None:
            processed_instances[processed_label] += 1

        if not keep_parents:
            # many-to-many
            for m2m_field in self._meta.many_to_many:
                for instance in self._get_instances(getattr(self, m2m_field.name), method):
                    processed_label = self._delete_or_undelete_instance(instance, method=method)
                    if processed_label is not None:
                        processed_instances[processed_label] += 1
            # foreign-key
            for related_object in self._meta.related_objects:
                for instance in self._get_instances(related_object, method):
                    processed_label = self._delete_or_undelete_instance(instance, method=method)
                    if processed_label is not None:
                        processed_instances[processed_label] += 1
        return (sum(processed_instances.values()), dict(processed_instances))

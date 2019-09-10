# pylint: disable=W0212,W0143,R0201

import logging
from collections import Counter

from django.db import models, router, transaction
from django.db.models.deletion import Collector
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
        return self.filter(status=self.model.STATUS_ONLINE)

    def deleted(self):
        return self.filter(status=self.model.STATUS_DELETED)

    def offlines(self):
        return self.filter(status=self.model.STATUS_OFFLINE)

    def drafts(self):
        return self.filter(status=self.model.STATUS_DRAFT)


class BaseModelWithSoftDeleteQuerySet(BaseModelQuerySet):
    """
    Available methods are:

    - `.all()`        : filter deleted records. returns actives, offlines and drafts.
    - `.actives()`    : filters `status` is `STATUS_ONLINE`
    - `.offlines()`   : filters `status` is `STATUS_OFFLINE`
    - `.drafts()`     : filters `status` is `STATUS_DRAFT`
    - `.deleted()`    : returns soft deleted objects.
    - `.delete()`     : soft deletes given objects.
    - `.undelete()`   : recovers given soft deleted object. fixes status and deleted_at values.
    - `.hard_delete()`: real delete method. no turning back!

    """

    def all(self):  # noqa: A003
        return self.filter(deleted_at__isnull=True).exclude(status=self.model.STATUS_DELETED)

    def delete(self):
        return self._delete_or_undelete()

    def undelete(self):
        return self._delete_or_undelete(undelete=True)

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
        (STATUS_OFFLINE, _('offline')),
        (STATUS_ONLINE, _('online')),
        (STATUS_DELETED, _('deleted')),
        (STATUS_DRAFT, _('draft')),
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_ONLINE, verbose_name=_('status'))

    objects = BaseModelManager()

    class Meta:
        abstract = True


class BaseModelWithSoftDelete(BaseModel):

    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name=_('deleted at'))

    objects = BaseModelWithSoftDeleteManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):  # pylint: disable=W0221
        if self.status == BaseModel.STATUS_DELETED:
            self.delete()
        else:
            self.deleted_at = None
        super().save(*args, **kwargs)

    def hard_delete(self, using=None, keep_parents=False):
        return super().delete(using=using, keep_parents=keep_parents)

    def delete(self, using=None, keep_parents=False):
        using = using or router.db_for_write(self.__class__, instance=self)
        return self._soft_delete(using=using, keep_parents=keep_parents)

    def undelete(self, using=None, keep_parents=False):
        using = using or router.db_for_write(self.__class__, instance=self)
        return self._undelete(using=using, keep_parents=keep_parents)

    def _collect_related(self, using=None, keep_parents=False):
        collector = Collector(using=using)
        collector.collect([self], keep_parents=keep_parents)
        fast_deletes = []
        for queryset in collector.fast_deletes:
            if queryset.count() > 0:
                fast_deletes.append(queryset)

        return dict(
            instances_with_model=collector.instances_with_model(), fast_deletes=fast_deletes, data=collector.data
        )

    def _undelete(self, using=None, keep_parents=False):
        return self._soft_delete(using=using, keep_parents=keep_parents, undelete=True)

    def _soft_delete(self, using=None, keep_parents=False, undelete=False):
        items = self._collect_related(using=using, keep_parents=keep_parents)
        deleted_counter = Counter()

        required_pre_signal = models.signals.pre_delete
        required_post_signal = models.signals.post_delete
        required_status = BaseModel.STATUS_DELETED
        required_deleted_at = timezone.now()

        if undelete:
            required_pre_signal = pre_undelete
            required_post_signal = post_undelete
            required_status = BaseModel.STATUS_ONLINE
            required_deleted_at = None

        with transaction.atomic(using=using, savepoint=False):

            # pre signal...
            for model, obj in items.get('instances_with_model'):
                if not model._meta.auto_created:
                    required_pre_signal.send(sender=model, instance=obj, using=using)

            # fast deletes-ish
            for queryset in items.get('fast_deletes'):
                count = queryset.count()

                if issubclass(queryset.model, BaseModelWithSoftDelete):
                    # this happens in database layer...
                    # try to mark as deleted if the model is inherited from
                    # BaseModelWithSoftDelete
                    count = queryset.update(status=required_status, deleted_at=required_deleted_at)
                else:
                    # well, just delete it...
                    count = queryset._raw_delete(using=using)
                deleted_counter[queryset.model._meta.label] += count

            for model, instances in items.get('data').items():
                pk_list = [obj.pk for obj in instances]
                queryset = model.objects.filter(id__in=pk_list)
                count = queryset.count()

                if issubclass(model, BaseModelWithSoftDelete):
                    count = queryset.update(status=required_status, deleted_at=required_deleted_at)

                deleted_counter[model._meta.label] += count

                if not model._meta.auto_created:
                    for obj in instances:
                        required_post_signal.send(sender=model, instance=obj, using=using)

        return sum(deleted_counter.values()), dict(deleted_counter)

from datetime import datetime

from django.db import models
from django.db.models import QuerySet

from .users import Users


class SoftDeletionQuerySet(QuerySet):
    def delete(self):
        return super(SoftDeletionQuerySet, self).update(deleted_at=datetime.now())

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)


class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class Base(models.Model):
    status = models.BooleanField(default=True)

    created_by = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='%(class)s_createdby',
        db_column='created_by',
        null=True
    )
    updated_by = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='%(class)s_updated_by',
        db_column='updated_by',
        null=True
    )
    deleted_by = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='%(class)s_deleted_by',
        db_column='deleted_by',
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self, **kwargs):
        self.deleted_at = datetime.now()
        self.save()

    def hard_delete(self):
        super(Base, self).delete()

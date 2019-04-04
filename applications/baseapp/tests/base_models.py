# pylint: disable=R0903

from django.db import models

from ..models import BaseModel, BaseModelWithSoftDelete


class BasicPost(BaseModel):
    title = models.CharField(max_length=255)

    class Meta:
        managed = False

    def __str__(self):
        return self.title


class Category(BaseModelWithSoftDelete):
    title = models.CharField(max_length=255)

    class Meta:
        managed = False

    def __str__(self):
        return self.title


class Post(BaseModelWithSoftDelete):
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)

    class Meta:
        managed = False

    def __str__(self):
        return self.title


class Person(BaseModelWithSoftDelete):
    name = models.CharField(max_length=255)

    class Meta:
        managed = False

    def __str__(self):
        return self.name


class Member(BaseModelWithSoftDelete):
    title = models.CharField(max_length=255)
    members = models.ManyToManyField(to='Person')

    class Meta:
        managed = False

    def __str__(self):
        return self.title

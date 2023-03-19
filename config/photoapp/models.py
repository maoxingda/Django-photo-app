"""Photoapp Models"""

from django.db import models

from django.contrib.auth import get_user_model

from taggit.managers import TaggableManager
from taggit.models import Tag, TaggedItem

import uuslug


class CnTag(Tag):
    class Meta:
        proxy = True

    def slugify(self, tag, i=None):
        return uuslug.slugify(self.name)


class CnTaggedItem(TaggedItem):
    class Meta:
        proxy = True

    @classmethod
    def tag_model(cls):
        return CnTag


class Photo(models.Model):
    title = models.CharField(max_length=45)

    description = models.CharField(max_length=250)

    created = models.DateTimeField(auto_now_add=True)

    image = models.ImageField(upload_to='photos/')

    submitter = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    tags = TaggableManager(through=CnTaggedItem)

    def __str__(self):
        return self.title

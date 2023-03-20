"""Photoapp Models"""

from django.db import models

from django.contrib.auth import get_user_model

from taggit.managers import TaggableManager
from taggit.models import TagBase, GenericTaggedItemBase

import uuslug


class CnTag(TagBase):
    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'

    def slugify(self, tag, i=None):
        return uuslug.slugify(tag)


class CnTaggedItem(GenericTaggedItemBase):
    class Meta:
        verbose_name = 'tag_item'
        verbose_name_plural = 'tag_items'

    tag = models.ForeignKey(
        CnTag,
        on_delete=models.CASCADE,
        related_name="tagged_items",  # TODO 全局替换
    )


class Photo(models.Model):
    title = models.CharField(max_length=45)

    description = models.CharField(max_length=250)

    created = models.DateTimeField(auto_now_add=True)

    image = models.ImageField(upload_to='photos/')

    submitter = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    tags = TaggableManager(through=CnTaggedItem, blank=True)

    def __str__(self):
        return self.title

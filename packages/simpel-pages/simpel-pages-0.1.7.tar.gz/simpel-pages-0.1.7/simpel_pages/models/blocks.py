from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField
from filer.fields.image import FilerImageField
from polymorphic.models import PolymorphicModel

# Create your models here.


class BaseBlock(PolymorphicModel):
    name = models.SlugField(
        _("name"),
        null=True,
        blank=True,
    )
    group = models.SlugField(
        _("group"),
        null=True,
        blank=True,
    )
    position = models.IntegerField(
        default=0,
        verbose_name=_("position"),
        help_text=_("Used for ordering block."),
    )

    class Meta:
        abstract = True

    def __str__(self):
        return "%s (%s)" % (self.__class__._meta.verbose_name, self.name)


class Block(BaseBlock):
    object_type = models.ForeignKey(
        ContentType,
        related_name="blocks",
        null=True,
        blank=True,
        verbose_name="object type",
        on_delete=models.CASCADE,
    )
    object_id = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_("object"),
    )
    object = GenericForeignKey(
        "object_type",
        "object_id",
    )

    class Meta:
        verbose_name = _("Block")
        verbose_name_plural = _("Blocks")


class RichTextBlock(Block):
    text = RichTextField()

    class Meta:
        verbose_name = _("Text Block")
        verbose_name_plural = _("Text Blocks")


class ImageBlock(Block):
    caption = models.CharField(
        max_length=200,
        verbose_name=_("Caption"),
    )
    thumb_height = models.IntegerField(
        default=100,
        verbose_name=_("Thumbnail Height"),
    )
    thumb_width = models.IntegerField(
        default=100,
        verbose_name=_("Thumbnail Width"),
    )
    image = FilerImageField(
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    class Meta:
        verbose_name = _("Image Block")
        verbose_name_plural = _("Image Blocks")

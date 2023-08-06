from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from filer.fields.image import FilerImageField
from polymorphic.models import PolymorphicModel
from simpel_atomics.component import Component
from tinymce.models import HTMLField

VALID_RENDER_FORMAT = ["html", "dict", "json"]


class BlockComponent(Component):
    template_name = "simpel_pages/blocks/block.html"


class RichTextBlockComponent(Component):
    template_name = "simpel_pages/blocks/richtext.html"


class ImageBlockComponent(Component):
    template_name = "simpel_pages/blocks/image.html"


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

    component_class = BlockComponent

    def get_component_class(self, request=None):
        return self.component_class

    def get_component_context(self, **kwargs):
        ctx = {"object": self}
        ctx.update(kwargs)
        return ctx

    def get_component_kwargs(self, **kwargs):
        return kwargs

    def get_component(self, request, **kwargs):
        return self.get_component_class(request)(**kwargs)

    def render(self, request=None, context=dict(), init_kwargs=dict()):
        ctx = self.get_component_context(**context)
        kwargs = self.get_component_kwargs(**init_kwargs)
        component = self.get_component(request, **kwargs)
        return component.render(ctx)

    class Meta:
        abstract = True

    def __str__(self):
        return "%s (%s)" % (self.__class__._meta.verbose_name, self.name)


class BlockManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by("position")


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
    text = HTMLField()
    component_class = RichTextBlockComponent

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
    component_class = ImageBlockComponent

    class Meta:
        verbose_name = _("Image Block")
        verbose_name_plural = _("Image Blocks")

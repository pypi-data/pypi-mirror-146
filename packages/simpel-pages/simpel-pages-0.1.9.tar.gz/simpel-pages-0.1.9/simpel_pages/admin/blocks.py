from polymorphic.admin import GenericStackedPolymorphicInline
from tinymce.widgets import TinyMCE

from simpel_pages.models.blocks import RichTextBlock

from ..models import Block, ImageBlock


class BaseBlockInline(GenericStackedPolymorphicInline.Child):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ["text", "richtext", "content"]:
            return db_field.formfield(
                widget=TinyMCE(
                    attrs={"cols": 80, "rows": 20, "height": 97},
                    mce_attrs={
                        "height": 300,
                    },
                )
            )
        return super().formfield_for_dbfield(db_field, **kwargs)


class BlockInline(GenericStackedPolymorphicInline):
    model = Block
    ct_field = "object_type"

    def get_child_models(self):
        """
        Register child model using defaults from settings
        """
        # Get deliverable child models map from hooks
        child_models = []
        if len(child_models) == 0:
            child_models = [RichTextBlock, ImageBlock]
        return child_models

    def get_child_inline_classes(self):
        child_models = self.get_child_models()
        child_inlines = []
        for child in child_models:
            class_name = child.__class__.__name__
            props = {"model": child, "ct_field": "object_type"}
            parent_class = (BaseBlockInline,)
            inline_class = type("%sInline" % class_name, parent_class, props)
            child_inlines.append(inline_class)
        return child_inlines

    def get_child_inline_instances(self):
        instances = []
        for ChildInlineType in self.get_child_inline_classes():
            instances.append(ChildInlineType(parent_inline=self))
        return instances

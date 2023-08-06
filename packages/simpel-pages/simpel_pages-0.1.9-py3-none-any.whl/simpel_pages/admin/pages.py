from copy import copy

from django.contrib import admin
from django.core.exceptions import ImproperlyConfigured
from django.utils import timezone
from django.utils.html import format_html
from django.utils.text import Truncator
from django.utils.translation import gettext_lazy as _

from mptt.admin import DraggableMPTTAdmin
from polymorphic.admin import PolymorphicInlineSupportMixin
from simpel_hookup import core as hookup
from tinymce.widgets import TinyMCE

from simpel_pages.admin.blocks import BlockInline

from ..forms import PageForm
from ..models import Category, Page, RootPage, Tag, Visitor


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    search_fields = ["name", "slug"]
    list_display = list(DraggableMPTTAdmin.list_display) + ["name", "slug", "description"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ["name", "description"]
    list_display = ["name", "slug", "description"]


@admin.register(Page)
class PageAdmin(PolymorphicInlineSupportMixin, DraggableMPTTAdmin):
    form_class = PageForm
    list_filter = ("index", "live", "allow_comments", "registration_required")
    list_display = [
        "tree_actions",
        "indented_title",
        "page_type",
        "visitor",
        "bookmark",
        "reader",
        "live",
    ]
    search_fields = ("url_path", "title")
    seo_settings = (
        _("SEO Settings"),
        {
            "fields": (
                "slug",
                "seo_title",
                "seo_description",
                "data",
                "template",
                "index",
                "per_page",
                "live",
            ),
            "classes": ["collapse"],
        },
    )
    perms_settings = (
        _("Permission Settings"),
        {
            "fields": (
                "allow_comments",
                "registration_required",
                "groups",
            ),
            "classes": ["collapse"],
        },
    )
    page_fields = [
        "parent",
        "title",
        "tags",
        "category",
        "thumbnail",
        "content",
    ]
    fieldsets = (
        (None, {"fields": page_fields}),
        seo_settings,
        perms_settings,
    )
    inlines = [BlockInline]

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == "content":
            return db_field.formfield(
                widget=TinyMCE(
                    attrs={"cols": 80, "rows": 20, "height": 97},
                    mce_attrs={
                        "height": 300,
                    },
                )
            )
        return super().formfield_for_dbfield(db_field, **kwargs)

    def get_inlines(self, request, obj):
        funcs = hookup.get_hooks("SIMPEL_PAGES_PAGE_INLINES")
        inlines = copy(self.inlines)
        for func in funcs:
            inline_class = func()
            if not issubclass(
                inline_class,
                admin.options.InlineModelAdmin,
            ):
                raise ImproperlyConfigured(_("%s must subclass InlineModelAdmin"))
            inlines.append(inline_class)
        return super().get_inlines(request, obj)

    def get_page_types(self):
        funcs = hookup.get_hooks("SIMPEL_PAGES_PAGE_TYPES")
        types = []
        for func in funcs:
            page_model = func()
            if not issubclass(page_model, Page):
                raise ImproperlyConfigured(_("%s must subclass simpel_pages.Page"))
            types.append(page_model)
        return types

    def bookmark(self, obj):
        return obj.bookmarks.count()

    def reader(self, obj):
        return obj.readers.count()

    def visitor(self, obj):
        return obj.visitor_count

    def indented_title(self, item):
        item_text = Truncator(item).chars(60)
        return format_html(
            '<div style="text-indent:{}px">{}</div>',
            item._mpttfield("level") * self.mptt_level_indent,
            item_text,
        )

    def save_model(self, request, obj, form, change):
        if obj.owner is None:
            obj.owner = request.user
        obj.updated_at = timezone.now()
        return super().save_model(request, obj, form, change)


@admin.register(RootPage)
class SiteRootAdmin(admin.ModelAdmin):
    list_display = ["site", "page"]
    pass


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ["created_at", "url", "ip", "referrer"]

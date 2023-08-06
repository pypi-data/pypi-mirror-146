from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404, HttpResponse, QueryDict
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.views.generic.list import ListView

from haystack.views import SearchView
from simpel_hookup import core as hookup
from tinymce.views import render_to_link_list

from .helpers import log_traffic
from .models import Category, RootPage, Tag
from .models.pages import Page, SearchQuery
from .settings import pages_settings


@csrf_protect
def serve_page(request, path):
    # we need a valid Site object corresponding to this request in order to proceed
    site = get_current_site(request)
    if not site:
        raise Http404

    path_components = [component for component in path.split("/") if component]
    site_root = RootPage.objects.get(site=site)
    page, args, kwargs = site_root.page.specific.route(request, path_components)

    for fn in hookup.get_hooks("PAGES_BEFORE_SERVE"):
        result = fn(page, request, args, kwargs)
        if isinstance(result, HttpResponse):
            return result
    log_traffic(request, content=page)
    if request.user.is_authenticated:
        page.readers.add(request.user)
    return page.serve(request, *args, **kwargs)


@csrf_protect
def serve_search(request, slug=None):
    if slug is not None:
        try:
            search_query = SearchQuery.objects.get(slug=slug)
            query = search_query.keyword
            request.GET = QueryDict(query_string=f"q={query}")
        except SearchQuery.DoesNotExist:
            pass
    query = request.GET.get("q", None)
    if query not in [None, "", " "]:
        query = query.strip().lower()
        search_query, _ = SearchQuery.objects.get_or_create(keyword=query)
        log_traffic(request, content=search_query)
    SearchViewClass = pages_settings.PAGE_SEARCH_VIEW
    if SearchViewClass is None:
        return SearchView(template="simpel_pages/search.html")(request)
    else:
        return SearchViewClass.as_view()(request)


@csrf_protect
def serve_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    site = get_current_site(request)
    site_root = RootPage.objects.get(site=site)
    real_model = request.GET.get("type", None)
    filters = dict()
    if real_model is not None:
        filters["real_model"] = real_model
    filters["category__slug__in"] = [category.slug]
    queryset = site_root.page.get_descendants().filter(**filters).live().order_by("-created_at")
    log_traffic(request, content=category)
    return ListView.as_view(
        queryset=queryset,
        paginate_by=pages_settings.ITEM_PER_PAGE,
        template_name="simpel_pages/category.html",
        extra_context={"object": category},
    )(request)


@csrf_protect
def serve_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    site = get_current_site(request)
    site_root = RootPage.objects.get(site=site)
    real_model = request.GET.get("type", None)
    filters = dict()
    if real_model is not None:
        filters["real_model"] = real_model
    filters["tags__slug__in"] = [tag.slug]
    queryset = site_root.page.get_descendants().filter(**filters).live().order_by("-created_at")
    log_traffic(request, content=tag)
    return ListView.as_view(
        queryset=queryset,
        paginate_by=pages_settings.ITEM_PER_PAGE,
        template_name="simpel_pages/tag.html",
        extra_context={"object": tag},
    )(request)


def serve_tags(request):
    return ListView.as_view(
        queryset=Tag.objects.order_by("name"),
        paginate_by=pages_settings.CATEGORY_PER_PAGE,
        template_name="simpel_pages/tag_list.html",
    )(request)


def serve_categories(request):
    return ListView.as_view(
        queryset=Category.objects.order_by("name"),
        paginate_by=pages_settings.TAG_PER_PAGE,
        template_name="simpel_pages/category_list.html",
    )(request)


def pages_link_list(request):
    """
    Returns a HttpResponse whose content is a Javascript file representing a
    list of links to pages.
    """
    link_list = [(page.title, page.url) for page in Page.objects.all()]
    return render_to_link_list(link_list)

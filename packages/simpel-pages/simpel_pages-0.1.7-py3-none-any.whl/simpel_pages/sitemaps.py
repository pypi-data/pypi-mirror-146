from django.apps import apps as django_apps
from django.contrib.sitemaps import Sitemap
from django.core.exceptions import ImproperlyConfigured


class PageSitemap(Sitemap):
    def items(self):
        if not django_apps.is_installed("django.contrib.sites"):
            raise ImproperlyConfigured(
                "SimpelPageSitemap requires django.contrib.sites, which isn't installed."
            )
        Site = django_apps.get_model("sites.Site")
        RootPage = django_apps.get_model("simpel_pages.RootPage", require_ready=False)
        current_site = Site.objects.get_current()
        root_page = RootPage.objects.get(site=current_site)
        return root_page.page.get_descendants().filter(registration_required=False, live=True)

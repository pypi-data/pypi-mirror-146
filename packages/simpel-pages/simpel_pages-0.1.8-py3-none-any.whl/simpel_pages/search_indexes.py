import datetime

from haystack import indexes

from .models import Page
from .settings import pages_settings


class PageIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(
        document=True,
        use_template=True,
        template_name=pages_settings.PAGE_HAYSTACK_TEMPLATE,
    )
    author = indexes.CharField(model_attr="owner", null=True)
    created_at = indexes.DateTimeField(model_attr="created_at")

    def get_model(self):
        return Page

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(created_at__lte=datetime.datetime.now())

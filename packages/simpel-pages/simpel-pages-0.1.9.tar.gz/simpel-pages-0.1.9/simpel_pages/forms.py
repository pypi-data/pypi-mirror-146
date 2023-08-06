from django import forms

from tinymce.widgets import TinyMCE

from .models import Page


class PageForm(forms.ModelForm):
    content = TinyMCE(
        attrs={"cols": 80, "rows": 20, "height": 97},
        mce_attrs={"height": 300},
    )

    class Meta:
        model = Page
        fields = "__all__"

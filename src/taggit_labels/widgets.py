from django import forms

from django.forms.utils import flatatt
from django.utils.html import format_html, format_html_join

from taggit.models import Tag
from taggit.utils import edit_string_for_tags


class LabelWidget(forms.TextInput):
    """
    Widget class for rendering an item's tags - and all existing tags - as
    selectable labels.
    """
    input_type = "hidden"
    model = Tag

    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop("model", None) or self.model
        super(LabelWidget, self).__init__(*args, **kwargs)

    @property
    def is_hidden(self):
        return False

    def tag_list(self, tags):
        """
        Generates a list of tags identifying those previously selected.

        Returns a list of tuples of the form (<tag name>, <CSS class name>).

        Uses the string names rather than the tags themselves in order to work
        with tag lists built from forms not fully submitted.
        """
        return [
            (
                tag.name,
                "selected taggit-tag" if tag.name in tags else "taggit-tag",
            )
            for tag in self.model.objects.all()
        ]

    def format_value(self, value):
        if value is not None and not isinstance(value, str):
            value = edit_string_for_tags([tag for tag in value])
        return value

    def render(self, name, value, attrs={}, renderer=None, **kwargs):
        # Case in which a new form is dispalyed
        if value is None:
            current_tags = []
            formatted_value = ""
            selected_tags = self.tag_list([])

        # Case in which a form is displayed with submitted but not saved
        # details, e.g. invalid form submission
        elif isinstance(value, str):
            current_tags = [tag.strip(' "') for tag in value.split(",") if tag]
            formatted_value = value
            selected_tags = self.tag_list(current_tags)

        # Case in which value is loaded from saved tags
        else:
            current_tags = [tag for tag in value]
            formatted_value = self.format_value(value)
            selected_tags = self.tag_list([t.name for t in current_tags])

        input_field = super(LabelWidget, self).render(
            name, formatted_value, attrs, **kwargs
        )
        if attrs.get("class") is None:
            attrs.update({"class": "taggit-labels taggit-list"})

        tag_list_items = format_html_join(
            "",
            '<li data-tag-name="{name}" class="{class}">{name}</li>',
            [{'name': tag[0], 'class': tag[1]} for tag in selected_tags]
        )
        tag_ul = format_html(
            "<ul{}>{}</ul>",
            flatatt(attrs), tag_list_items,
        )
        return format_html("{}{}", tag_ul, input_field)

    @property
    def media(self):
        js = [
            "taggit_labels/js/taggit_labels.js",
        ]
        css = {"all": ("taggit_labels/css/taggit_labels.css",)}

        return forms.Media(js=js, css=css)

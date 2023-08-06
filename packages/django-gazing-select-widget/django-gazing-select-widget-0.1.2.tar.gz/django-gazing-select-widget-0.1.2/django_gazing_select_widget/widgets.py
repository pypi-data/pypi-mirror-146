import json
from django.forms.widgets import Select

class DjangoGazingSelectWidget(Select):

    class Media:
        js = [
            "admin/js/vendor/jquery/jquery.js",
            "django-gazing-select-widget/js/django-gazing-select-widget.js",
            "admin/js/jquery.init.js",
        ]

    def __init__(self,
            gazing_field_name,
            this_field_name,
            choices_related=None,
            gazing_related=True,
            optgroups_related=None,
            empty_label="-"*10,
            hide_all_if_empty=True,
            attrs=None,
            choices=(),
            ):
        self.original_choices = choices
        if callable(choices):
            choices = choices()
        # keep private parameters
        self.choices_related = choices_related or {}
        self.optgroups_related = optgroups_related or {}
        # super.init
        attrs = attrs or {}
        attrs["class"] = attrs.get("class", "") + " django-gazing-select-widget"
        attrs["data-gazing-field-name"] = gazing_field_name
        attrs["data-this-field-name"] = this_field_name
        attrs["data-hide-all-if-empty"] = hide_all_if_empty and "true" or "false";
        attrs["data-gazing-related"] = gazing_related and "true" or "false";
        choices.insert(0, ("", empty_label))
        super().__init__(attrs, choices)

    def get_context(self, name, value, attrs):

        if callable(self.original_choices):
            self.choices = self.original_choices()

        if callable(self.choices_related):
            choices_related = self.choices_related()
        else:
            choices_related = self.choices_related

        if callable(self.optgroups_related):
            optgroups_related = self.optgroups_related()
        else:
            optgroups_related = self.optgroups_related
    
        context = super().get_context(name, value, attrs)
        for optgroup in context["widget"]["optgroups"]:
            group_title = optgroup[0]
            optgroup_for = optgroups_related.get(group_title, [])
            for option in optgroup[1]:
                option_value = option["value"]
                option_for = [] + optgroup_for
                if choices_related:
                    option_for += choices_related.get(option_value, [])
                option["attrs"]["data-for"] = json.dumps(option_for)
        return context

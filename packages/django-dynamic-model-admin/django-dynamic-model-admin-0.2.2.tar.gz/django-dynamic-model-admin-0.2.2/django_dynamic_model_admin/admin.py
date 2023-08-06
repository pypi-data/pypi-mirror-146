
from django import forms
from django.forms.models import ModelChoiceField
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin

from mptt.admin import DraggableMPTTAdmin
from mptt.admin import TreeRelatedFieldListFilter
from django_dynamic_resource_admin.admin import DjangoDynamicResourceAdmin
from django_cascading_dropdown_widget.widgets import DjangoCascadingDropdownWidget
from django_cascading_dropdown_widget.widgets import SimpleChoices2
from django_gazing_select_widget.widgets import DjangoGazingSelectWidget
from django_tabbed_changeform_admin.admin import DjangoTabbedChangeformAdmin

from .types import get_field_widget_choices
from .types import get_field_widget

class ModelFieldInline(admin.TabularInline):
    def __init__(self, model, data_model, parent_model, admin_site, fk_name, extra=0, classes=None):
        self.model = model
        self.data_model = data_model
        self.fk_name = fk_name
        self.extra = extra
        self.classes = classes
        self.verbose_name = model._meta.verbose_name
        self.verbose_name_plural = model._meta.verbose_name_plural
        super().__init__(parent_model, admin_site)

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj=obj, **kwargs)
        formset.form.base_fields["real_field_name"].widget = DjangoCascadingDropdownWidget(choices=SimpleChoices2(*self.data_model.get_data_field_choices()))
        # field widget settings
        field_widget_optgroups_related = self.data_model.get_field_widget_optgroups_related()
        field_widget_choices = get_field_widget_choices()
        formset.form.base_fields["field_widget"].widget = DjangoGazingSelectWidget(
            gazing_field_name="real_field_name",
            this_field_name="field_widget",
            optgroups_related=field_widget_optgroups_related,
            choices=field_widget_choices,
            )
        return formset


class ModelDefinitionRelatedInline(admin.TabularInline):

    def __init__(self, model, parent_model, admin_site, fk_name, extra=0, classes=None):
        self.model = model
        self.fk_name = fk_name
        self.extra = extra
        self.classes = classes
        self.verbose_name = model._meta.verbose_name
        self.verbose_name_plural = model._meta.verbose_name_plural
        super().__init__(parent_model, admin_site)

class ModelDefinitionAbstractAdmin(DraggableMPTTAdmin, DjangoTabbedChangeformAdmin, admin.ModelAdmin):

    class Media:
        css = {
            "all": [
                "django-dynamic-model-admin/css/modeldefinition-admin.css",
            ]
        }

    list_display = ["tree_actions", "indented_title"]
    list_display_links = ["indented_title"]
    search_fields = ["verbose_name"]
    list_filter = [
        ("parent", TreeRelatedFieldListFilter),
    ]
    data_model = None
    field_model = None
    fieldset_model = None
    inline_model = None
    tab_model = None
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_form(self, *args, **kwargs):
        self.field_inline_instance = ModelFieldInline(self.field_model, self.data_model, self.model, self.admin_site, "definition", 0, classes=["model-field-inlinegroup"])
        self.fieldset_inline_instance = ModelDefinitionRelatedInline(self.fieldset_model, self.model, self.admin_site, "definition", 0, classes=["model-fieldset-inlinegroup"])
        self.inline_inline_instance = ModelDefinitionRelatedInline(self.inline_model, self.model, self.admin_site, "definition", 0, classes=["model-inline-inlinegroup"])
        self.tab_inline_instance = ModelDefinitionRelatedInline(self.tab_model, self.model, self.admin_site, "definition", 0, classes=["model-changeform-tab-inlinegroup"])
        form = super().get_form(*args, **kwargs)
        return form

    def get_inline_instances(self, request, obj=None):
        return [
            self.field_inline_instance,
            self.fieldset_inline_instance,
            self.inline_inline_instance,
            self.tab_inline_instance,
        ]

    tabs = [
        (_("Basic Info"), ["tab-basic-info"]),
        (_("Model Fields"), ["model-field-inlinegroup"]),
        (_("Change Form"), ["model-fieldset-inlinegroup", "model-inline-inlinegroup", "model-changeform-tab-inlinegroup"]),
        (_("Style"), ["tab-style-info"]),
    ]

    fieldsets = [
        (None, {
            "fields": ["parent", "verbose_name", "verbose_name_plural", "title_template"],
            "classes": ["tab-basic-info"],
        }),
        (None, {
            "fields": ["label_width"],
            "classes": ["tab-style-info"],
        })
    ]

class DataInline(InlineModelAdmin):

    def __init__(self, model, parent_model, admin_site, fk_name, definition, extra=0):
        self.model = model
        self.fk_name = fk_name
        self.definition = definition
        self.extra = extra
        super().__init__(parent_model, admin_site)
        self.verbose_name = self.definition.verbose_name
        self.verbose_name_plural = self.definition.get_verbose_name_plural()

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields["definition"] = ModelChoiceField(ModelDefinition.objects, initial=self.definition, widget=forms.HiddenInput())
        fields_map = self.definition.get_fields_map()
        for field_name, field in formset.form.base_fields.items():
            if field_name in fields_map:
                field.label = fields_map[field_name].verbose_name
                field.help_text = fields_map[field_name].help_text
                field.required = fields_map[field_name].required
        return formset

    def get_fieldsets(self, request, obj=None):
        return self.definition.get_fieldsets(["definition"])

class DataTabularInline(admin.TabularInline, DataInline):
    pass

class DataStackedInline(admin.StackedInline, DataInline):
    pass

class DataAbstractAdmin(
        DjangoDynamicResourceAdmin,
        admin.ModelAdmin):

    class Media:
        css = {
            "all": [
                "django-dynamic-model-admin/css/data-admin.css",
            ]
        }
    list_display = ["pk", "title", "definition", "create_time", "update_time"]
    list_filter = [
        ("definition", TreeRelatedFieldListFilter),
    ]

    def get_css(self, request, **kwargs):
        extra_css = super().get_css(request, **kwargs)
        if "object_id" in kwargs and kwargs["object_id"]:
            object_id = int(kwargs["object_id"])
            obj = self.model.objects.get(pk=object_id)
            if obj.definition and obj.definition.label_width:
                extra_css.append(render_to_string("django-dynamic-model-admin/data/data-css.css", {
                    "lable_width": obj.definition.label_width,
                }))
        return extra_css

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        if obj:
            fields_map = obj.definition.get_fields_map()
            field_names = list(form.base_fields.keys())
            for field_name in field_names:
                field = form.base_fields[field_name]
                if field_name in ["definition"]:
                    field.widget = forms.HiddenInput()
                if field_name in fields_map:
                    new_field, new_widget = get_field_widget(self.model, field_name, obj)
                    if new_field:
                        form.base_fields[field_name] = new_field
                        field = new_field
                    field.label = fields_map[field_name].verbose_name
                    field.help_text = fields_map[field_name].help_text
                    field.required = fields_map[field_name].required
                    if new_widget:
                        field.widget = new_widget
        return form
    
    def get_fieldsets(self, request, obj=None):
        if obj:
            return obj.definition.get_fieldsets(["definition"])
        else:
            return [(None, {"fields": ["definition"]})]

    def get_inline_instances(self, request, obj=None):
        inline_instances = []
        if obj:
            for inline in obj.definition.inlines.all():
                if inline.type == inline.TabularInline:
                    instance = DataTabularInline(self.model, self.model, self.admin_site, inline.fk_name, inline.model, inline.extra)
                else:
                    instance = DataStackedInline(self.model, self.model, self.admin_site, inline.fk_name, inline.model, inline.extra)
                inline_instances.append(instance)
        return inline_instances


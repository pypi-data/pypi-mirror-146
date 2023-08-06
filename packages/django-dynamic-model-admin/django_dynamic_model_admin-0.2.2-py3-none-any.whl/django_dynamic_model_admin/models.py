
import yaml
from fastutils import strutils
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from .types import *

class ModelDefinitionAbstractBase(MPTTModel):
    parent = TreeForeignKey("self", on_delete=models.CASCADE, related_name="children", null=True, blank=True, verbose_name=_("Model Definition Category"))
    verbose_name = models.CharField(max_length=64, verbose_name=_("Verbose Name"))
    verbose_name_plural = models.CharField(max_length=64, null=True, blank=True, verbose_name=_("Verbose Name Plural"))
    title_template = models.CharField(max_length=128, null=True, blank=True, verbose_name=_("Title Template"))
    label_width = models.CharField(max_length=32, null=True, blank=True, verbose_name=_("Label Width"), help_text=_("Add unit, e.g. 120px"))

    class Meta:
        verbose_name = _("Model Definition")
        verbose_name_plural = _("Model Definitions")
        abstract = True

    def __str__(self):
        return self.verbose_name

    def get_verbose_name_plural(self):
        if self.verbose_name_plural:
            return self.verbose_name_plural
        else:
            return self.verbose_name

    def get_prefer_name_map(self):
        map = {}
        for field in self.fields.all():
            if field.verbose_name:
                map[field.verbose_name] = field.real_field_name
        return map

    def get_fieldsets(self, extra_fields=None):
        extra_fields = extra_fields or []
        fieldsets = []
        prefer_name_map = self.get_prefer_name_map()
        first = True
        for fieldset in self.fieldsets.all():
            if first:
                fieldsets.append(fieldset.get_fieldset(prefer_name_map, extra_fields))
            else:
                fieldsets.append(fieldset.get_fieldset(prefer_name_map))
            first = False
        return fieldsets

    def get_fields_map(self):
        map = {}
        for field in self.fields.all():
            map[field.real_field_name] = field
        return map

class ModelFieldsetAbstractBase(models.Model):
    name = models.CharField(max_length=64, null=True, blank=True, verbose_name=_("Name"))
    fields = models.TextField(null=True, blank=True, verbose_name=_("Fields"))
    classes = models.CharField(max_length=128, null=True, blank=True, verbose_name=_("Classes"))
    order = models.IntegerField(default=0, verbose_name=_("Order"))

    class Meta:
        verbose_name = _("Model Fieldset")
        verbose_name_plural = _("Model Fieldsets")
        ordering = ["order"]
        abstract = True

    def __str__(self):
        return str(self.pk)

    def get_fieldset(self, prefer_name_map, extra_fields=None):
        fields = [] + (extra_fields or [])
        if self.fields:
            for line in self.fields.splitlines():
                line = line.strip()
                if not line:
                    continue
                field_row = []
                for field in strutils.split(line, [",", "，", "、"]):
                    field = field.strip()
                    if not field:
                        continue
                    real_field_name = prefer_name_map.get(field, None)
                    if not real_field_name:
                        continue
                    field_row.append(real_field_name)
                fields.append(field_row)
        classes = []
        if self.classes:
            for klass in self.classes.split():
                klass = klass.strip()
                if not klass:
                    continue
                classes.append(klass)
        return [self.name, {"fields": fields, "classes": classes}]

class ModelInlineAbstractBase(models.Model):
    TabularInline = 1
    StackedInline = 2
    TYPES = [
        (TabularInline, _("TabularInline")),
        (StackedInline, _("StackedInline")),
    ]
    
    fk_name = models.CharField(max_length=64, verbose_name=_("FK Name"))
    extra = models.IntegerField(default=0, verbose_name=_("Extra Data Number"))
    type = models.IntegerField(default=TabularInline, choices=TYPES, verbose_name=_("Inline Type"))
    order = models.IntegerField(default=0, verbose_name=_("Order"))

    class Meta:
        verbose_name = _("Model Inline")
        verbose_name_plural = _("Model Inlines")
        ordering = ["order"]
        abstract = True

    def __str__(self):
        return self.fk_name

class ModelChangeformTabBase(models.Model):
    title = models.CharField(max_length=64, verbose_name=_("Tab Title"))
    classes = models.CharField(max_length=256, verbose_name=_("Tab Classes"), null=True, blank=True, help_text=_("Seperate with comma sign."))
    order = models.IntegerField(default=0, verbose_name=_("Order"))

    class Meta:
        verbose_name = _("Model Changeform Tab")
        verbose_name_plural = _("Model Changeform Tabs")
        ordering = ["order"]
        abstract = True

    def __str__(self):
        return self.title

class ModelFieldAbstractBase(models.Model):
    real_field_name = models.CharField(max_length=64, verbose_name=_("Real Field Name"))
    field_widget = models.CharField(max_length=64, null=True, blank=True, verbose_name=_("Field Widget"))
    verbose_name = models.CharField(max_length=64, null=True, blank=True, verbose_name=_("Verbose Name"))
    help_text = models.CharField(max_length=512, null=True, blank=True, verbose_name=_("Help Text"))
    required = models.BooleanField(default=False, verbose_name=_("Requried"))
    field_parameters_data = models.TextField(null=True, blank=True, verbose_name=_("Field Parameters"))
    widget_parameters_data = models.TextField(null=True, blank=True, verbose_name=_("Widget Parameters"))

    class Meta:
        abstract = True
        verbose_name = _("Model Field")
        verbose_name_plural = _("Model Fields")
        unique_together = [
            ("definition", "real_field_name"),
        ]

    @property
    def field_parameters(self):
        if not self.field_parameters_data:
            return {}
        else:
            return yaml.safe_load(self.field_parameters_data)

    @property
    def widget_parameters(self):
        if not self.widget_parameters_data:
            return {}
        else:
            return yaml.safe_load(self.widget_parameters_data)

    def __str__(self):
        return self.real_field_name

class DataAbstractBase(models.Model):

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=128, null=True, blank=True, verbose_name=_("Title"))

    class Meta:
        verbose_name = _("Data")
        verbose_name_plural = _("Datas")
        abstract = True

    def __str__(self):
        return self.title or self.get_title()

    def save(self, *args, **kwargs):
        new_title = self.get_title()
        if self.title != new_title:
            self.title = new_title
        return super().save(*args, **kwargs)

    def get_title(self):
        if self.definition and self.definition.title_template:
            title = self.definition.title_template.format(model_name=self.definition.verbose_name, **self.get_prefer_named_data())
        else:
            if self.definition:
                model_name = self.definition.verbose_name
            else:
                model_name = _("Unkown Type")
            if self.pk:
                title = _("{0} (ID={1})").format(model_name, self.pk)
            else:
                title = _("{0} (Draft)").format(model_name)
        return title

    def get_prefer_named_data(self):
        map = self.definition.get_prefer_name_map()
        data = {}
        for prefer_name, real_name in map.items():
            data[prefer_name] = getattr(self, real_name, None)
        return data

    @classmethod
    def get_data_field_choices(cls):
        choices = []
        typed_choices = {}
        for field_type, field_count in cls.field_counts:
            typed_choices[field_type] = []
            choices.append((field_type, typed_choices[field_type]))
        for field_name, info in cls.data_fields.items():
            field_type = info["field_type"]
            typed_choices[field_type].append((field_name, field_name))
        return choices

    @classmethod
    def get_field_widget_optgroups_related(cls):
        optgroups_related = {}
        for field_name, field_info in cls.data_fields.items():
            field_type = field_info["field_type"]
            if not field_type in optgroups_related:
                optgroups_related[field_type] = []
            optgroups_related[field_type] .append(field_name)
        return optgroups_related

    @classmethod
    def get_field_meta(cls, field_name):
        return cls.data_fields[field_name]["field_meta"]

    @classmethod
    def get_field_type(cls, field_name):
        return cls.data_fields[field_name]["field_type"]

def create_data_model(app_label, model_name, ModelDefinition, field_counts):
    check_field_counts(field_counts)
    kwargs = {
        "__module__": app_label + ".models",
        "definition": TreeForeignKey(ModelDefinition, on_delete=models.CASCADE, related_name="data", null=True, blank=True, verbose_name=_("Model Definition")),
        "field_counts": field_counts,
        "data_fields": {}
    }
    for field_type, field_count in field_counts:
        field_meta = get_field_types()[field_type]
        for idx in range(1, field_count + 1):
            field_name = "{prefix}{idx:03d}".format(prefix=field_meta["prefix"], idx=idx)
            field_class = field_meta["field_class"]
            default_field_kwargs = field_meta["field_kwargs"]
            field_kwargs = {}
            field_kwargs.update(default_field_kwargs)
            field = field_class(**field_kwargs)
            kwargs[field_name] = field
            kwargs["data_fields"][field_name] = {
                "field_type": field_type,
                "field_meta": field_meta,
            }
    return type(model_name, (DataAbstractBase,), kwargs)

def create_model_definition(
        app_label,
        definition_model_name="ModelDefinition",
        fieldset_model_name="ModelFieldset",
        inline_model_name="ModelInline",
        tab_model_name="ModelChangeformTab",
        field_model_name="ModelField",
        ):
    # ModelDefinition
    model_definition_kwargs = {
        "__module__": app_label + ".models",
    }
    ModelDefinition = type(definition_model_name, (ModelDefinitionAbstractBase,), model_definition_kwargs)
    # ModelFieldset
    model_fieldset_kwargs = {
        "__module__": app_label + ".models",
        "definition": models.ForeignKey(ModelDefinition, on_delete=models.CASCADE, related_name="fieldsets", verbose_name=_("Definition")),
    }
    ModelFieldset = type(fieldset_model_name, (ModelFieldsetAbstractBase,), model_fieldset_kwargs)
    # ModelInline
    model_inline_kwargs = {
        "__module__": app_label + ".models",
        "definition": models.ForeignKey(ModelDefinition, on_delete=models.CASCADE, related_name="inlines", verbose_name=_("Model Definition")),
        "model": TreeForeignKey(ModelDefinition, on_delete=models.CASCADE, related_name="+", verbose_name=_("Target Model Definition")),
    }
    ModelInline = type(inline_model_name, (ModelInlineAbstractBase,), model_inline_kwargs)
    # ModelChangeformTab
    model_changeform_tab_kwargs = {
        "__module__": app_label + ".models",
        "definition": models.ForeignKey(ModelDefinition, on_delete=models.CASCADE, related_name="tabs", verbose_name=_("Definition")),
    }
    ModelChangeformTab = type(tab_model_name, (ModelChangeformTabBase,), model_changeform_tab_kwargs)
    # ModelField
    model_field_kwargs = {
        "__module__": app_label + ".models",
        "definition": models.ForeignKey(ModelDefinition, on_delete=models.CASCADE, related_name="fields", verbose_name=_("Definition")),
    }
    ModelField = type(field_model_name, (ModelFieldAbstractBase,), model_field_kwargs)
    # return
    return ModelDefinition, ModelFieldset, ModelInline, ModelChangeformTab, ModelField

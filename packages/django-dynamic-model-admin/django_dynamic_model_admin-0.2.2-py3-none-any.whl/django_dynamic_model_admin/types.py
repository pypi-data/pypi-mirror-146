from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_yearmonth_widget.widgets import DjangoYearMonthWidget


CHAR16 = _("CharField_max16")
CHAR16_INDEXED = _("CharField_max16_indexed")
CHAR32 = _("CharField_max32")
CHAR32_INDEXED = _("CharField_max32_indexed")
CHAR64 = _("CharField_max64")
CHAR64_INDEXED = _("CharField_max64_indexed")
CHAR256 = _("CharField_max256")
CHAR256_INDEXED = _("CharField_max256_index")
CHAR1024 = _("CharField_max1024")
CHAR1024_INDEXED = _("CharField_max1024_indexed")
BOOLEAN = _("BooleanField")
BOOLEAN_INDEXED = _("BooleanField_indexed")
NULLABLE_BOOLEAN = _("NullBooleanField")
NULLABLE_BOOLEAN_INDEXED = _("NullBooleanField_indexed")
INTEGER = _("IntegerField")
INTEGER_INDEXED = _("IntegerField_indexed")
BIG_INTEGER = _("BigIntegerField")
BIG_INTEGER_INDEXED = _("BigIntegerField_indexed")
TEXT = _("TextField")
IMAGE = _("ImageField")
FILE = _("FileField")
DATE = _("DateField")
DATE_INDEXED = _("DateField_indexed")
DATETIME = _("DateTimeField")
DATETIME_INDEXED = _("DateTimeField_indexed")
FLOAT = _("FloatField")
FLOAT_INDEXED = _("FloatField_indexed")
DECIMAL = _("DecimalField")
DECIMAL_INDEXED = _("DecimalField_indexed")
FOREIGN_KEY = _("ForeignKey")


CHAR_WIDGETS = [
    (_("TextInput"), forms.TextInput),
    (_("Textarea"), forms.Textarea),
    (_("EmailInput"), forms.EmailInput),
    (_("Select"), forms.Select),
    (_("Year Month Select"), DjangoYearMonthWidget),
]

BOOL_WIDGETS = [
    (_("Yes or No Select"), forms.Select, {"choices": [(1, _("Yes"), (0, _("No")))]}),
    (_("NullBooleanSelect"), forms.NullBooleanSelect),
]

INT_WIDGETS = [
    (_("Select"), forms.Select),
]

TEXT_WIDGETS = [
    (_("TextInput"), forms.TextInput),
    (_("Textarea"), forms.Textarea),
]

UPLOAD_WIDGETS = []

DATETIME_WIDGETS = [
    (_("Year Month Select"), DjangoYearMonthWidget),
]

FLOAT_WIDGETS = []
DECIMAL_WIDGETS = []

def make_char_meta(max_length, db_index):
    return {
        "field_class": models.CharField,
        "field_kwargs": {"max_length": max_length, "null": True, "blank": True, "db_index": db_index},
        "field_size": max_length * 4,
        "db_index": db_index,
        "prefix": "{0}c{1}s".format(db_index and "i" or "", max_length),
        "form_field_class": forms.CharField,
        "form_field_kwargs": {"max_length": max_length},
        "widgets": CHAR_WIDGETS,
    }

def make_bool_meta(nullable, db_index):
    return {
        "field_class": nullable and models.NullBooleanField or models.BooleanField,
        "field_kwargs": {"null": nullable, "blank": nullable, "db_index": db_index, "default": nullable and None or False},
        "field_size": 1,
        "db_index": db_index,
        "prefix": "{0}{1}bool".format(db_index and "i" or "", nullable and "n" or ""),
        "form_field_class": nullable and forms.BooleanField or forms.NullBooleanField,
        "widgets": BOOL_WIDGETS,
    }

def make_int_meta(big, db_index):
    return {
        "field_class": big and models.BigIntegerField or models.IntegerField,
        "field_kwargs": {"null": True, "blank": True, "db_index": db_index},
        "field_size": big and 8 or 4,
        "db_index": db_index,
        "prefix": "{}{}int".format(db_index or "i" or "", big and "b" or ""),
        "widgets": INT_WIDGETS,
    }

def make_text_meta():
    return {
        "field_class": models.TextField,
        "field_kwargs": {"null": True, "blank": True},
        "field_size": 0,
        "db_index": False,
        "prefix": "text",
        "widgets": TEXT_WIDGETS,
    }

def make_upload_meta(image):
    return {
        "field_class": image and models.ImageField or models.FileField,
        "field_kwargs": {"upload_to": image and "images" or "files", "null": True, "blank": True},
        "field_size": 4 * 100,
        "db_index": False,
        "prefix": image and "img" or "file",
        "widgets": UPLOAD_WIDGETS,
    }

def make_datetime_meta(datetime, db_index):
    return {
        "field_class": datetime and models.DateTimeField or models.DateField,
        "field_kwargs": {"null": True, "blank": True, "db_index": db_index},
        "field_size": datetime and 8 or 3,
        "db_index": db_index,
        "prefix": "{0}{1}".format(db_index and "1" or "", datetime and "datetime" or "date"),
        "widgets": DATETIME_WIDGETS,
    }

def make_float_meta(db_index):
    return {
        "field_class": models.FloatField,
        "field_kwargs": {"null": True, "blank": True, "db_index": db_index},
        "field_size": 8,
        "db_index": db_index,
        "prefix": "{0}float".format(db_index and "1" or ""),
        "widgets": FLOAT_WIDGETS,
    }

def make_decimal_meta(db_index):
    return {
        "field_class": models.DecimalField,
        "field_kwargs": {"max_digits": 19, "decimal_places": 6, "null": True, "blank": True, "db_index": db_index},
        "field_size": 8,
        "db_index": db_index,
        "prefix": "{0}decimal".format(db_index and "1" or ""),
        "widgets": DECIMAL_WIDGETS,
    }

def make_foreign_key_meta():
    return {
        "field_class": models.ForeignKey,
        "field_kwargs": {"to": "self", "on_delete": models.SET_NULL, "null": True, "blank": True, "related_name": "+"},
        "field_size": 4,
        "db_index": True,
        "prefix": "fk",
        "widgets": []
    }


FIELD_TYPES = {
    CHAR16: make_char_meta(16, False),
    CHAR16_INDEXED: make_char_meta(16, True),
    CHAR32: make_char_meta(32, False),
    CHAR32_INDEXED: make_char_meta(32, True),
    CHAR64: make_char_meta(64, False),
    CHAR64_INDEXED: make_char_meta(64, True),
    CHAR256: make_char_meta(256, False),
    CHAR256_INDEXED: make_char_meta(256, True),
    CHAR1024: make_char_meta(1024, False),
    CHAR1024_INDEXED: make_char_meta(1024, True),
    BOOLEAN: make_bool_meta(False, False),
    BOOLEAN_INDEXED: make_bool_meta(False, True),
    NULLABLE_BOOLEAN: make_bool_meta(True, False),
    NULLABLE_BOOLEAN_INDEXED: make_bool_meta(True, True),
    INTEGER: make_int_meta(False, False),
    INTEGER_INDEXED: make_int_meta(False, True),
    BIG_INTEGER: make_int_meta(True, False),
    BIG_INTEGER_INDEXED: make_int_meta(True, True),
    TEXT: make_text_meta(),
    IMAGE: make_upload_meta(True),
    FILE: make_upload_meta(False),
    DATE: make_datetime_meta(False, False),
    DATE_INDEXED: make_datetime_meta(False, True),
    DATETIME: make_datetime_meta(True, False),
    DATETIME_INDEXED: make_datetime_meta(True, True),
    FLOAT: make_float_meta(False),
    FLOAT_INDEXED: make_float_meta(True),
    DECIMAL: make_decimal_meta(False),
    DECIMAL_INDEXED: make_decimal_meta(True),
    FOREIGN_KEY: make_foreign_key_meta(),
}

def check_field_types_prefix():
    prefixes = []
    for field_name, field_meta in FIELD_TYPES.items():
        prefix = field_meta["prefix"]
        if prefix in prefixes:
            raise RuntimeError("Field Prefix already used: {0}.".format(prefix))
        prefixes.append(prefix)
    return True

check_field_types_prefix()

SIMPLE_DATA_MODEL_FIELDS = [
    (CHAR16, 15),
    (CHAR16_INDEXED, 5),
    (CHAR32, 15),
    (CHAR32_INDEXED, 5),
    (CHAR64, 15),
    (CHAR64_INDEXED, 5),
    (CHAR256, 20),
    (CHAR1024, 5),
    (BOOLEAN, 20),
    (NULLABLE_BOOLEAN, 20),
    (TEXT, 20),
    (IMAGE, 10),
    (FILE, 10),
    (INTEGER, 50),
    (INTEGER_INDEXED, 5),
    (BIG_INTEGER, 50),
    (BIG_INTEGER_INDEXED, 5),
    (DATE, 15),
    (DATE_INDEXED, 5),
    (DATETIME, 15),
    (DATETIME_INDEXED, 5),
    (FLOAT, 15),
    (FLOAT_INDEXED, 5),
    (DECIMAL, 15),
    (DECIMAL_INDEXED, 5),
    (FOREIGN_KEY, 10),
]

MAX_ROW_SIZE = 65535
MAX_INDEX_COUNT = 64
MAX_INDEX_SIZE = 3072

def get_row_size(fields):
    return sum(FIELD_TYPES[x]["field_size"] * y for x, y in fields)

def get_index_count(fields):
    counter = 0
    for field_type, count in fields:
        if FIELD_TYPES[field_type]["db_index"]:
            counter += count
    return counter

def get_index_size(fields):
    size = 0
    for field_type, count in fields:
        if FIELD_TYPES[field_type]["db_index"]:
            size += FIELD_TYPES[field_type]["field_size"] * count
    return size

def check_field_counts(field_counts):
    row_size = get_row_size(field_counts)
    if row_size > MAX_ROW_SIZE:
        raise RuntimeError("Row size too large: {0}. The maximum row size for the used table type, not counting BLOBs, is 65535. This includes storage overhead, check the manual. You have to change some columns to TEXT or BLOBs.".format(row_size))
    index_count = get_index_count(field_counts)
    if index_count >= MAX_INDEX_COUNT:
        raise RuntimeError("Too many keys specified: {0}; max 64 keys allowed.".format(index_count))
    index_size = get_index_size(field_counts)
    if index_size >= MAX_INDEX_SIZE:
        raise RuntimeError("Specified key was too long: {0}; max key length is 3072 bytes.".format(index_size))

def get_field_widget_choices():
    choices = []
    for field_name, field_meta in FIELD_TYPES.items():
        typed_choices = []
        for widget_meta in field_meta["widgets"]:
            widget_name = widget_meta[0]
            typed_choices.append((widget_name, widget_name))
        choices.append((field_name, typed_choices))
    return choices


def get_field_widget(data_model, real_field_name, obj):
    model_field = obj.definition.fields.get(real_field_name=real_field_name)
    field_meta = data_model.get_field_meta(real_field_name)
    form_field_class = field_meta.get("form_field_class", None)
    if form_field_class:
        default_form_field_kwargs = field_meta.get("form_field_kwargs", {})
        form_field_kwargs = {}
        form_field_kwargs.update(default_form_field_kwargs)
        form_field_kwargs.update(model_field.field_parameters)
        field = form_field_class(**form_field_kwargs)
    else:
        field = None
    widget = None
    for widget_meta in field_meta["widgets"]:
        widget_name = widget_meta[0]
        if widget_name == model_field.field_widget:
            widget_class = widget_meta[1]
            if len(widget_meta) > 2:
                widget_extra_kwargs = widget_meta[2]
            else:
                widget_extra_kwargs = {}
            kwargs = {}
            kwargs.update(widget_extra_kwargs)
            kwargs.update(model_field.widget_parameters)
            widget = widget_class(**kwargs)
    return field, widget

def get_field_types():
    return FIELD_TYPES

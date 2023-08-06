from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DjangoDynamicModelAdminConfig(AppConfig):
    name = 'django_dynamic_model_admin'
    verbose_name = _("Django Dynamic Model Admin")

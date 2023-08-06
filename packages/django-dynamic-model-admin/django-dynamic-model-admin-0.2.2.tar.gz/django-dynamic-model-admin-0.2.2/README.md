# django-dynamic-model-admin

Define new type model in Django's admin site. New type model can be managed in admin site, and also provide the auto generated ModelForm.

## Install

```shell
pip install django-dynamic-model-admin
```

## Releases

### v0.2.2

1. Clean not used imports.

### v0.2.1

1. Add changeform-tab manager.
1. Use cascading-dropdown widget for real_field_name in ModelDefinitionAdmin.
1. Add custom model names in create_model_definition function.


### v0.2.0

1. Turn all models and admin sites to abstract class, so that it can be used multiple times.
1. Simplify the management, only keep model-definition-management and data management.

### v0.1.0

1. First release.
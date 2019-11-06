from django.apps import AppConfig


class ApiAppConfig(AppConfig):
    name = 'api'
    label = 'api'
    verbose_name = 'Api'

    def ready(self):
        import api.signals

# Django checksfor the `default_app_config` property of each registered app
# and use the correct app config based on that value.
default_app_config = 'api.ApiAppConfig'

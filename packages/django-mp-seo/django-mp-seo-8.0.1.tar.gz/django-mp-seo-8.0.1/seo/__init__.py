
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


def setup_settings(settings, **kwargs):

    settings['MIDDLEWARE'] += [
        'seo.middleware.PageMetaMiddleware'
    ]

    settings['INSTALLED_APPS'] += [
        app for app in [
            'sitemetrics',
            'seo'
        ] if app not in settings['INSTALLED_APPS']
    ]


class SeoConfig(AppConfig):
    name = 'seo'
    verbose_name = _("SEO")


default_app_config = 'seo.SeoConfig'

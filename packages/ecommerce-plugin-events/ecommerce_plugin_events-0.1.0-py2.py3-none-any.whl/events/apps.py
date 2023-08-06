"""
events Django application initialization.
"""

from django.apps import AppConfig
from edx_django_utils.plugins.constants import PluginSettings


class EventsConfig(AppConfig):
    """
    Configuration for the events Django application.
    """

    name = 'events'

    plugin_app = {
        PluginSettings.CONFIG: {
            'ecommerce.djangoapp': {
                'common': {
                    PluginSettings.RELATIVE_PATH: 'settings.common',
                },
                'devstack': {
                    PluginSettings.RELATIVE_PATH: 'settings.devstack',
                },
                'production': {
                    PluginSettings.RELATIVE_PATH: 'settings.production',
                },
            }
        }
    }

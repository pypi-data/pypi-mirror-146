"""
Devstack settings values.
"""


def plugin_settings(settings):
    """
    Default settings values.
    """
    settings.KAFKA_BOOTSTRAP_SERVER = 'edx.devstack.kafka:29092'
    settings.SCHEMA_REGISTRY_URL = 'http://edx.devstack.schema-registry:8081'
    settings.SCHEMA_REGISTRY_API_KEY = ''
    settings.SCHEMA_REGISTRY_API_SECRET = ''
    settings.KAFKA_API_KEY = ''
    settings.KAFKA_API_SECRET = ''

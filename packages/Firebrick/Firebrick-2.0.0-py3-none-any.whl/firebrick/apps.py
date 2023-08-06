from django.apps import AppConfig
from firebrick.database import get_or_404
from firebrick.tests import asserts


class FirebrickConfig(AppConfig):
    name = 'firebrick'
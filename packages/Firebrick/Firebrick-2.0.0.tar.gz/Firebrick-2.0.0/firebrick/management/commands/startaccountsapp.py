from django.core.management.base import BaseCommand, CommandError
from firebrick.templates.templating import GenerateFromTemplate, TemplateFromFiles
import argparse
import os


class Command(BaseCommand):
    help = 'Creates a firebrick accounts app in your django project.'
    
    def add_arguments(self, parser):
        parser.add_argument('-t', '--template', action=argparse.BooleanOptionalAction)
    
    def handle(self, template, *args, **options):
        GenerateFromTemplate(
            [
                TemplateFromFiles('accounts', base_local_path='accounts'),
                TemplateFromFiles('accounts_templates', base_local_path=os.path.join('accounts', 'templates', 'accounts'))
            ] if template else [
                TemplateFromFiles('accounts', base_local_path='accounts'),
            ]
        )
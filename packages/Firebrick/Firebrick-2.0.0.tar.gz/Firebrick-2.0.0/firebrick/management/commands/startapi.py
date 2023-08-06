from django.core.management.base import BaseCommand, CommandError
from django.core.management.templates import TemplateCommand
from firebrick.templates.templating import GenerateFromTemplate, TemplateFromFiles
import os


class Command(BaseCommand):
    help = 'Creates a firebrick api app.'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str)
    
    def handle(self, name, *args, **options):
        # Making a instance of the `TemplateCommand` class to use the `validate_name` function
        django_command_template = TemplateCommand()
        django_command_template.a_or_an = 'an'
        django_command_template.app_or_project = 'project'
        
        django_command_template.validate_name(name)
        # Check if the api dir exists if not make it
        if not os.path.isdir(os.path.join(os.getcwd(), 'api')):
            os.mkdir(os.path.join(os.getcwd(), 'api'))
            with open(os.path.join(os.getcwd(), 'api', '__init__.py'), 'w') as f:
                pass
        
        GenerateFromTemplate(
            [
                TemplateFromFiles('api', base_local_path=os.path.join('api', name))
            ],
            context={
                '{{appconfig-name}}': name.capitalize(),
                '{{name}}': name
            }
        )
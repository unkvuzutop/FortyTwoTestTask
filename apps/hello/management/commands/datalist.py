from django.core.management.base import BaseCommand
from django.db.models import get_app, get_models


class Command(BaseCommand):
    args = 'app name is needed'
    help = 'Return list of appp models and count objects.'

    def handle(self, app, **options):
        app = get_app(app)

        for model in get_models(app):
            try:
                message = 'Model name - {0}, have {1} objects'\
                    .format(model.__name__, model.objects.count())
            except Exception as e:
                self.stdout.write(e)

            self.stdout.write(message)
            self.stderr.write('error: '+message)

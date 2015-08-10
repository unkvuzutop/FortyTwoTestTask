import logging
from django.core.management.base import BaseCommand
from django.db.models import get_app, get_models
import sys

logger = logging.getLogger(__name__)


class InfoFilter(logging.Filter):
    def filter(self, rec):
        return rec.levelno in (logging.INFO,)


class Command(BaseCommand):
    args = 'app name is needed'
    help = 'Return list of appp models and count objects.'

    def handle(self, app, **options):
        app = get_app(app)

        handler = logging.StreamHandler(sys.stderr)
        handler.setLevel(logging.INFO)
        handler.addFilter(InfoFilter())
        handler.setFormatter(logging.Formatter('error: %(message)s'))

        logger.addHandler(handler)

        for model in get_models(app):
            message = 'Model name - {0}, have {1} objects'\
                .format(model.__name__, model.objects.count())
            logger.info(message)

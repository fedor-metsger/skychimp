
from django.core.management import BaseCommand

from crontab.manager import run

class Command(BaseCommand):
    def handle(self, *args, **options):
        run()

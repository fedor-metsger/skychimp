
from django.core.management import BaseCommand

from mailing.crontab import EmailManager

class Command(BaseCommand):
    def handle(self, *args, **options):

        EmailManager.run_sending()

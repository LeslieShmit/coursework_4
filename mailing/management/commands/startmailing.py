from django.core.management.base import BaseCommand, CommandError

from mailing.models import Mailing
from mailing.services import send_mailing

class Command(BaseCommand):
    help = 'Start a mailing with a given pk'

    def add_arguments(self, parser):
        parser.add_argument('pk', type=int, help='ID of the mailing to start')

    def handle(self, *args, **options):
        pk = options['pk']
        try:
            mailing = Mailing.objects.get(pk=pk)
        except Mailing.DoesNotExist:
            raise CommandError(f"Mailing with id={pk} does not exist")
        send_mailing(mailing)
        self.stdout.write(self.style.SUCCESS(f'Mailing with title {mailing.message.title} has been successfully sent'))
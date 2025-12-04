from django.core.management.base import BaseCommand
from modelTamrin.tasks import add

class Command(BaseCommand):
    help = 'Test the add task by calling it synchronously and printing the result'

    def handle(self, *args, **options):
        result = add.apply(args=(10, 20)).get()
        self.stdout.write(self.style.SUCCESS(f'Result of add(10, 20): {result}'))
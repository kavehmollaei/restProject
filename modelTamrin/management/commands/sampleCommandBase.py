from typing import Any
from django.core.management.base import BaseCommand
class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('name', type=str)
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        print("fffffffffffffffffffffffff")
        self.stdout.write("Helloppppppp")
        name=options['name']
        print(name)

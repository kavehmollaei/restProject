from django.core.management.base import BaseCommand
from modelTamrin.models import NetworkInterface
from datetime import datetime

class Command(BaseCommand):
    help = 'Add sample network interfaces to the database'

    def handle(self, *args, **options):
        interfaces = [
            {
                'name': 'eth0',
                'mac_address': '00:0a:95:9d:68:16',
                'ip_address': '192.168.1.10',
                'status': True,
                'mtu': 1500,
                'interface_type': 'ethernet'
            },
            {
                'name': 'wlan0',
                'mac_address': '00:0b:86:a2:4f:1c',
                'ip_address': '192.168.1.20',
                'status': True,
                'mtu': 1500,
                'interface_type': 'wireless'
            },
            {
                'name': 'lo',
                'mac_address': '00:00:00:00:00:00',
                'ip_address': '127.0.0.1',
                'status': True,
                'mtu': 65536,
                'interface_type': 'virtual'
            },
            {
                'name': 'docker0',
                'mac_address': '02:42:ac:11:00:02',
                'ip_address': '172.17.0.1',
                'status': False,
                'mtu': 1500,
                'interface_type': 'virtual'
            }
        ]

        for data in interfaces:
            NetworkInterface.objects.create(**data)

        self.stdout.write(self.style.SUCCESS('Successfully added sample network interfaces'))

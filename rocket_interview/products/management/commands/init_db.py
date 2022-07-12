import json
from django.core.management.base import BaseCommand
from products.models import Product, Cart


class Command(BaseCommand):
    help = 'Initialize database from json file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str)

    def handle(self, *args, **options):
        with open(options['json_file']) as f:
            data_list = json.load(f)

        Product.objects.all().delete()
        Cart.objects.all().delete()

        for data in data_list:
            data['id'] = data.pop('id')
            Product.objects.get_or_create(id=data['id'], defaults=data)

        Cart.objects.create()

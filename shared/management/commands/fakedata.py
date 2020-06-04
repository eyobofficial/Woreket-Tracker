import random

from django.core.management import BaseCommand

from purchases.tests.factories import SupplierFactory, ProductCategoryFactory, \
    ProductFactory, BatchFactory


class Command(BaseCommand):
    help = 'Create fake data for development.'

    def handle(self, *args, **kwargs):
        suppliers = SupplierFactory.create_batch(5)
        product_categories = ProductCategoryFactory.create_batch(5)

        products = []
        for _ in range(10):
            category = random.choice(product_categories)
            product = ProductFactory(category=category)
            products.append(product)

        for _ in range(20):
            product = random.choice(products)
            supplier = random.choice(suppliers)
            BatchFactory(product=product, supplier=supplier)

        self.stdout.write('Database is populated with fake data.')

from random import uniform, choice

import factory

from shared.models import Unit

from purchases.models import Supplier, Product, ProductCategory, Batch


class SupplierFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'Supplier {n}')
    city = factory.Faker('city')
    country = factory.Faker('country_code')

    class Meta:
        model = Supplier


class ProductCategoryFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'Product Category {n}')

    class Meta:
        model = ProductCategory


class ProductFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'Product {n}')
    category = factory.SubFactory(ProductCategoryFactory)
    unit = factory.LazyFunction(lambda: choice(Unit.objects.all()))

    class Meta:
        model = Product


class BatchFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'LOT {n}')
    lc_number = factory.Sequence(lambda n: f'LC{n}')
    product = factory.SubFactory(ProductFactory)
    supplier = factory.SubFactory(SupplierFactory)
    quantity = factory.LazyFunction(lambda: round(uniform(1000, 50000), 2))
    rate = factory.LazyFunction(lambda: round(uniform(50, 300), 2))
    year = factory.LazyFunction(lambda: choice(Batch.YEAR_CHOICES)[0])

    class Meta:
        model = Batch


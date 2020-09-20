import factory
import random

from customers.tests.factories import CustomerFactory, LocationFactory, \
    UnionFactory
from purchases.tests.factories import ProductFactory, SupplierFactory
from orders.models import Batch, UnionDistribution, DeliveryOrder, Allocation, \
    UnionAllocation, Distribution, UnionDistribution


class BatchFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'Batch {n}')
    lc_number = factory.Sequence(lambda n: f'lc_number{n}')
    product = factory.SubFactory(ProductFactory)
    supplier = factory.SubFactory(SupplierFactory)
    year = factory.LazyFunction(lambda: random.choice(Batch.YEAR_CHOICES)[0])
    quantity = 0
    rate = 0

    class Meta:
        model = Batch


class DeliveryOrderFactory(factory.django.DjangoModelFactory):
    batch = factory.SubFactory(BatchFactory)
    vessel = factory.Sequence(lambda n: f'Vessel {n}')
    bill_of_loading = factory.Sequence(lambda n: f'bill_of_loading{n}')
    arrival_date = factory.Faker('date_this_decade')

    class Meta:
        model = DeliveryOrder


class AllocationFactory(factory.django.DjangoModelFactory):
    delivery_order = factory.SubFactory(DeliveryOrderFactory)
    buyer = factory.SubFactory(CustomerFactory)

    class Meta:
        model = Allocation


class UnionAllocationFactory(factory.django.DjangoModelFactory):
    allocation = factory.SubFactory(AllocationFactory)
    union = factory.SubFactory(UnionFactory)
    location = factory.SubFactory(LocationFactory)
    quantity = 0

    class Meta:
        model = UnionAllocation


class DistributionFactory(factory.django.DjangoModelFactory):
    delivery_order = factory.SubFactory(DeliveryOrderFactory)
    buyer = factory.SubFactory(CustomerFactory)

    class Meta:
        model = Distribution


class UnionDistributionFactory(factory.django.DjangoModelFactory):
    distribution = factory.SubFactory(DistributionFactory)
    union = factory.SubFactory(UnionFactory)
    location = factory.SubFactory(LocationFactory)
    quantity = 0
    shortage = 0
    over = 0

    class Meta:
        model = UnionDistribution

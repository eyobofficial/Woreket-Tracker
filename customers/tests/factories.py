import random
import factory

from customers.models import Union, Customer, Location


class CustomerFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'Customer {n}')
    region = factory.Sequence(lambda n: f'Region {n}')
    code = factory.Sequence(lambda n: f'c{n}')

    class Meta:
        model = Customer


class UnionFactory(factory.django.DjangoModelFactory):
    name = factory.LazyAttributeSequence(
        lambda obj, n: f'{obj.customer.region} union {n}'
    )
    customer = factory.LazyFunction(
        lambda: random.choice(Customer.objects.all())
    )

    class Meta:
        model = Union


class LocationFactory(factory.django.DjangoModelFactory):
    name = factory.LazyAttributeSequence(
        lambda obj, n: f'{obj.customer.region} location {n}'
    )
    customer = factory.LazyFunction(
        lambda: random.choice(Customer.objects.all())
    )

    class Meta:
        model = Location

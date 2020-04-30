import random
import factory

from customers.models import Union, Customer


class UnionFactory(factory.django.DjangoModelFactory):
    name = factory.LazyAttributeSequence(
        lambda obj, n: f'{obj.customer.region} union {n}'
    )
    customer = factory.LazyFunction(
        lambda: random.choice(Customer.objects.all())
    )

    class Meta:
        model = Union


import random
import factory

from customers.models import Union, Customer


class UnionFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'Union {n}')
    customer = factory.LazyFunction(
        lambda: random.choice(Customer.objects.all())
    )

    class Meta:
        model = Union


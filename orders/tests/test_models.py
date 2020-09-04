from decimal import Decimal

from django.test import TestCase

from purchases.tests.factories import ProductFactory
from .factories import BatchFactory, DeliveryOrderFactory, AllocationFactory, \
    UnionAllocationFactory, DistributionFactory, UnionDistributionFactory


class BatchModelTests(TestCase):
    """
    Tests for the `Batch` model.
    """
    fixtures = ['units']

    def setUp(self):
        self.batch = BatchFactory(name='Test batch', quantity=100, rate=50)

        # Delivery Order 1
        delivery_order_1 = DeliveryOrderFactory(batch=self.batch)
        allocation_1_1 = AllocationFactory(delivery_order=delivery_order_1)
        UnionAllocationFactory(allocation=allocation_1_1, quantity=10)
        UnionAllocationFactory(allocation=allocation_1_1, quantity=20)

        allocation_1_2 = AllocationFactory(delivery_order=delivery_order_1)
        UnionAllocationFactory(allocation=allocation_1_2, quantity=30)
        UnionAllocationFactory(allocation=allocation_1_2, quantity=40)

        # Delivery Order 2
        delivery_order_2 = DeliveryOrderFactory(batch=self.batch)
        allocation_2_1 = AllocationFactory(delivery_order=delivery_order_2)
        UnionAllocationFactory(allocation=allocation_2_1, quantity=50)
        UnionAllocationFactory(allocation=allocation_2_1, quantity=60)

        allocation_2_2 = AllocationFactory(delivery_order=delivery_order_2)
        UnionAllocationFactory(allocation=allocation_2_2, quantity=70)
        UnionAllocationFactory(allocation=allocation_2_2, quantity=80)

    def test_get_agreement_amount_method(self):
        """
        Ensure `get_agreement_amount` method returns the multiplication
        of `quantity` and `rate`.
        """
        self.assertEqual(self.batch.get_agreement_amount(), 5000.0000)

    # def test_get_allocated_quantity_method(self):
    #     """
    #     Ensure `get_allocated_quantity` method returns the total allocated
    #     quantities in the product unit.
    #     """
    #     self.assertEqual(self.batch.get_allocated_quantity(), Decimal('360.0000'))

    # def test_get_allocated_amount_method(self):
    #     """
    #     Ensure `get_allocated_amount` method returns the total allocated
    #     amount in monetary currency.
    #     """
    #     self.assertEqual(
    #         self.batch.get_allocated_amount(),
    #         Decimal('18000.0000')
    #     )

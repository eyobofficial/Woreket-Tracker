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

        distribution_1_1 = DistributionFactory(delivery_order=delivery_order_1)
        UnionDistributionFactory(
            distribution=distribution_1_1,
            quantity=10, shortage=1, over=2
        )
        UnionDistributionFactory(
            distribution=distribution_1_1,
            quantity=20, shortage=1, over=2
        )

        allocation_1_2 = AllocationFactory(delivery_order=delivery_order_1)
        UnionAllocationFactory(allocation=allocation_1_2, quantity=30)
        UnionAllocationFactory(allocation=allocation_1_2, quantity=40)

        distribution_1_2 = DistributionFactory(delivery_order=delivery_order_1)
        UnionDistributionFactory(
            distribution=distribution_1_2,
            quantity=10, shortage=1, over=2
        )
        UnionDistributionFactory(
            distribution=distribution_1_2,
            quantity=20, shortage=1, over=2
        )

        # Delivery Order 2
        delivery_order_2 = DeliveryOrderFactory(batch=self.batch)
        allocation_2_1 = AllocationFactory(delivery_order=delivery_order_2)
        UnionAllocationFactory(allocation=allocation_2_1, quantity=50)
        UnionAllocationFactory(allocation=allocation_2_1, quantity=60)

        distribution_2_1 = DistributionFactory(delivery_order=delivery_order_2)
        UnionDistributionFactory(
            distribution=distribution_2_1,
            quantity=10, shortage=1, over=2
        )
        UnionDistributionFactory(
            distribution=distribution_2_1,
            quantity=20, shortage=1, over=2
        )

        allocation_2_2 = AllocationFactory(delivery_order=delivery_order_2)
        UnionAllocationFactory(allocation=allocation_2_2, quantity=70)
        UnionAllocationFactory(allocation=allocation_2_2, quantity=80)

        distribution_2_2 = DistributionFactory(delivery_order=delivery_order_2)
        UnionDistributionFactory(
            distribution=distribution_2_2,
            quantity=10, shortage=1, over=2
        )
        UnionDistributionFactory(
            distribution=distribution_2_2,
            quantity=20, shortage=1, over=2
        )

    def test_get_agreement_amount_method(self):
        """
        Ensure `get_agreement_amount` method returns the multiplication
        of `quantity` and `rate`.
        """
        self.assertEqual(self.batch.get_agreement_amount(), 5000.0000)

    def test_get_allocated_quantity_method(self):
        """
        Ensure `get_allocated_quantity` method returns the total allocated
        quantities in the product unit.
        """
        self.assertEqual(self.batch.get_allocated_quantity(), Decimal('360.0000'))

    def test_get_allocated_amount_method(self):
        """
        Ensure `get_allocated_amount` method returns the total allocated
        amount in monetary currency.
        """
        expected_amount = Decimal('18000.0000')
        self.assertEqual(self.batch.get_allocated_amount(), expected_amount)

    def test_get_advance_amount_method(self):
        """
        Ensure `get_advance_amount` method returns 90% of the total
        allocated amount for the batch.
        """
        expected_amount = Decimal('16200.0000')
        self.assertEqual(self.batch.get_advance_amount(), expected_amount)

    def test_get_retention_amount_method(self):
        """
        Ensure `get_retention_amount` method returns 10% of the total
        allocated amount for the batch.
        """
        expected_amount = Decimal('1800.0000')
        self.assertEqual(self.batch.get_retention_amount(), expected_amount)

    def test_get_distributed_quantity_method(self):
        """
        Ensure `get_distributed_quantity` method returns the total distributed
        quantities in the product unit.
        """
        expected_quantity = Decimal('144.0000')
        self.assertEqual(
            self.batch.get_distributed_quantity(),
            expected_quantity
        )

    def test_get_distributed_shortage_method(self):
        """
        Ensure `get_distributed_shortage` method returns the total distributed
        shortage (shortage + over quantity) in the product unit.
        """
        expected_quantity = Decimal('24.0000')
        self.assertEqual(
            self.batch.get_distributed_shortage(),
            expected_quantity
        )

    def test_get_distributed_amount_method(self):
        """
        Ensure `get_distributed_amount` method returns the total distributed
        amount in monetary currency.
        """
        expected_amount = Decimal('7200.0000')
        self.assertEqual(self.batch.get_distributed_amount(), expected_amount)

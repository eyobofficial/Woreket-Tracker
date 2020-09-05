from decimal import Decimal

from django.test import TestCase

from customers.tests.factories import CustomerFactory
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


class DeliveryOrderTests(TestCase):
    """
    Tests for the `DeliveryOrder` model methods.
    """
    fixtures = ['units']

    def setUp(self):
        batch = BatchFactory(rate=5)
        self.delivery_order = DeliveryOrderFactory(batch=batch)

        # Create customers
        self.customer_1 = CustomerFactory()
        self.customer_2 = CustomerFactory()
        self.customer_3 = CustomerFactory()

    def test_is_fully_allocated_method_no_allocation(self):
        """
        Ensure `is_fully_allocated` method returns `False` when a
        delivery_order instance has no allocation.
        """
        self.assertFalse(self.delivery_order.is_fully_allocated())


    def test_is_fully_allocated_method_with_partial_allocations(self):
        """
        Ensure `is_fully_allocated` method returns `False` when a
        delivery order instance is only partially allocated.
        """
        AllocationFactory(
            delivery_order=self.delivery_order,
            buyer=self.customer_1
        )
        self.assertFalse(self.delivery_order.is_fully_allocated())

    def test_is_fully_allocated_method_with_fully_allocated_order(self):
        """
        Ensure `is_fully_allocated` method returns `True` when a
        delivery order instance is fully allocated.
        """
        AllocationFactory(
            delivery_order=self.delivery_order,
            buyer=self.customer_1
        )
        AllocationFactory(
            delivery_order=self.delivery_order,
            buyer=self.customer_2
        )
        AllocationFactory(
            delivery_order=self.delivery_order,
            buyer=self.customer_3
        )
        self.assertTrue(self.delivery_order.is_fully_allocated())

    def test_is_fully_distributed_method_no_distribution(self):
        """
        Ensure `is_fully_distributed` method returns `False` when a
        delivery_order instance has no distribution.
        """
        self.assertFalse(self.delivery_order.is_fully_distributed())

    def test_is_fully_distributed_method_with_partial_distribution(self):
        """
        Ensure `is_fully_distributed` method returns `False` when a
        delivery order instance is only partially distributed.
        """
        DistributionFactory(
            delivery_order=self.delivery_order,
            buyer=self.customer_1
        )
        self.assertFalse(self.delivery_order.is_fully_distributed())

    def test_is_fully_distributed_method_with_fully_distributed_order(self):
        """
        Ensure `is_fully_distributed` method returns `True` when a
        delivery order instance is fully distributed.
        """
        DistributionFactory(
            delivery_order=self.delivery_order,
            buyer=self.customer_1
        )
        DistributionFactory(
            delivery_order=self.delivery_order,
            buyer=self.customer_2
        )
        DistributionFactory(
            delivery_order=self.delivery_order,
            buyer=self.customer_3
        )
        self.assertTrue(self.delivery_order.is_fully_distributed())

    def test_get_allocated_quantity_method(self):
        """
        Ensure `get_allocated_quantity` method returns the total allocated
        quantity of related unions.
        """
        allocation_1 = AllocationFactory(delivery_order=self.delivery_order)
        UnionAllocationFactory(allocation=allocation_1, quantity=10)
        UnionAllocationFactory(allocation=allocation_1, quantity=20)

        expected_quantity = Decimal('30.0000')
        self.assertEqual(
            self.delivery_order.get_allocated_quantity(),
            expected_quantity
        )

    def test_get_distributed_quantity_method(self):
        """
        Ensure `get_distributed_quantity` method returns the total distributed
        quantity of related unions.
        """
        distribution_1 = DistributionFactory(delivery_order=self.delivery_order)
        UnionDistributionFactory(
            distribution=distribution_1,
            quantity=10, shortage=1, over=2
        )
        UnionDistributionFactory(
            distribution=distribution_1,
            quantity=20, shortage=3, over=4
        )

        expected_quantity = Decimal('40.0000')
        self.assertEqual(
            self.delivery_order.get_distributed_quantity(),
            expected_quantity
        )

    def test_get_distributed_shortage_method(self):
        """
        Ensure `get_distributed_shortage` method returns the total distributed
        shortage quantity of related unions.
        """
        distribution_1 = DistributionFactory(delivery_order=self.delivery_order)
        UnionDistributionFactory(
            distribution=distribution_1,
            quantity=10, shortage=1, over=2
        )
        UnionDistributionFactory(
            distribution=distribution_1,
            quantity=20, shortage=3, over=4
        )

        expected_quantity = Decimal('10.0000')
        self.assertEqual(
            self.delivery_order.get_distributed_shortage(),
            expected_quantity
        )

    def test_get_allocated_amount_method(self):
        """
        Ensure `get_allocated_amount` method returns the total allocated
        amount of related unions.
        """
        allocation_1 = AllocationFactory(delivery_order=self.delivery_order)
        UnionAllocationFactory(allocation=allocation_1, quantity=10)
        UnionAllocationFactory(allocation=allocation_1, quantity=20)

        expected_amount = Decimal('150.0000')
        self.assertEqual(
            self.delivery_order.get_allocated_amount(),
            expected_amount
        )

    def test_get_allocated_advance_method(self):
        """
        Ensure `get_allocated_advance` method returns 90% of the total
        allocated amount of related unions.
        """
        allocation_1 = AllocationFactory(delivery_order=self.delivery_order)
        UnionAllocationFactory(allocation=allocation_1, quantity=10)
        UnionAllocationFactory(allocation=allocation_1, quantity=20)

        expected_advance = Decimal('135.0000')
        self.assertEqual(
            self.delivery_order.get_allocated_advance(),
            expected_advance
        )

    def test_get_allocated_retention_method(self):
        """
        Ensure `get_allocated_retention` method returns 10% of the total
        allocated amount of related unions.
        """
        allocation_1 = AllocationFactory(delivery_order=self.delivery_order)
        UnionAllocationFactory(allocation=allocation_1, quantity=10)
        UnionAllocationFactory(allocation=allocation_1, quantity=20)

        expected_retention = Decimal('15.0000')
        self.assertEqual(
            self.delivery_order.get_allocated_retention(),
            expected_retention
        )

    def test_get_distributed_amount_method(self):
        """
        Ensure `get_distributed_amount` method returns the total distributed
        amount of related unions.
        """
        distribution_1 = DistributionFactory(delivery_order=self.delivery_order)
        UnionDistributionFactory(
            distribution=distribution_1,
            quantity=10, shortage=1, over=2
        )
        UnionDistributionFactory(
            distribution=distribution_1,
            quantity=20, shortage=3, over=4
        )

        expected_amount = Decimal('200.0000')
        self.assertEqual(
            self.delivery_order.get_distributed_amount(),
            expected_amount
        )


class AllocationTests(TestCase):
    """
    Tests for `Allocation` model methods.
    """
    fixtures = ['units']

    def setUp(self):
        batch = BatchFactory(rate=5)
        self.delivery_order = DeliveryOrderFactory(batch=batch)

    def test_get_total_quantity_method(self):
        """
        Ensure `get_total_quantity` method returns the total union allocations
        quantity for an `Allocation` model instance.
        """
        allocation = AllocationFactory(delivery_order=self.delivery_order)
        UnionAllocationFactory(allocation=allocation, quantity=10)
        UnionAllocationFactory(allocation=allocation, quantity=20)
        self.assertEqual(allocation.get_total_quantity(), Decimal('30'))

    def test_get_percentage_method(self):
        """
        Ensure `get_percentage` method returns the percentage of the allocation
        quantity with respect to the related delivery order.
        """
        allocation_1 = AllocationFactory(delivery_order=self.delivery_order)
        UnionAllocationFactory(allocation=allocation_1, quantity=10)
        UnionAllocationFactory(allocation=allocation_1, quantity=20)

        allocation_2 = AllocationFactory(delivery_order=self.delivery_order)
        UnionAllocationFactory(allocation=allocation_2, quantity=30)
        UnionAllocationFactory(allocation=allocation_2, quantity=40)

        self.assertEqual(allocation_1.get_percentage(), Decimal('30'))
        self.assertEqual(allocation_2.get_percentage(), Decimal('70'))


class DistributionTests(TestCase):
    """
    Tests for `Distribution` model methods.
    """
    fixtures = ['units']

    def setUp(self):
        batch = BatchFactory(rate=5)
        self.delivery_order = DeliveryOrderFactory(batch=batch)

    def test_get_total_quantity_method(self):
        """
        Ensure `get_total_quantity` method returns the total union distribution
        quantity for an `Allocation` model instance.
        """
        distribution = DistributionFactory(delivery_order=self.delivery_order)
        kwargs_1 = {
            'distribution': distribution,
            'quantity': 10,
            'shortage': 1,
            'over': 2
        }
        kwargs_2 = {
            'distribution': distribution,
            'quantity': 20,
            'shortage': 3,
            'over': 4
        }
        UnionDistributionFactory(**kwargs_1)
        UnionDistributionFactory(**kwargs_2)
        self.assertEqual(distribution.get_total_quantity(), Decimal('40'))

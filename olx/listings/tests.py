# listings/tests.py
import uuid

from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase

from .models import (
    Category,
    Order,
    OrderItem,
    Product,
    ProductField,
    Subcategory,
    UserProfile,
)

User = get_user_model()


class ListingsModelsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create two users with unique email/phone
        cls.seller = User.objects.create_user(
            username="seller",
            email=f"seller_{uuid.uuid4().hex[:6]}@example.com",
            password="pass1234",
            phone_number=f"555{uuid.uuid4().int % 10**7:07d}",
        )
        cls.buyer = User.objects.create_user(
            username="buyer",
            email=f"buyer_{uuid.uuid4().hex[:6]}@example.com",
            password="pass1234",
            phone_number=f"556{uuid.uuid4().int % 10**7:07d}",
        )

        # Category & Subcategory
        cls.category = Category.objects.create(name="Electronics")
        cls.subcategory = Subcategory.objects.create(
            category=cls.category, name="Smartphones"
        )

        # Product & its Field
        cls.product = Product.objects.create(
            user=cls.seller,
            subcategory=cls.subcategory,
            title="Pixel 6",
            description="Latest Google phone",
            price=599,
        )
        cls.field = ProductField.objects.create(
            product=cls.product, key="Storage", value="128GB"
        )

        # Order & OrderItem
        cls.order = Order.objects.create(buyer=cls.buyer)
        cls.order_item = OrderItem.objects.create(
            order=cls.order,
            buyer=cls.buyer,
            product=cls.product,
            price=cls.product.price,
        )

        # UserProfile
        cls.profile = UserProfile.objects.create(
            user=cls.buyer,
            phone="123-456-7890",
            address="123 Main St",
            bio="Test buyer",
        )

    def test_category_str_and_uniqueness(self):
        self.assertEqual(str(self.category), "Electronics")
        with self.assertRaises(IntegrityError):
            Category.objects.create(name="Electronics")

    def test_subcategory_str_and_unique_together(self):
        self.assertEqual(str(self.subcategory), "Electronics > Smartphones")
        with self.assertRaises(IntegrityError):
            Subcategory.objects.create(category=self.category, name="Smartphones")

    def test_product_and_field_relations(self):
        self.assertEqual(str(self.product), "Pixel 6")
        self.assertEqual(self.product.user, self.seller)
        self.assertEqual(self.product.subcategory, self.subcategory)
        self.assertEqual(self.product.fields.count(), 1)
        self.assertEqual(self.product.fields.first().key, "Storage")
        self.assertEqual(self.product.fields.first().value, "128GB")

    def test_order_and_orderitem(self):
        self.assertEqual(
            str(self.order), f"Order #{self.order.id} by {self.buyer.username}"
        )
        self.assertEqual(self.order.items.count(), 1)
        item = self.order.items.first()
        self.assertEqual(item, self.order_item)
        self.assertEqual(
            str(item), f"{self.product.title} bought by {self.buyer.username}"
        )
        self.assertEqual(item.price, self.product.price)

    def test_userprofile_str_and_fields(self):
        self.assertEqual(str(self.profile), self.buyer.username)
        self.assertEqual(self.profile.phone, "123-456-7890")
        self.assertEqual(self.profile.address, "123 Main St")
        self.assertEqual(self.profile.bio, "Test buyer")

from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.
User = get_user_model()


class UserModelTests(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(
            username="testUser",
            password="12345",
            email="test@example.com",
            phone_number="827329820",
        )
        self.assertEqual(user.username, "testUser")
        self.assertTrue(user.check_password("12345"))
        self.assertEqual(str(user), "testUser")

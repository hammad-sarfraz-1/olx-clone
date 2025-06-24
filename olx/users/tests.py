from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.
User = get_user_model()


class UserModelTests(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(
            username="hammad",
            password="securepass",
            email="hammad@example.com",
            phone_number="1234567890",
        )
        self.assertEqual(user.username, "hammad")
        self.assertTrue(user.check_password("securepass"))
        self.assertEqual(str(user), "hammad")

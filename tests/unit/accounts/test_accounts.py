# tests/unit/accounts/test_accounts.py

from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

User = get_user_model()


class UserRegistrationTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("accounts:user-register")
        self.valid_payload = {
            "username": "kwame",
            "email": "kwame.nkrumah@ghana.com",
            "password": "SecurePass123!",
            "password_confirm": "SecurePass123!",
            "first_name": "Kwame",
            "last_name": "Nkrumah",
            "accept_terms": True,
        }

    def test_valid_user_registration(self):
        """Test user registration with valid data"""
        response = self.client.post(self.url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, "kwame.nkrumah@ghana.com")  # type: ignore
        self.assertEqual(User.objects.get().account_status, "PENDING")  # type: ignore

    def test_duplicate_email_registration(self):
        """Test that duplicate emails are not allowed"""
        # Create a user first
        User.objects.create_user(  # type: ignore
            username="existing", email="kwame.nkrumah@ghana.com", password="testpass123"
        )
        response = self.client.post(self.url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data.get("errors", {}))

    def test_password_mismatch(self):
        """Test that password and password_confirm must match"""
        self.valid_payload["password_confirm"] = "DifferentPass123!"  # noqa: S105
        response = self.client.post(self.url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password_confirm", response.data.get("errors", {}))


class UserLoginTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("accounts:user-login")
        self.user = User.objects.create_user(  # type: ignore
            username="testuser",
            email="test@example.com",
            password="testpass123",
            account_status="active",
            email_verified=True,
        )

    def test_successful_login(self):
        """Test user can login with correct credentials"""
        data = {"email": "test@example.com", "password": "testpass123"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_invalid_credentials(self):
        """Test login with invalid credentials"""
        data = {"email": "test@example.com", "password": "wrongpassword"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)


class UserProfileTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(  # type: ignore
            username="testuser",
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
            account_status="active",
            email_verified=True,
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse("accounts:user-me")

    def test_retrieve_profile(self):
        """Test retrieving user profile"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "test@example.com")
        self.assertEqual(response.data["first_name"], "Test")
        self.assertEqual(response.data["last_name"], "User")

    def test_update_profile(self):
        """Test updating user profile"""
        update_data = {
            "first_name": "Updated",
            "last_name": "Name",
        }
        response = self.client.patch(self.url, update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.user.last_name, "Name")


class PasswordChangeTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(  # type: ignore
            username="testuser",
            email="test@example.com",
            password="oldpassword123",
            account_status="active",
            email_verified=True,
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse("accounts:user-password-change")

    def test_password_change_success(self):
        """Test successful password change"""
        data = {
            "old_password": "oldpassword123",
            "new_password": "newsecurepass123!",
            "new_password_confirm": "newsecurepass123!",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newsecurepass123!"))

    def test_password_change_wrong_old_password(self):
        """Test password change with wrong old password"""
        data = {
            "old_password": "wrongpassword",
            "new_password": "newsecurepass123!",
            "new_password_confirm": "newsecurepass123!",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("old_password", response.data["errors"])


class EmailVerificationTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(  # type: ignore
            username="testuser",
            email="test@example.com",
            password="testpass123",
            account_status="pending",
            email_verified=False,
        )
        self.client.force_authenticate(user=self.user)
        self.verification_url = reverse("accounts:user-request-verification-email")
        self.verification_confirm_url = reverse("accounts:user-verify-email-confirm")
        self.verification_token = "test-verification-token"  # noqa: S105

    @patch("apps.accounts.tasks.send_verification_email.delay")
    def test_send_verification_email(self, mock_send_email):
        """Test sending verification email"""
        response = self.client.post(self.verification_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"], "Verification email sent successfully"
        )
        mock_send_email.assert_called_once()

    @patch("apps.accounts.models.User.verify_email")
    def test_verify_email_with_token(self, mock_verify_email):
        """Test email verification with valid token"""
        mock_verify_email.return_value = True
        data = {"email": self.user.email, "token": self.verification_token}
        response = self.client.post(self.verification_confirm_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"],
            "Email verified successfully. Your account is now active.",
        )
        mock_verify_email.assert_called_once_with(self.verification_token)


class AdminUserTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(  # type: ignore
            username="admin",
            email="admin@example.com",
            password="adminpass123",
            account_status="active",
        )
        self.user = User.objects.create_user(  # type: ignore
            username="testuser",
            email="test@example.com",
            password="testpass123",
            account_status="active",
        )
        self.client.force_authenticate(user=self.admin)

    def test_admin_can_list_users(self):
        """Test admin can list all users"""
        url = reverse("accounts:user-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_admin_can_deactivate_user(self):
        """Test admin can deactivate a user"""
        url = reverse("accounts:user-detail", args=[self.user.id])
        response = self.client.patch(url, {"is_active": False}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

# tests/unit/accounts/test_accounts.py

from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase


User = get_user_model()


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
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.count() == 1
        assert User.objects.get().email == "kwame.nkrumah@ghana.com"
        assert User.objects.get().account_status == "PENDING"

    @patch("apps.accounts.views.send_verification_email.delay")
    def test_registration_enqueues_verification_task(self, mock_task):
        response = self.client.post(self.url, self.valid_payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.count() == 1
        user = User.objects.first()
        mock_task.assert_called_once_with(user.id)

    def test_duplicate_email_registration(self):
        """Test that duplicate emails are not allowed"""
        # Create a user first
        User.objects.create_user(
            username="existing",
            email="kwame.nkrumah@ghana.com",
            password="testpass123",
        )
        response = self.client.post(self.url, self.valid_payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data.get("errors", {})

    def test_password_mismatch(self):
        """Test that password and password_confirm must match"""
        self.valid_payload["password_confirm"] = "DifferentPass123!"  # noqa: S105
        response = self.client.post(self.url, self.valid_payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "password_confirm" in response.data.get("errors", {})


class TokenFlowTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="refreshuser",
            email="refresh@example.com",
            password="testpass123",
            account_status="active",
            email_verified=True,
        )
        self.login_url = reverse("accounts:user-login")
        self.refresh_url = reverse("accounts:token-refresh")
        self.logout_url = reverse("accounts:user-logout")

    def _login(self):
        res = self.client.post(
            self.login_url,
            {"email": "refresh@example.com", "password": "testpass123"},
            format="json",
        )
        assert res.status_code == status.HTTP_200_OK
        return res.data["access"], res.data["refresh"]

    def test_token_refresh_success(self):
        _, refresh = self._login()
        res = self.client.post(self.refresh_url, {"refresh": refresh}, format="json")
        assert res.status_code == status.HTTP_200_OK
        assert "access" in res.data

    def test_token_refresh_failure_with_invalid_token(self):
        res = self.client.post(
            self.refresh_url,
            {"refresh": "invalid.token.here"},
            format="json",
        )
        assert res.status_code in (
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_logout_blacklists_refresh_token(self):
        _, refresh = self._login()
        # Logout with refresh => should be blacklisted
        res = self.client.post(self.logout_url, {"refresh": refresh}, format="json")
        assert res.status_code == status.HTTP_205_RESET_CONTENT
        # Attempt to refresh with the same token must fail
        res2 = self.client.post(self.refresh_url, {"refresh": refresh}, format="json")
        assert res2.status_code in (
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_401_UNAUTHORIZED,
        )


class UserLoginTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("accounts:user-login")
        self.user = User.objects.create_user(
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
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_invalid_credentials(self):
        """Test login with invalid credentials"""
        data = {"email": "test@example.com", "password": "wrongpassword"}
        response = self.client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "non_field_errors" in response.data


class UserProfileTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
            account_status="active",
            email_verified=True,
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse("accounts:user-profile-me")

    def test_retrieve_profile(self):
        """Test retrieving user profile"""
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == "test@example.com"
        assert response.data["first_name"] == "Test"
        assert response.data["last_name"] == "User"

    def test_update_profile(self):
        """Test updating user profile"""
        update_data = {
            "first_name": "Updated",
            "last_name": "Name",
        }
        # Use the profile update endpoint with PATCH
        response = self.client.patch(self.url, update_data, format="json")
        assert response.status_code == status.HTTP_200_OK
        self.user.refresh_from_db()
        assert self.user.first_name == "Updated"
        assert self.user.last_name == "Name"


class PasswordChangeTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
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
            "new_password": "newsecurepassword123",
            "new_password_confirm": "newsecurepassword123",
        }
        response = self.client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert "message" in response.data
        assert "Password changed successfully" in response.data["message"]
        self.user.refresh_from_db()
        assert self.user.check_password("newsecurepassword123")

    def test_password_change_wrong_old_password(self):
        """Test password change with wrong old password"""
        data = {
            "old_password": "wrongpassword",
            "new_password": "newsecurepassword123",
            "new_password_confirm": "newsecurepassword123",
        }
        response = self.client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "errors" in response.data
        assert "old_password" in response.data["errors"]
        self.user.refresh_from_db()
        assert self.user.check_password("oldpassword123")  # Password should not change


class PasswordResetConfirmTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="resetuser",
            email="reset@example.com",
            password="oldpassword123",
            account_status="active",
            email_verified=True,
        )
        self.url = reverse("accounts:user-password-reset-confirm")

    def test_password_reset_confirm_success(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        payload = {"uid": uid, "token": token, "new_password": "NewStrongPass123!"}
        res = self.client.post(self.url, payload, format="json")
        assert res.status_code == status.HTTP_200_OK
        # Verify password changed
        assert self.user.check_password("oldpassword123") is False
        self.user.refresh_from_db()
        assert self.user.check_password("NewStrongPass123!") is True

    def test_password_reset_confirm_invalid_token(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        payload = {
            "uid": uid,
            "token": "invalid-token",
            "new_password": "NewStrongPass123!",
        }
        res = self.client.post(self.url, payload, format="json")
        assert res.status_code == status.HTTP_400_BAD_REQUEST


class EmailVerificationTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            email_verified=False,
        )
        self.client.force_authenticate(user=self.user)
        self.verification_url = reverse("accounts:user-verify-email")
        self.verification_confirm_url = reverse("accounts:user-verify-email-confirm")

    @patch("apps.accounts.views.send_verification_email.delay")
    def test_send_verification_email(self, mock_send_email):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse("accounts:user-verify-email-request"),
            {"email": self.user.email, "redirect_url": "http://example.com/verify"},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        mock_send_email.assert_called_once_with(self.user.id)

    # @patch("apps.accounts.views.send_verification_email.delay")
    # def test_send_verification_email(self, mock_send_email):
    #     """Test sending verification email"""
    #     # The endpoint expects an email parameter
    #     data = {"email": self.user.email}
    #     self.verification_url = reverse("accounts:user-verify-email")
    #     response = self.client.post(self.verification_url, data, format="json")
    #     assert response.status_code == status.HTTP_200_OK
    #     assert "message" in response.data
    #     assert "verification email" in response.data["message"].lower()
    #     mock_send_email.assert_called_once()

    @patch("apps.accounts.views.default_token_generator.check_token")
    def test_verify_email_with_token(self, mock_check_token):
        """Test email verification with valid token"""
        mock_check_token.return_value = True
        token = "test-token"
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        data = {"token": token, "uid": uid}

        response = self.client.post(self.verification_confirm_url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert "message" in response.data
        assert "verified" in response.data["message"].lower()
        self.user.refresh_from_db()
        assert self.user.email_verified is True


class AdminUserTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="adminpass123",
            account_status="active",
        )
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            account_status="active",
        )
        self.client.force_authenticate(user=self.admin)

    def test_admin_can_list_users(self):
        """Test admin can list all users"""
        expected_user_count = 2  # admin user + test user
        url = reverse("accounts:user-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == expected_user_count

    def test_admin_can_deactivate_user(self):
        """Test admin can deactivate a user"""
        url = reverse("accounts:user-detail", args=[self.user.id])
        response = self.client.patch(url, {"is_active": False}, format="json")
        assert response.status_code == status.HTTP_200_OK
        self.user.refresh_from_db()
        assert not self.user.is_active

# apps/accounts/serializers.py

"""
User authentication serializers for the e-commerce API.
Handles user registration, login, profile management with security features.
"""

import re
from datetime import timedelta

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import User
from apps.core.serializers import BaseModelSerializer, SanitizedCharField


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration with comprehensive validation.
    Handles user creation with password confirmation and validation.
    """

    # Password fields
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"},
        help_text=_("Password must be at least 8 characters long"),
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
        help_text=_("Confirm your password"),
    )

    # Sanitized input fields
    username = SanitizedCharField(
        max_length=150, help_text=_("Unique username for login")
    )
    email = serializers.EmailField(help_text=_("Valid email address"))
    first_name = SanitizedCharField(max_length=150, required=False, allow_blank=True)
    last_name = SanitizedCharField(max_length=150, required=False, allow_blank=True)
    phone_number = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True,
        help_text=_("Phone number in format: +233123456"),
    )

    # Address fields
    address_line_1 = SanitizedCharField(
        max_length=255, required=False, allow_blank=True
    )
    address_line_2 = SanitizedCharField(
        max_length=255,
        required=False,
        allow_blank=True,
        help_text=_("Secondary address line (apartment, suite, etc.)"),
    )
    city = SanitizedCharField(max_length=100, required=False, allow_blank=True)
    state = SanitizedCharField(max_length=100, required=False, allow_blank=True)
    postal_code = SanitizedCharField(max_length=20, required=False, allow_blank=True)
    country = SanitizedCharField(max_length=100, required=False, allow_blank=True)

    # Terms and conditions
    accept_terms = serializers.BooleanField(
        write_only=True, help_text=_("Must accept terms and conditions")
    )

    class Meta:  # type: ignore
        model = User
        fields = [
            "username",
            "email",
            "password",
            "password_confirm",
            "first_name",
            "last_name",
            "phone_number",
            "address_line_1",
            "address_line_2",
            "city",
            "state",
            "postal_code",
            "country",
            "accept_terms",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_username(self, value):
        """Validate username format and uniqueness."""
        if not re.match(r"^[a-zA-Z0-9_]+$", value):
            raise serializers.ValidationError(
                _("Username can only contain letters, numbers, and underscores.")
            )

        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError(
                _("A user with this username already exists.")
            )

        return value.lower()

    def validate_email(self, value):
        """Validate email uniqueness."""
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                _("A user with this email address already exists.")
            )

        return value.lower()

    def validate_password(self, value):
        """Validate password strength."""
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))

        # Additional custom password validation
        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError(
                _("Password must contain at least one uppercase letter.")
            )
        if not re.search(r"[a-z]", value):
            raise serializers.ValidationError(
                _("Password must contain at least one lowercase letter.")
            )
        if not re.search(r"\d", value):
            raise serializers.ValidationError(
                _("Password must contain at least one digit.")
            )

        return value

    def validate_phone_number(self, value):
        """Validate phone number format."""
        if value and not re.match(r"^\+?1?\d{9,15}$", value):
            raise serializers.ValidationError(
                _("Phone number must be in format: +1234567890")
            )
        return value

    def validate_accept_terms(self, value):
        """Ensure terms and conditions are accepted."""
        if not value:
            raise serializers.ValidationError(
                _("You must accept the terms and conditions to register.")
            )
        return value

    def validate(self, data):  # type: ignore
        """Cross-field validation."""
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError(
                {"password_confirm": _("Password confirmation doesn't match.")}
            )

        return data

    def create(self, validated_data):
        """Create a new user account."""
        # Remove fields that shouldn't be passed to User.objects.create_user()
        validated_data.pop("password_confirm")
        validated_data.pop("accept_terms")

        password = validated_data.pop("password")

        # Create the user
        user = User.objects.create_user(
            password=password,
            user_type="CUSTOMER",  # Default to customer
            account_status="PENDING",  # Require email verification
            **validated_data,
        )

        # Generate email verification token
        user.generate_email_verification_token()

        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login with email and JWT token generation.
    """

    email = serializers.EmailField(help_text=_("Email address"))
    password = serializers.CharField(
        style={"input_type": "password"}, help_text=_("Your password")
    )
    remember_me = serializers.BooleanField(
        default=False, help_text=_("Keep me logged in")
    )

    def validate(self, data):  # type: ignore
        """
        Authenticate user and return tokens.
        """
        email = data.get("email")
        password = data.get("password")
        remember_me = data.get("remember_me", False)

        if not email or not password:
            raise serializers.ValidationError(
                {"detail": _("Both email and password are required.")}
            )

        # Authenticate user using email
        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password,
        )

        if not user:
            raise serializers.ValidationError(
                {"detail": _("Invalid email or password.")}
            )

        if not user.is_active:
            raise serializers.ValidationError(
                {"detail": _("This account is inactive.")}
            )

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Set token expiration based on remember_me
        if not remember_me:
            # Shorter token lifetime if remember_me is False
            refresh.set_exp(lifetime=timedelta(hours=12))
            access_token = str(refresh.access_token)

        # Update last login
        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

        # Get user data
        user_data = UserProfileSerializer(user, context=self.context).data

        return {"access": access_token, "refresh": refresh_token, "user": user_data}


class UserProfileSerializer(BaseModelSerializer):
    """
    Serializer for user profile management.
    Shows different fields based on user permissions.
    """

    # User fields
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField()
    first_name = SanitizedCharField(max_length=150, required=False)
    last_name = SanitizedCharField(max_length=150, required=False)
    phone_number = serializers.CharField(
        max_length=20, required=False, allow_blank=True
    )

    # Address fields
    address_line_1 = SanitizedCharField(
        max_length=255, required=False, allow_blank=True
    )
    address_line_2 = SanitizedCharField(
        max_length=255, required=False, allow_blank=True
    )
    city = SanitizedCharField(max_length=100, required=False, allow_blank=True)
    state = SanitizedCharField(max_length=100, required=False, allow_blank=True)
    postal_code = SanitizedCharField(max_length=20, required=False, allow_blank=True)
    country = SanitizedCharField(max_length=100, required=False, allow_blank=True)

    # Computed fields
    full_name = serializers.CharField(read_only=True)
    full_address = serializers.CharField(read_only=True)
    is_email_verified = serializers.BooleanField(
        source="email_verified", read_only=True
    )

    # Profile fields (from UserProfile model)
    bio = serializers.CharField(source="profile.bio", required=False, allow_blank=True)
    date_of_birth = serializers.DateField(
        source="profile.date_of_birth", required=False, allow_null=True
    )
    newsletter_subscription = serializers.BooleanField(
        source="profile.newsletter_subscription", required=False
    )

    # Admin-only fields
    account_status = serializers.CharField(read_only=True)
    user_type = serializers.CharField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    last_login = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")

    # Override sensitive fields for role-based access
    sensitive_fields = [
        "account_status",
        "user_type",
        "date_joined",
        "last_login",
        "created_by",
        "updated_by",
        "is_active",
    ]

    class Meta(BaseModelSerializer.Meta):
        model = User
        fields = [
            *BaseModelSerializer.Meta.fields,
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "address_line_1",
            "address_line_2",
            "city",
            "state",
            "postal_code",
            "country",
            "full_name",
            "full_address",
            "is_email_verified",
            "bio",
            "date_of_birth",
            "newsletter_subscription",
            "account_status",
            "user_type",
            "date_joined",
            "last_login",
        ]
        read_only_fields = [
            *BaseModelSerializer.Meta.read_only_fields,
            "username",
            "full_name",
            "full_address",
            "is_email_verified",
        ]

    def validate_email(self, value):
        """Validate email uniqueness for updates."""
        user = self.instance
        if (
            user
            and User.objects.filter(email__iexact=value).exclude(id=user.id).exists()  # type: ignore
        ):
            raise serializers.ValidationError(
                _("A user with this email address already exists.")
            )
        return value.lower()

    def update(self, instance, validated_data):
        """Update user profile with nested profile data."""
        # Extract profile data
        profile_data = validated_data.pop("profile", {})

        # Update user fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update profile fields
        if profile_data:
            for attr, value in profile_data.items():
                setattr(instance.profile, attr, value)  # type: ignore
            instance.profile.save()  # type: ignore

        return instance


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for changing user password.
    """

    old_password = serializers.CharField(
        style={"input_type": "password"}, help_text=_("Current password")
    )
    new_password = serializers.CharField(
        style={"input_type": "password"},
        min_length=8,
        help_text=_("New password (minimum 8 characters)"),
    )
    new_password_confirm = serializers.CharField(
        style={"input_type": "password"}, help_text=_("Confirm new password")
    )

    def validate_old_password(self, value):
        """Validate current password."""
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(_("Current password is incorrect."))
        return value

    def validate_new_password(self, value):
        """Validate new password strength."""
        try:
            validate_password(value, self.context["request"].user)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def validate(self, data):  # type: ignore
        """Cross-field validation."""
        if data["new_password"] != data["new_password_confirm"]:
            raise serializers.ValidationError(
                {"new_password_confirm": _("New password confirmation doesn't match.")}
            )

        if data["old_password"] == data["new_password"]:
            raise serializers.ValidationError(
                {
                    "new_password": _(
                        "New password must be different from current password."
                    )
                }
            )

        return data

    def save(self):  # type: ignore
        """Change the user's password."""
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for password reset request.
    """

    email = serializers.EmailField(
        help_text=_("Email address associated with your account")
    )

    def validate_email(self, value):
        """Validate that email exists in the system."""
        try:
            user = User.objects.get(email__iexact=value)
            if not user.is_active:
                raise serializers.ValidationError(_("This account is inactive."))
            return value.lower()
        except User.DoesNotExist:
            # Don't reveal whether email exists for security
            # But still raise an error to prevent enumeration
            raise serializers.ValidationError(
                _(
                    "If this email exists in our system, you will receive password reset instructions."
                )
            )

# apps/core/serializers.py

"""
Base serializers with security features for the e-commerce application.
Provides common functionality and security features for API serialization.
"""

import html
import re

from rest_framework import serializers


class SecurityMixin:
    """
    Mixin that provides security features for serializers.
    Includes input sanitization and basic XSS protection.
    """

    @staticmethod
    def sanitize_input(value):
        """
        Basic input sanitization to prevent XSS attacks.
        Removes potentially dangerous HTML tags and scripts.
        """
        if not isinstance(value, str):
            return value

        # Remove script tags and their content
        value = re.sub(
            r"<script[^>]*>.*?</script>", "", value, flags=re.DOTALL | re.IGNORECASE
        )

        # Remove potentially dangerous tags
        dangerous_tags = ["script", "iframe", "object", "embed", "form", "input"]
        for tag in dangerous_tags:
            value = re.sub(f"<{tag}[^>]*>", "", value, flags=re.IGNORECASE)
            value = re.sub(f"</{tag}>", "", value, flags=re.IGNORECASE)

        # Escape HTML entities
        value = html.escape(value)

        return value.strip()

    def validate_text_field(self, value):
        """
        Common validation for text fields.
        Sanitizes input and checks for minimum length.
        """
        if value:
            value = self.sanitize_input(value)
            if len(value.strip()) < 1:
                raise serializers.ValidationError("This field cannot be empty.")
        return value


class RoleBasedFieldMixin:
    """
    Mixin that provides role-based field visibility.
    Hides sensitive fields based on user permissions.
    """

    # Define sensitive fields that should be hidden from regular users
    sensitive_fields = ["created_by", "updated_by", "is_active"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = kwargs.get("context", {})

    def get_fields(self):
        """
        Override to dynamically show/hide fields based on user role.
        """
        fields = super().get_fields()
        request = self.context.get("request")

        # If no request context, return all fields
        if not request:
            return fields

        # If user is not authenticated, hide sensitive fields
        if not request.user or not request.user.is_authenticated:
            for field_name in self.sensitive_fields:
                fields.pop(field_name, None)

        # If user is not staff, hide audit fields for security
        elif not request.user.is_staff:
            audit_fields = ["created_by", "updated_by"]
            for field_name in audit_fields:
                fields.pop(field_name, None)

        return fields


class BaseModelSerializer(
    SecurityMixin, RoleBasedFieldMixin, serializers.ModelSerializer
):
    """
    Base serializer that provides common functionality for all model serializers.
    Includes security features, audit field handling, and consistent formatting.
    """

    # Read-only UUID field
    id = serializers.UUIDField(read_only=True)

    # Read-only timestamp fields with custom formatting
    created_at = serializers.DateTimeField(
        read_only=True, output_format="%Y-%m-%d %H:%M:%S"
    )
    updated_at = serializers.DateTimeField(
        read_only=True, output_format="%Y-%m-%d %H:%M:%S"
    )

    # User fields - shown only to staff users
    created_by = serializers.StringRelatedField(read_only=True)
    updated_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        # Common fields that should be included in all serializers
        fields = [
            "id",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
            "is_active",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]

    def validate(self, attrs):
        """
        Global validation that applies to all serializers.
        """
        # Sanitize all string fields
        for field_name, value in attrs.items():
            if isinstance(value, str):
                attrs[field_name] = self.sanitize_input(value)

        return super().validate(attrs)

    def create(self, validated_data):
        """
        Override create to automatically set created_by field.
        """
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            validated_data["created_by"] = request.user

        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Override update to automatically set updated_by field.
        """
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            validated_data["updated_by"] = request.user

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        """
        Customize the serialized output.
        """
        data = super().to_representation(instance)

        # Add additional metadata for API responses
        data["_meta"] = {"model": instance.__class__.__name__.lower(), "version": "v1"}

        return data


class SanitizedCharField(serializers.CharField):
    """
    Custom CharField that automatically sanitizes input.
    """

    def to_internal_value(self, data):
        """Override to sanitize input automatically."""
        data = super().to_internal_value(data)
        return SecurityMixin.sanitize_input(data)


class SanitizedTextField(serializers.CharField):
    """
    Custom TextField for longer content with enhanced sanitization.
    """

    def to_internal_value(self, data):
        """Override to sanitize input automatically."""
        data = super().to_internal_value(data)
        return SecurityMixin.sanitize_input(data)


# Example usage in a model serializer:
"""
from apps.core.serializers import BaseModelSerializer, SanitizedCharField

class ProductSerializer(BaseModelSerializer):
    name = SanitizedCharField(max_length=255)
    description = SanitizedTextField(required=False)

    class Meta(BaseModelSerializer.Meta):
        model = Product
        fields = BaseModelSerializer.Meta.fields + ['name', 'description', 'price']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value
"""

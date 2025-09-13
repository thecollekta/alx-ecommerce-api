# apps/core/models.py

"""
Base models for the e-commerce application.
Provides common functionality that can be inherited by other models.
"""

import uuid

from django.conf import settings
from django.db import models


class AuditStampedModelBase(models.Model):
    """
    Abstract base model that provides audit fields for tracking
    when records are created and updated, and by whom.

    This model should be inherited by other models that need
    audit trail functionality.
    """

    # Primary key as UUID for better security and scalability
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for this record",
    )

    # Timestamp fields - automatically managed
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="When this record was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="When this record was last updated"
    )

    # User tracking fields - tracks who created/updated the record
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created_by",
        help_text="User who created this record",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated_by",
        help_text="User who last updated this record",
    )

    # Soft delete functionality
    is_active = models.BooleanField(
        default=True, help_text="Whether this record is active (soft delete)"
    )

    class Meta:
        abstract = True
        # Default ordering by most recently updated
        ordering = ["-updated_at", "-created_at"]

    def __str__(self):
        """
        Default string representation showing the model name and ID.
        Child models should override this method.
        """
        return f"{self.__class__.__name__} ({self.id})"

    def soft_delete(self):
        """
        Soft delete the record by setting is_active to False
        instead of actually deleting it from the database.
        """
        self.is_active = False
        self.save(update_fields=["is_active", "updated_at"])

    def restore(self):
        """
        Restore a soft-deleted record by setting is_active to True.
        """
        self.is_active = True
        self.save(update_fields=["is_active", "updated_at"])


class ActiveManager(models.Manager):
    """
    Custom manager that only returns active (non-soft-deleted) records.
    """

    def get_queryset(self):
        """Override to filter out soft-deleted records by default."""
        return super().get_queryset().filter(is_active=True)


class AllObjectsManager(models.Manager):
    """
    Manager that returns all objects including soft-deleted ones.
    Useful for admin interfaces or data recovery.
    """

    def get_queryset(self):
        """Return all objects regardless of is_active status."""
        return super().get_queryset()


# Example usage in a model:
"""
from apps.core.models import AuditStampedModelBase, ActiveManager, AllObjectsManager

class Product(AuditStampedModelBase):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # Custom managers
    objects = ActiveManager()  # Default manager - only active records
    all_objects = AllObjectsManager()  # All records including deleted

    def __str__(self):
        return self.name
"""

# apps/core/middleware.py

"""
Django middleware for user tracking in request/response cycle.

This module provides middleware to track the current user making the request
and make this information available throughout the request/response cycle.
It's particularly useful for audit logging and automatic user tracking in models.
"""

import threading

from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin


class CurrentUserMiddleware(MiddlewareMixin):
    """
    Middleware to store current user in thread-local storage.

    This middleware enables automatic user tracking in models by storing the
    current user in thread-local storage at the beginning of each request.
    The stored user is automatically cleaned up after the request is processed.

    The middleware is used by `AuditStampedModelBase` to automatically track
    who created/updated records without explicitly passing user context.
    """

    _thread_local = threading.local()

    def process_request(self, request: HttpRequest) -> None:
        """
        Store the current user in thread-local storage before request processing.

        Args:
            request: The incoming HTTP request object containing the user.
        """
        if hasattr(request, "user") and request.user.is_authenticated:
            self._thread_local.django_user = request.user
            threading.current_thread()._django_user = request.user

    def process_response(
        self, request: HttpRequest, response: HttpResponse
    ) -> HttpResponse:
        """
        Clean up thread-local storage after request processing.

        Args:
            request: The HTTP request object.
            response: The HTTP response object.

        Returns:
            The HTTP response object.
        """
        self._cleanup_thread_local()
        return response

    def process_exception(
        self, request: HttpRequest, exception: Exception
    ) -> HttpResponse | None:
        """
        Clean up thread-local storage if an exception occurs.

        Args:
            request: The HTTP request object.
            exception: The exception that was raised.

        Returns:
            None to allow other exception middleware to process the exception.
        """
        self._cleanup_thread_local()
        return None

    def _cleanup_thread_local(self) -> None:
        """Remove the user from thread-local storage if it exists."""
        if hasattr(self._thread_local, "django_user"):
            delattr(self._thread_local, "django_user")
            delattr(threading.current_thread(), "_django_user")


class PerformanceMiddleware:
    def resolve(self, next, root, info, **args):
        # Add performance tracking
        import time

        start_time = time.time()
        result = next(root, info, **args)
        duration = time.time() - start_time

        # Log slow queries
        if duration > 1.0:  # More than 1 second
            print(f"Slow GraphQL query: {info.operation.name} took {duration:.2f}s")

        return result

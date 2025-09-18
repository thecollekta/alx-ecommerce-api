# apps/accounts/tasks.py

"""
Tasks for handling email verification asynchronously.
"""

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode

User = get_user_model()


def get_verification_url(user):
    """Generate email verification URL with token."""
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    relative_url = reverse(
        "accounts:user-verify-email", kwargs={"uidb64": uid, "token": token}
    )
    return f"{settings.FRONTEND_URL}{relative_url}"


@shared_task
def send_verification_email(user_id):
    """
    Send verification email to the user.

    Args:
        user_id (int): ID of the user to send verification email to.
    """
    try:
        user = User.objects.get(pk=user_id)

        subject = "Verify your email address"
        verification_url = get_verification_url(user)

        # Render HTML email
        html_message = render_to_string(
            "emails/verification_email.html",
            {
                "user": user,
                "verification_url": verification_url,
            },
        )

        # Create plain text version
        plain_message = strip_tags(html_message)

        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
        )

    except User.DoesNotExist:
        # Log error or handle as needed
        pass


def verify_email_token(uidb64, token):
    """
    Verify email token and activate user if valid.

    Args:
        uidb64 (str): Base64 encoded user ID
        token (str): Verification token

    Returns:
        User: The verified user if successful, None otherwise
    """
    try:
        # Decode user ID
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.encoding import force_str

        uid = force_str(urlsafe_base64_encode(uidb64))
        user = User.objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            user.email_verified = True
            if user.account_status == "pending":
                user.account_status = "active"
            user.save()
            return user
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        pass
    return None

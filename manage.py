#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "ecommerce_backend.settings.development"
    )
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Run tests with coverage if coverage is installed
    if len(sys.argv) == 1:
        try:
            import coverage

            cov = coverage.Coverage()
            cov.start()

            # Run tests
            test_args = [
                "manage.py",
                "test",
                "tests/unit/accounts/test_accounts.py",
                "-v",
                "2",
            ]
            execute_from_command_line(test_args)

            # Generate coverage report
            cov.stop()
            cov.save()
            cov.report(show_missing=True)

            # Generate HTML report
            cov.html_report(directory="htmlcov")
            print("\nCoverage HTML report generated in htmlcov/index.html")

        except ImportError:
            # Fallback to normal test command if coverage is not installed
            test_args = [
                "manage.py",
                "test",
                "tests/unit/accounts/test_accounts.py",
                "-v",
                "2",
            ]
            execute_from_command_line(test_args)
    else:
        execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()

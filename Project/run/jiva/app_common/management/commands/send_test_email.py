from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings


class Command(BaseCommand):
    help = "Send a test email"

    def handle(self, *args, **kwargs):
        subject = "Test Email from Django"
        message = "This is a test email sent from Django using SMTP."
        recipient_list = ["arunrg.osr.mgmt@gmail.com"]  # Change to your test email

        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
            self.stdout.write(self.style.SUCCESS("Test email sent successfully!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to send email: {str(e)}"))

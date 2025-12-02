from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta

from .models import JobApplication
from accounts.models import Notification

@receiver(post_save, sender=JobApplication)
def notify_employer_on_application(sender, instance, created, **kwargs):
    if not created:
        return

    job = instance.job
    employer = job.employer
    applicant = instance.applicant

    message = f"A new applicant has applied to your job."

    Notification.objects.create(
        user=employer,
        actor=applicant,
        message=message,
        type=Notification.NOTIF_APPLICATION,
        related_job=job,
        related_applicant=applicant,
    )


@receiver(post_delete, sender=JobApplication)
def notify_employer_on_withdraw(sender, instance, **kwargs):
    job = instance.job
    employer = job.employer
    applicant = instance.applicant

    message = f"An applicant has withdrawn their application from your job."

    Notification.objects.create(
        user=employer,
        actor=applicant,
        message=message[:255],
        type=Notification.NOTIF_WITHDRAW,
        related_job=job,
        related_applicant=applicant,
    )

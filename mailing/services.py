from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.utils import timezone

from .models import MailingAttempt


def send_mailing(mailing):
    now = timezone.now()

    if not (mailing.start_time <= now <= mailing.end_time):
        raise ValueError("Рассылка не может быть запущена сейчас")

    if mailing.is_blocked:
        raise PermissionDenied('"Рассылка заблокирована менеджером"')

    message = mailing.message
    mailing.status = mailing.Status.IN_PROGRESS
    mailing.save()

    for receiver in mailing.receivers.all():
        try:
            result = send_mail(
                subject=message.title,
                message=message.text,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[receiver.email],
                fail_silently=False,
            )
            MailingAttempt.objects.create(
                mailing=mailing,
                receiver=receiver,
                status=(
                    MailingAttempt.Status.SUCCESSFUL
                    if result
                    else MailingAttempt.Status.UNSUCCESSFUL
                ),
                mail_server_reply=f"send_mail returned {result}",
            )
        except Exception as e:
            MailingAttempt.objects.create(
                mailing=mailing,
                receiver=receiver,
                status=MailingAttempt.Status.UNSUCCESSFUL,
                mail_server_reply=str(e),
            )

    mailing.status = mailing.Status.DONE
    mailing.save()

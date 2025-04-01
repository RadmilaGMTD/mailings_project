from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from config import settings
from mailings.models import MailingAttempt, Mailings


class Command(BaseCommand):
    help = "Отправка рассылки по требованию"

    def add_arguments(self, parser):
        parser.add_argument("pk", type=int, help="ID рассылки для отправки")

    def handle(self, *args, **kwargs):
        pk = kwargs["pk"]
        try:
            mailing = Mailings.objects.get(id=pk)
        except ObjectDoesNotExist:
            self.stdout.write(self.style.ERROR(f"Рассылка с ID {pk} не найдена."))
            return
        if mailing.status != Mailings.STATUS_CREATED:
            self.stdout.write(
                self.style.WARNING(
                    f"Рассылка с ID {pk} не может быть отправлена, так как ее статус: {mailing.status}."
                )
            )
            return
        mailing.status = Mailings.STATUS_STARTED
        mailing.first_sending = timezone.now()
        mailing.save()
        for contact in mailing.contact.all():
            attempt = MailingAttempt(mailing=mailing)
            try:
                send_mail(
                    mailing.message.subject,
                    mailing.message.body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[contact.email],
                    fail_silently=False,
                )
                attempt.status = MailingAttempt.STATUS_SUCCESSFUL
                attempt.server_response = "Письмо отправлено успешно."
                self.stdout.write(self.style.SUCCESS(f"Письмо отправлено на {contact.email}."))
            except Exception as e:
                attempt.status = MailingAttempt.STATUS_NOT_SUCCESSFUL
                attempt.server_response = str(e)
                self.stdout.write(self.style.ERROR(f"Ошибка при отправке на {contact.email}: {e}"))

            attempt.save()

        mailing.status = Mailings.STATUS_COMPLETED
        mailing.end_sending = timezone.now()
        mailing.save()
        self.stdout.write(self.style.SUCCESS("Рассылка успешно отправлена!"))

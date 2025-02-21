from django.core.mail import send_mail
from django.core.management.base import BaseCommand

from mailings.models import MailingAttempt, Mailings


class Command(BaseCommand):
    help = "Отправка рассылки по требованию"

    def add_arguments(self, parser):
        parser.add_argument("pk", type=int, help="ID рассылки для отправки")

    def handle(self, *args, **kwargs):
        pk = kwargs["pk"]
        mailing = Mailings.objects.get(id=pk)
        for contact in mailing.contact.all():
            try:
                send_mail(
                    mailing.message.subject,
                    mailing.message.body,
                    "rmiftyaeva@mail.ru",
                    [contact.email],
                    fail_silently=False,
                )
                status = "Успешно"
                server_response = "Письмо отправлено успешно."
            except Exception as e:
                status = "Не успешно"
                server_response = str(e)

            MailingAttempt.objects.create(mailing=mailing, status=status, server_response=server_response)
        self.stdout.write(self.style.SUCCESS("Рассылка успешно отправлена!"))

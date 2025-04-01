from django.db import models

from users.models import User


class Contact(models.Model):
    email = models.EmailField(verbose_name="Электронная почта", unique=True)
    full_name = models.CharField(max_length=150, verbose_name="ФИО")
    comment = models.TextField(verbose_name="Комментарий", null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Владелец", null=True, blank=True)

    class Meta:
        verbose_name = "Получатель рассылки"
        verbose_name_plural = "Получатели рассылок"
        permissions = [
            ("can_view_contact", "Can_view_contact"),
        ]

    def __str__(self):
        return self.full_name


class Message(models.Model):
    subject = models.CharField(max_length=150, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Тело письма")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Владелец", null=True, blank=True)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        permissions = [
            ("can_view_message", "Can_view_message"),
        ]

    def __str__(self):
        return self.subject


class Mailings(models.Model):
    STATUS_CREATED = "created"
    STATUS_STARTED = "started"
    STATUS_COMPLETED = "completed"

    MAILING_STATUSES_CHOICES = [
        (STATUS_CREATED, "Создана"),
        (STATUS_STARTED, "Запущена"),
        (STATUS_COMPLETED, "Завершена"),
    ]

    first_sending = models.DateTimeField(verbose_name="Дата и время первой отправки", null=True, blank=True)
    end_sending = models.DateTimeField(verbose_name="Дата и время окончания отправки", null=True, blank=True)
    status = models.CharField(
        max_length=9, choices=MAILING_STATUSES_CHOICES, default=STATUS_CREATED, verbose_name="Статус"
    )
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="Сообщение")
    contact = models.ManyToManyField(Contact, verbose_name="Получатели")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Владелец", null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["status"]
        permissions = [
            ("can_is_active_mailings", "Can_is_active_mailings"),
            ("can_view_mailings", "Can_view_mailings"),
        ]


class MailingAttempt(models.Model):
    STATUS_SUCCESSFUL = "successfully"
    STATUS_NOT_SUCCESSFUL = "not successful"

    STATUSES_CHOICES = [
        (STATUS_SUCCESSFUL, "Успешно"),
        (STATUS_NOT_SUCCESSFUL, "Не успешно"),
    ]

    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время попытки")
    status = models.CharField(max_length=20, choices=STATUSES_CHOICES, verbose_name="Статус")
    server_response = models.TextField(blank=True, verbose_name="Ответ почтового сервера ")
    mailing = models.ForeignKey(Mailings, on_delete=models.CASCADE, verbose_name="Рассылка")

    def __str__(self):
        return f"Attempt: {self.attempt_time} - {self.status}"

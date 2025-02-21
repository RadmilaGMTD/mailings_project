from django.db import models


class Contact(models.Model):
    email = models.EmailField(verbose_name="Электронная почта", unique=True)
    full_name = models.CharField(max_length=150, verbose_name="ФИО")
    comment = models.TextField(verbose_name="Комментарий", null=True, blank=True)

    class Meta:
        verbose_name = "Получатель рассылки"
        verbose_name_plural = "Получатели рассылок"

    def __str__(self):
        return self.full_name


class Message(models.Model):
    subject = models.CharField(max_length=150, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Тело письма")

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

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

    first_sending = models.DateTimeField(verbose_name="Дата и время первой отправки")
    end_sending = models.DateTimeField(verbose_name="Дата и время окончания отправки")
    status = models.CharField(
        max_length=9, choices=MAILING_STATUSES_CHOICES, default=STATUS_CREATED, verbose_name="Статус"
    )
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="Сообщение")
    contact = models.ManyToManyField(Contact, verbose_name="Получатели")

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["status"]


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

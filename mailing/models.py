from django.db import models

class Receiver(models.Model):
    """Model for mailing receiver"""
    email = models.EmailField(unique=True, verbose_name='Email')
    name = models.CharField(max_length=150, verbose_name='ФИО')
    comment = models.TextField(null=True, blank=True, verbose_name='Комментарий')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'получатель'
        verbose_name_plural = 'получатели'
        ordering = ['email', ]

class Message(models.Model):
    """Model for message"""
    title = models.CharField(max_length=50, verbose_name='Тема письма')
    text = models.TextField(verbose_name='Тело письма')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'
        ordering = ['title', ]

class Mailing(models.Model):
    """Model for mailing"""
    class Status(models.TextChoices):
        NEW = 'NEW', 'Создана'
        IN_PROGRESS = 'INP', 'Запущена'
        DONE = 'DONE', 'Завершена'

    start_time = models.DateTimeField(verbose_name='Время начала отправки')
    finish_time = models.DateTimeField(null=True, blank=True, verbose_name='Время завершения отправки')
    status = models.CharField(
        max_length=4,
        choices=Status.choices,
        default=Status.NEW
    )
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='mailings', verbose_name='Сообщение')
    receiver = models.ManyToManyField(Receiver, verbose_name='Получатели')

    def __str__(self):
        return f'Тема - {self.message.title}. Начало отправки - {self.start_time.strftime("%d.%m.%Y %H:%M")}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        ordering = ['-start_time', ]


class MailingAttempt(models.Model):
    """Model for mailing attempt"""
    class Status(models.TextChoices):
        SUCCESSFUL = 'SUC', 'Успешно'
        UNSUCCESSFUL = 'UNS', 'Не успешно'
    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name='Время попытки отправки')
    status = models.CharField(
        max_length=3,
        choices=Status.choices,
        default=Status.SUCCESSFUL
    )
    mail_server_reply = models.TextField(verbose_name='Ответ почтового сервера')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='mailing_attempts', verbose_name='Рассылка')

    def __str__(self):
        return f'Тема - {self.mailing.message.title}. Время попытки - {self.attempt_time.strftime("%d.%m.%Y %H:%M")}'

    class Meta:
        verbose_name = 'попытка рассылки'
        verbose_name_plural = 'попытки рассылки'
        ordering = ['-attempt_time', ]



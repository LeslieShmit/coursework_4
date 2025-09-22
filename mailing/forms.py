from django import forms

from .models import Receiver, Mailing, Message
from .mixins import FormStyleMixin

class ReceiverForm(FormStyleMixin, forms.ModelForm):
    placeholder_fields = {
        "email": "Введите email",
        "name": "Введите ФИО",
        "comment": "Комментарий (необязательно)",
    }

    class Meta:
        model = Receiver
        fields = "__all__"

class MessageForm(FormStyleMixin, forms.ModelForm):
    placeholder_fields = {
        "title": "Введите тему письма",
        "text": "Введите текст письма",
    }

class MailingForm(FormStyleMixin, forms.ModelForm):
    placeholder_fields = {
        "message": "Выберете сообщение для отправки",
        "receiver": "Выберете получателей",
    }

    class Meta:
        model = Mailing
        exclude = ["start_time", "finish_time", "status",]


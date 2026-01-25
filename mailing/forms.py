from django import forms
from django.utils import timezone

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

    class Meta:
        model = Message
        fields = "__all__"

class MailingForm(FormStyleMixin, forms.ModelForm):
    placeholder_fields = {
        "message": "Выберите сообщение для отправки",
        "receivers": "Выберите получателей",
        "start_time": "С какого времени рассылка может быть запущена",
        "end_time": "До какого времени рассылка может быть запущена",
    }

    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        }),
        label='Начало рассылки',
        input_formats=['%Y-%m-%dT%H:%M']
    )

    end_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        }),
        label='Конец рассылки',
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = Mailing
        exclude = ["status"]

    def clean_start_time(self):
        start_time = self.cleaned_data.get('start_time')
        if start_time is None:
            raise forms.ValidationError("Введите дату и время начала рассылки")
        if start_time < timezone.now():
            raise forms.ValidationError('Нельзя указывать прошедшее время')
        return start_time

    def clean_end_time(self):
        end_time = self.cleaned_data.get('end_time')
        if end_time is None:
            raise forms.ValidationError("Введите дату и время окончания рассылки")
        return end_time

    def clean(self):
        """Проверка на то, что end_time > start_time"""
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time:
            if start_time >= end_time:
                raise forms.ValidationError("Конечное время должно быть позже начального")

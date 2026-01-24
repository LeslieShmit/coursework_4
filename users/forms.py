from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from .mixins import FormStyleMixin


class CustomUserCreationForm(FormStyleMixin, UserCreationForm):
    phone_number = forms.CharField(
        required=False,
        max_length=15,
        help_text='Введите номер телефона (опционально)'
    )
    country = forms.CharField(
        required=False,
        max_length=50,
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'country', 'phone_number', 'password1', 'password2')

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError('Номер телефона может состоять только из цифр.')
        return phone_number

class CustomUserChangeForm(FormStyleMixin, UserChangeForm):
    password = None

    phone_number = forms.CharField(
        required=False,
        max_length=15,
        help_text='Введите номер телефона (опционально)'
    )
    country = forms.CharField(
        required=False,
        max_length=50,
    )
    avatar = forms.ImageField(required=False, help_text='Загрузите свой аватар(Опционально)')

    class Meta:
        model = CustomUser
        fields = ('email', 'country', 'phone_number', 'avatar',)

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError('Номер телефона может состоять только из цифр.')
        return phone_number
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import get_user_model

from .models import CustomUser


class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:password_reset_done')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        activation_url = self.request.build_absolute_uri(
            reverse('users:activate', args=[uid, token])
        )

        send_mail(
            subject='Подтверждение регистрации',
            message=f'Перейдите по ссылке для активации аккаунта:\n{activation_url}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

        self.object = user
        return redirect(self.get_success_url())

class EditUserView(LoginRequiredMixin, UpdateView):
    template_name = 'users/update.html'
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('mailing:home')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        # Дополнительно проверяем, что редактируемый объект — это текущий пользователь
        if form.instance != self.request.user:
            raise PermissionDenied("Вы не можете редактировать другого пользователя")
        return super().form_valid(form)

User = get_user_model()

class ActivateUserView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()

        return redirect('users:login')

class UserDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    context_object_name = 'user'
    template_name = 'users/user_details.html'


    def get_object(self, queryset=None):
        return self.request.user
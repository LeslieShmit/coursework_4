from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView


from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


class RegisterView(CreateView):
    template_name = "users/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:password_reset_done")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        activation_url = self.request.build_absolute_uri(
            reverse("users:activate", args=[uid, token])
        )

        send_mail(
            subject="Подтверждение регистрации",
            message=f"Перейдите по ссылке для активации аккаунта:\n{activation_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

        self.object = user
        return redirect(self.get_success_url())


class EditUserView(LoginRequiredMixin, UpdateView):
    template_name = "users/update.html"
    form_class = CustomUserChangeForm
    success_url = reverse_lazy("mailing:home")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
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

        return redirect("users:login")


class UserDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    context_object_name = "user"
    template_name = "users/user_details.html"

    def get_object(self, queryset=None):
        return self.request.user


class UserListView(PermissionRequiredMixin, ListView):
    model = CustomUser
    template_name = "users/user_list.html"
    permission_required = "users.view_all_users"
    paginate_by = 20


class UserBlockView(PermissionRequiredMixin, View):
    permission_required = "users.block_user"

    def post(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        user.is_active = False
        user.save()
        messages.success(request, "Пользователь заблокирован")
        return redirect("users:user_list")


class UserDetailAdminView(PermissionRequiredMixin, DetailView):
    model = CustomUser
    template_name = "users/user_detail_admin.html"
    context_object_name = "user"
    permission_required = "users.view_all_users"

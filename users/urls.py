from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import path, reverse_lazy

from .views import (ActivateUserView, EditUserView, RegisterView,
                    UserBlockView, UserDetailAdminView, UserDetailView,
                    UserListView)

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("activate/<uidb64>/<token>/", ActivateUserView.as_view(), name="activate"),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="mailing:home"), name="logout"),
    path("profile/edit/", EditUserView.as_view(), name="edit_profile"),
    path("profile/details/", UserDetailView.as_view(), name="user_details"),
    path("profiles/", UserListView.as_view(), name="user_list"),
    path("profiles/<int:pk>/block/", UserBlockView.as_view(), name="user_block"),
    path("profiles/<int:pk>/", UserDetailAdminView.as_view(), name="user_detail_admin"),
    path(
        "profile/password/",
        PasswordChangeView.as_view(
            template_name="users/change_password.html",
            success_url=reverse_lazy("mailing:home"),
        ),
        name="change_password",
    ),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="users/password_reset.html",
            email_template_name="users/password_reset_email.html",
            success_url=reverse_lazy("users:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
            success_url=reverse_lazy("users:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]

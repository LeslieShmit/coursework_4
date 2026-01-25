from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from mailing.services import send_mailing

from .forms import MailingForm, MessageForm, ReceiverForm
from .mixins import OwnerRequiredMixin
from .models import Mailing, MailingAttempt, Message, Receiver


@method_decorator(cache_page(60 * 15), name="dispatch")
class HomePageView(TemplateView):
    template_name = "mailing/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_mailings"] = Mailing.objects.count()
        context["active_mailings"] = Mailing.objects.filter(status="INP").count()
        context["unique_receivers"] = Receiver.objects.count()
        return context


class StatisticView(TemplateView):
    template_name = "mailing/statistics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        user_mailings = Mailing.objects.filter(owner=user)

        context["mailing_attempts_suc"] = MailingAttempt.objects.filter(
            mailing__in=user_mailings, status="SUC"
        ).count()
        context["mailing_attempts_uns"] = MailingAttempt.objects.filter(
            mailing__in=user_mailings, status="UNS"
        ).count()
        context["total_messages_sent"] = MailingAttempt.objects.filter(
            mailing__in=user_mailings
        ).count()

        return context


class MailingListView(ListView):
    model = Mailing
    context_object_name = "mailings"
    template_name = "mailing/mailing_list.html"
    ordering = ["-start_time"]
    paginate_by = 20

    def get_queryset(self):
        user = self.request.user
        if user.has_perm("mailing.view_all_mailings"):
            return cache.get_or_set(
                "manager_mailing_list",
                Mailing.objects.all().order_by("-start_time"),
                300,
            )
        return Mailing.objects.filter(owner=user)


class MailingDetailView(DetailView):
    model = Mailing
    context_object_name = "mailing"
    template_name = "mailing/mailing_detail.html"


class MailingCreateView(CreateView):
    model = Mailing
    template_name = "mailing/form.html"
    form_class = MailingForm
    success_url = reverse_lazy("mailing:mailing_list")

    def form_valid(self, form):
        cache.delete("manager_mailing_list")
        mailing = form.save(commit=False)
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Создать рассылку"
        context["submit_text"] = "Создать"
        context["cancel_url"] = reverse("mailing:mailing_list")
        return context


class MailingSendView(View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        if mailing.owner != request.user:
            raise PermissionDenied
        send_mailing(mailing)
        messages.success(request, "Рассылка отправлена")
        return redirect("mailing:mailing_detail", pk=pk)


class MailingUpdateView(OwnerRequiredMixin, UpdateView):
    model = Mailing
    template_name = "mailing/form.html"
    form_class = MailingForm
    success_url = reverse_lazy("mailing:mailing_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        cache.delete("manager_mailing_list")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Редактировать рассылку"
        context["submit_text"] = "Создать изменения"
        context["cancel_url"] = reverse("mailing:mailing_list")
        return context


class MailingDeleteView(OwnerRequiredMixin, DeleteView):
    model = Mailing
    template_name = "mailing/confirm_delete.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        cache.delete("manager_mailing_list")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_name"] = "рассылку"
        context["object_description"] = self.object.message.title
        context["cancel_url"] = reverse(
            "mailing:mailing_details", args=[self.object.pk]
        )
        return context


class MailingBlockView(PermissionRequiredMixin, View):
    permission_required = "mailing.block_mailing"

    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        mailing.is_blocked = True
        mailing.save()
        messages.success(request, "Рассылка заблокирована")
        return redirect("mailing:mailing_list")


class MessageListView(ListView):
    model = Message
    context_object_name = "messages"
    template_name = "mailing/message_list.html"
    paginate_by = 20

    def get_queryset(self):
        user = self.request.user
        if user.has_perm("mailing.view_all_messages"):
            return cache.get_or_set(
                "manager_messages_list", Message.objects.all(), 60 * 5
            )
        return Message.objects.filter(owner=user)


class MessageDetailView(DetailView):
    model = Message
    context_object_name = "message"
    template_name = "mailing/message_detail.html"


class MessageCreateView(CreateView):
    model = Message
    template_name = "mailing/form.html"
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Создать сообщение"
        context["submit_text"] = "Создать"
        context["cancel_url"] = reverse("mailing:message_list")
        return context

    def form_valid(self, form):
        cache.delete("manager_messages_list")
        message = form.save(commit=False)
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(OwnerRequiredMixin, UpdateView):
    model = Message
    template_name = "mailing/form.html"
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        cache.delete("manager_messages_list")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Редактировать сообщение"
        context["submit_text"] = "Сохранить изменения"
        context["cancel_url"] = reverse("mailing:message_list")
        return context


class MessageDeleteView(OwnerRequiredMixin, DeleteView):
    model = Message
    template_name = "mailing/confirm_delete.html"
    success_url = reverse_lazy("mailing:message_list")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        cache.delete("manager_messages_list")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_name"] = "сообщение"
        context["object_description"] = self.object.title
        context["cancel_url"] = reverse(
            "mailing:message_details", args=[self.object.pk]
        )
        return context


class ReceiverListView(ListView):
    model = Receiver
    context_object_name = "receivers"
    template_name = "mailing/receiver_list.html"
    paginate_by = 20

    def get_queryset(self):
        user = self.request.user
        if user.has_perm("mailing.view_all_receivers"):
            return cache.get_or_set(
                "manager_receivers_list", Receiver.objects.all(), 60 * 5
            )
        return Receiver.objects.filter(owner=user)


class ReceiverDetailView(DetailView):
    model = Receiver
    context_object_name = "receiver"
    template_name = "mailing/receiver_detail.html"


class ReceiverCreateView(CreateView):
    model = Receiver
    template_name = "mailing/form.html"
    form_class = ReceiverForm
    success_url = reverse_lazy("mailing:receiver_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Создать получателя"
        context["submit_text"] = "Создать"
        context["cancel_url"] = reverse("mailing:receiver_list")
        return context

    def form_valid(self, form):
        cache.delete("manager_receivers_list")
        receiver = form.save(commit=False)
        user = self.request.user
        receiver.owner = user
        receiver.save()
        return super().form_valid(form)


class ReceiverUpdateView(OwnerRequiredMixin, UpdateView):
    model = Receiver
    template_name = "mailing/form.html"
    form_class = ReceiverForm
    success_url = reverse_lazy("mailing:receiver_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        cache.delete("manager_receivers_list")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Редактировать получателя"
        context["submit_text"] = "Сохранить изменения"
        context["cancel_url"] = reverse("mailing:receiver_list")
        return context


class ReceiverDeleteView(OwnerRequiredMixin, DeleteView):
    model = Receiver
    template_name = "mailing/confirm_delete.html"
    success_url = reverse_lazy("mailing:receiver_list")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        cache.delete("manager_receivers_list")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_name"] = "получателя"
        context["object_description"] = self.object.email
        context["cancel_url"] = reverse(
            "mailing:receiver_details", args=[self.object.pk]
        )
        return context


class MailingAttemptListView(ListView):
    model = MailingAttempt
    context_object_name = "mailing_attempts"
    template_name = "mailing/mailing_attempt_list.html"
    paginate_by = 20

    def get_queryset(self):
        mailing_id = self.kwargs["mailing_id"]
        return MailingAttempt.objects.filter(mailing_id=mailing_id).order_by(
            "-attempt_time"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mailing"] = Mailing.objects.get(id=self.kwargs["mailing_id"])
        return context


class MailingAttemptDetailView(DetailView):
    model = MailingAttempt
    context_object_name = "mailing_attempt"
    template_name = "mailing/mailing_attempt_detail.html"

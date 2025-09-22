from django.shortcuts import render
from .models import Receiver, Message, Mailing, MailingAttempt
from .forms import ReceiverForm, MessageForm, MailingForm

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

class MailingListView(ListView):
    model = Mailing
    context_object_name = 'mailings'
    template_name = 'mailing/home.html'
    ordering = ['-start_time']
    paginate_by = 20

class MailingDetailView(DetailView):
    model = Mailing
    context_object_name = 'mailing'
    template_name = 'mailing/mailing_detail.html'

class MailingCreateView(CreateView):
    model = Mailing
    template_name = 'mailing/mailing_form.html'
    form_class = MailingForm
    success_url = reverse_lazy('mailing:home')

class MailingSendView(View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        message = mailing.message

        for receiver in mailing.receivers.all():
            try:
                result = send_mail(
                    subject=message.title,
                    message=message.text,
                    from_email="noreply@example.com",
                    recipient_list=[receiver.email],
                    fail_silently=False,
                )
                MailingAttempt.objects.create(
                    mailing=mailing,
                    receiver=receiver,
                    status="SUC" if result else "UNS",
                    mail_server_reply=f"send_mail returned {result}",
                )
            except Exception as e:
                MailingAttempt.objects.create(
                    mailing=mailing,
                    receiver=receiver,
                    status="UNS",
                    mail_server_reply=str(e),
                )

        messages.success(request, "Рассылка отправлена")
        return redirect("mailing:mailing_detail", pk=pk)

class MailingUpdateView(UpdateView):
    model = Mailing
    template_name = 'mailing/mailing_form.html'
    form_class = MailingForm
    success_url = reverse_lazy('mailing:home')

class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:home')

class MessageListView(ListView):
    model = Message
    context_object_name = 'messages'
    template_name = 'mailing/message_list.html'
    paginate_by = 20


class MessageDetailView(DetailView):
    model = Mailing
    context_object_name = 'message'
    template_name = 'mailing/message_detail.html'


class MessageCreateView(CreateView):
    model = Mailing
    template_name = 'mailing/message_form.html'
    form_class = MessageForm
    success_url = reverse_lazy('mailing:home')


class MessageUpdateView(UpdateView):
    model = Mailing
    template_name = 'mailing/message_form.html'
    form_class = MessageForm
    success_url = reverse_lazy('mailing:home')


class MessageDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailing/message_confirm_delete.html'
    success_url = reverse_lazy('mailing:home')

class ReceiverListView(ListView):
    model = Receiver
    context_object_name = 'receivers'
    template_name = 'mailing/receiver_list.html'
    paginate_by = 20


class ReceiverDetailView(DetailView):
    model = Mailing
    context_object_name = 'receiver'
    template_name = 'mailing/receiver_detail.html'


class ReceiverCreateView(CreateView):
    model = Mailing
    template_name = 'mailing/receiver_form.html'
    form_class = ReceiverForm
    success_url = reverse_lazy('mailing:home')


class ReceiverUpdateView(UpdateView):
    model = Mailing
    template_name = 'mailing/receiver_form.html'
    form_class = ReceiverForm
    success_url = reverse_lazy('mailing:home')


class ReceiverDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailing/receiver_confirm_delete.html'
    success_url = reverse_lazy('mailing:home')

class MailingAttemptListView(ListView):
    model = MailingAttempt
    context_object_name = 'mailing_attempts'
    template_name = 'mailing/mailing_attempt_list.html'
    paginate_by = 20

class MailingAttemptDetailView(DetailView):
    model = Mailing
    context_object_name = 'mailing_attempt'
    template_name = 'mailing/mailing_attempt_detail.html'

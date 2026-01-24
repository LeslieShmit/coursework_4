from django.shortcuts import render
from .models import Receiver, Message, Mailing, MailingAttempt
from .forms import ReceiverForm, MessageForm, MailingForm

from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from mailing.services import send_mailing


class HomePageView(TemplateView):
    template_name = 'mailing/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_mailings'] = Mailing.objects.count()
        context['active_mailings'] = Mailing.objects.filter(status='INP').count()
        context['unique_receivers'] = Receiver.objects.count()
        return context

class MailingListView(ListView):
    model = Mailing
    context_object_name = 'mailings'
    template_name = 'mailing/mailing_list.html'
    ordering = ['-start_time']
    paginate_by = 20


class MailingDetailView(DetailView):
    model = Mailing
    context_object_name = 'mailing'
    template_name = 'mailing/mailing_detail.html'

class MailingCreateView(CreateView):
    model = Mailing
    template_name = 'mailing/form.html'
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Создать рассылку'
        context['submit_text'] = 'Создать'
        context['cancel_url'] = reverse('mailing:mailing_list')
        return context

class MailingSendView(View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        send_mailing(mailing)
        messages.success(request, "Рассылка отправлена")
        return redirect("mailing:mailing_detail", pk=pk)


class MailingUpdateView(UpdateView):
    model = Mailing
    template_name = 'mailing/form.html'
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Редактировать рассылку'
        context['submit_text'] = 'Создать изменения'
        context['cancel_url'] = reverse('mailing:mailing_list')
        return context

class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailing/confirm_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'рассылку'
        context['object_description'] = self.object.message.title
        context['cancel_url'] = reverse('mailing:mailing_details', args=[self.object.pk])
        return context

class MessageListView(ListView):
    model = Message
    context_object_name = 'messages'
    template_name = 'mailing/message_list.html'
    paginate_by = 20


class MessageDetailView(DetailView):
    model = Message
    context_object_name = 'message'
    template_name = 'mailing/message_detail.html'


class MessageCreateView(CreateView):
    model = Message
    template_name = 'mailing/form.html'
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Создать сообщение'
        context['submit_text'] = 'Создать'
        context['cancel_url'] = reverse('mailing:message_list')
        return context


class MessageUpdateView(UpdateView):
    model = Message
    template_name = 'mailing/form.html'
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Редактировать сообщение'
        context['submit_text'] = 'Сохранить изменения'
        context['cancel_url'] = reverse('mailing:message_list')
        return context


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'mailing/confirm_delete.html'
    success_url = reverse_lazy('mailing:message_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'сообщение'
        context['object_description'] = self.object.title
        context['cancel_url'] = reverse('mailing:message_details', args=[self.object.pk])
        return context

class ReceiverListView(ListView):
    model = Receiver
    context_object_name = 'receivers'
    template_name = 'mailing/receiver_list.html'
    paginate_by = 20


class ReceiverDetailView(DetailView):
    model = Receiver
    context_object_name = 'receiver'
    template_name = 'mailing/receiver_detail.html'


class ReceiverCreateView(CreateView):
    model = Receiver
    template_name = 'mailing/form.html'
    form_class = ReceiverForm
    success_url = reverse_lazy('mailing:receiver_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Создать получателя'
        context['submit_text'] = 'Создать'
        context['cancel_url'] = reverse('mailing:receiver_list')
        return context


class ReceiverUpdateView(UpdateView):
    model = Receiver
    template_name = 'mailing/form.html'
    form_class = ReceiverForm
    success_url = reverse_lazy('mailing:receiver_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Редактировать получателя'
        context['submit_text'] = 'Сохранить изменения'
        context['cancel_url'] = reverse('mailing:receiver_list')
        return context


class ReceiverDeleteView(DeleteView):
    model = Receiver
    template_name = 'mailing/confirm_delete.html'
    success_url = reverse_lazy('mailing:receiver_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'получателя'
        context['object_description'] = self.object.email
        context['cancel_url'] = reverse('mailing:receiver_details', args=[self.object.pk])
        return context

class MailingAttemptListView(ListView):
    model = MailingAttempt
    context_object_name = 'mailing_attempts'
    template_name = 'mailing/mailing_attempt_list.html'
    paginate_by = 20

    def get_queryset(self):
        mailing_id = self.kwargs['mailing_id']
        return MailingAttempt.objects.filter(mailing_id=mailing_id).order_by('-attempt_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailing'] = Mailing.objects.get(id=self.kwargs['mailing_id'])
        return context

class MailingAttemptDetailView(DetailView):
    model = MailingAttempt
    context_object_name = 'mailing_attempt'
    template_name = 'mailing/mailing_attempt_detail.html'

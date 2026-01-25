from django.urls import path
from mailing.apps import MailingConfig

from .views import MailingListView, MailingSendView, MailingCreateView, MailingDetailView, MailingDeleteView, \
    MessageListView, MessageCreateView, MessageDeleteView, MessageUpdateView, MessageDetailView, MailingUpdateView, \
    ReceiverCreateView, ReceiverDeleteView, ReceiverDetailView, ReceiverUpdateView, ReceiverListView, \
    MailingAttemptDetailView, MailingAttemptListView, HomePageView, StatisticView, MailingBlockView

app_name = MailingConfig.name

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('mailing/statistic', StatisticView.as_view(), name='statistic'),
    path('mailing/<int:pk>/send/', MailingSendView.as_view(), name='mailing_send'),
    path('mailing/new/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing/<int:pk>/', MailingDetailView.as_view(), name='mailing_details'),
    path('mailing/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailing/<int:pk>/edit/', MailingUpdateView.as_view(), name='mailing_edit'),
    path('mailing/<int:pk>/block/', MailingBlockView.as_view(), name='mailing_block'),
    path('messages', MessageListView.as_view(), name='message_list'),
    path('message/new/', MessageCreateView.as_view(), name='message_create'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message_details'),
    path('message/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),
    path('message/<int:pk>/edit/', MessageUpdateView.as_view(), name='message_edit'),
    path('receivers', ReceiverListView.as_view(), name='receiver_list'),
    path('receiver/new/', ReceiverCreateView.as_view(), name='receiver_create'),
    path('receiver/<int:pk>/', ReceiverDetailView.as_view(), name='receiver_details'),
    path('receiver/<int:pk>/delete/', ReceiverDeleteView.as_view(), name='receiver_delete'),
    path('receiver/<int:pk>/edit/', ReceiverUpdateView.as_view(), name='receiver_edit'),
    path('mailing/<int:mailing_id>/attempts/', MailingAttemptListView.as_view(), name='mailing_attempts'),
    path('mailing/<int:mailing_id>/attempt/<int:pk>/', MailingAttemptDetailView.as_view(), name='mailing_attempt'),
]

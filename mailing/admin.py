from django.contrib import admin

from .models import Mailing, MailingAttempt, Message, Receiver

# Register your models here.
admin.site.register(Receiver)
admin.site.register(Message)
admin.site.register(Mailing)
admin.site.register(MailingAttempt)

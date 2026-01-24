from django.contrib import admin
from .models import Receiver, Message, Mailing, MailingAttempt

# Register your models here.
admin.site.register(Receiver)
admin.site.register(Message)
admin.site.register(Mailing)
admin.site.register(MailingAttempt)
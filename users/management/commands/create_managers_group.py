from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create managers group"

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name="Менеджеры")

        permissions = Permission.objects.filter(
            codename__in=[
                "view_all_mailings",
                "block_mailing",
                "view_all_receivers",
                "view_all_messages",
                "view_all_users",
                "block_user",
            ]
        )

        group.permissions.set(permissions)
        self.stdout.write(self.style.SUCCESS('Group "Менеджеры" created'))

# In your_app/signals.py

from django.core.management import call_command
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def load_fixtures(sender, **kwargs):
    call_command("loaddata", "initial_admin.json", app_label="register")

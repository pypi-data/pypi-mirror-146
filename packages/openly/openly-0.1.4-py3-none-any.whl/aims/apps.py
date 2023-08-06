from django.apps import apps, AppConfig
from django.db.models.signals import post_migrate
from django.core.management import call_command


def my_callback(sender, **kwargs):
    model = apps.get_model("aims", "CommitmentTotal")
    model.finance_annotate()


def call_sync_translation_fields(*arga, **kwargs):
    call_command("sync_translation_fields", "--noinput")


def call_update_translation_fields(*arga, **kwargs):
    call_command("update_translation_fields")


class AimsConfig(AppConfig):
    name = "aims"

    def ready(self):
        post_migrate.connect(my_callback, sender=self)
        post_migrate.connect(call_sync_translation_fields, sender=self)
        post_migrate.connect(call_update_translation_fields, sender=self)

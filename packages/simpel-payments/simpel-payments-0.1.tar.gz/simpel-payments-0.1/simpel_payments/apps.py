from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate
from django.utils.translation import gettext_lazy as _


class SimpelPaymentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = "simpel_payments"
    label = "simpel_payments"
    verbose_name = _("Payments")
    icon = "credit-card-check-outline"

    def ready(self):
        from actstream import registry

        from simpel_payments import signals  # NOQA


        registry.register(self.get_model("Payment"))
        return super().ready()


def init_app(sender, **kwargs):
    pass

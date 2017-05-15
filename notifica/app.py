from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class NotificaConfig(AppConfig):
    name = 'notifica'
    verbose_name = _('notifica')

    def ready(self):
        import notifica.signals

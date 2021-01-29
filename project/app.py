from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ProjectConfig(AppConfig):
    name = 'project'
    verbose_name = _('Project')

    def ready(self):
        import notifica.signals

from django.apps import AppConfig


class SimpelProjectsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "simpel_projects"
    icon = "bulletin-board"
    label = "simpel_projects"
    verbose_name = "Projects"

    def ready(self):
        from actstream import registry

        from . import signals  # NOQA
        registry.register(self.get_model('WorkOrder'))
        registry.register(self.get_model('Task'))
        registry.register(self.get_model('Deliverable'))
        registry.register(self.get_model('CancelationDeliverable'))
        return super().ready()

from django.db import models
from django.utils.translation import gettext_lazy as _

from simpel_actions import mixins

from . import const

LEN_SHORT = 128
LEN_LONG = 255


class WorkOrderActionMixin(
    mixins.DraftMixin,
    mixins.TrashMixin,
    mixins.ValidateMixin,
    mixins.CompleteMixin,
    mixins.StatusMixin,
):
    DRAFT = const.DRAFT
    TRASH = const.TRASH
    VALID = const.VALID
    PROCESSED = const.PROCESSED
    COMPLETE = const.COMPLETE
    STATUS_CHOICES = (
        (DRAFT, _("Draft")),
        (TRASH, _("Trash")),
        (VALID, _("Valid")),
        (PROCESSED, _("Processed")),
        (COMPLETE, _("Complete")),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=const.DRAFT)

    class Meta:
        abstract = True

    @property
    def trash_ignore_condition(self):
        return self.is_trash

    @property
    def trash_valid_condition(self):
        return self.is_draft

    @property
    def validate_ignore_condition(self):
        return self.is_valid

    @property
    def validate_valid_condition(self):
        return self.is_draft

    @property
    def complete_ignore_condition(self):
        return self.is_complete

    @property
    def complete_valid_condition(self):
        return self.is_valid

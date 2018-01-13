from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel

from djangae.fields import RelatedSetField


class Project(TimeStampedModel):
    title = models.CharField(max_length=200)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)

    def __str__(self):
        return self.title


class Ticket(TimeStampedModel):
    SHORT_DESCRIPTION_MAX_LENGTH = 200

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    project = models.ForeignKey(Project, related_name="tickets")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, related_name="created_tickets")
    assignees = RelatedSetField(
        settings.AUTH_USER_MODEL, related_name="tickets")

    def __str__(self):
        return self.title

    @property
    def short_description(self):
        """A shorterned version of description."""
        trunc = '...'
        real_max_length = self.SHORT_DESCRIPTION_MAX_LENGTH - len(trunc)
        if len(self.description) < real_max_length:
            return self.description

        return self.description[0:real_max_length] + trunc

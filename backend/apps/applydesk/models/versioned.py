from django.db import models


class VersionStatus(models.TextChoices):
    DRAFT = "draft", "Draft"

    PUBLISHED = "published", "Published"

    ARCHIVED = "archived", "Archived"


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True


class BaseVersion(TimestampedModel):
    version = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=VersionStatus.choices,
        default=VersionStatus.DRAFT,
    )

    data = models.JSONField(
        default=dict,
    )

    class Meta:
        abstract = True


class VersionedModel(
    TimestampedModel,
):
    class Meta:
        abstract = True

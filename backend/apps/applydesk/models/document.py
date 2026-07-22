from django.db import models

from apps.applydesk.models.versioned import BaseVersion, VersionedModel, VersionStatus
from apps.applydesk.services.documents.storage import (
    document_upload_path,
)


class DocumentType(models.TextChoices):
    CV = "cv", "CV"

    COVER_LETTER = (
        "cover_letter",
        "Cover Letter",
    )

    CERTIFICATE_WORK = (
        "certificate_work",
        "Work Certificate",
    )

    CERTIFICATE_SCHOOL = (
        "certificate_school",
        "School Certificate",
    )

    CERTIFICATE = (
        "certificate",
        "Certificate",
    )

    PHOTO = "photo", "Photo"

    OTHER = "other", "Other"


class Document(models.Model):
    title = models.CharField(
        max_length=255,
    )

    document_type = models.CharField(
        max_length=50,
        choices=DocumentType.choices,
    )

    file = models.FileField(
        upload_to=document_upload_path,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.title


class DocumentDraft(models.Model):
    application = models.ForeignKey(
        "Application",
        on_delete=models.CASCADE,
        related_name="drafts",
    )

    document_type = models.CharField(max_length=50)

    field_values = models.JSONField(default=dict)

    source_draft = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    created_at = models.DateTimeField(auto_now_add=True)


class DocumentSchema(VersionedModel):
    name = models.CharField(max_length=255)

    document_type = models.CharField(
        max_length=50,
        choices=DocumentType.choices,
    )
    schema = models.JSONField(default=dict)

    @property
    def draft_version(self):
        return self.versions.filter(status=VersionStatus.DRAFT).first()  # ty:ignore[unresolved-attribute]

    @property
    def latest_published_version(self):
        return (
            self.versions.filter(status=VersionStatus.PUBLISHED)  # ty:ignore[unresolved-attribute]
            .order_by("-version")
            .first()
        )

    @property
    def published_versions(self):
        return self.versions.filter(  # ty:ignore[unresolved-attribute]
            status=VersionStatus.PUBLISHED
        ).order_by("-version")

    @property
    def latest_version(self):
        return self.versions.order_by("-version").first()  # ty:ignore[unresolved-attribute]


class DocumentSchemaVersion(BaseVersion):
    schema = models.ForeignKey(
        "DocumentSchema",
        on_delete=models.CASCADE,
        related_name="versions",
    )

    class Meta:
        indexes = [
            models.Index(fields=["schema", "status"]),
        ]

    def __str__(self):
        return f"{self.schema.name} v{self.version}"

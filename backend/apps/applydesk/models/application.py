from django.db import models

from .company import Company
from .document import Document, DocumentType


class Application(models.Model):
    STATUS_CHOICES = [
        ("saved", "Saved"),
        ("pre_call", "Pre-screening call"),
        ("prepared", "Prepared"),
        ("applied", "Applied"),
        ("waiting", "Waiting"),
        ("interview", "Interview"),
        ("offer", "Offer"),
        ("rejected", "Rejected"),
        ("closed", "Closed"),
        ("archived", "Archived"),
    ]

    LOCATION_TYPE_CHOICES = [
        ("remote", "Remote"),
        ("onsite", "On-site"),
        ("hybrid", "Hybrid"),
    ]

    PRIORITY_CHOICES = [
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
        ("I", "Initiative"),
    ]

    position_title = models.CharField(max_length=100)
    position_description = models.TextField(null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    location = models.CharField(max_length=100, null=True, blank=True)
    location_type = models.CharField(
        max_length=20,
        choices=LOCATION_TYPE_CHOICES,
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="saved",
    )

    notes = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)

    contact_person = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    contact_email = models.EmailField(null=True, blank=True)
    contact_phone = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    priority = models.CharField(
        max_length=1,
        choices=PRIORITY_CHOICES,
        default="B",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status_changed_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.position_title


class ApplicationDocument(models.Model):
    application = models.ForeignKey(
        "Application",
        on_delete=models.CASCADE,
        related_name="application_documents",
    )

    document = models.ForeignKey(
        "Document",
        on_delete=models.CASCADE,
        related_name="document_applications",
    )

    is_primary_cv = models.BooleanField(
        default=False,
    )

    is_primary_cover_letter = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = (
            "application",
            "document",
        )

    def __str__(self):
        return f"{self.application_id} ↔ {self.document_id}"  # ty:ignore[unresolved-attribute]


class ApplicationRequiredDocument(models.Model):
    application = models.ForeignKey(
        "Application",
        on_delete=models.CASCADE,
        related_name="required_documents",
    )

    document_type = models.CharField(max_length=50)

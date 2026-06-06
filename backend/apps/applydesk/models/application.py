from django.db import models

from .company import Company
from .file import FileAsset


class Application(models.Model):
    STATUS_CHOICES = [
        ("saved", "Saved"),
        ("prepared", "Prepared"),
        ("applied", "Applied"),
        ("waiting", "Waiting"),
        ("interview", "Interview"),
        ("offer", "Offer"),
        ("rejected", "Rejected"),
        ("archived", "Archived"),
    ]

    LOCATION_TYPE_CHOICES = [
        ("remote", "Remote"),
        ("onsite", "On-site"),
        ("hybrid", "Hybrid"),
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.position_title


class ApplicationFile(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    file = models.ForeignKey(FileAsset, on_delete=models.CASCADE)

    role = models.CharField(max_length=50)

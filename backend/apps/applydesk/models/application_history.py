from django.db import models

from apps.applydesk.models import Application


class ApplicationStatusHistory(models.Model):
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="history",
    )

    from_status = models.CharField(max_length=30, null=True, blank=True)
    to_status = models.CharField(max_length=30)

    created_at = models.DateTimeField(auto_now_add=True)

    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.application} {self.from_status} → {self.to_status}"

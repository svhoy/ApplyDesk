from django.db import models


class FileAsset(models.Model):
    TYPE = [
        ("cv", "CV"),
        ("cover_letter", "Cover Letter"),
        ("photo", "Photo"),
        ("certificate", "Certificate"),
        ("generated", "Generated"),
    ]

    type = models.CharField(max_length=30, choices=TYPE)

    file_path = models.CharField(max_length=500)  # RELATIV

    filename = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

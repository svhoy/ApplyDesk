from django.db import models

PRIORITY_CHOICES = [
    ("A", "A"),
    ("B", "B"),
    ("C", "C"),
]


class Company(models.Model):
    name = models.CharField(max_length=200)
    street = models.CharField(max_length=200, null=True, blank=True)
    street_number = models.CharField(max_length=10, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    zipcode = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    career_site = models.URLField(null=True, blank=True)
    priority = models.CharField(
        max_length=1,
        choices=PRIORITY_CHOICES,
        default="B",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.name

from collections import defaultdict

from apps.applydesk.models import Application


def list_applications():

    return Application.objects.select_related("company").order_by("-created_at")


def get_application(application_id):
    return Application.objects.select_related("company").get(pk=application_id)

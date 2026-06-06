from django.urls import path

from apps.applydesk.views.application import (
    application_create,
    application_delete,
    application_detail,
    application_edit,
    application_form,
    application_list,
    change_status,
    move_application,
)
from apps.applydesk.views.company import (
    company_create,
    company_delete,
    company_detail,
    company_edit,
    company_list,
)
from apps.applydesk.views.dashboard import dashboard
from apps.applydesk.views.pipeline import application_pipeline

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path(
        "applications/",
        application_list,
        name="application_list",
    ),
    path(
        "applications/create/",
        application_create,
        name="application_create",
    ),
    path(
        "applications/<int:application_id>/edit/",
        application_edit,
        name="application_edit",
    ),
    path(
        "applications/form/",
        application_form,
        name="application_form",
    ),
    path(
        "applications/<int:application_id>/",
        application_detail,
        name="application_detail",
    ),
    path(
        "applications/<int:application_id>/delete/",
        application_delete,
        name="application_delete",
    ),
    path(
        "applications/<int:application_id>/change-status/",
        change_status,
        name="change_status",
    ),
    path(
        "applications/move/",
        move_application,
        name="move_application",
    ),
    path(
        "applications/pipeline/",
        application_pipeline,
        name="application_pipeline",
    ),
    path(
        "companies/",
        company_list,
        name="company_list",
    ),
    path(
        "companies/<int:company_id>/",
        company_detail,
        name="company_detail",
    ),
    path("companies/create/", company_create, name="company_create"),
    path("companies/<int:company_id>/edit/", company_edit, name="company_edit"),
    path("companies/<int:company_id>/delete/", company_delete, name="company_delete"),
]

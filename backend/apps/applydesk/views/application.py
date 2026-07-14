from django.shortcuts import get_object_or_404, redirect, render

from apps.applydesk.forms.application import ApplicationForm, ApplicationUpdateForm
from apps.applydesk.models import Application
from apps.applydesk.queries.applications import get_application
from apps.applydesk.queries.pipeline import get_pipeline
from apps.applydesk.services.applications.completeness import (
    calculate_application_completeness,
)
from apps.applydesk.services.applications.create import create_application
from apps.applydesk.services.applications.delete import delete_application
from apps.applydesk.services.applications.document_state import (
    get_application_document_state,
)
from apps.applydesk.services.applications.documents import (
    sync_required_documents,
)
from apps.applydesk.services.applications.listings import list_applications_with_metrics
from apps.applydesk.services.applications.transition import transition_application
from apps.applydesk.services.applications.update import update_application
from apps.applydesk.services.applications.workflow import get_available_actions


def application_create(request):

    if request.method == "POST":
        form = ApplicationForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            required_docs = data.pop("required_documents", [])
            company_name = data.pop("company_name")

            application = create_application(
                company_name=company_name,
                **data,
            )

            sync_required_documents(application, required_docs)

    else:
        form = ApplicationForm()

    return render(
        request,
        "applications/partials/list.html",
        {
            "applications": list_applications_with_metrics(),
            "form": form,
        },
    )


def application_form(request):

    form = ApplicationForm()

    return render(
        request,
        "applications/partials/form.html",
        {
            "form": form,
        },
    )


def application_list(request):

    applications = list_applications_with_metrics()

    form = ApplicationForm()

    return render(
        request,
        "applications/list.html",
        {
            "applications": applications,
            "form": form,
        },
    )


def application_detail(
    request,
    application_id,
):

    application = get_application(
        application_id,
    )

    actions = get_available_actions(
        application,
    )

    completeness = calculate_application_completeness(
        application,
    )

    document_state = get_application_document_state(
        application,
    )

    return render(
        request,
        "applications/detail.html",
        {
            "application": application,
            "actions": actions,
            "completeness": completeness,
            "document_state": document_state,
        },
    )


def application_edit(request, application_id):

    application = get_object_or_404(
        Application,
        pk=application_id,
    )

    if request.method == "POST":
        form = ApplicationUpdateForm(
            request.POST,
            instance=application,
        )

        if form.is_valid():
            data = form.cleaned_data

            required_docs = form.cleaned_data.get("required_documents", [])

            update_application(
                application,
                **data,
            )

            sync_required_documents(
                application,
                required_docs,
            )

            return redirect(
                "application_detail",
                application.pk,
            )

    else:
        form = ApplicationUpdateForm(
            instance=application,
        )

    return render(
        request,
        "applications/edit.html",
        {
            "application": application,
            "form": form,
        },
    )


def application_delete(request, application_id):

    application = get_object_or_404(Application, pk=application_id)

    if request.method == "POST":
        delete_application(application)
        return redirect("application_list")

    return render(
        request,
        "applications/confirm_delete.html",
        {"application": application},
    )


def change_status(request, application_id):

    application = get_object_or_404(Application, pk=application_id)

    new_status = request.POST.get("status")
    old_status = application.status

    context = request.POST.get("context", "detail")

    transition_application(application, new_status)

    application = (
        Application.objects.select_related("company")
        .prefetch_related("history")
        .get(pk=application.pk)
    )

    actions = get_available_actions(application)

    if context == "kanban":
        columns = get_pipeline()

        return render(
            request,
            "applications/partials/kanban/kanban_update.html",
            {
                "application": application,
                "old_status": old_status,
                "columns": columns,
            },
        )

    # default = detail
    return render(
        request,
        "applications/partials/application_status_update.html",
        {
            "application": application,
            "actions": actions,
        },
    )


def move_application(request):

    application_id = request.POST.get("application_id")
    new_status = request.POST.get("status")

    application = get_object_or_404(
        Application,
        pk=application_id,
    )

    old_status = application.status

    transition_application(application, new_status)

    application.refresh_from_db()

    columns = get_pipeline()

    return render(
        request,
        "applications/partials/kanban/kanban_update.html",
        {
            "application": application,
            "old_status": old_status,
            "columns": columns,
        },
    )

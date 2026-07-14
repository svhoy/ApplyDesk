from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from apps.applydesk.forms.document import (
    DocumentForm,
)
from apps.applydesk.models import (
    Application,
    ApplicationDocument,
    Document,
)
from apps.applydesk.services.documents.attach_document import (
    attach_document_to_application,
    detach_document_from_application,
    upload_document_to_application,
)


def attach_document_modal(request, application_id):

    application = Application.objects.get(pk=application_id)

    documents = Document.objects.exclude(document_applications__application=application)

    return render(
        request,
        "applications/partials/attach_document_modal.html",
        {
            "application": application,
            "documents": documents,
        },
    )


def attach_document(
    request,
    application_id,
    document_id,
):

    application = get_object_or_404(
        Application,
        pk=application_id,
    )

    document = get_object_or_404(
        Document,
        pk=document_id,
    )

    link = attach_document_to_application(
        application=application,
        document=document,
    )

    return render(
        request,
        "applications/partials/document_row.html",
        {
            "link": link,
        },
    )


def detach_document(
    request,
    link_id,
):

    link = get_object_or_404(
        ApplicationDocument,
        pk=link_id,
    )

    detach_document_from_application(
        link=link,
    )

    return HttpResponse("")


def upload_document_for_application(
    request,
    application_id,
):

    application = get_object_or_404(
        Application,
        pk=application_id,
    )

    if request.method == "POST":
        form = DocumentForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            document = upload_document_to_application(
                application=application,
                document_type=form.cleaned_data["document_type"],
                file=form.cleaned_data["file"],
            )

            application.refresh_from_db()

            return render(
                request,
                "applications/partials/detail/application_documents.html",
                {
                    "application": application,
                },
            )

    else:
        document_type = request.GET.get("type")
        form = DocumentForm(initial={"document_type": document_type})
        return render(
            request,
            "applications/partials/upload_document_form.html",
            {
                "form": form,
                "application": application,
            },
        )

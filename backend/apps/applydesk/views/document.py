from django.shortcuts import get_object_or_404, render

from apps.applydesk.forms.document import DocumentForm
from apps.applydesk.models import Application, Document, DocumentSchema
from apps.applydesk.queries.document_schema import list_document_schemas
from apps.applydesk.services.documents.form_builder import build_document_form
from apps.applydesk.services.documents.generate import generate_document


def document_list(request):

    documents = Document.objects.all().order_by("-created_at")
    schemas = list_document_schemas()

    return render(
        request,
        "documents/document_list.html",
        {
            "documents": documents,
            "schemas": schemas,
        },
    )


def document_detail(request, pk):

    document = get_object_or_404(
        Document.objects.prefetch_related("document_applications__application"),
        pk=pk,
    )

    return render(
        request,
        "documents/document_detail.html",
        {
            "document": document,
            "applications": [
                link.application
                for link in document.document_applications.all()  # ty:ignore[unresolved-attribute]
            ],
        },
    )


def document_inspector(request, pk):

    document = get_object_or_404(
        Document.objects.prefetch_related("document_applications__application"),
        pk=pk,
    )

    return render(
        request,
        "documents/partials/document_inspector.html",
        {
            "document": document,
            "applications": [
                link.application
                for link in document.document_applications.all()  # ty:ignore[unresolved-attribute]
            ],
        },
    )


def document_upload_form(request):

    return render(
        request,
        "documents/partials/upload_form.html",
        {
            "form": DocumentForm(),
        },
    )


def document_upload_button(request):

    return render(
        request,
        "documents/partials/upload_button.html",
    )


def upload_document(request):

    form = DocumentForm(
        request.POST,
        request.FILES,
    )

    if form.is_valid():
        form.save()

    documents = Document.objects.all().order_by("-created_at")

    action = request.POST.get("action")

    template = "documents/partials/document_list_wrapper.html"

    context = {
        "documents": documents,
        "form": DocumentForm(),
        "action": action,
    }

    return render(
        request,
        template,
        context,
    )


def open_document_modal(request, application_id, document_type):

    application = get_object_or_404(
        Application,
        pk=application_id,
    )

    template = get_object_or_404(
        DocumentSchema,
        document_type=document_type,
    )

    FormClass = build_document_form(template.schema)

    form = FormClass()

    return render(
        request,
        "applications/partials/document_modal.html",
        {
            "form": form,
            "template": template,
            "application": application,
            "document_type": document_type,
        },
    )


def generate_document_view(request, application_id, document_type):

    application = get_object_or_404(
        Application,
        pk=application_id,
    )

    template = get_object_or_404(
        DocumentSchema,
        document_type=document_type,
    )

    FormClass = build_document_form(template.schema)

    form = FormClass(request.POST)

    if form.is_valid():
        document = generate_document(
            application=application,
            document_type=document_type,
            field_values=form.cleaned_data,
        )

        return render(
            request,
            "applications/partials/document_row.html",
            {
                "document": document,
            },
        )

    return render(
        request,
        "applications/partials/document_modal.html",
        {
            "form": form,
            "template": template,
            "application": application,
            "document_type": document_type,
        },
    )

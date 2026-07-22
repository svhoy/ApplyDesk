from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods, require_POST

from apps.applydesk.forms.document_schema import (
    DocumentSchemaFieldForm,
    DocumentSchemaGeneralForm,
)
from apps.applydesk.models import DocumentSchema
from apps.applydesk.queries.document_schema import (
    get_document_schema,
    list_document_schemas,
)
from apps.applydesk.services.documents.schema import (
    create_schema,
    duplicate_schema,
    update_schema,
)
from apps.applydesk.services.documents.schema_fields import (
    append_field,
    delete_field,
    get_field,
    move_field,
    update_field,
)
from apps.applydesk.services.documents.schema_versioning import (
    get_or_create_draft,
    publish_schema,
)


def render_schema_fields(request, schema):

    draft = schema.draft_version

    return render(
        request,
        "documents/schema/partials/schema_field_list.html",
        {
            "schema": schema,
            "draft": draft,
            "fields": draft.data.get("fields", []),
        },
    )


def schema_editor_new(request):
    form = DocumentSchemaGeneralForm()

    return render(
        request,
        "documents/schema/partials/schema_editor_panel.html",
        {
            "schema": None,
            "form": form,
            "version": None,
            "fields": [],
            "is_create": True,
        },
    )


def schema_create(request):
    version = None

    if request.method == "POST":
        form = DocumentSchemaGeneralForm(request.POST)
        if not form.is_valid():
            return render(
                request,
                "documents/schema/partials/schema_general_form.html",
                {
                    "form": form,
                },
            )
        schema = create_schema(
            name=form.cleaned_data["name"],
            document_type=form.cleaned_data["document_type"],
        )

        version = schema.latest_version()

        response = render(
            request,
            "documents/schema/partials/schema_editor_panel.html",
            {
                "schema": schema,
                "version": version,
                "form": DocumentSchemaGeneralForm(instance=schema),
                "fields": version.data.get("fields", []),
                "is_create": False,
            },
        )
        response["HX-Trigger"] = "schemaUpdated"
        return response

    return render(
        request,
        "documents/schema/partials/schema_general_form.html",
        {
            "form": DocumentSchemaGeneralForm(),
        },
    )


def schema_update(request, schema_id):
    schema = get_object_or_404(DocumentSchema, pk=schema_id)

    if request.method == "POST":
        form = DocumentSchemaGeneralForm(request.POST, instance=schema)

        if form.is_valid():
            update_schema(
                schema=schema,
                name=form.cleaned_data["name"],
                document_type=form.cleaned_data["document_type"],
            )

    version = schema.latest_version

    response = render(
        request,
        "documents/schema/partials/schema_editor_panel.html",
        {
            "schema": schema,
            "version": version,
            "fields": version.data.get("fields", []),
            "form": DocumentSchemaGeneralForm(instance=schema),
            "is_create": False,
        },
    )
    response["HX-Trigger"] = "schemaUpdated"
    return response


def schema_duplicate(request, schema_id):
    schema = get_document_schema(schema_id)

    duplicate = duplicate_schema(
        schema=schema,
    )

    version = get_or_create_draft(duplicate)

    form = DocumentSchemaGeneralForm(instance=duplicate)

    return render(
        request,
        "documents/schema/partials/schema_editor_panel.html",
        {
            "schema": duplicate,
            "version": version,
            "form": form,
            "fields": version.data.get("fields", []),
            "is_create": False,
        },
    )


def schema_field_form(
    request,
    schema_id,
):
    form = DocumentSchemaFieldForm()

    return render(
        request,
        "documents/schema/partials/schema_field_form.html",
        {
            "form": form,
            "schema_id": schema_id,
            "is_edit": False,
        },
    )


def schema_field_create(request, schema_id):
    schema = get_object_or_404(DocumentSchema, pk=schema_id)
    version = get_or_create_draft(schema)

    form = DocumentSchemaFieldForm()

    return render(
        request,
        "documents/schema/partials/schema_field_form.html",
        {
            "form": form,
            "schema": schema,
            "fields": version.data.get("fields", []),
        },
    )


def schema_editor(request, schema_id):
    schema = get_object_or_404(DocumentSchema, pk=schema_id)

    draft = schema.draft_version

    form = DocumentSchemaGeneralForm(
        instance=schema,
    )

    return render(
        request,
        "documents/schema/partials/schema_editor_panel.html",
        {
            "schema": schema,
            "form": form,
            "draft": draft,
            "published_versions": schema.published_versions,
            "fields": draft.data.get("fields", []),
            "is_create": False,
        },
    )


def schema_list(request):
    schemas = list_document_schemas()

    return render(
        request,
        "documents/schema/schema_list.html",
        {
            "schemas": schemas,
        },
    )


def schema_publish(
    request,
    schema_id,
):

    schema = get_object_or_404(
        DocumentSchema,
        pk=schema_id,
    )

    result = publish_schema(
        schema=schema,
    )

    if not result["success"]:
        return render(
            request,
            "documents/schema/partials/schema_publish_errors.html",
            {
                "errors": result["errors"],
            },
        )

    return render(
        request,
        "documents/schema/partials/schema_editor_panel.html",
        {
            "schema": schema,
            "version": schema.draft_version,
            "fields": schema.draft_version.data.get("fields", []),
        },
    )


def schema_field_edit(
    request,
    schema_id,
    field_id,
):
    schema = get_object_or_404(
        DocumentSchema,
        pk=schema_id,
    )

    version = schema.draft_version

    field = get_field(
        version,
        field_id,
    )

    if not field:
        raise Http404("Field not found")

    form = DocumentSchemaFieldForm(
        initial={
            "name": field["name"],
            "label": field["label"],
            "field_type": field["type"],
            "required": field["required"],
        }
    )

    return render(
        request,
        "documents/schema/partials/schema_field_form.html",
        {
            "form": form,
            "schema_id": schema.id,  # ty:ignore[unresolved-attribute]
            "field_id": field_id,
            "is_edit": True,
        },
    )


@require_POST  # ty:ignore[invalid-argument-type]
def schema_field_store(request, schema_id):

    schema = get_object_or_404(
        DocumentSchema,
        id=schema_id,
    )

    form = DocumentSchemaFieldForm(request.POST)

    if not form.is_valid():
        return render(
            request,
            "documents/schema/partials/schema_field_form.html",
            {
                "form": form,
            },
        )
    draft = schema.draft_version

    append_field(
        draft,
        name=form.cleaned_data["name"],
        label=form.cleaned_data["label"],
        field_type=form.cleaned_data["field_type"],
        required=form.cleaned_data["required"],
    )

    return render_schema_fields(
        request,
        schema,
    )


@require_POST  # ty:ignore[invalid-argument-type]
def schema_field_update(
    request,
    schema_id,
    field_id,
):

    schema = get_object_or_404(
        DocumentSchema,
        id=schema_id,
    )

    draft = schema.draft_version

    form = DocumentSchemaFieldForm(request.POST)

    if form.is_valid():
        update_field(
            draft,
            field_id=field_id,
            name=form.cleaned_data["name"],
            label=form.cleaned_data["label"],
            type=form.cleaned_data["field_type"],
            required=form.cleaned_data["required"],
        )

    return render_schema_fields(
        request,
        schema,
    )


@require_POST  # ty:ignore[invalid-argument-type]
def schema_field_move(
    request,
    schema_id,
    field_id,
):

    schema = get_object_or_404(
        DocumentSchema,
        id=schema_id,
    )

    draft = schema.draft_version

    new_index = int(request.POST.get("index", 0))

    move_field(
        draft,
        field_id=field_id,
        new_index=new_index,
    )

    return render_schema_fields(
        request,
        schema,
    )


@require_http_methods(["DELETE"])  # ty:ignore[invalid-argument-type]
def schema_field_delete(
    request,
    schema_id,
    field_id,
):

    schema = get_object_or_404(
        DocumentSchema,
        id=schema_id,
    )

    draft = schema.draft_version

    delete_field(
        draft,
        field_id=field_id,
    )

    return render_schema_fields(
        request,
        schema,
    )

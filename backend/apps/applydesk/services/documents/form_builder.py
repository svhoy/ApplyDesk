from django import forms


def build_document_form(schema, initial=None):

    initial = initial or {}

    if hasattr(schema, "schema"):
        schema = schema.schema

    fields = schema.get("fields", [])

    form_fields = {}

    for field in fields:
        name = field.get("name")
        field_type = field.get("type")

        if not name or not field_type:
            continue

        label = field.get("label", name)
        required = field.get("required", False)

        # TEXT
        if field_type == "text":
            form_fields[name] = forms.CharField(
                label=label,
                required=required,
                initial=initial.get(name),
            )

        # TEXTAREA
        elif field_type == "textarea":
            form_fields[name] = forms.CharField(
                label=label,
                required=required,
                widget=forms.Textarea,
                initial=initial.get(name),
            )

        # CHECKBOX
        elif field_type == "checkbox":
            form_fields[name] = forms.BooleanField(
                label=label,
                required=False,
                initial=initial.get(name, False),
            )

        # IGNORE UNKNOWN TYPES
        else:
            continue

    return type(
        "DynamicDocumentForm",
        (forms.Form,),
        form_fields,
    )

import re

from django import forms
from django.core.exceptions import ValidationError

from apps.applydesk.models import DocumentSchema
from apps.applydesk.models.document import DocumentType

FIELD_TYPE_CHOICES = (
    ("text", "Text"),
    ("textarea", "Textarea"),
    ("date", "Date"),
    ("number", "Number"),
    ("email", "Email"),
    ("boolean", "Checkbox"),
)


class DocumentSchemaGeneralForm(forms.ModelForm):
    document_type = forms.ChoiceField(choices=DocumentType.choices)

    class Meta:
        model = DocumentSchema
        fields = ["name", "document_type"]


class DocumentSchemaFieldForm(forms.Form):
    name = forms.CharField(max_length=100)

    label = forms.CharField(max_length=100)

    field_type = forms.ChoiceField(
        choices=FIELD_TYPE_CHOICES,
    )

    required = forms.BooleanField(
        required=False,
    )

    def clean_name(self):

        name = self.cleaned_data["name"]

        if not re.match(
            r"^[a-z][a-z0-9_]*$",
            name,
        ):
            raise ValidationError("Field name must be snake_case.")

        return name

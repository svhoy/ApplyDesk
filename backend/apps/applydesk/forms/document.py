from django import forms

from apps.applydesk.models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document

        fields = [
            "document_type",
            "file",
        ]

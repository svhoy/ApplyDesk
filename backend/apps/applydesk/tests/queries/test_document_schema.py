import pytest

from apps.applydesk.models import (
    DocumentSchema,
)
from apps.applydesk.queries.document_schema import (
    get_document_schema,
    list_document_schemas,
)


@pytest.mark.django_db
def test_get_document_schema():

    schema = DocumentSchema.objects.create(
        name="Test",
        document_type="cover_letter",
        schema={},
    )

    result = get_document_schema(
        schema.pk,
    )

    assert result == schema


@pytest.mark.django_db
def test_list_document_schemas():

    DocumentSchema.objects.create(
        name="A",
        document_type="cover_letter",
        schema={},
    )

    DocumentSchema.objects.create(
        name="B",
        document_type="cv",
        schema={},
    )

    result = list(list_document_schemas())

    assert len(result) == 2

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_missing_documents_show_upload_button(
    client,
    application,
):

    response = client.get(reverse("application_detail", args=[application.id]))

    assert b"Upload" in response.content

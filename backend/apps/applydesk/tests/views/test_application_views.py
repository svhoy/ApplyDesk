import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_application_list_view(client):

    response = client.get(reverse("application_list"))

    assert response.status_code == 200


@pytest.mark.django_db
def test_application_detail_view(client, application):

    response = client.get(reverse("application_detail", args=[application.pk]))

    assert response.status_code == 200
    assert application.position_title in response.content.decode()


@pytest.mark.django_db
def test_application_create_view(client):

    response = client.post(
        reverse("application_create"),
        {
            "company_name": "Google",
            "position_title": "Engineer",
        },
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_application_detail_contains_completeness_card(
    client,
    application,
):

    response = client.get(
        reverse(
            "application_detail",
            args=[application.id],
        )
    )

    assert response.status_code == 200

    assert b"Application Readiness" in response.content

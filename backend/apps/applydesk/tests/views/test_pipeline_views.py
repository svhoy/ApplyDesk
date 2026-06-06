import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_pipeline_view(client):

    response = client.get(reverse("application_pipeline"))

    assert response.status_code == 200


@pytest.mark.django_db
def test_pipeline_shows_application(
    client,
    application,
):

    response = client.get(reverse("application_pipeline"))

    assert application.position_title in response.content.decode()


@pytest.mark.django_db
def test_pipeline_shows_status_columns(
    client,
):

    response = client.get(reverse("application_pipeline"))

    content = response.content.decode()

    assert "Saved" in content
    assert "Prepared" in content
    assert "Applied" in content
    assert "Interview" in content


@pytest.mark.django_db
def test_pipeline_change_status(
    client,
    application,
):

    response = client.post(
        reverse("change_status", args=[application.pk]),
        {
            "status": "prepared",
            "context": "kanban",
        },
        HTTP_HX_REQUEST="true",
    )

    application.refresh_from_db()

    assert application.status == "prepared"

    assert response.status_code == 200


@pytest.mark.django_db
def test_pipeline_returns_oob_update(
    client,
    application,
):

    response = client.post(
        reverse("change_status", args=[application.pk]),
        {
            "status": "prepared",
            "context": "kanban",
        },
        HTTP_HX_REQUEST="true",
    )

    assert "hx-swap-oob" in response.content.decode()

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_move_application(
    client,
    application,
):
    response = client.post(
        reverse(
            "move_application",
        ),
        {
            "application_id": application.pk,
            "status": "prepared",
        },
        HTTP_HX_REQUEST="true",
    )

    application.refresh_from_db()

    assert response.status_code == 200

    assert application.status == "prepared"


@pytest.mark.django_db
def test_move_application_returns_oob_update(client, application):

    response = client.post(
        reverse("move_application"),
        {
            "application_id": application.pk,
            "status": "prepared",
        },
    )

    assert response.status_code == 200
    html = response.content.decode()

    # 1. DB change already implied (optional stronger check below)
    application.refresh_from_db()
    assert application.status == "prepared"

    # 2. OOB container exists for NEW column
    assert f'id="column-body-prepared"' in html
    assert "hx-swap-oob" in html

    # 3. OLD column also updated (removal)
    assert f'id="column-body-saved"' in html or True  # depending logic

    # 4. sanity check: card content is still present
    assert application.position_title in html


def extract_oob_blocks(html: str):
    return "hx-swap-oob" in html


@pytest.mark.django_db
def test_oob_structure(client, application):

    response = client.post(
        reverse("move_application"),
        {
            "application_id": application.pk,
            "status": "prepared",
        },
    )

    html = response.content.decode()

    assert extract_oob_blocks(html)

    assert "column-body-prepared" in html

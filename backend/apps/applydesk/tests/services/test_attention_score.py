from datetime import timedelta

import pytest
from django.utils import timezone

from apps.applydesk.services.attention_score import (
    calculate_attention_score,
)


@pytest.mark.django_db
def test_application_priority_affects_score(
    application_factory,
):

    a = application_factory(
        priority="A",
    )

    b = application_factory(
        priority="B",
    )

    c = application_factory(
        priority="C",
    )

    assert (
        calculate_attention_score(a)
        > calculate_attention_score(b)
        > calculate_attention_score(c)
    )


@pytest.mark.django_db
def test_interview_scores_higher_than_applied(
    application_factory,
):

    applied = application_factory(
        status="applied",
    )

    interview = application_factory(
        status="interview",
    )

    assert calculate_attention_score(interview) > calculate_attention_score(applied)


@pytest.mark.django_db
def test_company_priority_affects_score(
    application_factory,
):

    app_a = application_factory()

    app_a.company.priority = "A"
    app_a.company.save()

    app_c = application_factory()

    app_c.company.priority = "C"
    app_c.company.save()

    app_a.refresh_from_db()
    app_c.refresh_from_db()
    assert app_a.company_id != app_c.company_id
    assert calculate_attention_score(app_a) > calculate_attention_score(app_c)


@pytest.mark.django_db
def test_age_increases_score(
    application_factory,
):

    fresh = application_factory()

    old = application_factory()

    old.status_changed_at = timezone.now() - timedelta(days=10)
    old.save()

    assert calculate_attention_score(old) > calculate_attention_score(fresh)

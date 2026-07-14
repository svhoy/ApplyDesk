from apps.applydesk.services.documents.file_naming import (
    build_document_base_name,
    get_next_versioned_name,
)


def test_build_cv_name():

    result = build_document_base_name(
        document_type="cv",
        company_name="Google",
    )

    assert result == "cv_google"


def test_build_cover_letter_name():

    result = build_document_base_name(
        document_type="cover_letter",
        company_name="Amazon",
    )

    assert result == "cover_letter_amazon"


def test_company_name_is_normalized():

    result = build_document_base_name(
        document_type="cv",
        company_name="  Google Inc. ",
    )

    assert result == "cv_google_inc"


def test_first_version_has_no_suffix(db):

    name = get_next_versioned_name(
        base_name="cv_google",
    )

    assert name == "cv_google"


def test_second_version_gets_v2(
    document_factory,
):

    document_factory(
        title="cv_google",
    )

    name = get_next_versioned_name(
        base_name="cv_google",
    )

    assert name == "cv_google_v2"


def test_third_version_gets_v3(
    document_factory,
):

    document_factory(
        title="cv_google",
    )

    document_factory(
        title="cv_google_v2",
    )

    name = get_next_versioned_name(
        base_name="cv_google",
    )

    assert name == "cv_google_v3"

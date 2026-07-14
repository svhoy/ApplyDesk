from apps.applydesk.models import (
    Application,
    ApplicationRequiredDocument,
)


def update_application(
    application: Application,
    required_documents=None,
    **data,
) -> Application:

    ALLOWED_FIELDS = {
        "position_title",
        "position_description",
        "location",
        "location_type",
        "notes",
        "url",
        "start_date",
        "contact_person",
        "contact_email",
        "contact_phone",
    }

    # ----------------------------
    # update normal fields
    # ----------------------------
    for field, value in data.items():
        if field not in ALLOWED_FIELDS:
            continue

        setattr(application, field, value)

    application.save()

    # ----------------------------
    # sync required documents
    # ----------------------------
    if required_documents is not None:
        ApplicationRequiredDocument.objects.filter(application=application).delete()

        ApplicationRequiredDocument.objects.bulk_create(
            [
                ApplicationRequiredDocument(
                    application=application,
                    document_type=doc,
                )
                for doc in required_documents
            ]
        )

    return application

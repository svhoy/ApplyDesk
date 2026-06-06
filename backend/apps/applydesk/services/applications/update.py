from apps.applydesk.models import (
    Application,
)


def update_application(
    application: Application,
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

    for field, value in data.items():
        if field not in ALLOWED_FIELDS:
            continue

        setattr(
            application,
            field,
            value,
        )

    application.save()

    return application

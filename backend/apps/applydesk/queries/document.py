def get_required_document_types(application):

    return set(
        application.required_documents.values_list(
            "document_type",
            flat=True,
        )
    )


def get_attached_document_types(application):

    return set(
        application.application_documents.values_list(
            "document__document_type",
            flat=True,
        )
    )

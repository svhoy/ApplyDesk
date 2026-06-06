from django.shortcuts import render

from apps.applydesk.queries.pipeline import (
    PIPELINE_STATUSES,
    get_pipeline,
)


def application_pipeline(request):

    return render(
        request,
        "applications/pipeline.html",
        {
            "columns": get_pipeline(),
            "statuses": PIPELINE_STATUSES,
        },
    )

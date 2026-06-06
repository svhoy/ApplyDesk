WORKFLOW_ACTIONS = {
    "saved": [
        {
            "to": "prepared",
            "label": "Mark as Prepared",
            "color": "green",
        }
    ],
    "prepared": [
        {
            "to": "applied",
            "label": "Mark as Applied",
            "color": "green",
        }
    ],
    "applied": [
        {
            "to": "waiting",
            "label": "Move to Waiting",
            "color": "gray",
        },
        {
            "to": "interview",
            "label": "Interview",
            "color": "green",
        },
        {
            "to": "rejected",
            "label": "Reject",
            "color": "red",
        },
    ],
    "waiting": [
        {
            "to": "interview",
            "label": "Interview",
            "color": "green",
        },
        {
            "to": "rejected",
            "label": "Reject",
            "color": "red",
        },
    ],
    "interview": [
        {
            "to": "offer",
            "label": "Offer",
            "color": "green",
        },
        {
            "to": "rejected",
            "label": "Reject",
            "color": "red",
        },
    ],
    "offer": [
        {
            "to": "archived",
            "label": "Archive",
            "color": "gray",
        }
    ],
    "rejected": [
        {
            "to": "archived",
            "label": "Archive",
            "color": "gray",
        }
    ],
}


def get_available_actions(application):
    return WORKFLOW_ACTIONS.get(application.status, [])

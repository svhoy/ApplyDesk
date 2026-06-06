let draggedId = null;
let isUpdating = false;
let draggedStatus = null;

const allowedTransitions = {
    saved: ["prepared"],
    prepared: ["applied"],
    applied: ["waiting", "interview", "rejected"],
    waiting: ["interview", "rejected"],
    interview: ["offer", "rejected"],
    offer: ["archived"],
    rejected: ["archived"]
};

document.addEventListener("dragstart", (e) => {
    const card = e.target.closest(".kanban-card");
    if (!card) return;

    draggedId = card.dataset.id;
    card.classList.add("dragging");
    draggedStatus = card.dataset.status;
});

document.addEventListener("dragend", (e) => {
    const card = e.target.closest(".kanban-card");
    if (!card) return;

    card.classList.remove("dragging");
});

document.addEventListener("dragover", (e) => {
    const zone = e.target.closest(".drop-zone");
    if (!zone) return;

    e.preventDefault();

    const allowed = (
        allowedTransitions[draggedStatus] || []
    ).includes(zone.dataset.status);

    if (allowed) {
        zone.classList.add("drag-over");
    } else {
        zone.classList.add("drag-over-invalid");
    }
});

document.addEventListener("dragleave", (e) => {
    const zone = e.target.closest(".drop-zone");
    if (!zone) return;

    zone.classList.remove("drag-over");
    zone.classList.remove("drag-over-invalid");
});

document.addEventListener("drop", (e) => {
    e.preventDefault();

    const zone = e.target.closest(".drop-zone");
    if (!zone) return;

    const targetStatus = zone.dataset.status;
    console.log({
        draggedStatus,
        targetStatus,
        allowedTransitions: allowedTransitions[draggedStatus],
    });
    const allowed = (
        allowedTransitions[draggedStatus] || []
    ).includes(targetStatus);

    if (!allowed) {
        zone.classList.add("shake");

        setTimeout(() => {
            zone.classList.remove("shake");
            zone.classList.remove("drag-over-invalid");
        }, 300);

        return;
    }

    zone.classList.add("drop-flash");

    setTimeout(() => {
        zone.classList.remove("drop-flash");
    }, 200);

    htmx.ajax(
        "POST",
        "/applications/move/",
        {
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            values: {
                application_id: draggedId,
                status: targetStatus,
                context: "kanban",
            },
            swap: "none",
        }
    );

});


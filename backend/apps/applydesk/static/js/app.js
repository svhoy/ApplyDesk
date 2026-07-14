function openModal() {

    document
        .getElementById("modal-backdrop")
        .classList.add("open");

    document
        .getElementById("modal-container")
        .classList.add("open");
}

function closeModal() {

    document
        .getElementById("modal-backdrop")
        .classList.remove("open");

    document
        .getElementById("modal-container")
        .classList.remove("open");

    setTimeout(() => {
        document
            .getElementById("modal-container")
            .innerHTML = "";
    }, 200);
}


document.addEventListener("DOMContentLoaded", () => {

    const backdrop = document.getElementById(
        "modal-backdrop"
    );

    if (backdrop) {
        backdrop.addEventListener(
            "click",
            closeModal,
        );
    }

});

document.body.addEventListener("htmx:afterSwap", function (evt) {

    if (evt.detail.target.id === "modal-container") {
        openModal();
    }
});
document.addEventListener("htmx:afterSwap", function (evt) {

    const panel = document.getElementById("side-panel");

    if (evt.target.id === "side-panel") {
        panel.classList.add("open");
    }
});

function openSidePanel() {

    document
        .getElementById("side-panel")
        .classList.add("open");

    document
        .getElementById("side-panel-backdrop")
        .classList.add("open");
}

function closeSidePanel() {

    document
        .getElementById("side-panel")
        .classList.remove("open");

    document
        .getElementById("side-panel-backdrop")
        .classList.remove("open");

    setTimeout(() => {
        document.getElementById("side-panel").innerHTML = "";
    }, 200);
}

document.addEventListener("click", (event) => {

    const link = event.target.closest("a");

    if (!link) {
        return;
    }

    if (link.target === "_blank") {
        return;
    }

    closeSidePanel();
});

document.addEventListener("keydown", (event) => {

    if (event.key !== "Escape") {
        return;
    }

    closeSidePanel();
});

document.addEventListener("DOMContentLoaded", () => {

    const backdrop = document.getElementById(
        "side-panel-backdrop"
    );

    if (backdrop) {
        backdrop.addEventListener(
            "click",
            closeSidePanel,
        );
    }
});
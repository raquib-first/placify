document.addEventListener("DOMContentLoaded", () => {
    const bell = document.getElementById("notificationBell");
    const dropdown = document.getElementById("notificationDropdown");

    bell?.addEventListener("click", () => {
        dropdown.classList.toggle("hidden");
    });

    document.querySelectorAll(".notification-item").forEach(item => {
        item.addEventListener("click", () => {
            const id = item.dataset.id;

            fetch(`/notifications/read/${id}/`)
                .then(() => {
                    item.classList.remove("unread");
                });

            alert(item.querySelector("strong").innerText + "\n\n" +
                  item.querySelector(".preview").innerText);
        });
    });

    document.addEventListener("click", (e) => {
        if (!bell.contains(e.target) && !dropdown.contains(e.target)) {
            dropdown.classList.add("hidden");
        }
    });
});

document.addEventListener("DOMContentLoaded", function () {

    const notifBtn = document.getElementById("notificationBell");
    const dropdown = document.getElementById("notificationDropdown");
    const count = document.getElementById("notificationCount");
    const list = document.getElementById("notificationList");

    let lastUnreadCount = 0;

    // Toggle dropdown
    notifBtn?.addEventListener("click", () => {
        dropdown.classList.toggle("hidden");
    });

    // Render notifications
    function renderNotifications(notifications) {
        list.innerHTML = "";

        if (notifications.length === 0) {
            list.innerHTML = `<p class="empty-state">All caught up!</p>`;
            return;
        }

        notifications.forEach(n => {
            const div = document.createElement("div");
            div.className = `notification-item ${n.is_read ? "" : "unread"}`;
            div.dataset.id = n.id;

            div.innerHTML = `
                <strong>${n.title}</strong>
                <p>${n.message}</p>
                <small>${n.created_at}</small>
            `;

            // Mark as read on click
            div.addEventListener("click", () => {
                markAsRead(n.id, div);
            });

            list.appendChild(div);
        });
    }

    // Fetch notifications
    function fetchNotifications() {
        fetch("/notifications/fetch/")
            .then(res => res.json())
            .then(data => {

                // Update badge
                if (count) {
                    count.innerText = data.unread_count;
                }

                // Update dropdown UI
                renderNotifications(data.notifications);

                lastUnreadCount = data.unread_count;
            })
            .catch(err => console.error("ERROR:", err));
    }

    // Mark as read
    function markAsRead(id, element) {
        fetch(`/notifications/read/${id}/`)
            .then(() => {
                element.classList.remove("unread");

                // decrease count
                if (count && parseInt(count.innerText) > 0) {
                    count.innerText = parseInt(count.innerText) - 1;
                }
            });
    }

    // Run every 5 sec
    fetchNotifications();
    setInterval(fetchNotifications, 5000);

});
const bell = document.getElementById("notificationBell");
const dropdown = document.getElementById("notificationDropdown");

if (bell) {
    bell.onclick = () => {
        dropdown.classList.toggle("hidden");
    };
}

const settingsBtn = document.getElementById("settingsBtn");
const settingsDropdown = document.getElementById("settingsDropdown");

if (settingsBtn) {
    settingsBtn.onclick = () => {
        settingsDropdown.classList.toggle("hidden");
    };
}
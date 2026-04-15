document.addEventListener("DOMContentLoaded", function () {

    const settingsBtn = document.getElementById("settingsBtn");
    const settingsDropdown = document.getElementById("settingsDropdown");

    if (!settingsBtn || !settingsDropdown) return;

    // Toggle dropdown
    settingsBtn.addEventListener("click", function (e) {
        e.stopPropagation(); // prevent instant closing
        settingsDropdown.classList.toggle("hidden");
    });

    // Close when clicking outside
    document.addEventListener("click", function (e) {
        if (!settingsBtn.contains(e.target) && !settingsDropdown.contains(e.target)) {
            settingsDropdown.classList.add("hidden");
        }
    });

});
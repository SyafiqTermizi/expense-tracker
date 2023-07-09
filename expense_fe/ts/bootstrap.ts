const profileButton = document.getElementById("profile-button");
const profileDropdown = document.getElementById("profile-dropdown");

profileButton.addEventListener("click", () => {
    if (profileButton.classList.contains("show")) {
        profileButton.classList.remove("show");
        profileDropdown.classList.remove("show");
    } else {
        profileButton.classList.add("show");
        profileDropdown.classList.add("show");
    }
});


const navbarToggleButton = document.getElementById("navbar-toggle-button");
const navbarMobileMenu = document.getElementById("navbar-mobile-menu");

navbarToggleButton.classList.add("collapsed");
navbarToggleButton.addEventListener("click", () => {
    if (navbarToggleButton.classList.contains("collapsed")) {
        navbarToggleButton.classList.remove("collapsed");
        navbarMobileMenu.classList.add("show");
    } else {
        navbarToggleButton.classList.add("collapsed");
        navbarMobileMenu.classList.remove("show");
    }
});

import { Modal } from "bootstrap"

export { };

(() => {
    console.log("JAVASCRIPT.JS ЗАПУЩЕН");
    document.addEventListener("DOMContentLoaded", () => {

        // ВЫПАДАЮЩЕЕ МЕНЮ

        const menuToggle = document.querySelector("#menu-toggle");
        const siteMenu = document.querySelector("#site-menu");

        if (menuToggle && siteMenu) {
            menuToggle.addEventListener("click", () => {
                const isOpen = !siteMenu.hidden;

                siteMenu.hidden = isOpen;
                menuToggle.classList.toggle("active", !isOpen);
                menuToggle.setAttribute("aria-expanded", String(!isOpen));
            });

            document.addEventListener("click", (event) => {
                if (
                    !siteMenu.hidden &&
                    !siteMenu.contains(event.target) &&
                    !menuToggle.contains(event.target)
                ) {
                    siteMenu.hidden = true;
                    menuToggle.classList.remove("active");
                    menuToggle.setAttribute("aria-expanded", "false");
                }
            });

            document.addEventListener("keydown", (event) => {
                if (event.key === "Escape") {
                    siteMenu.hidden = true;
                    menuToggle.classList.remove("active");
                    menuToggle.setAttribute("aria-expanded", "false");
                }
            });
        }

        // СЛАЙДЕР

        const slides = document.querySelectorAll(".slide");
        const prevButton = document.querySelector(".prev");
        const nextButton = document.querySelector(".next");

        if (slides.length > 0 && prevButton && nextButton) {
            let currentSlide = 0;

            function showSlide(index) {
                slides[currentSlide].classList.remove("active");

                currentSlide = (index + slides.length) % slides.length;

                slides[currentSlide].classList.add("active");
            }

            prevButton.addEventListener("click", () => {
                showSlide(currentSlide - 1);
            });

            nextButton.addEventListener("click", () => {
                showSlide(currentSlide + 1);
            });
        }

    });
})();

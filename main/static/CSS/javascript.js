
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


document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.querySelector("#user-search-input");
    const resultsContainer = document.querySelector("#search-results");
    const spinner = document.querySelector("#search-spinner");

    if (!searchInput || !resultsContainer) {
        return;
    }

    let searchTimeout = null;
    let requestController = null;

    function closeResults() {
        resultsContainer.hidden = true;
        resultsContainer.innerHTML = "";
        searchInput.setAttribute("aria-expanded", "false");
    }

    function showMessage(message) {
        resultsContainer.innerHTML = "";

        const messageElement = document.createElement("div");
        messageElement.className = "search-message";
        messageElement.textContent = message;

        resultsContainer.appendChild(messageElement);
        resultsContainer.hidden = false;
        searchInput.setAttribute("aria-expanded", "true");
    }

    function showUsers(users) {
        resultsContainer.innerHTML = "";

        if (users.length === 0) {
            showMessage("Пользователи не найдены");
            return;
        }

        users.forEach(user => {
            const link = document.createElement("a");

            link.className = "search-result";
            link.href = `/profile/${encodeURIComponent(user.username)}/`;
            link.setAttribute("role", "option");

            const avatar = document.createElement("span");
            avatar.className = "search-result-avatar";
            avatar.textContent = user.username.charAt(0).toUpperCase();

            const name = document.createElement("span");
            name.className = "search-result-name";
            name.textContent = user.username;

            link.appendChild(avatar);
            link.appendChild(name);

            resultsContainer.appendChild(link);
        });

        resultsContainer.hidden = false;
        searchInput.setAttribute("aria-expanded", "true");
    }

    async function searchUsers(query) {
        if (requestController) {
            requestController.abort();
        }

        requestController = new AbortController();

        spinner.hidden = false;

        try {
            const response = await fetch(
                `/search-users/?q=${encodeURIComponent(query)}`,
                {
                    method: "GET",
                    headers: {
                        "X-Requested-With": "XMLHttpRequest"
                    },
                    signal: requestController.signal
                }
            );

            if (!response.ok) {
                throw new Error("Ошибка поиска");
            }

            const data = await response.json();
            showUsers(data.users);

        } catch (error) {
            if (error.name !== "AbortError") {
                showMessage("Не удалось выполнить поиск");
                console.error(error);
            }
        } finally {
            if (!requestController.signal.aborted) {
                spinner.hidden = true;
            }
        }
    }

    searchInput.addEventListener("input", () => {
        const query = searchInput.value.trim();

        clearTimeout(searchTimeout);

        if (requestController) {
            requestController.abort();
            requestController = null;
        }

        spinner.hidden = true;

        if (query.length < 2) {
            closeResults();
            return;
        }

        searchTimeout = setTimeout(() => {
            searchUsers(query);
        }, 300);
    });

    document.addEventListener("click", event => {
        if (
            !resultsContainer.contains(event.target) &&
            !searchInput.contains(event.target)
        ) {
            closeResults();
        }
    });

    searchInput.addEventListener("keydown", event => {
        if (event.key === "Escape") {
            closeResults();
            searchInput.blur();
        }
    });
});

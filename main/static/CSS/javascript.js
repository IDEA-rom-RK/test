
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

        document.addEventListener("click", event => {
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

        document.addEventListener("keydown", event => {
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


    // ПОИСК ПОЛЬЗОВАТЕЛЕЙ

    
    // ПОИСК ПОЛЬЗОВАТЕЛЕЙ

    const searchInput = document.querySelector("#user-search-input");
    const resultsContainer = document.querySelector("#search-results");
    const spinner = document.querySelector("#search-spinner");
    const emptyHint = document.querySelector("#search-empty-hint");
    const clearFiltersButton = document.querySelector("#clear-search-filters");

    if (searchInput && resultsContainer) {

        let searchTimeout = null;
        let requestController = null;

        function getSelectedInterests() {
            return Array.from(
                document.querySelectorAll(
                    'input[name="interests"]:checked'
                )
            ).map(input => input.value);
        }

        function closeResults() {
            resultsContainer.hidden = true;
            resultsContainer.innerHTML = "";

            if (emptyHint) {
                emptyHint.hidden = false;
            }

            searchInput.setAttribute("aria-expanded", "false");
        }

        function showMessage(message) {
            resultsContainer.innerHTML = "";

            const messageElement = document.createElement("div");
            messageElement.className = "search-message";
            messageElement.textContent = message;

            resultsContainer.appendChild(messageElement);
            resultsContainer.hidden = false;

            if (emptyHint) {
                emptyHint.hidden = true;
            }

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
                link.href = `/userprofile/${encodeURIComponent(user.username)}/`;
                link.setAttribute("role", "option");

                const avatar = document.createElement("span");
                avatar.className = "search-result-avatar";
                avatar.textContent = user.username.charAt(0).toUpperCase();

                const info = document.createElement("span");
                info.className = "search-result-info";

                const name = document.createElement("span");
                name.className = "search-result-name";
                name.textContent = user.username;

                info.appendChild(name);

                if (user.common_interests_count > 0) {
                    const common = document.createElement("span");
                    common.className = "search-result-common";
                    common.textContent =
                        `Общих интересов: ${user.common_interests_count}`;

                    info.appendChild(common);
                }

                link.appendChild(avatar);
                link.appendChild(info);

                resultsContainer.appendChild(link);
            });

            resultsContainer.hidden = false;

            if (emptyHint) {
                emptyHint.hidden = true;
            }

            searchInput.setAttribute("aria-expanded", "true");
        }

        async function searchUsers() {
            const query = searchInput.value.trim();
            const interests = getSelectedInterests();

            if (!query && interests.length === 0) {
                closeResults();
                return;
            }

            if (requestController) {
                requestController.abort();
            }

            const controller = new AbortController();
            requestController = controller;

            const params = new URLSearchParams();

            if (query) {
                params.set("q", query);
            }

            interests.forEach(interest => {
                params.append("interests", interest);
            });

            if (spinner) {
                spinner.hidden = false;
            }

            try {
                console.log("URL поиска:", `/search-users/?${params.toString()}`);
                const response = await fetch(
                    `/search-users/?${params.toString()}`,
                    {
                        method: "GET",
                        headers: {
                            "X-Requested-With": "XMLHttpRequest"
                        },
                        signal: controller.signal
                    }
                );

                if (!response.ok) {
                    const errorText = await response.text();

                    console.error("Статус ответа:", response.status);
                    console.error("Ответ сервера:", errorText);

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
                if (requestController === controller) {
                    requestController = null;

                    if (spinner) {
                        spinner.hidden = true;
                    }
                }
            }
        }

        function scheduleSearch() {
            clearTimeout(searchTimeout);

            if (requestController) {
                requestController.abort();
                requestController = null;
            }

            if (spinner) {
                spinner.hidden = true;
            }

            searchTimeout = setTimeout(searchUsers, 300);
        }

        // Поиск при вводе никнейма
        searchInput.addEventListener("input", scheduleSearch);

        // Поиск при выборе интересов
        document.querySelectorAll(
            'input[name="interests"]'
        ).forEach(checkbox => {
            checkbox.addEventListener("change", scheduleSearch);
        });

        // Сброс выбранных интересов
        if (clearFiltersButton) {
            clearFiltersButton.addEventListener("click", () => {
                document.querySelectorAll(
                    'input[name="interests"]'
                ).forEach(checkbox => {
                    checkbox.checked = false;
                });

                scheduleSearch();
            });
        }

        // Закрытие результатов при клике вне поиска
        document.addEventListener("click", event => {
            const filters = document.querySelector(".search-filters");

            if (
                !resultsContainer.contains(event.target) &&
                !searchInput.contains(event.target) &&
                (!filters || !filters.contains(event.target))
            ) {
                closeResults();
            }
        });

        // Закрытие результатов по Escape
        searchInput.addEventListener("keydown", event => {
            if (event.key === "Escape") {
                closeResults();
                searchInput.blur();
            }
        });
    }


    searchInput.addEventListener("keydown", event => {
        if (event.key === "Escape") {
            closeResults();
            searchInput.blur();
        }
    });

});

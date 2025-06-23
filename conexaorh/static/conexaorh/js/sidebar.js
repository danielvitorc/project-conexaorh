document.addEventListener("DOMContentLoaded", () => {
    // --- LÓGICA DO TEMA (A LÓGICA DA SIDEBAR FOI REMOVIDA) ---
    const themeToggleButton = document.getElementById('themeToggleButton');
    const themeIcon = document.getElementById("themeIcon");

    // Função para aplicar o tema
    function applyTheme(theme) {
        document.documentElement.setAttribute("data-theme", theme);
        if (theme === "dark") {
            if (themeIcon) {
                themeIcon.classList.remove("fa-moon");
                themeIcon.classList.add("fa-sun");
            }
        } else {
            if (themeIcon) {
                themeIcon.classList.remove("fa-sun");
                themeIcon.classList.add("fa-moon");
            }
        }
    }
    
    // Função global para alternar o tema, chamada pelo botão no HTML
    window.toggleTheme = function() {
        const currentTheme = document.documentElement.getAttribute("data-theme");
        const newTheme = currentTheme === "dark" ? "light" : "dark";
        applyTheme(newTheme);
        localStorage.setItem("theme", newTheme);
    };

    // Carregar tema salvo ao carregar a página
    const savedTheme = localStorage.getItem("theme") || "light";
    applyTheme(savedTheme);

    // Adiciona o listener de clique apenas ao botão de tema
    if (themeToggleButton) {
        themeToggleButton.addEventListener('click', toggleTheme);
    }
});
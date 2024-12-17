document.addEventListener("DOMContentLoaded", () => {
  const themeToggleButton = document.getElementById("theme-toggle");

  if (!themeToggleButton) return;

  const currentTheme =
    document.documentElement.getAttribute("data-theme") || "light";
  updateButtonText(currentTheme);

  themeToggleButton.addEventListener("click", () => {
    const newTheme =
      document.documentElement.getAttribute("data-theme") === "light"
        ? "dark"
        : "light";

    // Actualiza localStorage
    localStorage.setItem("theme", newTheme);

    // Recarga la página para aplicar el nuevo tema
    location.reload();
  });

  function updateButtonText(theme) {
    themeToggleButton.textContent =
      theme === "dark" ? "Light Mode" : "Dark Mode";
  }
});

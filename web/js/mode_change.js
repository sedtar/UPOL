const modeButton = document.querySelector('.mode_button');
modeButton.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');

    // Uloží volbu do localStorage (aby se po reloadu zachovala)
    if (document.body.classList.contains('dark-mode')) {
        localStorage.setItem('theme', 'dark');
        modeButton.textContent = 'Light Mode';
    } else {
        localStorage.setItem('theme', 'light');
        modeButton.textContent = 'Dark Mode';
    }
});

// Při načtení stránky zkontroluj, jestli uživatel měl zapnutý dark mode
window.addEventListener('load', () => {
    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.add('dark-mode');
        modeButton.textContent = 'Light Mode';
    }
});
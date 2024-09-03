document.addEventListener('DOMContentLoaded', function() {
    const recipeCategorySelect = document.getElementById("recipe-category-select");
    const recipeCategory = recipeCategorySelect.textContent.trim();
    const recipeNavLinks = document.querySelectorAll(".recipe-nav a");

    recipeNavLinks.forEach(link => {
        const category = link.href.split('=')[1];
        if (category === recipeCategory) {
            link.classList.add('category-select');
        } else {
            link.classList.remove('category-select');
        }
    });
});

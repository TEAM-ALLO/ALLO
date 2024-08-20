document.addEventListener('DOMContentLoaded', function() {
    const interiorCategorySelect = document.getElementById("interior-detail-category");
    const interiorCategory = interiorCategorySelect.textContent.trim();
    const interiorNavLinks = document.querySelectorAll(".interior-nav a");

    interiorNavLinks.forEach(link => {
        const category = link.textContent.trim();
        console.log(`category: ${category}, interiorCategory: ${interiorCategory}`);
        if (category === interiorCategory) {
            link.classList.add('category-select');
        } else {
            link.classList.remove('category-select');
        }
    });
});

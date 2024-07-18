function showSubCategory(type) {
    document.querySelectorAll('.sub-categories > div').forEach(function(section) {
        section.classList.add('hidden');
    });
    document.getElementById(type).classList.remove('hidden');
}

function showContent(type, category) {
    document.querySelectorAll('.content-section').forEach(function(section) {
        section.classList.add('hidden');
    });
    document.getElementById(`${type}-${category}`).classList.remove('hidden');
}
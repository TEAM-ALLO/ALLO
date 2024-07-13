const hamburgerBtn = document.getElementById('hamburger-btn');
const sidebar = document.getElementById('sidebar');
document.addEventListener('DOMContentLoaded', function() {
    hamburgerBtn.addEventListener('click', function() {
        if (sidebar.classList.contains('hidden')) {
            sidebar.classList.remove('hidden');
            sidebar.style.display = 'inline-flex';
        } else {
            sidebar.classList.add('hidden');
            sidebar.style.display = 'none';
        }
    });
})
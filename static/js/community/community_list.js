document.addEventListener('DOMContentLoaded', function() {
    let postBoxes = document.querySelectorAll('.community-post-box');
    postBoxes.forEach(box => {
        box.addEventListener('click', function() {
            let url = box.getAttribute('data-url');
            if (url) {
                window.location.href = url;
            }
        });
    });
});
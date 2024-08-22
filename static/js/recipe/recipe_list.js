document.addEventListener('DOMContentLoaded', function() {
    let likeButtons = document.querySelectorAll('.recommend-like');
    let hateButtons = document.querySelectorAll('.recommend-hate');

    likeButtons.forEach(function(likeButton, index) {
        let hateButton = hateButtons[index];
        let recipeId = likeButton.closest('form').getAttribute('data-recipe-id');

        let likeStatus = localStorage.getItem('like_' + recipeId);
        let hateStatus = localStorage.getItem('hate_' + recipeId);

        if (likeStatus === 'liked') {
            likeButton.style.color = 'red';
            hateButton.disabled = true;
        }

        if (hateStatus === 'hated') {
            hateButton.style.color = 'red';
            likeButton.disabled = true;
        }

        likeButton.addEventListener('click', function(event) {
            event.preventDefault();
            
            if (likeButton.style.color === 'red') {
                likeButton.style.color = 'black';
                hateButton.disabled = false;
                localStorage.removeItem('like_' + recipeId);
            } else {
                likeButton.style.color = 'red';
                hateButton.disabled = true;
                localStorage.setItem('like_' + recipeId, 'liked');
                localStorage.removeItem('hate_' + recipeId);
            }

            let form = likeButton.closest('form');
            let formData = new FormData(form);

            fetch(form.action, {
                method: form.method,
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });

    hateButtons.forEach(function(hateButton, index) {
        let likeButton = likeButtons[index];
        let recipeId = hateButton.closest('form').getAttribute('data-recipe-id');

        let likeStatus = localStorage.getItem('like_' + recipeId);
        let hateStatus = localStorage.getItem('hate_' + recipeId);

        if (likeStatus === 'liked') {
            likeButton.style.color = 'red';
            hateButton.disabled = true;
        }

        if (hateStatus === 'hated') {
            hateButton.style.color = 'red';
            likeButton.disabled = true;
        }

        hateButton.addEventListener('click', function(event) {
            event.preventDefault();

            if (hateButton.style.color === 'red') {
                hateButton.style.color = 'black';
                likeButton.disabled = false;
                localStorage.removeItem('hate_' + recipeId);
            } else {
                hateButton.style.color = 'red';
                likeButton.disabled = true;
                localStorage.setItem('hate_' + recipeId, 'hated');
                localStorage.removeItem('like_' + recipeId);
            }
            let form = hateButton.closest('form');
            let formData = new FormData(form);

            fetch(form.action, {
                method: form.method,
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
});

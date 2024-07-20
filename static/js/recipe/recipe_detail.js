document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('like-button').addEventListener('click', function() {
        const recipeId = this.dataset.recipeId;
        const url = `/recipe/${recipeId}/like/`;

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCsrfToken(),
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.liked) {
                this.querySelector('img').src = '/static/img/full-heart.svg';
            } else {
                this.querySelector('img').src = '/static/img/heart.svg';
            }
            document.getElementById('likes-count').textContent = data.likes_count;
        })
        .catch(error => console.error('Error:', error));
    });

    document.getElementById('bookmark-button').addEventListener('click', function() {
        const recipeId = this.dataset.recipeId;
        const url = `/recipe/${recipeId}/bookmark/`;

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCsrfToken(),
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.bookmarked) {
                this.querySelector('img').src = '/static/img/full-bookmark.svg';
            } else {
                this.querySelector('img').src = '/static/img/bookmark.svg';
            }
            document.getElementById('bookmarks-count').textContent = data.bookmarks_count;
        })
        .catch(error => console.error('Error:', error));
    });

    document.getElementById('friend-request-button').addEventListener('click', function() {
        const username = this.dataset.username;
        const url = `/recipe/send_friend_request/${username}/`;

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCsrfToken(),
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                this.textContent = '신청함';
                this.disabled = true;
            } else {
                alert(data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    });
});

function getCsrfToken() {
    const cookieValue = document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken='))
        .split('=')[1];
    return cookieValue;
}

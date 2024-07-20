document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('like-button').addEventListener('click', function() {
        const postId = this.dataset.postId;
        const url = `/interior/${postId}/like/`;

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
        const postId = this.dataset.postId;
        const url = `/interior/${postId}/bookmark/`;

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
        })
        .catch(error => console.error('Error:', error));
    });

    document.getElementById('friend-request-button').addEventListener('click', function() {
        const username = this.dataset.username;
        const url = `/interior/send_friend_request/${username}/`;

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

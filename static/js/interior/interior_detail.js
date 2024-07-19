function getCsrfToken() {
    const cookieValue = document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken='))
        .split('=')[1];
    return cookieValue;
}

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
                this.textContent = '좋아요 취소';
            } else {
                this.textContent = '좋아요';
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
                this.textContent = '북마크 취소';
            } else {
                this.textContent = '북마크';
            }
        })
        .catch(error => console.error('Error:', error));
    });
});

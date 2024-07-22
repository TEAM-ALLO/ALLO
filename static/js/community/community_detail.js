document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('like-button').addEventListener('click', function() {
        const postId = this.dataset.postId;
        const url = `/community/post/${postId}/like/`;

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
        const url = `/community/post/${postId}/bookmark/`;

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
        const url = `/community/send_friend_request/${username}/`;

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

    const commentForm = document.getElementById('comment-form');

    commentForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(commentForm);

        fetch(commentForm.action, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('comment-section').innerHTML = data.html;
                commentForm.reset();
            } else {
                alert('댓글 작성에 실패했습니다.');
            }
        });
    });

    document.getElementById('comment-section').addEventListener('submit', function(event) {
        event.preventDefault();

        const form = event.target;
        if (form.classList.contains('comment-delete-form')) {
            fetch(form.action, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: new FormData(form)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById('comment-section').innerHTML = data.html;
                } else {
                    alert('댓글 삭제에 실패했습니다.');
                }
            });
        }
    });
    
});

function getCsrfToken() {
    const cookieValue = document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken='))
        .split('=')[1];
    return cookieValue;
}

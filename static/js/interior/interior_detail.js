document.addEventListener('DOMContentLoaded', function() {
    const postId = document.getElementById('post-id').value;

    function getCsrfToken() {
        const cookieValue = document.cookie.split('; ')
            .find(row => row.startsWith('csrftoken='))
            .split('=')[1];
        return cookieValue;
    }

    function setupLikeButton() {
        const likeButton = document.getElementById('like-button');
        if (likeButton) {
            likeButton.addEventListener('click', function() {
                const url = `/interior/${postId}/like/`;

                fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCsrfToken(),
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
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
        }
    }

    function setupBookmarkButton() {
        const bookmarkButton = document.getElementById('bookmark-button');
        if (bookmarkButton) {
            bookmarkButton.addEventListener('click', function() {
                const url = `/interior/${postId}/bookmark/`;

                fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCsrfToken(),
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
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
        }
    }

    function setupFriendRequestButton() {
        const friendRequestButton = document.getElementById('friend-request-button');
        if (friendRequestButton) {
            friendRequestButton.addEventListener('click', function() {
                const username = this.dataset.username;
                const url = `/interior/send_friend_request/${username}/`;

                fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCsrfToken(),
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
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
        }
    }

    function setupCommentForm() {
        const commentForm = document.getElementById('comment-form');
        if (commentForm) {
            commentForm.addEventListener('submit', function(e) {
                e.preventDefault();
                const url = commentForm.action;
                const formData = new FormData(commentForm);

                fetch(url, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': getCsrfToken(),
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        updateCommentList(data.comments, data.total_comments);
                        commentForm.reset();
                    } else {
                        console.error('Failed to submit comment:', data.errors);
                    }
                })
                .catch(error => console.error('Error:', error));
            });
        }
    }

    function setupCommentDeleteEventListeners() {
        const deleteForms = document.querySelectorAll('.comment-delete-form');
        deleteForms.forEach(form => {
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                const commentId = form.getAttribute('data-comment-id');
                const url = form.action;

                fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCsrfToken(),
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        updateCommentList(data.comments, data.total_comments);
                    } else {
                        console.error('Failed to delete comment:', data.errors);
                    }
                })
                .catch(error => console.error('Error:', error));
            });
        });
    }

    function updateCommentList(comments, totalComments) {
        const commentList = document.getElementById('comment-list');
        const commentCount = document.querySelector('.interior-detail-comment-title');

        commentList.innerHTML = '';
        comments.forEach(comment => {
            const commentItem = document.createElement('li');
            commentItem.className = 'interior-detail-comment-container';
            commentItem.innerHTML = `
                <div class="interior-detail-comment-user">
                    ${comment.user__username}
                    ${comment.user__username === '{{ request.user.username }}' ? `
                        <form class="comment-delete-form" data-comment-id="${comment.id}" action="/interior/detail/${postId}/comments/delete/${comment.id}/" method="POST" class="d-inline">
                            <input type="hidden" name="csrfmiddlewaretoken" value="${getCsrfToken()}">
                            <input type="submit" value="삭제" class="interior-detail-comment-delete">
                        </form>
                    ` : ''}
                </div>
                <div>${comment.content}</div>
            `;
            commentList.appendChild(commentItem);
        });

        commentCount.textContent = `${totalComments}개의 댓글이 있습니다.`;
        setupCommentDeleteEventListeners(); // 이벤트 리스너 재설정
    }

    setupLikeButton();
    setupBookmarkButton();
    setupFriendRequestButton();
    setupCommentForm();
    setupCommentDeleteEventListeners(); // 초기 이벤트 리스너 설정
});

document.addEventListener('DOMContentLoaded', function() {
    const postIdElement = document.getElementById('post-id');
    const currentUsernameElement = document.getElementById('current-username');

    if (!postIdElement || !currentUsernameElement) {
        console.error('post-id or current-username element is missing.');
        return;
    }

    const postId = postIdElement.value;
    const currentUsername = currentUsernameElement.value;

    console.log('postId:', postId);
    console.log('currentUsername:', currentUsername);

    function getCsrfToken() {
        const cookieValue = document.cookie.split('; ')
            .find(row => row.startsWith('csrftoken='))
            .split('=')[1];
        return cookieValue;
    }

    function createCommentList() {
        const commentListContainer = document.createElement('ul');
        commentListContainer.id = 'comment-list';
        commentListContainer.className = 'post-detail-comment-container';
        return commentListContainer;
    }

    function updateCommentList(comments, totalComments) {
        let commentList = document.getElementById('comment-list');
        const commentCount = document.querySelector('.post-detail-comment-title');

        if (!commentList) {
            commentList = createCommentList();
            document.querySelector('.post-detail-big-container').appendChild(commentList);
        }

        commentList.innerHTML = '';
        comments.forEach(comment => {
            const commentItem = document.createElement('li');
            commentItem.className = 'post-detail-comment-container';
            commentItem.innerHTML = `
                <div class="post-detail-comment-user">
                    ${comment.user__username}
                    ${comment.user__username === currentUsername ? `
                        <button class="comment-delete-button" data-comment-id="${comment.id}">삭제</button>
                    ` : ''}
                </div>
                <div>${comment.content}</div>
            `;
            commentList.appendChild(commentItem);
        });

        commentCount.textContent = `${totalComments}개의 댓글이 있습니다.`;
        setupCommentDeleteEventListeners(); // 이벤트 리스너 재설정
    }

    function setupCommentForm() {
        const commentForm = document.getElementById('comment-form');
        if (commentForm) {
            commentForm.addEventListener('submit', function(e) {
                e.preventDefault(); // 폼 제출 기본 동작 막기
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
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
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
        const deleteButtons = document.querySelectorAll('.comment-delete-button');
        deleteButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault(); // 버튼 클릭 기본 동작 막기
                const commentId = button.getAttribute('data-comment-id');
                const url = `/community/post/${postId}/comments/${commentId}/delete/`;

                fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCsrfToken(),
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        updateCommentList(data.comments, data.total_comments);
                    } else {
                        console.error('Failed to delete comment:', data.message);
                    }
                })
                .catch(error => console.error('Error:', error));
            });
        });
    }

    function setupLikeButton() {
        const likeButton = document.getElementById('like-button');
        if (likeButton) {
            likeButton.addEventListener('click', function() {
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
        }
    }

    function setupBookmarkButton() {
        const bookmarkButton = document.getElementById('bookmark-button');
        if (bookmarkButton) {
            bookmarkButton.addEventListener('click', function() {
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
                    document.getElementById('bookmarks-count').textContent = data.bookmarks_count;
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
        }
    }

    setupCommentForm();
    setupCommentDeleteEventListeners(); // 초기 이벤트 리스너 설정
    setupLikeButton(); // 좋아요 버튼 설정
    setupBookmarkButton(); // 북마크 버튼 설정
    setupFriendRequestButton(); // 친구 추가 버튼 설정
});

// document.addEventListener('DOMContentLoaded', function() {
//     document.getElementById('like-button').addEventListener('click', function() {
//         const recipeId = this.dataset.recipeId;
//         const url = `/recipe/${recipeId}/like/`;

//         fetch(url, {
//             method: 'POST',
//             headers: {
//                 'X-CSRFToken': getCsrfToken(),
//                 'Content-Type': 'application/json'
//             }
//         })
//         .then(response => response.json())
//         .then(data => {
//             if (data.liked) {
//                 this.querySelector('img').src = '/static/img/full-heart.svg';
//             } else {
//                 this.querySelector('img').src = '/static/img/heart.svg';
//             }
//             document.getElementById('likes-count').textContent = data.likes_count;
//         })
//         .catch(error => console.error('Error:', error));
//     });

//     document.getElementById('bookmark-button').addEventListener('click', function() {
//         const recipeId = this.dataset.recipeId;
//         const url = `/recipe/${recipeId}/bookmark/`;

//         fetch(url, {
//             method: 'POST',
//             headers: {
//                 'X-CSRFToken': getCsrfToken(),
//                 'Content-Type': 'application/json'
//             }
//         })
//         .then(response => response.json())
//         .then(data => {
//             if (data.bookmarked) {
//                 this.querySelector('img').src = '/static/img/full-bookmark.svg';
//             } else {
//                 this.querySelector('img').src = '/static/img/bookmark.svg';
//             }
//             document.getElementById('bookmarks-count').textContent = data.bookmarks_count;
//         })
//         .catch(error => console.error('Error:', error));
//     });

//     document.getElementById('friend-request-button').addEventListener('click', function() {
//         const username = this.dataset.username;
//         const url = `/recipe/send_friend_request/${username}/`;

//         fetch(url, {
//             method: 'POST',
//             headers: {
//                 'X-CSRFToken': getCsrfToken(),
//                 'Content-Type': 'application/json'
//             }
//         })
//         .then(response => response.json())
//         .then(data => {
//             if (data.status === 'success') {
//                 this.textContent = '신청함';
//                 this.disabled = true;
//             } else {
//                 alert(data.message);
//             }
//         })
//         .catch(error => console.error('Error:', error));
//     });
// });

// function getCsrfToken() {
//     const cookieValue = document.cookie.split('; ')
//         .find(row => row.startsWith('csrftoken='))
//         .split('=')[1];
//     return cookieValue;
// }

document.addEventListener('DOMContentLoaded', function() {
    const recipeIdElement = document.getElementById('recipe-id');
    const currentUsernameElement = document.getElementById('current-username');

    if (!recipeIdElement || !currentUsernameElement) {
        console.error('recipe-id or current-username element is missing.');
        return;
    }

    const recipeId = recipeIdElement.value;
    const currentUsername = currentUsernameElement.value;

    console.log('recipeId:', recipeId);
    console.log('currentUsername:', currentUsername);

    function getCsrfToken() {
        const cookieValue = document.cookie.split('; ')
            .find(row => row.startsWith('csrftoken='))
            .split('=')[1];
        return cookieValue;
    }

    function updateCommentList(comments, totalComments) {
        const commentList = document.getElementById('comment-list');
        const commentCount = document.querySelector('.recipe-detail-comment-title');

        commentList.innerHTML = '';
        comments.forEach(comment => {
            const commentItem = document.createElement('li');
            commentItem.className = 'recipe-detail-comment-container';
            commentItem.innerHTML = `
                <div class="recipe-detail-comment-user">
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
                const url = `/recipe/${recipeId}/comments/${commentId}/delete/`;

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
                const url = `/recipe/${recipeId}/like/`;

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
    }


    function setupFriendRequestButton() {
        const friendRequestButton = document.getElementById('friend-request-button');
        if (friendRequestButton) {
            friendRequestButton.addEventListener('click', function() {
                const username = this.dataset.username;
                const url = `/recipe/send_friend_request/${username}/`;


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

    setupLikeButton();
    setupBookmarkButton();
    setupFriendRequestButton();
    setupCommentForm();
    setupCommentDeleteEventListeners(); // 초기 이벤트 리스너 설정
});


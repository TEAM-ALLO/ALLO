document.addEventListener('DOMContentLoaded', function() {
    let likeButtons = document.querySelectorAll('.recommend-like');
    let hateButtons = document.querySelectorAll('.recommend-hate');

    likeButtons.forEach(function(likeButton, index) {
        likeButton.addEventListener('click', function(event) {
            event.preventDefault();
            let hateButton = hateButtons[index];  // 같은 인덱스의 싫어요 버튼 가져오기

            if (likeButton.style.color === 'red') {
                likeButton.style.color = 'black';
                hateButton.disabled = false;
            } else {
                likeButton.style.color = 'red';
                hateButton.disabled = true;
            }

            // AJAX 요청을 사용하여 폼을 비동기적으로 제출
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
        hateButton.addEventListener('click', function(event) {
            event.preventDefault();
            let likeButton = likeButtons[index];  // 같은 인덱스의 좋아요 버튼 가져오기

            if (hateButton.style.color === 'red') {
                hateButton.style.color = 'black';
                likeButton.disabled = false;
            } else {
                hateButton.style.color = 'red';
                likeButton.disabled = true;
            }

            // AJAX 요청을 사용하여 폼을 비동기적으로 제출
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


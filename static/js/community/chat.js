// 채팅 컨테이너를 맨 아래로 스크롤하는 함수
function scrollToBottom() {
    var chatContainer = document.getElementById("chat-messages");
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// 페이지 로드 시 맨 아래로 스크롤
window.onload = function() {
    scrollToBottom();
};

// 폼 제출 시 AJAX를 사용하여 페이지를 다시 로드하지 않고 메시지 전송
document.getElementById("message-form").addEventListener("submit", function(event) {
    event.preventDefault();
    var formData = new FormData(this);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", this.action, true);
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhr.onload = function() {
        if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            var chatMessages = document.getElementById("chat-messages");
            var newMessage = document.createElement("div");

            if (response.sender === "{{ request.user.username }}") {
                newMessage.classList.add("bubble-container-right");
                newMessage.innerHTML = response.content;
                if (response.image) {
                    var imgContainer = document.createElement("div");
                    imgContainer.classList.add("message-image-container");
                    var img = document.createElement("img");
                    img.src = response.image;
                    img.alt = "채팅 이미지";
                    img.classList.add("chat-image");
                    imgContainer.appendChild(img);
                    newMessage.appendChild(imgContainer);
                }
                var bubbleTail = document.createElement("img");
                bubbleTail.src = "{% static 'img/my-bubble.svg' %}";
                bubbleTail.alt = "말풍선 꼬리 이미지";
                bubbleTail.classList.add("my-bubble");
                newMessage.appendChild(bubbleTail);
            } else {
                newMessage.classList.add("bubble-big-container-left");
                var topContainer = document.createElement("div");
                topContainer.classList.add("bubble-big-container-top");

                var profileImg = document.createElement("img");
                if (receiver.profile_image) {
                    profileImg.src = "{{ receiver.profile_image.url }}";
                } else {
                    profileImg.src = "{% static 'img/user.svg' %}";
                }
                profileImg.alt = "프로필 사진";
                profileImg.classList.add("mypage-img");
                topContainer.appendChild(profileImg);

                var contentContainer = document.createElement("div");
                contentContainer.classList.add("bubble-container-left");
                contentContainer.innerHTML = response.content;
                if (response.image) {
                    var imgContainerLeft = document.createElement("div");
                    imgContainerLeft.classList.add("message-image-container");
                    var imgLeft = document.createElement("img");
                    imgLeft.src = response.image;
                    imgLeft.alt = "채팅 이미지";
                    imgLeft.classList.add("chat-image");
                    imgContainerLeft.appendChild(imgLeft);
                    contentContainer.appendChild(imgContainerLeft);
                }
                var bubbleTailLeft = document.createElement("img");
                bubbleTailLeft.src = "{% static 'img/bubble-writer.svg' %}";
                bubbleTailLeft.alt = "말풍선 꼬리 이미지";
                bubbleTailLeft.classList.add("bubble-writer");
                contentContainer.appendChild(bubbleTailLeft);

                topContainer.appendChild(contentContainer);
                newMessage.appendChild(topContainer);

                var username = document.createElement("p");
                username.textContent = response.sender;
                newMessage.appendChild(username);
            }

            chatMessages.appendChild(newMessage);
            scrollToBottom();
            document.getElementById("message-form").reset(); // 폼 초기화
        }
    };
    xhr.send(formData);
});
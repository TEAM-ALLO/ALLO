function addFurnitureField() {
    var container = document.getElementById("furniture_fields");
    var itemCount = container.getElementsByClassName("furniture-item").length;

    if (itemCount >= 20) {
        alert('가구 목록은 최대 20개까지 추가할 수 있습니다.');
        return;
    }

    var newItem = document.createElement("div");
    newItem.className = "furniture-item";

    var input = document.createElement("input");
    input.type = "text";
    input.name = "furniture_list[]";
    input.className = "form-control";

    var removeButton = document.createElement("button");
    removeButton.type = "button";
    removeButton.innerText = "삭제";
    removeButton.className = "interior-furniture-remove-btn";
    removeButton.onclick = function() {
        removeFurnitureField(this);
    };

    newItem.appendChild(input);
    newItem.appendChild(removeButton);
    container.appendChild(newItem);
}

function removeFurnitureField(button) {
    var container = document.getElementById("furniture_fields");
    var itemCount = container.getElementsByClassName("furniture-item").length;

    if (itemCount > 1) {
        container.removeChild(button.parentElement);
    } else {
        alert('가구 목록은 최소 하나 이상이어야 합니다.');
    }
}

document.querySelector('form').addEventListener('submit', function(e) {
    var furnitureListInputs = document.querySelectorAll('input[name="furniture_list[]"]');
    var furnitureList = [];

    furnitureListInputs.forEach(function(input) {
        if (input.value.trim() !== "") {
            furnitureList.push(input.value.trim());
        }
    });

    if (furnitureList.length === 0) {
        e.preventDefault();
        alert('가구 목록은 최소 하나 이상이어야 합니다.');
        return;
    }

    var hiddenInput = document.querySelector('input[name="furniture_list"]');
    hiddenInput.value = furnitureList.join('\n');
});

function addFurnitureField() {
    var container = document.getElementById("furniture_fields");
    var input = document.createElement("input");
    input.type = "text";
    input.name = "furniture_list[]";
    input.className = "form-control";
    container.appendChild(input);
}
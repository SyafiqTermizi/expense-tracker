const imageInput = document.getElementById("imageInput") as HTMLInputElement;
const imagePreview = document.getElementById("imagePreview") as HTMLImageElement;
const imageLink = document.getElementById("imageLink") as HTMLAnchorElement;
const imageContainer = document.getElementById("imageContainer");
const imageRemoveButton = document.getElementById("imageRemoveButton");

imageInput.onchange = _ => {
    const [file] = imageInput.files;
    if (file) {
        imagePreview.classList.remove("d-none");
        imagePreview.src = URL.createObjectURL(file);
        imageLink.href = URL.createObjectURL(file);
        imageContainer.classList.add("input-group");
        imageRemoveButton.classList.remove("d-none");
    }
}

imageRemoveButton.onclick = _ => {
    imagePreview.classList.add("d-none");
    imagePreview.src = "";
    imageLink.href = "#";
    imageContainer.classList.remove("input-group");
    imageRemoveButton.classList.add("d-none");
    imageInput.files = null;
    imageInput.value = "";
}
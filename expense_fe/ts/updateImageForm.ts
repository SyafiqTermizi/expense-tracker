const imageInput = document.getElementById("imageInput") as HTMLInputElement;
const imagePreview = document.getElementById("imagePreview") as HTMLImageElement;
const imageLink = document.getElementById("imageLink") as HTMLAnchorElement;
const imageRemoveButton = document.getElementById("imageRemoveButton");
const existingImageSrc = imagePreview.src;

imageInput.onchange = _ => {
    const [file] = imageInput.files;
    if (file) {
        imagePreview.classList.remove("d-none");
        imagePreview.src = URL.createObjectURL(file);
        imageLink.href = URL.createObjectURL(file);
    }
}

imageRemoveButton.onclick = _ => {
    imagePreview.src = existingImageSrc;
    imageLink.href = existingImageSrc;
    imageInput.files = null;
    imageInput.value = "";
}

export { }
<script lang="ts">
    export let images;
    let imageURL = "";
    let imageInput;

    function fileObjToUrl() {
        const [file] = images;
        if (file) {
            imageURL = URL.createObjectURL(file);
        }
    }
</script>

<div class="mb-2" class:input-group={images}>
    <input
        bind:files={images}
        bind:this={imageInput}
        on:change={fileObjToUrl}
        class="form-control"
        type="file"
        name="image"
        accept="image/*"
    />
    {#if images}
        <button
            class="btn btn-outline-secondary"
            on:click={() => {
                images = null;
                imageInput.value = "";
                imageURL = "";
            }}
            type="button"
        >
            Clear
        </button>
    {/if}
</div>
{#if images}
    <div class="mb-2 form-text">Upload new image to replace current image</div>
    <img
        class="img-thumbnail mb-2"
        src={imageURL}
        alt="Expenses attachment"
        style="object-fit: cover; width: 100px; height: 100px"
    />
{/if}

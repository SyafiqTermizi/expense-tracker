<script lang="ts">
    interface Option {
        selectedDisplay: string;
        optionDisplay: string;
        value: string | number;
    }

    export let label = "";
    export let placeholder = "Choose an option";
    export let options: Option[];
    export let selectedValue: string | number = null;
    export let errorMessage = "";

    function handleDropdownClick(value: string | number): void {
        selectedValue = value;
    }
</script>

<label for={label} class="form-label">{label}:</label>
<div
    class="dropdown d-grid gap-2"
    class:border={errorMessage}
    class:border-danger={errorMessage}
    class:rounded-2={errorMessage}
>
    <button
        id="dropdown-button"
        class="text-left btn btn-outline-dark dropdown-toggle"
        type="button"
        data-bs-toggle="dropdown"
    >
        {#if selectedValue}
            {options.find((option) => option.value == selectedValue)
                .selectedDisplay}
        {:else}
            {placeholder}
        {/if}
    </button>
    <ul class="dropdown-menu">
        {#each options as { value, optionDisplay }}
            <li>
                <button
                    class="dropdown-item"
                    on:click={() => handleDropdownClick(value)}
                >
                    {optionDisplay}
                </button>
            </li>
        {/each}
    </ul>
</div>
<p class="text-danger">{errorMessage}</p>

<style>
    #dropdown-button {
        border-color: #dee2e6;
        text-align: left;
    }
    #dropdown-button:hover {
        background-color: white;
        color: black;
    }
</style>

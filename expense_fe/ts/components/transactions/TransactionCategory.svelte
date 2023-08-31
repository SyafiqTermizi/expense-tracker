<script lang="ts">
    import { expenseCategories, selectedCategory, showAll } from "./store";
</script>

<div class="col-md-4 col-sm-12 mt-2 text-sm-start text-md-end">
    {#if $showAll}
        <div />
    {:else}
        <div class="dropdown">
            <button
                class="btn btn-outline-secondary btn-sm dropdown-toggle"
                id="unique123"
                type="button"
                data-bs-toggle="dropdown"
                style="min-width: 130px;"
            >
                {#if $selectedCategory}
                    {$selectedCategory}
                {:else}
                    Pick a category
                {/if}
            </button>
            <ul class="dropdown-menu">
                {#each $expenseCategories as expenseCategory}
                    <li>
                        <button
                            class="dropdown-item"
                            on:click={() =>
                                selectedCategory.set(expenseCategory)}
                            >{expenseCategory}</button
                        >
                    </li>
                {/each}
                <li><hr class="dropdown-divider" /></li>
                <li>
                    <button
                        class="dropdown-item"
                        on:click={() => selectedCategory.set("")}>Clear</button
                    >
                </li>
            </ul>
        </div>
    {/if}
</div>

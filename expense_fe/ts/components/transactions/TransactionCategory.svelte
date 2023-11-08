<script lang="ts">
    import { expenseCategories, selectedCategory, showAll } from "./store";
</script>

{#if $showAll}
    <div />
{:else}
    <div class="dropdown">
        <button
            class="btn btn-outline-secondary btn-sm dropdown-toggle"
            id="123"
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
                        on:click={() => selectedCategory.set(expenseCategory)}
                        >{expenseCategory}</button
                    >
                </li>
            {/each}
            <li><hr class="dropdown-divider" /></li>
            <li>
                <button
                    class="dropdown-item"
                    on:click={() => selectedCategory.set("")}
                >
                    All categories
                </button>
            </li>
        </ul>
    </div>
{/if}

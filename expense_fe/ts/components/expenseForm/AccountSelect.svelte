<script lang="ts">
    export let accountBalances: Account[];
    export let userCurrency = "";
    export let selectedAccount: string = null;

    function handleAccountDropdownClick(accountSlug: string): void {
        selectedAccount = accountSlug;
    }
</script>

<div class="dropdown d-grid gap-2">
    <button
        id="dropdown-button"
        class="text-left btn btn-outline-dark dropdown-toggle"
        type="button"
        data-bs-toggle="dropdown"
    >
        {#if selectedAccount}
            {accountBalances.find((account) => account.slug == selectedAccount)
                .name}
        {:else}
            Select an account
        {/if}
    </button>
    <ul class="dropdown-menu">
        {#each accountBalances as { slug, name, balance }}
            <li>
                <button
                    class="dropdown-item"
                    on:click={() => handleAccountDropdownClick(slug)}
                >
                    {name} - balance: {userCurrency}
                    {balance}
                </button>
            </li>
        {/each}
    </ul>
</div>

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

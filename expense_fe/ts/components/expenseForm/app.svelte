<script lang="ts">
    export let accountBalances: Account[];
    export let userCurrency = "";

    import AccountSelect from "./AccountSelect.svelte";

    let fromAccountSlug: string = "";
</script>

<div class="card-body p-4">
    <div class="mb-3">
        <label for="id_from_account" class="form-label">From Account:</label>
        <AccountSelect
            {accountBalances}
            {userCurrency}
            bind:selectedAccount={fromAccountSlug}
        />
    </div>
</div>

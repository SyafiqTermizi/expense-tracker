<script lang="ts">
    export let accountBalances: Account[];
    export let userCurrency = "";
    export let expenseCategories: { name: string; slug: string }[] = [];

    import AccountSelect from "./AccountSelect.svelte";

    let fromAccount: string = "";
    let amount: number;
    let description: string;
    let category: string;
</script>

<div class="card-body p-4">
    <div class="mb-3">
        <label for="id_from_account" class="form-label">From Account:</label>
        <AccountSelect
            {accountBalances}
            {userCurrency}
            bind:selectedAccount={fromAccount}
        />
    </div>

    <div class="mb-3">
        <label class="form-label" for="id_amount">
            Amount ({userCurrency}):
        </label>
        <input
            class="form-control"
            type="number"
            name="amount"
            step="0.01"
            required
            id="id_amount"
            bind:value={amount}
        />
    </div>

    <div class="mb-3">
        <label class="form-label" for="id_description">Description:</label>
        <input
            class="form-control"
            type="text"
            name="description"
            maxlength="255"
            id="id_description"
            bind:value={description}
        />
    </div>

    <div>
        <label class="form-label" for="id_category">category:</label>
        <select
            class="form-select"
            name="category"
            id="id_category"
            bind:value={category}
        >
            <option value="">----</option>
            {#each expenseCategories as category}
                <option value={category.slug}>
                    {category.name}
                </option>
            {/each}
        </select>

        <div class="row">
            <div class="col-6" />
            <div class="col-6 text-end">
                <p>
                    <a
                        class="card-link"
                        href="/expenses/categories/add?next=/expenses/add"
                    >
                        Add new category
                    </a>
                </p>
            </div>
        </div>
    </div>
</div>

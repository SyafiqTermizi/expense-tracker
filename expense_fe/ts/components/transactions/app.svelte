<script lang="ts">
    import TransactionList from "./TransactionList.svelte";
    import TransactionFilter from "./TransactionFilter.svelte";
    import TransactionSearch from "./TransactionSearch.svelte";

    const currency: string =
        document.getElementById("user-currency").textContent;
</script>

<div class="row mt-5">
    <div class="col-8" id="transaction-filter">
        <TransactionFilter />
    </div>
    <div class="col-4" id="transaction-search">
        <TransactionSearch />
    </div>
</div>
<div class="row mt-2 mb-5" id="transaction-list">
    <TransactionList {currency} />
</div>

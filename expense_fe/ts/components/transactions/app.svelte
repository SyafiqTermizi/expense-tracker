<script lang="ts">
    import TransactionList from "./TransactionList.svelte";
    import TransactionFilter from "./TransactionFilter.svelte";
    import TransactionSearch from "./TransactionSearch.svelte";

    const currency: string =
        document.getElementById("user-currency").textContent;
</script>

<div class="card">
    <div class="row pt-2 px-3">
        <TransactionFilter />
        <TransactionSearch />
    </div>
    <hr />
    <TransactionList {currency} />
</div>

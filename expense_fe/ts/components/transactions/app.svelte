<script lang="ts">
    import TransactionList from "./TransactionList.svelte";
    import TransactionFilter from "./TransactionFilter.svelte";
    import TransactionSearch from "./TransactionSearch.svelte";
    import Modal from "./Modal.svelte";

    export let currency = "MYR";
    export let hideFilter = false;
</script>

<div class="card">
    <div class="row pt-2 px-3">
        <TransactionSearch />
        {#if !hideFilter}
            <TransactionFilter />
        {/if}
    </div>
    <hr />
    <TransactionList {currency} />
    <Modal {currency} />
</div>

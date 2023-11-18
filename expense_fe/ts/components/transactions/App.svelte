<script lang="ts">
    import TransactionSearch from "./TransactionSearch.svelte";
    import ExpenseCategory from "./ExpenseCategory.svelte";
    import TransactionList from "./TransactionList.svelte";
    import Filter from "./Filter.svelte";
    import Modal from "./Modal.svelte";

    import { activeFilter } from "./store";
    import Summary from "./Summary.svelte";

    export let currency;
    export let showOnlyFilter: FilterType = null;

    let categoryClass = "col-md-4 col-sm-12";
    if (showOnlyFilter) {
        activeFilter.set(showOnlyFilter);
        categoryClass = "col-12";
    }
</script>

<div class="card">
    <div class="row pt-2 px-3">
        {#if !showOnlyFilter}
            <div class="col-md-8 col-sm-12 mt-2">
                <Filter />
            </div>
        {/if}
        <div class={`${categoryClass} ps-3 mt-2 text-sm-start text-md-end`}>
            {#if $activeFilter === "transactions"}
                <TransactionSearch />
            {:else if $activeFilter === "expenses"}
                <ExpenseCategory />
            {:else}
                <div />
            {/if}
        </div>
    </div>
    <hr />
    {#if $activeFilter === "summary"}
        <Summary {currency} />
    {:else}
        <TransactionList {currency} />
        <Modal {currency} />
    {/if}
</div>

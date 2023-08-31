<script lang="ts">
    import TransactionList from "./TransactionList.svelte";
    import TransactionFilter from "./TransactionFilter.svelte";
    import TransactionCategory from "./TransactionCategory.svelte";
    import Modal from "./Modal.svelte";

    import { showAll } from "./store";

    export let currency = "MYR";
    export let hideFilter = false;

    let categoryClass = "col-md-4 col-sm-12";
    if (hideFilter) {
        showAll.set(false);
        categoryClass = "col-12";
    }
</script>

<div class="card">
    <div class="row pt-2 px-3">
        {#if !hideFilter}
            <div class="col-md-8 col-sm-12 mt-2">
                <TransactionFilter />
            </div>
        {/if}
        <div class={`${categoryClass} mt-2 text-sm-start text-md-end`}>
            <TransactionCategory />
        </div>
    </div>
    <hr />
    <TransactionList {currency} />
    <Modal {currency} />
</div>

<script lang="ts">
    import { showAll } from "./store";

    const activeClass = "ms-1 btn btn-primary btn-sm";
    const inactiveClass = "ms-1 btn btn-outline-secondary btn-sm";
    const date = new Date();
    const month = date.toLocaleString("default", { month: "long" });
</script>

<div class="col-md-8 col-sm-12 mt-2 text-sm-start text-md-end">
    Show {month}'s:
    <button
        class={$showAll ? activeClass : inactiveClass}
        on:click={() => showAll.set(true)}
    >
        Transactions
    </button>
    <button
        class={!$showAll ? activeClass : inactiveClass}
        on:click={() => showAll.set(false)}
    >
        Expenses
    </button>
</div>

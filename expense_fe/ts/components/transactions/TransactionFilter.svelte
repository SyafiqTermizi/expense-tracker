<script lang="ts">
    import { showAll } from "./store";

    const activeClass = "ms-1 btn btn-primary btn-sm";
    const inactiveClass = "ms-1 btn btn-outline-secondary btn-sm";
</script>

Show:
<button
    class={$showAll ? activeClass : inactiveClass}
    on:click={() => showAll.set(true)}
>
    All Transactions
</button>
<button
    class={!$showAll ? activeClass : inactiveClass}
    on:click={() => showAll.set(false)}
>
    Expenses
</button>

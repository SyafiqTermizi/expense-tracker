<script lang="ts">
    import { showAll } from "./store";

    const activeClass = "ms-1 btn btn-primary btn-sm";
    const inactiveClass = "ms-1 btn btn-outline-secondary btn-sm";
</script>

<div class="col-12">
    Show:
    <button
        class={$showAll ? activeClass : inactiveClass}
        on:click={() => showAll.set(true)}
    >
        All Activities
    </button>
    <button
        class={!$showAll ? activeClass : inactiveClass}
        on:click={() => showAll.set(false)}
    >
        Expenses
    </button>
</div>

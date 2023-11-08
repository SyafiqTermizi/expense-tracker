<script lang="ts">
    import { showAll, selectedCategory, keyword } from "./store";

    const activeClass = "ms-1 btn btn-primary btn-sm";
    const inactiveClass = "ms-1 btn btn-outline-secondary btn-sm";
    const date = new Date();
    const month = date.toLocaleString("default", { month: "long" });
</script>

Show {month}'s:
<button
    class={$showAll ? activeClass : inactiveClass}
    on:click={() => {
        showAll.set(true);
        selectedCategory.set("");
        keyword.set("");
    }}
>
    Transactions
</button>
<button
    class={!$showAll ? activeClass : inactiveClass}
    on:click={() => {
        showAll.set(false);
        selectedCategory.set("");
        keyword.set("");
    }}
>
    Expenses
</button>

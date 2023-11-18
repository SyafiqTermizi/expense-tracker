<script lang="ts">
    import { activeFilter, selectedCategory, searchKeyword } from "./store";

    const activeClass = "ms-1 btn btn-primary btn-sm";
    const inactiveClass = "ms-1 btn btn-outline-secondary btn-sm";
</script>

<button
    class={$activeFilter === "transactions" ? activeClass : inactiveClass}
    on:click={() => {
        activeFilter.set("transactions");
        selectedCategory.set("");
        searchKeyword.set("");
    }}
>
    Transactions
</button>
<button
    class={$activeFilter === "expenses" ? activeClass : inactiveClass}
    on:click={() => {
        activeFilter.set("expenses");
        selectedCategory.set("");
        searchKeyword.set("");
    }}
>
    Expenses
</button>

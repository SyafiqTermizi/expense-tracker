import TransactionList from "./TransactionList.svelte";
import TransactionFilter from "./TransactionFilter.svelte";
import TransactionSearch from "./TransactionSearch.svelte";

const currency: string = document.getElementById("user-currency").textContent

new TransactionList({
    target: document.getElementById("transaction-list"),
    props: {
        currency: currency,
    }
});

new TransactionFilter({
    target: document.getElementById("transaction-filter"),
});

new TransactionSearch({
    target: document.getElementById("transaction-search"),
});
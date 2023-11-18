import App from "./App.svelte";

import { initialTransactions } from "./store";

const transactionData: Transaction[] = JSON.parse(document.getElementById("transaction-data")!.textContent) || [];
initialTransactions.set(transactionData);

const currency: string =
    document.getElementById("user-currency").textContent;

const showOnlyFilter: FilterType =
    document.getElementById("show-only-filter") &&
    (document.getElementById("show-only-filter").textContent as FilterType);

new App({
    target: document.getElementById("transactions"),
    props: { currency, showOnlyFilter }
});

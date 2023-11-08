import App from "./App.svelte";

import { initialTransactions } from "./store";

const transactionData: Transaction[] = JSON.parse(document.getElementById("transaction-data")!.textContent) || [];
initialTransactions.set(transactionData);

const currency: string =
    document.getElementById("user-currency").textContent;

const hideFilter: boolean =
    document.getElementById("hide-filter") &&
    document.getElementById("hide-filter").textContent === "true";

new App({
    target: document.getElementById("transactions"),
    props: { currency, hideFilter }
});

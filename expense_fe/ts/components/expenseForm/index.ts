import App from "./app.svelte";

const userCurrency: string =
    document.getElementById("user-currency").textContent;

const accountBalances =
    JSON.parse(document.getElementById("account-balances").textContent);

const activeEvents = JSON.parse(document.getElementById("expense-events").textContent);

const expenseCategories = JSON.parse(document.getElementById("expense-categories").textContent);

new App({
    target: document.getElementById("form"),
    props: { accountBalances, userCurrency, expenseCategories, activeEvents }
});

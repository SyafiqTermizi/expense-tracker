import App from "./app.svelte";

const userCurrency: string =
    document.getElementById("user-currency").textContent;

const accountBalances =
    JSON.parse(document.getElementById("account-balances").textContent);

new App({
    target: document.getElementById("form"),
    props: { accountBalances, userCurrency }
});

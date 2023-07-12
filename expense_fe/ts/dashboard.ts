const expenseData: Expense[] = JSON.parse(document.getElementById("expenses-data")!.textContent)
const transactionData: Transaction[] = JSON.parse(document.getElementById("transaction-data")!.textContent)

const currency: string = document.getElementById("user-currency").textContent

import TransactionList from "./components/transactions/TransactionList.svelte";
import TransactionFilter from "./components/transactions/TransactionFilter.svelte";

new TransactionList({
    target: document.getElementById("transaction-list"),
    props: {
        transactions: transactionData,
        currency: currency,
    }
});

new TransactionFilter({
    target: document.getElementById("transaction-filter"),
});

var options = {
    chart: {
        type: 'donut'
    },
    series: expenseData.map(expense => parseFloat(expense["amount"])),
    labels: expenseData.map(expense => expense["category"]),
    legend: {
        position: 'bottom'
    },
    tooltip: {
        y: {
            formatter: (value) => `${currency} ${value}`
        }
    }
}

window.addEventListener("load", () => {
    import("apexcharts").then((ApexCharts) => {
        const Chart = ApexCharts.default;

        const chart = new Chart(document.getElementById("chart"), options);
        chart.render();
    })
});

export { };
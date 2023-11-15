const expenseData: Expense[] = JSON.parse(document.getElementById("expenses-data")!.textContent)
const currency: string = document.getElementById("user-currency").textContent

import { chartColors } from "./utils";

var options = {
    chart: {
        type: 'pie'
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
    },
    colors: chartColors
}

window.addEventListener("load", () => {
    import("apexcharts").then((ApexCharts) => {
        const Chart = ApexCharts.default;

        const chart = new Chart(document.getElementById("chart"), options);
        chart.render();
    })
});

export { };

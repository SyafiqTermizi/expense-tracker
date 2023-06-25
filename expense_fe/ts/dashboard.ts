const filterAllActivityButton = document.getElementById("filter-all-activities");
const filterExpenseButton = document.getElementById("filter-expenses");
const activityTable = document.getElementById("activity-table");
const expenseTable = document.getElementById("expense-table");

filterAllActivityButton.addEventListener("click", () => {
    filterAllActivityButton.classList.remove("btn-outline-secondary");
    filterAllActivityButton.classList.add("btn-primary");

    filterExpenseButton.classList.add("btn-outline-secondary");
    filterExpenseButton.classList.remove("btn-primary");

    activityTable.classList.remove("d-none");
    expenseTable.classList.add("d-none");
});

filterExpenseButton.addEventListener("click", () => {
    filterExpenseButton.classList.remove("btn-outline-secondary");
    filterExpenseButton.classList.add("btn-primary");

    filterAllActivityButton.classList.add("btn-outline-secondary");
    filterAllActivityButton.classList.remove("btn-primary");

    expenseTable.classList.remove("d-none");
    activityTable.classList.add("d-none");
});

import Chart from "apexcharts";

const expenseData: Expense[] = JSON.parse(document.getElementById("expenses-data")!.textContent)


var options = {
    chart: {
        type: 'donut'
    },
    series: expenseData.map(expense => parseFloat(expense["amount"])),
    labels: expenseData.map(expense => expense["category"]),
    legend: {
        position: 'bottom'
    },
}

const chart = new Chart(document.getElementById("chart"), options);
chart.render();
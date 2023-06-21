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

const dailyBalance: ChartData[] = JSON.parse(document.getElementById("balances-data")!.textContent)

dailyBalance.sort((a, b) => {
    return parseInt(a.x.slice(0, 2)) > parseInt(b.x.slice(0, 2)) ? 1 : -1
})

import { LineChart, AutoScaleAxis } from "chartist";

new LineChart(
    "#chart",
    {
        labels: dailyBalance.map(data => data.x),
        series: [dailyBalance.map(data => data.y)],
    },
    {
        axisY: {
            showLabel: true,
            type: AutoScaleAxis
        }
    }
)
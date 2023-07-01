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

import Chart from "apexcharts"

const currency: string = document.getElementById("user-currency").textContent

const options = {
    chart: {
        type: 'line',
        height: '100%'
    },
    series: [
        {
            name: "Monthly Balance",
            data: dailyBalance.map(data => data.y)
        }
    ],
    xaxis: {
        categories: dailyBalance.map(data => data.x)
    },
    dataLabels: {
        enabled: true,
        formatter: (value) => `${currency} ${value}`
    },
    markers: {
        size: 1
    },
    grid: {
        show: false
    },
    tooltip: {
        enabled: false
    }
}

const chart = new Chart(document.getElementById("chart"), options);
chart.render();


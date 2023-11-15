
import { getChartOption, getChartLegend } from "./utils/chart";


const expenseData: Expense[] = JSON.parse(document.getElementById("expenses-data")!.textContent)

const formattedExpenseData = {};
for (const data of expenseData) {
    formattedExpenseData[data.category] = data.amount
}

window.addEventListener("load", () => {
    import("apexcharts").then((ApexCharts) => {
        const Chart = ApexCharts.default;

        const chart = new Chart(
            document.getElementById("chart"),
            getChartOption(formattedExpenseData, "donut"),
        );
        chart.render();

        const accountLegend = document.getElementById("chart-legend");
        accountLegend.innerHTML = getChartLegend(formattedExpenseData);
    })
});

export { };

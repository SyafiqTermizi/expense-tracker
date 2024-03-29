import { getChartOption, getChartLegend } from "./utils/chart";

const expenseByCategory = JSON.parse(document.getElementById("expense-by-category")!.textContent);
const expenseByAccount = JSON.parse(document.getElementById("expense-by-account")!.textContent);

window.addEventListener("load", () => {
    import("apexcharts").then((ApexCharts) => {
        const Chart = ApexCharts.default;

        const categoryChart = new Chart(
            document.getElementById("category-chart"),
            getChartOption(expenseByCategory, "donut"),
        );
        categoryChart.render();

        const categoryLegend = document.getElementById("category-chart-legend");
        categoryLegend.innerHTML = getChartLegend(expenseByCategory);

        const accountChart = new Chart(
            document.getElementById("account-chart"),
            getChartOption(expenseByAccount, "pie"),
        );
        accountChart.render();

        const accountLegend = document.getElementById("account-chart-legend");
        accountLegend.innerHTML = getChartLegend(expenseByAccount);

        const categoryChartContainer = document.getElementById("category-chart-container");
        const categoryChartContainerHeight = categoryChartContainer.offsetHeight;

        const accountChartContainer = document.getElementById("account-chart-container");
        const accountChartContainerHeight = accountChartContainer.offsetHeight;

        if (categoryChartContainerHeight >= accountChartContainerHeight) {

            accountChartContainer.style.height = `${categoryChartContainerHeight}px`;
        } else {

            categoryChartContainer.style.height = `${accountChartContainerHeight}px`;
        }
    })
});


export { };

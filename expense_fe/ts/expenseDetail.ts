import Chart from "apexcharts";

const expenseByCategory = JSON.parse(document.getElementById("expense-by-category")!.textContent);
const expenseByAccount = JSON.parse(document.getElementById("expense-by-account")!.textContent);

function getChartOption(data) {
    return {
        chart: {
            type: 'bar',
            height: '100%'
        },
        series: [
            {
                name: "Monthly Balance",
                data: data.map(data => data.y)
            }
        ],
        xaxis: {
            categories: data.map(data => data.x)
        },
        dataLabels: {
            enabled: true,
        },
        markers: {
            size: 1
        },
        grid: {
            show: false
        }
    }
}
const categoryChart = new Chart(document.getElementById("category-chart"), getChartOption(expenseByCategory));
categoryChart.render();

const accountChart = new Chart(document.getElementById("account-chart"), getChartOption(expenseByAccount));
accountChart.render();

const showByCategory = document.getElementById("show-by-category");
const showByAccount = document.getElementById("show-by-account");
const categoryChartContainer = document.getElementById("category-chart");
const accountChartContainer = document.getElementById("account-chart");
const chartTitle = document.getElementById("chart-title");

showByCategory.addEventListener("click", () => {
    showByCategory.classList.remove("btn-outline-secondary");
    showByCategory.classList.add("btn-primary");

    showByAccount.classList.add("btn-outline-secondary");
    showByAccount.classList.remove("btn-primary");

    categoryChartContainer.classList.remove("d-none");
    accountChartContainer.classList.add("d-none");
    chartTitle.textContent = "Expense by category";

});

showByAccount.addEventListener("click", () => {
    showByAccount.classList.remove("btn-outline-secondary");
    showByAccount.classList.add("btn-primary");

    showByCategory.classList.add("btn-outline-secondary");
    showByCategory.classList.remove("btn-primary");

    accountChartContainer.classList.remove("d-none");
    categoryChartContainer.classList.add("d-none");
    chartTitle.textContent = "Expense by acccount";
});

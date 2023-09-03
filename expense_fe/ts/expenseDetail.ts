const currency: string = document.getElementById("user-currency").textContent

const expenseByCategory = JSON.parse(document.getElementById("expense-by-category")!.textContent);
const expenseByAccount = JSON.parse(document.getElementById("expense-by-account")!.textContent);

function getChartOption(data, chartType) {
    return {
        chart: {
            type: chartType,
        },
        series: Object.values(data).map((value) => parseFloat(value as string)),
        labels: Object.keys(data),
        legend: {
            position: 'bottom'
        },
        tooltip: {
            y: {
                formatter: (value) => `${currency} ${value}`
            }
        },
    }
}


window.addEventListener("load", () => {
    import("apexcharts").then((ApexCharts) => {
        const Chart = ApexCharts.default;

        const categoryChart = new Chart(
            document.getElementById("category-chart"),
            getChartOption(expenseByCategory, "pie"),
        );
        categoryChart.render();

        const accountChart = new Chart(
            document.getElementById("account-chart"),
            getChartOption(expenseByAccount, "donut"),
        );
        accountChart.render();

    })
});


export { };
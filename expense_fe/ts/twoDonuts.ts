const currency: string = document.getElementById("user-currency").textContent

const expenseByCategory = JSON.parse(document.getElementById("expense-by-category")!.textContent);
const expenseByAccount = JSON.parse(document.getElementById("expense-by-account")!.textContent);

function getChartOption(data, chartType) {
    const values = Object.values(data).map((value) => parseFloat(value as string))
    const sum = values.reduce((partialSum, a) => partialSum + a, 0);

    return {
        dataLabels: {
            formatter: function (val, opts) {
                return `${currency} ${((val * sum) / 100).toFixed(2)}`
            },
        },
        chart: {
            type: chartType,
        },
        series: values,
        labels: Object.keys(data),
        legend: {
            position: 'bottom'
        },
        tooltip: {
            y: {
                formatter: (value) => `${((value / sum) * 100).toFixed(2)}%`
            }
        },
    }
}


window.addEventListener("load", () => {
    import("apexcharts").then((ApexCharts) => {
        const Chart = ApexCharts.default;

        const categoryChart = new Chart(
            document.getElementById("category-chart"),
            getChartOption(expenseByCategory, "donut"),
        );
        categoryChart.render();

        const accountChart = new Chart(
            document.getElementById("account-chart"),
            getChartOption(expenseByAccount, "pie"),
        );
        accountChart.render();

    })
});


export { };

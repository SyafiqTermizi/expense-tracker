const expenseData: Expense[] = JSON.parse(document.getElementById("expenses-data")!.textContent)
const currency: string = document.getElementById("user-currency").textContent

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
    colors: [
        "#008FFB",
        "#00E396",
        "#FEB019",
        "#FF4560",
        "#775DD0",
        "#4caf50",
        "#546E7A",
        "#f9a3a4",
        "#F86624",
        "#662E9B",
        "#2E294E",
        "#5A2A27",
        "#D7263D"
    ]
}

window.addEventListener("load", () => {
    import("apexcharts").then((ApexCharts) => {
        const Chart = ApexCharts.default;

        const chart = new Chart(document.getElementById("chart"), options);
        chart.render();
    })
});

export { };

const currency: string = document.getElementById("user-currency").textContent

const dailyBalance: ChartData[] = JSON.parse(document.getElementById("balances-data")!.textContent)

dailyBalance.sort((a, b) => {
    return parseInt(a.x.slice(0, 2)) > parseInt(b.x.slice(0, 2)) ? 1 : -1
})

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

window.addEventListener("load", () => {
    import("apexcharts").then((ApexCharts) => {
        const Chart = ApexCharts.default;

        const chart = new Chart(document.getElementById("chart"), options);
        chart.render();

    })
});

export { };
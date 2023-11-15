const currency: string = document.getElementById("user-currency").textContent

export const chartColors = [
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

const formatter = new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: currency,
});

export function getChartOption(data, chartType) {
    const values = Object.values(data).map((value) => parseFloat(value as string))
    const sum = values.reduce((partialSum, a) => partialSum + a, 0);

    return {
        dataLabels: {
            formatter: function (val, opts) {
                const amount = parseFloat(((val * sum) / 100).toFixed(2))
                return `${formatter.format(amount)}`
            },
        },
        chart: {
            type: chartType,
        },
        series: values,
        labels: Object.keys(data),
        legend: {
            show: false
        },
        tooltip: {
            y: {
                formatter: (value) => `${((value / sum) * 100).toFixed(2)}%`
            }
        },
        colors: chartColors
    }
}

export function getChartLegend(keyValuePair) {
    const classNames = "badge rounded-pill"

    const values = Object.values(keyValuePair).map((value) => parseFloat(value as string))
    const sum = values.reduce((partialSum, a) => partialSum + a, 0);

    let theLegend = "";
    let colorIndex = 0;

    for (const key of Object.keys(keyValuePair)) {

        const style = `color: white; background-color: ${chartColors[colorIndex]}`
        const percent = ((keyValuePair[key] / sum) * 100).toFixed(1)
        const textContent = `${formatter.format(keyValuePair[key])}
        <span class="text-secondary">${percent}%</span>`;

        theLegend += `<small class="text-nowrap p-1 text-small">
            <span class=${classNames} style="${style}">${key}</span>
            &nbsp;${textContent}
        </small>`

        if (colorIndex >= chartColors.length - 1) {
            colorIndex = 0
        } else {
            colorIndex += 1;
        }
    }

    return theLegend;
}

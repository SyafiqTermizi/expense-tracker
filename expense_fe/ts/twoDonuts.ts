import { text } from "svelte/internal";
import { chartColors } from "./utils";

const currency: string = document.getElementById("user-currency").textContent

const expenseByCategory = JSON.parse(document.getElementById("expense-by-category")!.textContent);
const expenseByAccount = JSON.parse(document.getElementById("expense-by-account")!.textContent);

console.log(Object.values(expenseByCategory).map(val => parseFloat(val as string)))

function getChartOption(data, chartType) {
    const values = Object.values(data).map((value) => parseFloat(value as string))
    const sum = values.reduce((partialSum, a) => partialSum + a, 0);

    console.log(data);
    console.log(values)

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


const formatter = new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: currency,
});

function getLegend(keyValuePair) {
    const classNames = "badge rounded-pill"

    const values = Object.values(keyValuePair).map((value) => parseFloat(value as string))
    const sum = values.reduce((partialSum, a) => partialSum + a, 0);

    let theLegend = "";
    let colorIndex = 0;

    for (const key of Object.keys(keyValuePair)) {

        const style = `color: white; background-color: ${chartColors[colorIndex]}`
        const percent = ((keyValuePair[key] / sum) * 100).toFixed(0)
        const textContent = `${formatter.format(keyValuePair[key])}
        <span class="text-secondary">${percent}%</span>`;

        theLegend += `<div class="text-nowrap">
            <span class=${classNames} style="${style}">${key}</span>
            &nbsp;${textContent}
        </div>`

        if (colorIndex >= chartColors.length - 1) {
            colorIndex = 0
        } else {
            colorIndex += 1;
        }
    }

    return theLegend;
}

window.addEventListener("load", () => {
    import("apexcharts").then((ApexCharts) => {
        const Chart = ApexCharts.default;

        const categoryChart = new Chart(
            document.getElementById("category-chart"),
            getChartOption(expenseByCategory, "donut"),
        );
        categoryChart.render();

        const categoryLegend = document.getElementById("category-chart-legend");
        categoryLegend.innerHTML = getLegend(expenseByCategory);

        const accountChart = new Chart(
            document.getElementById("account-chart"),
            getChartOption(expenseByAccount, "pie"),
        );
        accountChart.render();

        const accountLegend = document.getElementById("account-chart-legend");
        accountLegend.innerHTML = getLegend(expenseByAccount);

    })
});


export { };

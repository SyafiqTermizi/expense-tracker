const dateDropdownButton = document.getElementById("expense-date-button");
const dateDropdownList = document.getElementById("expense-date-dropdown");
const dropdownArrow = document.getElementById("dropdown-arrow");

dateDropdownButton.addEventListener("click", () => {
    if (dateDropdownButton.classList.contains("show")) {
        dateDropdownButton.classList.remove("show");
        dateDropdownList.classList.remove("show");
        dropdownArrow.style.transform = "rotate(0deg)";
    } else {
        dateDropdownButton.classList.add("show");
        dateDropdownList.classList.add("show");
        dropdownArrow.style.transform = "rotate(180deg)";
    }
});


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

const currency: string = document.getElementById("user-currency").textContent

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
                name: "Spent",
                data: data.map(data => data.y)
            }
        ],
        xaxis: {
            categories: data.map(data => data.x)
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
            y: {
                formatter: (value) => `${currency} ${value}`
            }
        }
    }
}


window.addEventListener("load", () => {
    import("apexcharts").then((ApexCharts) => {
        const Chart = ApexCharts.default;

        const categoryChart = new Chart(document.getElementById("category-chart"), getChartOption(expenseByCategory));
        categoryChart.render();

        const accountChart = new Chart(document.getElementById("account-chart"), getChartOption(expenseByAccount));
        accountChart.render();

    })
});


export { };
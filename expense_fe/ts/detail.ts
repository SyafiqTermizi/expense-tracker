import ActivityFilter from "./components/activities/ActivityFilter.svelte";
import ActivityList from "./components/activities/ActivityList.svelte";

const recentActivities = JSON.parse(document.getElementById("activities-data")!.textContent || "{}");

new ActivityFilter({
    target: document.getElementById("activityFilter")!,
});

new ActivityList({
    target: document.getElementById("activityList")!,
    props: {
        activities: recentActivities,
    }
});

import Chart from "apexcharts";

const dailyBalance: ChartData[] = JSON.parse(document.getElementById("balances-data")!.textContent)

dailyBalance.sort((a, b) => {
    return a.x > b.x ? 1 : -1
})
var options = {
    chart: {
        type: 'line'
    },
    series: [{ data: dailyBalance }],
    legend: {
        position: 'bottom'
    },
}

const chart = new Chart(document.getElementById("chart"), options);
chart.render();
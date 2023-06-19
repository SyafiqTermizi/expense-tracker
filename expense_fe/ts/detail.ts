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

const dailyBalance: ChartData[] = JSON.parse(document.getElementById("balances-data")!.textContent)

dailyBalance.sort((a, b) => {
    return parseInt(a.x.slice(0, 2)) > parseInt(b.x.slice(0, 2)) ? 1 : -1
})

import { LineChart, AutoScaleAxis } from "chartist";

new LineChart(
    "#chart",
    {
        labels: dailyBalance.map(data => data.x),
        series: [dailyBalance.map(data => data.y)],
    },
    {
        axisY: {
            showLabel: true,
            type: AutoScaleAxis
        }
    }
)
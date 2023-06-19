import ActivityFilter from "./components/activities/ActivityFilter.svelte";
import ActivityList from "./components/activities/ActivityList.svelte";
import AccountList from "./components/accounts/AccountList.svelte";

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

const accounts = JSON.parse(document.getElementById("accounts-data")!.textContent || "{}");

new AccountList({
    target: document.getElementById("accountBalance")!,
    props: { accounts }
});

import { PieChart } from "chartist"
const expenseData: Expense[] = JSON.parse(document.getElementById("expenses-data")!.textContent)

new PieChart(
    document.getElementById("chart"),
    {
        series: expenseData.map(expense => parseFloat(expense["amount"])),
        labels: expenseData.map(expense => expense["category"]),
    },
    {
        donut: true,
        donutWidth: "50%",
        height: "50vh",
        showLabel: true
    }
)
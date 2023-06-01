import ActivityFilter from "./ActivityFilter.svelte";
import ActivityList from "./ActivityList.svelte";
import AccountList from "./AccountList.svelte";

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

const accountBalance = JSON.parse(document.getElementById("balance-data")!.textContent || "{}");

new AccountList({
    target: document.getElementById("accountBalance")!,
    props: {
        accountBalance: accountBalance,
    }
});
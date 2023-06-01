<script lang="ts">
    import { onDestroy } from "svelte";
    import { showAll } from "./store";

    export let activities: AccountActivity[] = [];
    let filteredActivities: AccountActivity[];
    let cardTitle: string;

    const unsubscribe = showAll.subscribe((value) => {
        if (value) {
            filteredActivities = activities;
            cardTitle = "Recent account activities";
        } else {
            cardTitle = "Recent expenses";
            filteredActivities = activities.filter(
                (activity) => activity.expense
            );
        }
    });

    onDestroy(unsubscribe);
</script>

<div class="col-12">
    <div class="card">
        <div class="card-header">
            <h6 class="card-title ms-2 my-2">{cardTitle}</h6>
        </div>
        <div class="card-body">
            <table class="table table-hover">
                <thead>
                    <tr>
                        <th scope="col">Description</th>
                        <th scope="col">Amount</th>
                        <th scope="col">Account</th>
                        <th scope="col">Date</th>
                    </tr>
                </thead>
                <tbody>
                    {#each filteredActivities as activity}
                        <tr>
                            <td>{activity.description}</td>
                            <td
                                class={activity.action === "DEBIT"
                                    ? "text-danger"
                                    : "text-success"}>{activity.amount}</td
                            >
                            <td>{activity.account}</td>
                            <td>{activity.created_at}</td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>
    </div>
</div>

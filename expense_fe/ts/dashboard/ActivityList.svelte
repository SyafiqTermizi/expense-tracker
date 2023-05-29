<script lang="ts">
    import { onDestroy } from "svelte";
    import { showAll } from "./store";

    export let activities: AccountActivity[] = [];
    let filteredActivities: AccountActivity[];

    const unsubscribe = showAll.subscribe((value) => {
        if (value) {
            filteredActivities = activities;
        } else {
            filteredActivities = activities.filter(
                (activity) => activity.expense
            );
        }
    });

    onDestroy(unsubscribe);
</script>

<div class="col-12">
    <div class="card">
        <div class="card-body">
            <table class="table table-striped">
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
                            <td>{activity.account_type}</td>
                            <td>{activity.created_at}</td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>
    </div>
</div>

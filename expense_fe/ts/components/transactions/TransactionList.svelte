<script lang="ts">
    import { onDestroy } from "svelte";
    import { showAll } from "./store";
    import { isoToLocalDate } from "../../utils";

    export let transactions: Transaction[] = [];
    export let currency: string = "";

    let filteredTransactions: Transaction[];
    let cardTitle: string;

    const date = new Date();
    const month = date.toLocaleString("default", { month: "long" });

    const unsubscribe = showAll.subscribe((value) => {
        if (value) {
            filteredTransactions = transactions;
            cardTitle = `${month}'s Transactions`;
        } else {
            cardTitle = `${month}'s Expenses`;
            filteredTransactions = transactions.filter(
                (transaction) => transaction.expense
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
                        <th scope="col">Amount ({currency})</th>
                        <th scope="col">Account</th>
                        <th scope="col">Date</th>
                    </tr>
                </thead>
                <tbody>
                    {#each filteredTransactions as transaction}
                        <tr>
                            <td
                                data-bs-toggle="modal"
                                data-bs-target="#expense-modal-{transaction.uid}"
                            >
                                {transaction.description}
                                {#if transaction.expense}
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        class="text-primary"
                                        width="12"
                                        height="12"
                                        viewBox="0 0 24 24"
                                        stroke-width="2"
                                        stroke="currentColor"
                                        fill="none"
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                    >
                                        <path
                                            stroke="none"
                                            d="M0 0h24v24H0z"
                                            fill="none"
                                        />
                                        <path d="M14 3v4a1 1 0 0 0 1 1h4" />
                                        <path
                                            d="M17 21h-10a2 2 0 0 1 -2 -2v-14a2 2 0 0 1 2 -2h7l5 5v11a2 2 0 0 1 -2 2z"
                                        />
                                        <path d="M9 17h6" />
                                        <path d="M9 13h6" />
                                    </svg>
                                {/if}
                            </td>
                            <td
                                class={transaction.action === "DEBIT"
                                    ? "text-danger"
                                    : "text-success"}>{transaction.amount}</td
                            >
                            <td>{transaction.account}</td>
                            <td>{isoToLocalDate(transaction.created_at)}</td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>
    </div>
</div>

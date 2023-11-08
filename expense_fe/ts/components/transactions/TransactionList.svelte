<script lang="ts">
    import { transactions, transactionModalID } from "./store";
    import { isoToLocalDate } from "../../utils";

    export let currency: string = "";

    const formatter = new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: currency,
    });
</script>

<div class="card-body">
    <table class="table table-hover">
        <thead>
            <tr>
                <th scope="col">Description</th>
                <th scope="col">Amount</th>
                <th class="d-none d-lg-block" scope="col">Account</th>
                <th scope="col">Date</th>
            </tr>
        </thead>
        <tbody>
            {#each $transactions as transaction}
                <tr
                    on:click={() => {
                        if (transaction.expense) {
                            transactionModalID.set(transaction.id);
                        }
                    }}
                >
                    <td
                        data-bs-toggle={transaction.expense ? "modal" : ""}
                        data-bs-target={transaction.expense
                            ? "#expense-modal"
                            : ""}
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
                        class={transaction.action === "CREDIT"
                            ? "text-success"
                            : "text-danger"}
                        >{formatter.format(transaction.amount)}
                    </td>
                    <td class="d-none d-lg-block">{transaction.account}</td>
                    <td>{isoToLocalDate(transaction.created_at)}</td>
                </tr>
            {/each}
        </tbody>
    </table>
</div>

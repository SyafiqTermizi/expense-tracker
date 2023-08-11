<script lang="ts">
    import { onDestroy } from "svelte";

    import { isoToLocalDate } from "../../utils";
    import { transactionModalID } from "./store";

    export let currency = "";

    let expenseData: Transaction = null;
    const unsub = transactionModalID.subscribe((modalId) => {
        if (modalId) {
            const request = new XMLHttpRequest();
            request.open("GET", `/expenses/detail/${modalId}`);
            request.onreadystatechange = function () {
                if (request.readyState == XMLHttpRequest.DONE) {
                    expenseData = JSON.parse(request.responseText);
                }
            };
            request.send();
        }
    });
    onDestroy(unsub);
</script>

<div class="modal fade" id="expense-modal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-body">
                {#if expenseData}
                    <h1 class="modal-title fs-5 mb-3" id="expense-modal-label">
                        {expenseData.description}
                    </h1>
                    <p><b>Account:</b>&nbsp;{expenseData.account}</p>
                    <p><b>Amount:</b>&nbsp;{currency} {expenseData.amount}</p>
                    <p><b>Category:</b>&nbsp;{expenseData.category}</p>
                    <p>
                        <b>Created at:</b>&nbsp;{isoToLocalDate(
                            expenseData.created_at
                        )}
                    </p>
                    {#each expenseData.images as image}
                        <img
                            class="img-thumbnail mb-2"
                            src={image}
                            alt="Expenses attachment"
                        />
                    {/each}
                {/if}
                <button
                    type="button"
                    class="text-end btn btn-secondary"
                    data-bs-dismiss="modal">Close</button
                >
            </div>
        </div>
    </div>
</div>

<script lang="ts">
    import { onDestroy } from "svelte";

    import { isoToLocalDate } from "../../utils";
    import { transactionModalID } from "./store";

    export let currency = "";

    let expenseData: Transaction = {
        id: "",
        category: "",
        account: "",
        created_at: "",
        description: "",
        amount: 0,
        action: "",
    };

    const unsub = transactionModalID.subscribe((modalId) => {
        Object.keys(expenseData).forEach((key) => (expenseData[key] = null));
        if (modalId) {
            const request = new XMLHttpRequest();

            request.onreadystatechange = function () {
                if (request.readyState == XMLHttpRequest.DONE) {
                    expenseData = JSON.parse(request.responseText);
                }
            };

            request.open("GET", `/expenses/detail/${modalId}`);
            request.send();
        }
    });
    onDestroy(unsub);
</script>

<div class="modal fade" id="expense-modal" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-body">
                {#if expenseData.description}
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
                        <a href={image} target="_blank">
                            <img
                                class="img-thumbnail mb-2"
                                src={image}
                                alt="Expenses attachment"
                                style="object-fit: cover; width: 100px; height: 100px"
                            />
                        </a>
                    {/each}
                {:else}
                    <h1
                        class="modal-title fs-5 mb-3 placeholder-glow"
                        id="expense-modal-label"
                    >
                        <span class="placeholder col-2" />
                        <span class="placeholder col-5" />
                    </h1>
                    <p class="placeholder-glow">
                        <span class="placeholder col-2" />
                        <span class="placeholder col-3" />
                    </p>
                    <p class="placeholder-glow">
                        <span class="placeholder col-2" />
                        <span class="placeholder col-1" />
                        <span class="placeholder col-3" />
                    </p>
                    <p class="placeholder-glow">
                        <span class="placeholder col-3" />
                        <span class="placeholder col-3" />
                    </p>
                    <p class="placeholder-glow">
                        <span class="placeholder col-3" />
                        <span class="placeholder col-1" />
                        <span class="placeholder col-4" />
                    </p>
                    <div
                        class="img-thumbnail mb-2"
                        style="width: 100px; height: 100px"
                    />
                {/if}
                <br />
                <button
                    type="button"
                    class="text-end btn btn-secondary"
                    data-bs-dismiss="modal">Close</button
                >
            </div>
        </div>
    </div>
</div>

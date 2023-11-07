<script lang="ts">
    export let accountBalances: Account[];
    export let userCurrency = "";

    import { extractErrors, submitFormData } from "../../utils";

    import AlertError from "../AlertError.svelte";
    import Select from "../Select.svelte";

    import { addFormSchema } from "./schema";

    const baseData = {
        account: null,
        amount: null,
        description: null,
    };

    let loading = false;
    function updateLoading() {
        loading = !loading;
    }

    let errors = { ...baseData, __all__: null };

    const queryParams = new URLSearchParams(window.location.search);

    let data = {
        ...baseData,
        account: queryParams.get("account"),
    };

    function updateErrorMessage(errorMessage) {
        errors = { ...errors, ...errorMessage };
    }

    function validateThenSubmit() {
        addFormSchema
            .validate(data, { abortEarly: false, stripUnknown: true })
            .then((validatedData) => {
                submitFormData(
                    validatedData,
                    null,
                    updateLoading,
                    updateErrorMessage
                );
            })
            .catch((err) => {
                errors = { ...errors, ...extractErrors(err) };
            });

        return false;
    }
</script>

<form on:submit|preventDefault class="card-body p-4">
    {#if errors.__all__}<AlertError message={errors.__all__} />{/if}

    <div class="mb-3">
        <Select
            label="Account"
            options={accountBalances.map((_account) => {
                return {
                    selectedDisplay: _account.name,
                    optionDisplay: `${_account.name} - Balance ${userCurrency} ${_account.balance}`,
                    value: _account.slug,
                };
            })}
            placeholder="Select an account"
            errorMessage={errors.account || ""}
            bind:selectedValue={data.account}
        />
    </div>

    <div class="mb-3">
        <label class="form-label" for="id_amount">
            Amount ({userCurrency}):
        </label>
        <input
            class="form-control"
            class:is-invalid={errors.amount}
            type="number"
            name="amount"
            step="0.01"
            id="id_amount"
            bind:value={data.amount}
        />
        <p class="text-danger">{errors.amount || ""}</p>
    </div>

    <div class="mb-3">
        <label class="form-label" for="id_description">Description:</label>
        <input
            class="form-control"
            class:is-invalid={errors.description}
            type="text"
            name="description"
            maxlength="255"
            id="id_description"
            bind:value={data.description}
        />
        <p class="text-danger">{errors.description || ""}</p>
    </div>

    <input
        value="Add"
        type="submit"
        class="mt-3 btn btn-primary"
        on:click={validateThenSubmit}
        disabled={loading}
    />
</form>

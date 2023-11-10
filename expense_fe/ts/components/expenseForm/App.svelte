<script lang="ts">
    export let accountBalances: Account[];
    export let userCurrency = "";
    export let expenseCategories: { name: string; slug: string }[] = [];
    export let activeEvents = [];

    import { extractErrors, submitFormData } from "../../utils";

    import AlertError from "../AlertError.svelte";
    import Select from "../Select.svelte";

    import { expenseSchema } from "./schema";
    import ImageInput from "./ImageInput.svelte";

    const queryParams = new URLSearchParams(window.location.search);

    const baseData = {
        fromAccount: null,
        amount: null,
        description: null,
        category: null,
        event: null,
    };

    let loading = false;
    function updateLoading() {
        loading = !loading;
    }

    let errors = { ...baseData, __all__: null };
    function updateErrorMessage(errorMessage) {
        errors = { ...errors, ...errorMessage };
    }

    let data = {
        ...baseData,
        fromAccount: queryParams.get("account"),
        event: queryParams.get("event"),
        imageInput: null,
    };

    function validateThenSubmit() {
        expenseSchema
            .validate(data, { abortEarly: false, stripUnknown: true })
            .then((validatedData) => {
                let fileInputData: FileInputData = null;

                if (data.imageInput.files.length) {
                    fileInputData = {
                        fieldName: "image",
                        file: data.imageInput.files[0],
                        fileName: data.imageInput.value,
                    };
                }

                submitFormData(
                    validatedData,
                    fileInputData,
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

<form class="card-body p-4" method="post" on:submit|preventDefault>
    {#if errors.__all__}<AlertError message={errors.__all__} />{/if}

    <div class="mb-3">
        <Select
            label="From Account"
            options={accountBalances.map((account) => {
                return {
                    selectedDisplay: account.name,
                    optionDisplay: `${account.name} - Balance ${userCurrency} ${account.balance}`,
                    value: account.slug,
                };
            })}
            placeholder="Select an account"
            errorMessage={errors.fromAccount || ""}
            bind:selectedValue={data.fromAccount}
        />
    </div>

    <div class="mb-3">
        <label class="form-label" for="amount">
            Amount ({userCurrency}):
        </label>
        <input
            class="form-control"
            class:is-invalid={errors.amount}
            type="number"
            name="amount"
            step="0.01"
            id="amount"
            bind:value={data.amount}
        />
        <p class="text-danger">{errors.amount || ""}</p>
    </div>

    <div class="mb-3">
        <label class="form-label" for="descr">Description:</label>
        <input
            class="form-control"
            class:is-invalid={errors.description}
            type="text"
            name="description"
            id="descr"
            bind:value={data.description}
        />
        <p class="text-danger">{errors.description || ""}</p>
    </div>

    <div class="mb-3">
        <Select
            label="Category"
            errorMessage={errors.category || ""}
            options={expenseCategories.map((category) => {
                return {
                    selectedDisplay: category.name,
                    optionDisplay: category.name,
                    value: category.slug,
                };
            })}
            placeholder="Select a category"
            bind:selectedValue={data.category}
        />
        <a
            class="mt-0 mb-3 card-link"
            href="/expenses/categories/add?next=/expenses/add"
        >
            Add new category
        </a>
    </div>

    <div class="mb-3">
        <label class="form-label" for="id_image">Image:</label>
        <ImageInput bind:imageInput={data.imageInput} />
    </div>

    {#if activeEvents.length}
        <div class="mb-3">
            <Select
                label="Event"
                errorMessage={errors.event || ""}
                options={activeEvents.map((event) => {
                    return {
                        selectedDisplay: event.name,
                        optionDisplay: event.name,
                        value: event.slug,
                    };
                })}
                placeholder="Select an event"
                bind:selectedValue={data.event}
            />
        </div>
    {/if}

    <input
        value="Create"
        type="submit"
        class="mt-3 btn btn-primary"
        on:click={validateThenSubmit}
        disabled={loading}
    />
</form>

<script lang="ts">
    export let accountBalances: Account[];
    export let userCurrency = "";
    export let expenseCategories: { name: string; slug: string }[] = [];
    export let activeEvents = [];

    import { getCookie } from "../../utils";

    import { expenseSchema, extractErrors } from "./schema";
    import Select from "./Select.svelte";
    import ImageInput from "./ImageInput.svelte";

    const baseData = {
        fromAccount: null,
        amount: null,
        description: null,
        category: null,
        event: null,
    };

    let errors = { ...baseData, __all__: null };

    let data = { ...baseData, imageInput: null };

    function submitForm() {
        const formdata = new FormData();

        formdata.append("amount", data.amount.toString());
        formdata.append("category", data.category);
        formdata.append("from_account", data.fromAccount);

        if (data.description) {
            formdata.append("description", data.description);
        }

        if (data.imageInput.files.length) {
            formdata.append(
                "image",
                data.imageInput.files[0],
                data.imageInput.value
            );
        }

        if (data.event) {
            formdata.append("event", data.event);
        }

        const request = new XMLHttpRequest();

        const url = new URL(window.location.href);
        url.searchParams.append("response_type", "json");

        request.open("POST", url.href);
        request.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));

        request.onload = () => {
            switch (request.status) {
                case 200:
                    window.location.replace("/");
                    break;
                case 400:
                    const serverErrMsg = JSON.parse(
                        request.responseText
                    ).errors;
                    const localErrMsg = {};

                    for (const fieldName of Object.keys(serverErrMsg)) {
                        localErrMsg[fieldName] =
                            serverErrMsg[fieldName][0].message;
                    }

                    // Clear all local error message in favor of server error message
                    errors = { __all__: null, ...baseData, ...localErrMsg };
                    break;
                default:
                    break;
            }
        };

        request.send(formdata);
    }

    function validateThenSubmit() {
        expenseSchema
            .validate(data, { abortEarly: false, stripUnknown: true })
            .then((_) => submitForm())
            .catch((err) => {
                errors = { ...errors, ...extractErrors(err) };
            });

        return false;
    }
</script>

<form class="card-body p-4" method="post" on:submit|preventDefault>
    {#if errors.__all__}
        <div class="mb-3">
            <div
                class="alert alert-danger alert-dismissible fade show"
                role="alert"
            >
                {errors.__all__}
            </div>
        </div>
    {/if}

    <div class="mb-3">
        <label for="id_from_account" class="form-label">From Account:</label>
        <Select
            errorMessage={errors.fromAccount || ""}
            options={accountBalances.map((account) => {
                return {
                    selectedDisplay: account.name,
                    optionDisplay: `${account.name} - Balance ${userCurrency} ${account.balance}`,
                    value: account.slug,
                };
            })}
            placeholder="Select an account"
            bind:selectedValue={data.fromAccount}
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

    <div class="mb-3">
        <label class="form-label" for="id_category">Category:</label>
        <Select
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
            <label for="id_event" class="form-label">Event:</label>
            <Select
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
    />
</form>

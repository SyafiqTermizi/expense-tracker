<script lang="ts">
    export let accountBalances: Account[];
    export let userCurrency = "";
    export let expenseCategories: { name: string; slug: string }[] = [];

    import Joi from "joi";

    import { getCookie } from "../../utils";

    import Select from "./Select.svelte";
    import ImageInput from "./ImageInput.svelte";

    let fromAccount: string = "";
    let amount: number;
    let description: string;
    let category: string = "";
    let imageInput: HTMLInputElement;
    let errors = {
        fromAccount: "",
        amount: "",
        description: "",
        category: "",
    };

    function validate() {
        const schema = Joi.object({
            fromAccount: Joi.string().label("From account").required(),
            amount: Joi.number().label("Amount").required().min(0.01),
            category: Joi.string().label("Category").required(),
            description: Joi.string().label("Descipription").alphanum().min(2),
        }).options({ abortEarly: false });

        errors = {
            ...schema
                .validate(
                    {
                        fromAccount,
                        amount,
                        description,
                        category,
                    },
                    { abortEarly: false }
                )
                .error.details.reduce(
                    (obj, item) =>
                        Object.assign(obj, { [item.path[0]]: item.message }),
                    errors
                ),
        };
    }

    function submitForm() {
        validate();

        const formdata = new FormData();

        formdata.append("amount", amount.toString());
        formdata.append("category", category);
        formdata.append("from_account", fromAccount);

        if (description) {
            formdata.append("description", description);
        }

        if (imageInput.files.length) {
            formdata.append("image", imageInput.files[0], imageInput.value);
        }

        const request = new XMLHttpRequest();
        request.open("POST", window.location.href);
        request.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
        request.send(formdata);
    }
</script>

<form class="card-body p-4" on:submit|preventDefault={submitForm} method="post">
    <div class="mb-3">
        <label for="id_from_account" class="form-label">From Account:</label>
        <Select
            hasError={Boolean(errors.fromAccount)}
            options={accountBalances.map((account) => {
                return {
                    selectedDisplay: account.name,
                    optionDisplay: `${account.name} - Balance ${userCurrency} ${account.balance}`,
                    value: account.slug,
                };
            })}
            placeholder="Select an account"
            bind:selectedValue={fromAccount}
        />
        <p class="text-danger">{errors.fromAccount}</p>
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
            required
            id="id_amount"
            bind:value={amount}
        />
        <p class="text-danger">{errors.amount}</p>
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
            bind:value={description}
        />
        <p class="text-danger">{errors.description}</p>
    </div>

    <div>
        <label class="form-label" for="id_category">category:</label>
        <Select
            hasError={Boolean(errors.category)}
            options={expenseCategories.map((category) => {
                return {
                    selectedDisplay: category.name,
                    optionDisplay: category.name,
                    value: category.slug,
                };
            })}
            placeholder="Select a category"
            bind:selectedValue={category}
        />

        <div class="row">
            <div class="col-6">
                <p class="text-danger">{errors.category} {category}</p>
            </div>
            <div class="col-6 text-end">
                <p>
                    <a
                        class="card-link"
                        href="/expenses/categories/add?next=/expenses/add"
                    >
                        Add new category
                    </a>
                </p>
            </div>
        </div>
    </div>

    <div class="mb-3">
        <label class="form-label" for="id_image">Image:</label>
        <ImageInput bind:imageInput />
    </div>

    <input value="Create" type="submit" class="mt-3 btn btn-primary" />
</form>

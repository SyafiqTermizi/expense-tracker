<script lang="ts">
    export let accountBalances: Account[];
    export let userCurrency = "";
    export let expenseCategories: { name: string; slug: string }[] = [];

    import * as yup from "yup";

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

    function extractErrors(err) {
        return err.inner.reduce((acc, err) => {
            return { ...acc, [err.path]: err.message };
        }, {});
    }

    function submitForm() {
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

    function validateThenSubmit() {
        let schema = yup.object().shape({
            fromAccount: yup.string().label("From Account").required(),
            amount: yup
                .number()
                .label("Amount")
                .required()
                .positive()
                .integer()
                .min(0.01)
                .max(9999999999.99),
            description: yup
                .string()
                .label("Description")
                .min(2)
                .max(255)
                .trim(),
            category: yup.string().required().label("Category"),
        });

        schema
            .validate(
                {
                    fromAccount,
                    amount,
                    description,
                    category,
                },
                { abortEarly: false }
            )
            .then((stuff) => {
                console.log(stuff);
                submitForm();
            })
            .catch((err) => {
                errors = { ...errors, ...extractErrors(err) };
            });

        return false;
    }
</script>

<form class="card-body p-4" method="post" on:submit|preventDefault>
    <div class="mb-3">
        <label for="id_from_account" class="form-label">From Account:</label>
        <Select
            errorMessage={errors.fromAccount}
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

    <div class="mb-3">
        <label class="form-label" for="id_category">Category:</label>
        <Select
            errorMessage={errors.category}
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
        <a
            class="mt-0 mb-3 card-link"
            href="/expenses/categories/add?next=/expenses/add"
        >
            Add new category
        </a>
    </div>

    <div class="mb-3">
        <label class="form-label" for="id_image">Image:</label>
        <ImageInput bind:imageInput />
    </div>

    <input
        value="Create"
        type="submit"
        class="mt-3 btn btn-primary"
        on:click={validateThenSubmit}
    />
</form>

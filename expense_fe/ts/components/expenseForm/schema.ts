import * as yup from "yup";

export const expenseSchema = yup.object().shape({
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
    event: yup
        .string()
        .label("Event")
});

export function extractErrors(err) {
    return err.inner.reduce((acc, err) => {
        return { ...acc, [err.path]: err.message };
    }, {});
}

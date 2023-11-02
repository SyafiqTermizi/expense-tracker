import * as yup from "yup";

export const addFormSchema = yup.object().shape({
    account: yup.string().label("Account").required(),
    amount: yup
        .number()
        .label("Amount")
        .required()
        .positive()
        .min(0.01)
        .max(9999999999.99),
    description: yup
        .string()
        .required()
        .label("Description")
        .min(2)
        .max(255)
        .trim(),
});

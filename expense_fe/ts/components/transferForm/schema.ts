import * as yup from "yup";

export const transferSchema = yup.object().shape({
    fromAccount: yup.string().label("From Account").required(),
    toAccount: yup.string().label("From Account").required(),
    amount: yup
        .number()
        .label("Amount")
        .required()
        .positive()
        .min(0.01)
        .max(9999999999.99),
    description: yup
        .string()
        .nullable()
        .label("Description")
        .min(2)
        .max(255)
        .trim(),
});

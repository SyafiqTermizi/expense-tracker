import * as yup from "yup";

import { getCookie, snakeToCamel } from "../../utils";

export const expenseSchema = yup.object().shape({
    fromAccount: yup.string().label("From Account").required(),
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
    category: yup.string().required().label("Category"),
    event: yup.string().nullable().label("Event")
});

export function extractErrors(err) {
    return err.inner.reduce((acc, err) => {
        return { ...acc, [err.path]: err.message };
    }, {});
}

export function submitFormData(validatedData, fileInputData: FileInputData, errorCB) {
    const formdata = new FormData();

    for (const key in Object.keys(validatedData)) {
        if (validatedData[key]) {
            formdata.append(key, validatedData[key].toString());
        }
    }

    if (fileInputData) {
        formdata.append(
            fileInputData.fieldName,
            fileInputData.file,
            fileInputData.fileName
        );
    }

    const request = new XMLHttpRequest();

    request.open("POST", window.location.href);
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
                    const formattedFieldName = snakeToCamel(fieldName)
                    localErrMsg[formattedFieldName] =
                        serverErrMsg[fieldName][0].message;
                }

                errorCB(localErrMsg);
                break;
            default:
                break;
        }
    };

    request.send(formdata);
}

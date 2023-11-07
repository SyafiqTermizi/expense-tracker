export function isoToLocalDate(isoDate: string) {
    const monthNames = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec"
    ]
    const jsDate = new Date(isoDate);
    return `${jsDate.getDate()} ${monthNames[jsDate.getMonth()]}`;
}

export function getCookie(name: string): string {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }
    return cookieValue;
}

export const snakeToCamel = str =>
    // Convert 🐍 case ➡️ 🐪 case
    str.toLowerCase().replace(/([-_][a-z])/g, group =>
        group
            .toUpperCase()
            .replace('-', '')
            .replace('_', '')
    );

// Convert 🐪 case ➡️ 🐍 case
const camelToSnakeCase = str => str.replace(/[A-Z]/g, letter => `_${letter.toLowerCase()}`);

export function extractErrors(err) {
    return err.inner.reduce((acc, err) => {
        return { ...acc, [err.path]: err.message };
    }, {});
}

export function submitFormData(validatedData, fileInputData: FileInputData, errorCB) {
    const formdata = new FormData();

    for (const key of Object.keys(validatedData)) {

        if (validatedData[key]) {
            formdata.append(camelToSnakeCase(key), validatedData[key].toString());
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

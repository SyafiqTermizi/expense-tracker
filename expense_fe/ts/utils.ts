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

export function submitFormData(
    validatedData,
    fileInputData: FileInputData,
    updateLoadingStatus,
    errorCallBack
) {
    updateLoadingStatus();

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
        updateLoadingStatus();

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
                    const formattedFieldName = fieldName === "__all__" ?
                        fieldName : snakeToCamel(fieldName);
                    localErrMsg[formattedFieldName] =
                        serverErrMsg[fieldName][0].message;
                }

                errorCallBack(localErrMsg);
                break;
            default:
                break;
        }
    };

    request.send(formdata);
}

export const chartColors = [
    "#008FFB",
    "#00E396",
    "#FEB019",
    "#FF4560",
    "#775DD0",
    "#4caf50",
    "#546E7A",
    "#f9a3a4",
    "#F86624",
    "#662E9B",
    "#2E294E",
    "#5A2A27",
    "#D7263D"
]

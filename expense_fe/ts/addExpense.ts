// Set default value for select element

function selectElement(id: string, valueToSelect: string) {
    let element = document.getElementById(id) as HTMLSelectElement;
    element.value = valueToSelect;
}

const queryParams = new URLSearchParams(window.location.search);

const selectedAccount = queryParams.get("account");
if (selectedAccount) {
    selectElement("id_from_account", selectedAccount);
}

const selectedEvent = queryParams.get("event");
if (selectedEvent) {
    selectElement("id_event", selectedEvent);
}

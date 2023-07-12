export function isoToLocalDate(isoDate: string) {
    const monthNames = [
        "January",
        "Feburary",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ]
    const dateArr = new Date(isoDate).toLocaleDateString().split("/");
    const month = monthNames[parseInt(dateArr[0]) - 1];

    return `${dateArr[1]} ${month} ${dateArr[2]}`;
}
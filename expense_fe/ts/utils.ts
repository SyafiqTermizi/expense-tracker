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
    const dateArr = new Date(isoDate).toLocaleDateString().split("/");
    const month = monthNames[parseInt(dateArr[0]) - 1];

    return `${dateArr[1]} ${month}`;
}
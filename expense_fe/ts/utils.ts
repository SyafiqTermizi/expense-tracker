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

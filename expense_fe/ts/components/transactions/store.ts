import { writable, readable, derived } from 'svelte/store';

const transactionData: Transaction[] = JSON.parse(document.getElementById("transaction-data")!.textContent) || [];

const initialTransactions = readable(transactionData, function start(set) {
    return function stop() {
        return []
    }
});

export const showAll = writable(true);
export const keyword = writable("");

export const transactions = derived([showAll, keyword, initialTransactions], ([$showAll, $keyword, $initialTransactions]) => {
    let tempTransactions = [];
    if ($showAll) {
        tempTransactions = $initialTransactions;
    } else {
        tempTransactions = $initialTransactions.filter(transaction => transaction.expense);
    }

    if ($keyword) {
        tempTransactions = tempTransactions.filter(transaction => transaction["description"].toLowerCase().includes($keyword.toLowerCase()));
    }

    return tempTransactions
});

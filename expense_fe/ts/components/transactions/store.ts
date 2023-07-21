import { writable, derived } from 'svelte/store';

export const initialTransactions = writable([]);

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

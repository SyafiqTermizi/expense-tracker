import { writable, derived } from 'svelte/store';

export const initialTransactions = writable([]);
export const showAll = writable(true);
export const keyword = writable("");
export const selectedCategory = writable("");

export const transactions = derived([showAll, initialTransactions, selectedCategory], ([$showAll, $initialTransactions, $selectedCategory]) => {
    let tempTransactions = [];

    if ($showAll) {
        tempTransactions = $initialTransactions;
    } else {
        tempTransactions = $initialTransactions.filter(transaction => transaction.expense);
    }

    if ($selectedCategory) {
        tempTransactions = tempTransactions.filter(transaction => transaction.category == $selectedCategory)
    }
    return tempTransactions;
});

export const expenseCategories = derived([initialTransactions], ([initialTransactions]) => {
    return [...new Set(initialTransactions.map(transaction => transaction.category).filter(Boolean))];
});

export const transactionModalID = writable(0);
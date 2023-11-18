import { writable, derived } from 'svelte/store';

export const initialTransactions = writable([]);
export const activeFilter = writable<FilterType>("transactions");
export const searchKeyword = writable("");
export const selectedCategory = writable("");

export const displayData = derived(
    [activeFilter, initialTransactions, selectedCategory, searchKeyword],
    ([$activeFilter, $initialTransactions, $selectedCategory, $searchKeyword]) => {
        let filteredDisplayData = [];

        if ($activeFilter === "transactions" && $searchKeyword) {
            filteredDisplayData = $initialTransactions.filter(
                transaction => transaction.description.toLowerCase().includes($searchKeyword.toLowerCase())
            );
        } else if ($activeFilter === "transactions" && !$searchKeyword) {
            filteredDisplayData = $initialTransactions;
        } else if ($activeFilter === "expenses" && !$selectedCategory) {
            filteredDisplayData = $initialTransactions.filter(transaction => transaction.expense);
        } else if ($activeFilter === "expenses" && selectedCategory) {
            filteredDisplayData = $initialTransactions.filter(
                transaction => transaction.category == $selectedCategory
            );
        }

        return filteredDisplayData;
    });

export const expenseCategories = derived([initialTransactions], ([initialTransactions]) => {
    return [...new Set(initialTransactions.map(transaction => transaction.category).filter(Boolean))];
});

export const transactionModalID = writable(0);

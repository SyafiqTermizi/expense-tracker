import { writable, derived } from 'svelte/store';

export const initialTransactions = writable<Transaction[]>([]);
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

export const summaryData = derived(
    [initialTransactions],
    ([$initialTransactions]) => {
        const expenses = $initialTransactions.filter(trx => trx.expense)

        const totalExpense = expenses.reduce(
            (accumulator, { amount }) => parseFloat(accumulator.toString()) + parseFloat(amount.toString()),
            0
        );

        const totalExpenseByCategory = {}

        for (const expense of expenses) {
            const currentValue = parseFloat(
                totalExpenseByCategory[expense.category] ?
                    totalExpenseByCategory[expense.category].total :
                    "0.00"
            );
            const expenseAmount = parseFloat(expense.amount.toString());

            const currentTotal = (currentValue + expenseAmount);
            const currentPercent = (currentTotal / totalExpense) * 100;

            totalExpenseByCategory[expense.category] = {
                total: currentTotal,
                percent: currentPercent.toFixed(1)
            };


        }

        // sort the category summary alphabetically
        const orderedtotalExpenseByCategory = Object.keys(totalExpenseByCategory).sort().reduce(
            (obj, key) => {
                obj[key] = totalExpenseByCategory[key];
                return obj;
            },
            {}
        );

        return orderedtotalExpenseByCategory;
    })

export const expenseCategories = derived([initialTransactions], ([initialTransactions]) => {
    return [...new Set(initialTransactions.map(transaction => transaction.category).filter(Boolean))];
});

export const transactionModalID = writable(0);

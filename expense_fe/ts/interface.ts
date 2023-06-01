interface Expense {
    amount: string;
    category: string;
    created_at: string;
    description: string;
    from_action: string;
}

interface AccountActivity {
    expense?: Expense;
    account_type: string;
    created_at: string;
    description: string;
    amount: number;
    action: string;
}

interface AccountBalance {
    [key: string]: number;
}
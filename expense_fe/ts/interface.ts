interface Expense {
    amount: string;
    category: string;
    created_at: string;
    description: string;
    from_action: string;
}

interface AccountActivity {
    expense?: Expense;
    account: string;
    created_at: string;
    description: string;
    amount: number;
    action: string;
}

interface Account {
    name: string;
    balance: number;
    url: string;
}

interface ChartData {
    x: number;
    y: number;
}
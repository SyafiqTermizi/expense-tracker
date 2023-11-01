interface Expense {
    amount: string;
    category: string;
    created_at: string;
    description: string;
    from_action: string;
}

interface Transaction {
    expense?: Expense;
    images?: string[];
    id: string;
    category: string;
    account: string;
    created_at: string;
    description: string;
    amount: number;
    action: string;
    url?: string;
}

interface Account {
    name: string;
    balance: number;
    url: string;
    slug: string;
}

interface ChartData {
    x: string;
    y: number;
}

interface FileInputData {
    fieldName: string;
    file: File;
    fileName: string;
}

export interface TransactionCreate {
  amount: number;
  currency: string;
  transaction_type: 'DEPOSIT' | 'WITHDRAWAL' | 'TRANSFER';
  description?: string;
  recipient_id?: number;
} 
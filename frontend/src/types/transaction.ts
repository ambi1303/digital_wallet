export interface Transaction {
  id: number;
  user_id: number;
  wallet_id: number;
  transaction_type: 'DEPOSIT' | 'WITHDRAWAL' | 'TRANSFER';
  amount: number;
  currency: string;
  description?: string;
  recipient_id?: number;
  is_flagged: boolean;
  flag_reason?: string;
  status: 'PENDING' | 'COMPLETED' | 'FAILED';
  created_at: string;
} 
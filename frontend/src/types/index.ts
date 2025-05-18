export interface User {
  id: number;
  email: string;
  is_active: boolean;
  is_admin: boolean;
  created_at: string;
}

export interface Wallet {
  id: number;
  user_id: number;
  balance: number;
  currency: string;
  is_active: boolean;
  created_at: string;
}

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

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: User;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
}

export interface TransactionCreate {
  amount: number;
  currency: string;
  transaction_type: 'DEPOSIT' | 'WITHDRAWAL' | 'TRANSFER';
  description?: string;
  recipient_id?: number;
} 
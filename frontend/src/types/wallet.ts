export interface Wallet {
  id: number;
  user_id: number;
  balance: number;
  currency: string;
  is_active: boolean;
  created_at: string;
} 
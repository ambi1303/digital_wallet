import api from './api';
import { Wallet, Transaction, TransactionCreate } from '../types';

class WalletService {
  async getWallet(): Promise<Wallet> {
    const response = await api.get<Wallet>('/wallet');
    return response.data;
  }

  async createWallet(userId: number): Promise<Wallet> {
    const response = await api.post<Wallet>('/wallet', { user_id: userId });
    return response.data;
  }

  async getTransactions(): Promise<Transaction[]> {
    const response = await api.get<Transaction[]>('/transactions');
    return response.data;
  }

  async createTransaction(data: TransactionCreate): Promise<Transaction> {
    const response = await api.post<Transaction>('/transactions', data);
    return response.data;
  }

  async getTransactionHistory(): Promise<Transaction[]> {
    const response = await api.get<Transaction[]>('/transactions/history');
    return response.data;
  }

  async deposit(amount: number, currency: string): Promise<Transaction> {
    return this.createTransaction({
      amount,
      currency,
      transaction_type: 'DEPOSIT'
    });
  }

  async withdraw(amount: number, currency: string): Promise<Transaction> {
    return this.createTransaction({
      amount,
      currency,
      transaction_type: 'WITHDRAWAL'
    });
  }

  async transfer(amount: number, currency: string, recipientId: number): Promise<Transaction> {
    return this.createTransaction({
      amount,
      currency,
      transaction_type: 'TRANSFER',
      recipient_id: recipientId
    });
  }
}

export default new WalletService(); 
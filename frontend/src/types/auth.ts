import type { User } from './user';

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: User;
} 
import { User } from './user.model';

export interface LoginRequest {
  email: string;
  password: string;
}

export interface Token {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: User;
}

export interface TokenPayload {
  sub?: number;
  type?: string;
} 
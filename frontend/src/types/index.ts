// types/index.ts
// Definisi TypeScript types untuk seluruh aplikasi frontend

export interface User {
  id: string;
  phone_number: string;
  name: string | null;
  is_active: boolean;
  session_state: string | null;
  created_at: string;
  updated_at: string;
}

export interface Transaction {
  id: string;
  user_id: string;
  phone_number: string;
  transaction_type: "income" | "expense";
  description: string;
  amount: number;
  transaction_date: string;
  created_at: string;
}

export interface Debt {
  id: string;
  user_id: string;
  phone_number: string;
  description: string;
  amount: number;
  status: "unpaid" | "paid";
  due_date: string | null;
  created_at: string;
  updated_at: string;
}

export interface Log {
  id: string;
  phone_number: string;
  message: string;
  response: string;
  created_at: string;
}

export interface DashboardSummary {
  total_users: number;
  active_users_today: number;
  total_transactions_today: number;
  total_income_today: number;
  total_expense_today: number;
  net_profit_today: number;
  total_unpaid_debts: number;
  total_messages_today: number;
  total_income_today_formatted: string;
  total_expense_today_formatted: string;
  net_profit_today_formatted: string;
  total_unpaid_debts_formatted: string;
}

export interface DailyReport {
  report_date: string;
  total_income: number;
  total_expense: number;
  net_profit: number;
  transaction_count: number;
  total_income_formatted: string;
  total_expense_formatted: string;
  net_profit_formatted: string;
}

export interface MonthlyReport {
  year: number;
  month: number;
  month_name: string;
  total_income: number;
  total_expense: number;
  total_debt: number;
  net_profit: number;
  total_income_formatted: string;
  total_expense_formatted: string;
  total_debt_formatted: string;
  net_profit_formatted: string;
  transaction_count: number;
  debt_count: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
  total_pages: number;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface AdminInfo {
  id: string;
  username: string;
  email: string;
  is_active: boolean;
  created_at: string;
}

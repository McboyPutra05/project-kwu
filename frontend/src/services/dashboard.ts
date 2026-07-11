// services/dashboard.ts
import { api } from "@/lib/api";
import {
  DashboardSummary,
  DailyReport,
  MonthlyReport,
  PaginatedResponse,
  Transaction,
  User,
  Debt,
  Log,
} from "@/types";

export const dashboardService = {
  // ── Reports ──────────────────────────────────────────────────
  async getSummary(): Promise<DashboardSummary> {
    return api.get<DashboardSummary>("/api/v1/reports/summary");
  },

  async getDailyReport(phoneNumber: string): Promise<DailyReport> {
    return api.get<DailyReport>(
      `/api/v1/reports/daily?phone_number=${encodeURIComponent(phoneNumber)}`
    );
  },

  async getMonthlyReport(phoneNumber: string): Promise<MonthlyReport> {
    return api.get<MonthlyReport>(
      `/api/v1/reports/monthly?phone_number=${encodeURIComponent(phoneNumber)}`
    );
  },

  // ── Users ─────────────────────────────────────────────────────
  async getUsers(page = 1, limit = 20): Promise<PaginatedResponse<User>> {
    return api.get<PaginatedResponse<User>>(
      `/api/v1/users?page=${page}&limit=${limit}`
    );
  },

  async getUser(userId: string): Promise<User> {
    return api.get<User>(`/api/v1/users/${userId}`);
  },

  // ── Transactions ──────────────────────────────────────────────
  async getTransactions(
    page = 1,
    limit = 20,
    type?: string,
    phoneNumber?: string
  ): Promise<PaginatedResponse<Transaction>> {
    let url = `/api/v1/transactions?page=${page}&limit=${limit}`;
    if (type) url += `&transaction_type=${type}`;
    if (phoneNumber) url += `&phone_number=${encodeURIComponent(phoneNumber)}`;
    return api.get<PaginatedResponse<Transaction>>(url);
  },

  // ── Debts ─────────────────────────────────────────────────────
  async getDebts(
    page = 1,
    limit = 20,
    status?: string,
    phoneNumber?: string
  ): Promise<PaginatedResponse<Debt>> {
    let url = `/api/v1/debts?page=${page}&limit=${limit}`;
    if (status) url += `&status=${status}`;
    if (phoneNumber) url += `&phone_number=${encodeURIComponent(phoneNumber)}`;
    return api.get<PaginatedResponse<Debt>>(url);
  },

  async markDebtAsPaid(debtId: string): Promise<Debt> {
    return api.patch<Debt>(`/api/v1/debts/${debtId}/pay`);
  },

  // ── Logs ─────────────────────────────────────────────────────
  async getLogs(
    page = 1,
    limit = 20,
    phoneNumber?: string
  ): Promise<PaginatedResponse<Log>> {
    let url = `/api/v1/logs?page=${page}&limit=${limit}`;
    if (phoneNumber) url += `&phone_number=${encodeURIComponent(phoneNumber)}`;
    return api.get<PaginatedResponse<Log>>(url);
  },
};

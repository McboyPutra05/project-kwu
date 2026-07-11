"use client";

// src/app/dashboard/page.tsx
import { useEffect, useState } from "react";
import { dashboardService } from "@/services/dashboard";
import { StatsCard } from "@/components/dashboard/StatsCard";
import { Card } from "@/components/ui/card";
import type { DashboardSummary, Transaction, Log } from "@/types";
import { formatDateTimeId, formatRupiah, truncate } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";

export default function DashboardPage() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [recentTransactions, setRecentTransactions] = useState<Transaction[]>([]);
  const [recentLogs, setRecentLogs] = useState<Log[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [summaryData, txData, logsData] = await Promise.all([
          dashboardService.getSummary(),
          dashboardService.getTransactions(1, 5),
          dashboardService.getLogs(1, 5),
        ]);
        setSummary(summaryData);
        setRecentTransactions(txData.items);
        setRecentLogs(logsData.items);
      } catch (err) {
        console.error("Failed to fetch dashboard data:", err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
    // Auto refresh setiap 30 detik
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white">Dashboard</h1>
        <p className="text-slate-400 text-sm mt-1">
          Ringkasan aktivitas FinanceBot UMKM hari ini
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatsCard
          id="stat-total-users"
          title="Total Pengguna"
          value={isLoading ? "..." : String(summary?.total_users ?? 0)}
          subtitle={`${summary?.active_users_today ?? 0} aktif hari ini`}
          icon="👥"
          color="blue"
          isLoading={isLoading}
        />
        <StatsCard
          id="stat-income-today"
          title="Pemasukan Hari Ini"
          value={isLoading ? "..." : (summary?.total_income_today_formatted ?? "Rp 0")}
          subtitle={`${summary?.total_transactions_today ?? 0} transaksi`}
          icon="💰"
          color="green"
          isLoading={isLoading}
        />
        <StatsCard
          id="stat-expense-today"
          title="Pengeluaran Hari Ini"
          value={isLoading ? "..." : (summary?.total_expense_today_formatted ?? "Rp 0")}
          icon="💸"
          color="red"
          isLoading={isLoading}
        />
        <StatsCard
          id="stat-net-profit"
          title="Laba Bersih Hari Ini"
          value={isLoading ? "..." : (summary?.net_profit_today_formatted ?? "Rp 0")}
          icon="📈"
          color="purple"
          isLoading={isLoading}
        />
        <StatsCard
          id="stat-unpaid-debts"
          title="Hutang Belum Lunas"
          value={isLoading ? "..." : (summary?.total_unpaid_debts_formatted ?? "Rp 0")}
          icon="📋"
          color="yellow"
          isLoading={isLoading}
        />
        <StatsCard
          id="stat-messages-today"
          title="Pesan Masuk Hari Ini"
          value={isLoading ? "..." : String(summary?.total_messages_today ?? 0)}
          icon="💬"
          color="blue"
          isLoading={isLoading}
        />
      </div>

      {/* Bottom Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Transactions */}
        <Card className="bg-slate-900/50 border-slate-800 p-5">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-base font-semibold text-white">Transaksi Terbaru</h2>
            <a href="/dashboard/transactions" className="text-xs text-purple-400 hover:text-purple-300">
              Lihat semua →
            </a>
          </div>

          {isLoading ? (
            <div className="space-y-3">
              {[...Array(5)].map((_, i) => (
                <div key={i} className="h-12 bg-slate-800/50 rounded-lg animate-pulse" />
              ))}
            </div>
          ) : recentTransactions.length === 0 ? (
            <p className="text-slate-500 text-sm text-center py-8">Belum ada transaksi</p>
          ) : (
            <div className="space-y-2">
              {recentTransactions.map((tx) => (
                <div
                  key={tx.id}
                  className="flex items-center justify-between p-3 bg-slate-800/30 rounded-xl hover:bg-slate-800/50 transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <span className="text-xl">
                      {tx.transaction_type === "income" ? "💰" : "💸"}
                    </span>
                    <div>
                      <p className="text-sm font-medium text-white leading-tight">
                        {truncate(tx.description, 25)}
                      </p>
                      <p className="text-xs text-slate-500">{tx.phone_number}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className={`text-sm font-semibold ${tx.transaction_type === "income" ? "text-emerald-400" : "text-red-400"}`}>
                      {tx.transaction_type === "income" ? "+" : "-"}{formatRupiah(tx.amount)}
                    </p>
                    <Badge
                      variant="outline"
                      className={`text-xs ${tx.transaction_type === "income" ? "border-emerald-500/30 text-emerald-400" : "border-red-500/30 text-red-400"}`}
                    >
                      {tx.transaction_type === "income" ? "Masuk" : "Keluar"}
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
          )}
        </Card>

        {/* Recent Logs */}
        <Card className="bg-slate-900/50 border-slate-800 p-5">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-base font-semibold text-white">Log Chatbot Terbaru</h2>
            <a href="/dashboard/logs" className="text-xs text-purple-400 hover:text-purple-300">
              Lihat semua →
            </a>
          </div>

          {isLoading ? (
            <div className="space-y-3">
              {[...Array(5)].map((_, i) => (
                <div key={i} className="h-16 bg-slate-800/50 rounded-lg animate-pulse" />
              ))}
            </div>
          ) : recentLogs.length === 0 ? (
            <p className="text-slate-500 text-sm text-center py-8">Belum ada percakapan</p>
          ) : (
            <div className="space-y-2">
              {recentLogs.map((log) => (
                <div
                  key={log.id}
                  className="p-3 bg-slate-800/30 rounded-xl hover:bg-slate-800/50 transition-colors"
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-xs font-medium text-purple-400">{log.phone_number}</span>
                    <span className="text-xs text-slate-500">{formatDateTimeId(log.created_at)}</span>
                  </div>
                  <p className="text-xs text-slate-300">
                    <span className="text-slate-500">User:</span> {truncate(log.message, 40)}
                  </p>
                  <p className="text-xs text-slate-400 mt-0.5">
                    <span className="text-slate-500">Bot:</span> {truncate(log.response, 50)}
                  </p>
                </div>
              ))}
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}

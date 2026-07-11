"use client";

// src/app/dashboard/reports/page.tsx
import { useEffect, useState } from "react";
import { dashboardService } from "@/services/dashboard";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import type { DailyReport, MonthlyReport } from "@/types";
import { formatDateId } from "@/lib/utils";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";

export default function ReportsPage() {
  const [phone, setPhone] = useState("");
  const [dailyReport, setDailyReport] = useState<DailyReport | null>(null);
  const [monthlyReport, setMonthlyReport] = useState<MonthlyReport | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchReports = async () => {
    if (!phone.trim()) return;
    setIsLoading(true);
    setError("");
    try {
      const [daily, monthly] = await Promise.all([
        dashboardService.getDailyReport(phone),
        dashboardService.getMonthlyReport(phone),
      ]);
      setDailyReport(daily);
      setMonthlyReport(monthly);
    } catch (err) {
      setError("Gagal mengambil laporan. Pastikan nomor HP valid.");
    } finally {
      setIsLoading(false);
    }
  };

  // Chart data untuk monthly
  const monthlyChartData = monthlyReport
    ? [
        {
          name: "Pemasukan",
          value: monthlyReport.total_income,
          formatted: monthlyReport.total_income_formatted,
          color: "#10b981",
        },
        {
          name: "Pengeluaran",
          value: monthlyReport.total_expense,
          formatted: monthlyReport.total_expense_formatted,
          color: "#ef4444",
        },
        {
          name: "Hutang",
          value: monthlyReport.total_debt,
          formatted: monthlyReport.total_debt_formatted,
          color: "#f59e0b",
        },
        {
          name: "Laba Bersih",
          value: Math.max(0, monthlyReport.net_profit),
          formatted: monthlyReport.net_profit_formatted,
          color: "#8b5cf6",
        },
      ]
    : [];

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-sm">
          <p className="text-white font-medium">{payload[0].payload.name}</p>
          <p className="text-slate-300">{payload[0].payload.formatted}</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Laporan Keuangan</h1>
        <p className="text-slate-400 text-sm mt-1">
          Lihat laporan harian dan bulanan per pengguna
        </p>
      </div>

      {/* Search by Phone */}
      <Card className="bg-slate-900/50 border-slate-800 p-5">
        <div className="flex gap-4 items-end">
          <div className="flex-1 max-w-xs">
            <Label className="text-slate-300 text-sm mb-2 block">Nomor HP Pengguna</Label>
            <Input
              id="report-phone"
              placeholder="628123456789"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              className="bg-slate-800 border-slate-700 text-white placeholder:text-slate-500"
            />
          </div>
          <button
            onClick={fetchReports}
            disabled={isLoading || !phone.trim()}
            className="px-6 py-2 bg-purple-600 text-white rounded-lg text-sm hover:bg-purple-500 transition-colors disabled:opacity-50"
          >
            {isLoading ? "Memuat..." : "Tampilkan"}
          </button>
        </div>
        {error && <p className="text-red-400 text-sm mt-3">{error}</p>}
      </Card>

      {(dailyReport || monthlyReport) && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Daily Report */}
          {dailyReport && (
            <Card className="bg-slate-900/50 border-slate-800 p-5">
              <h2 className="text-base font-semibold text-white mb-4">
                📅 Laporan Hari Ini
              </h2>
              <div className="space-y-3">
                <div className="flex items-center justify-between py-2 border-b border-slate-800">
                  <span className="text-slate-400 text-sm">💰 Total Pemasukan</span>
                  <span className="text-emerald-400 font-semibold">{dailyReport.total_income_formatted}</span>
                </div>
                <div className="flex items-center justify-between py-2 border-b border-slate-800">
                  <span className="text-slate-400 text-sm">💸 Total Pengeluaran</span>
                  <span className="text-red-400 font-semibold">{dailyReport.total_expense_formatted}</span>
                </div>
                <div className="flex items-center justify-between py-2 border-b border-slate-800">
                  <span className="text-slate-400 text-sm">📈 Laba Bersih</span>
                  <span className={`font-bold ${dailyReport.net_profit >= 0 ? "text-purple-400" : "text-red-400"}`}>
                    {dailyReport.net_profit_formatted}
                  </span>
                </div>
                <div className="flex items-center justify-between py-2">
                  <span className="text-slate-400 text-sm">📝 Total Transaksi</span>
                  <span className="text-white font-medium">{dailyReport.transaction_count}</span>
                </div>
              </div>
            </Card>
          )}

          {/* Monthly Report */}
          {monthlyReport && (
            <Card className="bg-slate-900/50 border-slate-800 p-5">
              <h2 className="text-base font-semibold text-white mb-4">
                🗓️ Laporan {monthlyReport.month_name} {monthlyReport.year}
              </h2>
              <div className="space-y-3">
                <div className="flex items-center justify-between py-2 border-b border-slate-800">
                  <span className="text-slate-400 text-sm">💰 Total Pemasukan</span>
                  <span className="text-emerald-400 font-semibold">{monthlyReport.total_income_formatted}</span>
                </div>
                <div className="flex items-center justify-between py-2 border-b border-slate-800">
                  <span className="text-slate-400 text-sm">💸 Total Pengeluaran</span>
                  <span className="text-red-400 font-semibold">{monthlyReport.total_expense_formatted}</span>
                </div>
                <div className="flex items-center justify-between py-2 border-b border-slate-800">
                  <span className="text-slate-400 text-sm">💳 Hutang Belum Lunas</span>
                  <span className="text-amber-400 font-semibold">{monthlyReport.total_debt_formatted}</span>
                </div>
                <div className="flex items-center justify-between py-2 border-b border-slate-800">
                  <span className="text-slate-400 text-sm">📈 Laba Bersih</span>
                  <span className={`font-bold ${monthlyReport.net_profit >= 0 ? "text-purple-400" : "text-red-400"}`}>
                    {monthlyReport.net_profit_formatted}
                  </span>
                </div>
                <div className="flex items-center justify-between py-2">
                  <span className="text-slate-400 text-sm">📝 Total Transaksi</span>
                  <span className="text-white">{monthlyReport.transaction_count}</span>
                </div>
              </div>
            </Card>
          )}
        </div>
      )}

      {/* Chart */}
      {monthlyChartData.length > 0 && (
        <Card className="bg-slate-900/50 border-slate-800 p-5">
          <h2 className="text-base font-semibold text-white mb-5">
            📊 Grafik Keuangan Bulanan
          </h2>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={monthlyChartData} margin={{ top: 5, right: 20, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="name" tick={{ fill: "#94a3b8", fontSize: 12 }} axisLine={false} />
              <YAxis tick={{ fill: "#94a3b8", fontSize: 12 }} axisLine={false} tickLine={false}
                tickFormatter={(v) => `${(v / 1000).toFixed(0)}rb`} />
              <Tooltip content={<CustomTooltip />} cursor={{ fill: "rgba(255,255,255,0.03)" }} />
              <Bar dataKey="value" radius={[6, 6, 0, 0]}>
                {monthlyChartData.map((entry, i) => (
                  <Cell key={i} fill={entry.color} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </Card>
      )}
    </div>
  );
}

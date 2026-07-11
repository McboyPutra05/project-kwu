"use client";

// src/app/dashboard/debts/page.tsx
import { useEffect, useState } from "react";
import { dashboardService } from "@/services/dashboard";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import type { Debt, PaginatedResponse } from "@/types";
import { formatDateTimeId, formatRupiah } from "@/lib/utils";

export default function DebtsPage() {
  const [data, setData] = useState<PaginatedResponse<Debt> | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [filter, setFilter] = useState<"" | "unpaid" | "paid">("");
  const [markingId, setMarkingId] = useState<string | null>(null);

  const fetchData = async () => {
    setIsLoading(true);
    try {
      const result = await dashboardService.getDebts(page, 20, filter || undefined);
      setData(result);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => { fetchData(); }, [page, filter]);

  const handleMarkPaid = async (debtId: string) => {
    if (markingId) return;
    setMarkingId(debtId);
    try {
      await dashboardService.markDebtAsPaid(debtId);
      await fetchData();
    } catch (err) {
      console.error(err);
    } finally {
      setMarkingId(null);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Hutang</h1>
        <p className="text-slate-400 text-sm mt-1">
          Daftar semua catatan hutang pengguna
        </p>
      </div>

      {/* Filter */}
      <Card className="bg-slate-900/50 border-slate-800 p-4">
        <div className="flex gap-2">
          {(["", "unpaid", "paid"] as const).map((f) => (
            <button
              key={f}
              onClick={() => { setFilter(f); setPage(1); }}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                filter === f
                  ? "bg-purple-600 text-white"
                  : "bg-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              {f === "" ? "Semua" : f === "unpaid" ? "🔴 Belum Lunas" : "✅ Sudah Lunas"}
            </button>
          ))}
        </div>
      </Card>

      {/* Table */}
      <Card className="bg-slate-900/50 border-slate-800 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-slate-800">
                <th className="text-left text-xs font-medium text-slate-500 uppercase tracking-wider px-4 py-3">Deskripsi</th>
                <th className="text-left text-xs font-medium text-slate-500 uppercase tracking-wider px-4 py-3">No. HP</th>
                <th className="text-right text-xs font-medium text-slate-500 uppercase tracking-wider px-4 py-3">Jumlah</th>
                <th className="text-left text-xs font-medium text-slate-500 uppercase tracking-wider px-4 py-3">Status</th>
                <th className="text-left text-xs font-medium text-slate-500 uppercase tracking-wider px-4 py-3">Dicatat</th>
                <th className="text-center text-xs font-medium text-slate-500 uppercase tracking-wider px-4 py-3">Aksi</th>
              </tr>
            </thead>
            <tbody>
              {isLoading ? (
                [...Array(5)].map((_, i) => (
                  <tr key={i} className="border-b border-slate-800/50">
                    {[...Array(6)].map((_, j) => (
                      <td key={j} className="px-4 py-3">
                        <Skeleton className="h-4 bg-slate-800" />
                      </td>
                    ))}
                  </tr>
                ))
              ) : data?.items.length === 0 ? (
                <tr>
                  <td colSpan={6} className="text-center text-slate-500 py-12">
                    Tidak ada hutang ditemukan
                  </td>
                </tr>
              ) : (
                data?.items.map((debt) => (
                  <tr key={debt.id} className="border-b border-slate-800/30 hover:bg-slate-800/20 transition-colors">
                    <td className="px-4 py-3 text-sm text-white font-medium">{debt.description}</td>
                    <td className="px-4 py-3 text-sm text-slate-400">{debt.phone_number}</td>
                    <td className="px-4 py-3 text-sm font-semibold text-amber-400 text-right">
                      {formatRupiah(debt.amount)}
                    </td>
                    <td className="px-4 py-3">
                      <Badge
                        className={debt.status === "paid"
                          ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20"
                          : "bg-red-500/10 text-red-400 border-red-500/20"
                        }
                        variant="outline"
                      >
                        {debt.status === "paid" ? "✅ Lunas" : "🔴 Belum Lunas"}
                      </Badge>
                    </td>
                    <td className="px-4 py-3 text-sm text-slate-400">{formatDateTimeId(debt.created_at)}</td>
                    <td className="px-4 py-3 text-center">
                      {debt.status === "unpaid" && (
                        <button
                          onClick={() => handleMarkPaid(debt.id)}
                          disabled={markingId === debt.id}
                          className="px-3 py-1 bg-emerald-600/20 text-emerald-400 border border-emerald-500/30 rounded-lg text-xs hover:bg-emerald-600/40 transition-colors disabled:opacity-50"
                        >
                          {markingId === debt.id ? "..." : "Tandai Lunas"}
                        </button>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        {data && data.total_pages > 1 && (
          <div className="flex items-center justify-between px-4 py-3 border-t border-slate-800">
            <p className="text-xs text-slate-500">
              {data.total} hutang — Halaman {data.page} dari {data.total_pages}
            </p>
            <div className="flex gap-2">
              <button onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page === 1}
                className="px-3 py-1.5 text-xs bg-slate-800 text-slate-400 rounded-lg disabled:opacity-50 hover:bg-slate-700">
                ← Prev
              </button>
              <button onClick={() => setPage(p => Math.min(data.total_pages, p + 1))} disabled={page === data.total_pages}
                className="px-3 py-1.5 text-xs bg-slate-800 text-slate-400 rounded-lg disabled:opacity-50 hover:bg-slate-700">
                Next →
              </button>
            </div>
          </div>
        )}
      </Card>
    </div>
  );
}

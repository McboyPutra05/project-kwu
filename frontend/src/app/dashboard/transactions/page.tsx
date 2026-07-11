"use client";

// src/app/dashboard/transactions/page.tsx
import { useEffect, useState } from "react";
import { dashboardService } from "@/services/dashboard";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import { Search, ArrowDownRight, ArrowUpRight, Filter, ChevronLeft, ChevronRight } from "lucide-react";
import type { Transaction, PaginatedResponse } from "@/types";
import { formatDateTimeId, formatRupiah } from "@/lib/utils";
import { cn } from "@/lib/utils";

export default function TransactionsPage() {
  const [data, setData] = useState<PaginatedResponse<Transaction> | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [filter, setFilter] = useState<"" | "income" | "expense">("");
  const [search, setSearch] = useState("");

  const fetchData = async () => {
    setIsLoading(true);
    try {
      const result = await dashboardService.getTransactions(
        page,
        20,
        filter || undefined,
        search || undefined
      );
      setData(result);
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [page, filter]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setPage(1);
    fetchData();
  };

  return (
    <div className="space-y-8">
      {/* Header Area */}
      <div>
        <h1 className="text-3xl font-bold text-white tracking-tight">Transaksi</h1>
        <p className="text-slate-400 mt-2 text-sm max-w-2xl">
          Pantau dan kelola seluruh riwayat pemasukan dan pengeluaran UMKM Anda secara real-time.
        </p>
      </div>

      {/* Filters & Actions Area */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 glass rounded-2xl p-2 pl-4 pr-2">
        
        {/* Type Filter (Segmented Control) */}
        <div className="flex items-center gap-1 bg-white/5 p-1 rounded-xl border border-white/10">
          <div className="pl-2 pr-1 flex items-center text-slate-500">
            <Filter className="w-4 h-4" />
          </div>
          {(["", "income", "expense"] as const).map((f) => {
            const labels = {
              "": "Semua",
              "income": "Pemasukan",
              "expense": "Pengeluaran"
            };
            return (
              <button
                key={f}
                onClick={() => { setFilter(f); setPage(1); }}
                className={cn(
                  "px-4 py-1.5 rounded-lg text-sm font-medium transition-all duration-300",
                  filter === f
                    ? "bg-gradient-to-r from-purple-600 to-blue-600 text-white shadow-lg"
                    : "text-slate-400 hover:text-white hover:bg-white/5"
                )}
              >
                {labels[f]}
              </button>
            );
          })}
        </div>

        {/* Search Bar */}
        <form onSubmit={handleSearch} className="flex gap-2 w-full sm:w-auto">
          <div className="relative w-full sm:w-64 group">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500 group-focus-within:text-purple-400 transition-colors" />
            <Input
              id="search-phone"
              placeholder="Cari nomor HP..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="bg-slate-900/50 border-white/10 text-white pl-10 h-10 rounded-xl focus:border-purple-500 focus:ring-purple-500/20 w-full placeholder:text-slate-600"
            />
          </div>
          <button
            type="submit"
            className="px-4 py-2 bg-white/5 hover:bg-white/10 border border-white/10 text-white rounded-xl text-sm font-medium transition-all duration-300"
          >
            Cari
          </button>
        </form>
      </div>

      {/* Main Table */}
      <div className="glass rounded-3xl overflow-hidden border border-white/10 shadow-2xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-white/5 bg-white/[0.02]">
                <th className="px-6 py-4 text-xs font-semibold text-slate-400 uppercase tracking-wider">Deskripsi</th>
                <th className="px-6 py-4 text-xs font-semibold text-slate-400 uppercase tracking-wider">No. HP</th>
                <th className="px-6 py-4 text-xs font-semibold text-slate-400 uppercase tracking-wider">Tipe</th>
                <th className="px-6 py-4 text-xs font-semibold text-slate-400 uppercase tracking-wider text-right">Jumlah</th>
                <th className="px-6 py-4 text-xs font-semibold text-slate-400 uppercase tracking-wider">Tanggal</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              {isLoading ? (
                [...Array(5)].map((_, i) => (
                  <tr key={i}>
                    {[...Array(5)].map((_, j) => (
                      <td key={j} className="px-6 py-4">
                        <Skeleton className="h-5 w-full bg-white/5 rounded" />
                      </td>
                    ))}
                  </tr>
                ))
              ) : data?.items.length === 0 ? (
                <tr>
                  <td colSpan={5} className="text-center text-slate-500 py-16">
                    <div className="flex flex-col items-center justify-center">
                      <div className="w-16 h-16 bg-white/5 rounded-full flex items-center justify-center mb-4">
                        <Search className="w-8 h-8 text-slate-600" />
                      </div>
                      <p className="text-lg font-medium text-slate-400">Tidak ada transaksi ditemukan</p>
                      <p className="text-sm text-slate-500 mt-1">Coba sesuaikan filter atau pencarian Anda.</p>
                    </div>
                  </td>
                </tr>
              ) : (
                data?.items.map((tx) => {
                  const isIncome = tx.transaction_type === "income";
                  return (
                    <tr 
                      key={tx.id} 
                      className="group hover:bg-white/[0.02] transition-colors duration-200"
                    >
                      <td className="px-6 py-4">
                        <p className="text-sm font-medium text-slate-200 group-hover:text-white transition-colors">{tx.description}</p>
                      </td>
                      <td className="px-6 py-4">
                        <span className="text-sm text-slate-400 font-mono bg-slate-900/50 px-2 py-1 rounded-md border border-white/5">{tx.phone_number}</span>
                      </td>
                      <td className="px-6 py-4">
                        <div className={cn(
                          "inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium border",
                          isIncome 
                            ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20" 
                            : "bg-red-500/10 text-red-400 border-red-500/20"
                        )}>
                          {isIncome ? <ArrowDownRight className="w-3.5 h-3.5" /> : <ArrowUpRight className="w-3.5 h-3.5" />}
                          {isIncome ? "Pemasukan" : "Pengeluaran"}
                        </div>
                      </td>
                      <td className={cn(
                        "px-6 py-4 text-sm font-bold text-right tracking-tight",
                        isIncome ? "text-emerald-400" : "text-red-400"
                      )}>
                        {isIncome ? "+" : "-"}{formatRupiah(tx.amount)}
                      </td>
                      <td className="px-6 py-4 text-sm text-slate-400">
                        {formatDateTimeId(tx.transaction_date)}
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination Footer */}
        {data && data.total_pages > 1 && (
          <div className="flex items-center justify-between px-6 py-4 bg-black/20 border-t border-white/5">
            <p className="text-sm text-slate-400 font-medium">
              Total <span className="text-white">{data.total}</span> transaksi
            </p>
            <div className="flex items-center gap-3">
              <span className="text-sm text-slate-500">Halaman {data.page} dari {data.total_pages}</span>
              <div className="flex gap-2">
                <button
                  onClick={() => setPage(p => Math.max(1, p - 1))}
                  disabled={page === 1}
                  className="p-2 bg-white/5 border border-white/10 text-slate-300 rounded-lg hover:bg-white/10 hover:text-white disabled:opacity-30 disabled:hover:bg-white/5 disabled:hover:text-slate-300 transition-all"
                >
                  <ChevronLeft className="w-4 h-4" />
                </button>
                <button
                  onClick={() => setPage(p => Math.min(data.total_pages, p + 1))}
                  disabled={page === data.total_pages}
                  className="p-2 bg-white/5 border border-white/10 text-slate-300 rounded-lg hover:bg-white/10 hover:text-white disabled:opacity-30 disabled:hover:bg-white/5 disabled:hover:text-slate-300 transition-all"
                >
                  <ChevronRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

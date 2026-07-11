"use client";

// src/app/dashboard/users/page.tsx
import { useEffect, useState } from "react";
import { dashboardService } from "@/services/dashboard";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import type { User, PaginatedResponse } from "@/types";
import { formatDateId } from "@/lib/utils";

export default function UsersPage() {
  const [data, setData] = useState<PaginatedResponse<User> | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [page, setPage] = useState(1);

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      try {
        const result = await dashboardService.getUsers(page, 20);
        setData(result);
      } finally {
        setIsLoading(false);
      }
    };
    fetchData();
  }, [page]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Pengguna</h1>
          <p className="text-slate-400 text-sm mt-1">
            Daftar pengguna yang terdaftar di chatbot
          </p>
        </div>
        {data && (
          <div className="bg-slate-800 border border-slate-700 rounded-xl px-4 py-2 text-center">
            <p className="text-2xl font-bold text-white">{data.total}</p>
            <p className="text-xs text-slate-400">Total User</p>
          </div>
        )}
      </div>

      <Card className="bg-slate-900/50 border-slate-800 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-slate-800">
                <th className="text-left text-xs font-medium text-slate-500 uppercase tracking-wider px-4 py-3">Pengguna</th>
                <th className="text-left text-xs font-medium text-slate-500 uppercase tracking-wider px-4 py-3">No. HP</th>
                <th className="text-left text-xs font-medium text-slate-500 uppercase tracking-wider px-4 py-3">Status</th>
                <th className="text-left text-xs font-medium text-slate-500 uppercase tracking-wider px-4 py-3">State Bot</th>
                <th className="text-left text-xs font-medium text-slate-500 uppercase tracking-wider px-4 py-3">Bergabung</th>
              </tr>
            </thead>
            <tbody>
              {isLoading ? (
                [...Array(5)].map((_, i) => (
                  <tr key={i} className="border-b border-slate-800/50">
                    {[...Array(5)].map((_, j) => (
                      <td key={j} className="px-4 py-3">
                        <Skeleton className="h-4 bg-slate-800" />
                      </td>
                    ))}
                  </tr>
                ))
              ) : data?.items.length === 0 ? (
                <tr>
                  <td colSpan={5} className="text-center text-slate-500 py-12">
                    Belum ada pengguna terdaftar
                  </td>
                </tr>
              ) : (
                data?.items.map((user) => (
                  <tr key={user.id} className="border-b border-slate-800/30 hover:bg-slate-800/20 transition-colors">
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 bg-purple-600/20 rounded-full flex items-center justify-center text-sm border border-purple-500/20">
                          {user.name ? user.name[0].toUpperCase() : "?"}
                        </div>
                        <span className="text-sm font-medium text-white">
                          {user.name ?? <span className="text-slate-500 italic">Belum set</span>}
                        </span>
                      </div>
                    </td>
                    <td className="px-4 py-3 text-sm text-slate-400 font-mono">{user.phone_number}</td>
                    <td className="px-4 py-3">
                      <Badge
                        variant="outline"
                        className={user.is_active
                          ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20"
                          : "bg-slate-500/10 text-slate-400 border-slate-500/20"
                        }
                      >
                        {user.is_active ? "Aktif" : "Nonaktif"}
                      </Badge>
                    </td>
                    <td className="px-4 py-3">
                      <span className="text-xs font-mono text-slate-400 bg-slate-800 px-2 py-1 rounded">
                        {user.session_state ?? "idle"}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-sm text-slate-400">{formatDateId(user.created_at)}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {data && data.total_pages > 1 && (
          <div className="flex items-center justify-between px-4 py-3 border-t border-slate-800">
            <p className="text-xs text-slate-500">
              {data.total} pengguna — Halaman {data.page} dari {data.total_pages}
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

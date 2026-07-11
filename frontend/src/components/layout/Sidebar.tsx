"use client";

// src/components/layout/Sidebar.tsx
import Link from "next/link";
import { usePathname } from "next/navigation";
import { authService } from "@/services/auth";
import { cn } from "@/lib/utils";
import { 
  LayoutDashboard, 
  ArrowRightLeft, 
  Receipt, 
  LineChart, 
  Users, 
  MessageSquare,
  LogOut,
  WalletCards
} from "lucide-react";

const navItems = [
  {
    href: "/dashboard",
    icon: LayoutDashboard,
    label: "Dashboard",
    id: "nav-dashboard",
  },
  {
    href: "/dashboard/transactions",
    icon: ArrowRightLeft,
    label: "Transaksi",
    id: "nav-transactions",
  },
  {
    href: "/dashboard/debts",
    icon: Receipt,
    label: "Hutang",
    id: "nav-debts",
  },
  {
    href: "/dashboard/reports",
    icon: LineChart,
    label: "Laporan",
    id: "nav-reports",
  },
  {
    href: "/dashboard/users",
    icon: Users,
    label: "Pengguna",
    id: "nav-users",
  },
  {
    href: "/dashboard/logs",
    icon: MessageSquare,
    label: "Log Chatbot",
    id: "nav-logs",
  },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed inset-y-0 left-0 w-64 bg-slate-950/80 backdrop-blur-2xl flex flex-col z-50 border-r border-white/5">
      {/* Logo Area */}
      <div className="h-20 flex items-center px-6 border-b border-white/5 bg-gradient-to-b from-white/[0.02] to-transparent">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-purple-600 to-blue-600 rounded-xl flex items-center justify-center shadow-lg shadow-purple-500/20">
            <WalletCards className="w-5 h-5 text-white" />
          </div>
          <div>
            <p className="text-white font-bold text-[15px] tracking-wide leading-tight">FinanceBot</p>
            <p className="text-purple-400/80 text-[11px] uppercase tracking-wider font-semibold">UMKM Admin</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-6 space-y-2 overflow-y-auto">
        <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-4 px-2">Menu Utama</div>
        
        {navItems.map((item) => {
          const isActive =
            item.href === "/dashboard"
              ? pathname === "/dashboard"
              : pathname.startsWith(item.href);
              
          const Icon = item.icon;

          return (
            <Link
              key={item.href}
              id={item.id}
              href={item.href}
              className={cn(
                "group flex items-center gap-3 px-3 py-3 rounded-xl text-sm font-medium transition-all duration-300 relative overflow-hidden",
                isActive
                  ? "text-white"
                  : "text-slate-400 hover:text-white"
              )}
            >
              {/* Active Background & Glow */}
              {isActive && (
                <>
                  <div className="absolute inset-0 bg-gradient-to-r from-purple-600/20 to-blue-600/10" />
                  <div className="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-purple-500 to-blue-500 rounded-r-full shadow-[0_0_10px_rgba(168,85,247,0.5)]" />
                </>
              )}
              
              {/* Hover Background */}
              {!isActive && (
                <div className="absolute inset-0 bg-white/5 opacity-0 group-hover:opacity-100 transition-opacity" />
              )}
              
              <Icon className={cn(
                "w-5 h-5 relative z-10 transition-colors duration-300",
                isActive ? "text-purple-400" : "text-slate-500 group-hover:text-purple-400"
              )} />
              <span className="relative z-10">{item.label}</span>
            </Link>
          );
        })}
      </nav>

      {/* Bottom Area */}
      <div className="p-4 border-t border-white/5 bg-gradient-to-t from-white/[0.02] to-transparent">
        <button
          id="btn-logout"
          onClick={() => authService.logout()}
          className="group w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-slate-400 hover:text-white transition-all duration-300 relative overflow-hidden"
        >
          <div className="absolute inset-0 bg-red-500/10 opacity-0 group-hover:opacity-100 transition-opacity" />
          <LogOut className="w-5 h-5 relative z-10 text-slate-500 group-hover:text-red-400 transition-colors" />
          <span className="relative z-10">Keluar Sistem</span>
        </button>
      </div>
    </aside>
  );
}

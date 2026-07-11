// src/components/dashboard/StatsCard.tsx
import { Card } from "@/components/ui/card";
import { cn } from "@/lib/utils";

interface StatsCardProps {
  id?: string;
  title: string;
  value: string;
  subtitle?: string;
  icon: string;
  trend?: "up" | "down" | "neutral";
  color?: "purple" | "green" | "red" | "yellow" | "blue";
  isLoading?: boolean;
}

const colorMap = {
  purple: "from-purple-500/20 to-purple-600/10 border-purple-500/20 text-purple-400",
  green: "from-emerald-500/20 to-emerald-600/10 border-emerald-500/20 text-emerald-400",
  red: "from-red-500/20 to-red-600/10 border-red-500/20 text-red-400",
  yellow: "from-amber-500/20 to-amber-600/10 border-amber-500/20 text-amber-400",
  blue: "from-blue-500/20 to-blue-600/10 border-blue-500/20 text-blue-400",
};

export function StatsCard({
  id,
  title,
  value,
  subtitle,
  icon,
  trend,
  color = "purple",
  isLoading = false,
}: StatsCardProps) {
  return (
    <Card
      id={id}
      className={cn(
        "relative overflow-hidden bg-gradient-to-br border p-5 transition-all duration-200 hover:scale-[1.02] hover:shadow-lg",
        colorMap[color]
      )}
    >
      {/* Background decoration */}
      <div className="absolute top-0 right-0 w-24 h-24 opacity-10">
        <div className="text-6xl translate-x-4 -translate-y-2">{icon}</div>
      </div>

      {isLoading ? (
        <div className="space-y-2 animate-pulse">
          <div className="h-4 bg-white/10 rounded w-3/4" />
          <div className="h-8 bg-white/10 rounded w-1/2" />
          <div className="h-3 bg-white/10 rounded w-2/3" />
        </div>
      ) : (
        <>
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <p className="text-xs font-medium text-slate-400 uppercase tracking-wider mb-1">
                {title}
              </p>
              <p className="text-2xl font-bold text-white leading-tight mb-1">
                {value}
              </p>
              {subtitle && (
                <p className="text-xs text-slate-400">{subtitle}</p>
              )}
            </div>

            <div className={cn("text-2xl", colorMap[color].split(" ")[3])}>
              {icon}
            </div>
          </div>

          {trend && (
            <div className="mt-3 flex items-center gap-1 text-xs">
              {trend === "up" && <span className="text-emerald-400">↑ Naik</span>}
              {trend === "down" && <span className="text-red-400">↓ Turun</span>}
              {trend === "neutral" && <span className="text-slate-400">→ Stabil</span>}
              <span className="text-slate-500">dari kemarin</span>
            </div>
          )}
        </>
      )}
    </Card>
  );
}

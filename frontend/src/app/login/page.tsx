"use client";

// src/app/login/page.tsx
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { authService } from "@/services/auth";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { WalletCards, ArrowRight, Loader2, Lock, User } from "lucide-react";

export default function LoginPage() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      await authService.login({ username, password });
      router.push("/dashboard");
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Login gagal");
    } finally {
      setIsLoading(false);
    }
  };

  if (!isMounted) return null;

  return (
    <div className="relative min-h-screen flex items-center justify-center overflow-hidden bg-slate-950">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 w-full h-full pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-purple-600/30 rounded-full blur-[120px] animate-blob" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-blue-600/30 rounded-full blur-[120px] animate-blob" style={{ animationDelay: '2s' }} />
        <div className="absolute top-[40%] left-[60%] w-[30%] h-[30%] bg-indigo-500/20 rounded-full blur-[100px] animate-blob" style={{ animationDelay: '4s' }} />
      </div>

      <div className="relative z-10 w-full max-w-[1000px] mx-4 flex rounded-3xl overflow-hidden glass shadow-2xl animate-in fade-in zoom-in duration-700">
        
        {/* Left Side: Branding / Intro (Hidden on mobile) */}
        <div className="hidden md:flex flex-col justify-between w-1/2 p-12 bg-gradient-to-br from-purple-900/40 to-blue-900/40 border-r border-white/5 relative overflow-hidden">
          <div className="absolute inset-0 bg-black/20" />
          <div className="relative z-10">
            <div className="inline-flex items-center justify-center w-14 h-14 bg-white/10 rounded-2xl border border-white/20 mb-8 backdrop-blur-md">
              <WalletCards className="w-8 h-8 text-purple-300" />
            </div>
            <h1 className="text-4xl font-bold text-white mb-4 leading-tight">
              Kendalikan<br/>Keuangan UMKM<br/>Anda.
            </h1>
            <p className="text-slate-300 text-lg max-w-sm">
              Dashboard pintar untuk memonitor pemasukan, pengeluaran, dan laporan secara real-time.
            </p>
          </div>
          
          <div className="relative z-10">
            <div className="flex items-center gap-3 bg-white/5 p-4 rounded-2xl border border-white/10 backdrop-blur-sm w-fit">
              <div className="flex -space-x-3">
                {[1, 2, 3].map((i) => (
                  <div key={i} className={`w-8 h-8 rounded-full border-2 border-slate-900 bg-gradient-to-tr from-purple-500 to-blue-500`} />
                ))}
              </div>
              <p className="text-sm text-slate-300 font-medium">Dipercaya ratusan pengguna</p>
            </div>
          </div>
        </div>

        {/* Right Side: Login Form */}
        <div className="w-full md:w-1/2 p-8 md:p-12 bg-slate-950/50 backdrop-blur-xl">
          <div className="max-w-sm mx-auto">
            <div className="md:hidden flex flex-col items-center mb-8">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-purple-600/20 rounded-2xl border border-purple-500/30 mb-4">
                <WalletCards className="w-8 h-8 text-purple-400" />
              </div>
              <h1 className="text-2xl font-bold text-white">FinanceBot</h1>
            </div>

            <div className="mb-10">
              <h2 className="text-2xl font-bold text-white mb-2">Selamat Datang 👋</h2>
              <p className="text-slate-400">Silakan masuk ke akun admin Anda.</p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-6">
              {error && (
                <div className="bg-red-500/10 border border-red-500/20 rounded-xl p-4 text-red-400 text-sm flex items-start gap-3 animate-in slide-in-from-top-2">
                  <span className="text-lg">⚠️</span>
                  <p className="pt-0.5">{error}</p>
                </div>
              )}

              <div className="space-y-4">
                <div className="space-y-2 relative group">
                  <Label htmlFor="username" className="text-slate-300 text-sm font-medium ml-1">Username</Label>
                  <div className="relative">
                    <User className="absolute left-3.5 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500 group-focus-within:text-purple-400 transition-colors" />
                    <Input
                      id="username"
                      type="text"
                      placeholder="Masukkan username"
                      value={username}
                      onChange={(e) => setUsername(e.target.value)}
                      required
                      className="bg-white/5 border-white/10 text-white pl-11 h-12 rounded-xl focus:border-purple-500 focus:ring-purple-500/20 transition-all placeholder:text-slate-600"
                    />
                  </div>
                </div>

                <div className="space-y-2 relative group">
                  <div className="flex justify-between items-center ml-1">
                    <Label htmlFor="password" className="text-slate-300 text-sm font-medium">Password</Label>
                  </div>
                  <div className="relative">
                    <Lock className="absolute left-3.5 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500 group-focus-within:text-purple-400 transition-colors" />
                    <Input
                      id="password"
                      type="password"
                      placeholder="••••••••"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      required
                      className="bg-white/5 border-white/10 text-white pl-11 h-12 rounded-xl focus:border-purple-500 focus:ring-purple-500/20 transition-all placeholder:text-slate-600 tracking-widest"
                    />
                  </div>
                </div>
              </div>

              <Button
                type="submit"
                disabled={isLoading}
                className="w-full h-12 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 text-white font-semibold rounded-xl transition-all duration-300 hover:shadow-[0_0_20px_rgba(168,85,247,0.4)] group"
              >
                {isLoading ? (
                  <span className="flex items-center gap-2">
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Memproses...
                  </span>
                ) : (
                  <span className="flex items-center gap-2">
                    Masuk ke Dashboard
                    <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                  </span>
                )}
              </Button>
            </form>

            <div className="mt-10 pt-6 border-t border-white/5 text-center">
              <p className="text-slate-500 text-xs">
                FinanceBot UMKM v1.0.0 &copy; {new Date().getFullYear()}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

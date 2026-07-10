export default function Footer() {
  return (
    <footer className="bg-darkSlate border-t border-slate-800 py-12">
      <div className="max-w-7xl mx-auto px-6 lg:px-8 flex flex-col md:flex-row justify-between items-center gap-6">
        <div className="text-center md:text-left">
          <span className="text-2xl font-black tracking-tight text-white italic">Finance<span className="text-primary">Bot</span></span>
          <p className="text-slate-500 text-sm mt-2">Solusi pencatatan keuangan UMKM masa kini.</p>
        </div>
        <div className="flex gap-6">
          <a href="#" className="text-slate-400 hover:text-white transition-colors text-sm">Kebijakan Privasi</a>
          <a href="#" className="text-slate-400 hover:text-white transition-colors text-sm">Syarat & Ketentuan</a>
        </div>
        <div className="text-slate-500 text-sm">
          &copy; {new Date().getFullYear()} FinanceBot UMKM. All rights reserved.
        </div>
      </div>
    </footer>
  );
}

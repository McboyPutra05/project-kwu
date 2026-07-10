export default function Pricing() {
  return (
    <div id="pricing" className="py-24 bg-lightGray relative overflow-hidden">
      {/* Decorative Background */}
      <div className="absolute top-0 right-0 -mt-20 -mr-20 w-80 h-80 bg-blue-50 rounded-full blur-3xl opacity-50"></div>
      
      <div className="max-w-7xl mx-auto px-6 lg:px-8 relative z-10">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <h2 className="text-3xl md:text-4xl font-extrabold text-slate-900 mb-4">Pilih Paket Sesuai Kebutuhan Anda</h2>
          <p className="text-lg text-slate-500">
            Mulai dari pencatatan harian sederhana hingga fitur analisis bisnis lanjutan. Tidak ada biaya tersembunyi.
          </p>
        </div>

        <div className="flex flex-col lg:flex-row justify-center gap-8 max-w-5xl mx-auto">
          
          {/* Sederhana Plan */}
          <div className="flex-1 bg-white rounded-3xl p-8 shadow-sm border border-slate-200 flex flex-col hover:shadow-xl transition-shadow">
            <h3 className="text-2xl font-bold text-slate-900 mb-2">Paket Sederhana</h3>
            <p className="text-slate-500 text-sm mb-6">Sangat cocok untuk usaha kecil atau personal yang baru memulai digitalisasi.</p>
            <div className="mb-6 flex items-baseline gap-1">
              <span className="text-4xl font-extrabold text-slate-900">Rp 180.000</span>
              <span className="text-slate-500 font-medium">/ tahun</span>
            </div>
            
            <a href="#" className="w-full bg-blue-50 text-primary hover:bg-blue-100 py-3 rounded-full font-bold transition-colors text-center mb-8">
              Pilih Paket Ini
            </a>
            
            <ul className="space-y-4 flex-1">
              <li className="flex gap-3 text-slate-600 text-sm">
                <svg className="w-5 h-5 text-green-500 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                Pencatatan Pemasukan & Pengeluaran
              </li>
              <li className="flex gap-3 text-slate-600 text-sm">
                <svg className="w-5 h-5 text-green-500 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                Laporan Harian (Excel)
              </li>
              <li className="flex gap-3 text-slate-600 text-sm">
                <svg className="w-5 h-5 text-green-500 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                Manajemen Maksimal 50 Transaksi / Bulan
              </li>
              <li className="flex gap-3 text-slate-400 text-sm">
                <svg className="w-5 h-5 text-slate-300 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
                Manajemen Hutang / Piutang
              </li>
            </ul>
          </div>
          
          {/* Bisnis Plan */}
          <div className="flex-1 bg-darkSlate rounded-3xl p-8 shadow-2xl border border-slate-700 flex flex-col relative transform lg:-translate-y-4">
            <div className="absolute top-0 right-8 transform -translate-y-1/2">
              <span className="bg-gradient-to-r from-blue-500 to-indigo-500 text-white text-xs font-bold uppercase tracking-wider py-1 px-3 rounded-full shadow-lg">
                Paling Laris
              </span>
            </div>
            <h3 className="text-2xl font-bold text-white mb-2">Paket Bisnis</h3>
            <p className="text-slate-400 text-sm mb-6">Fitur lengkap untuk bisnis berkembang yang butuh pencatatan tiada henti.</p>
            <div className="mb-6 flex items-baseline gap-1">
              <span className="text-4xl font-extrabold text-white">Rp 1.200.000</span>
              <span className="text-slate-400 font-medium">/ tahun</span>
            </div>
            
            <a href="#" className="w-full bg-primary hover:bg-primaryHover text-white py-3 rounded-full font-bold transition-colors text-center mb-8 shadow-lg shadow-primary/30">
              Pilih Paket Bisnis
            </a>
            
            <ul className="space-y-4 flex-1">
              <li className="flex gap-3 text-slate-300 text-sm">
                <svg className="w-5 h-5 text-primary flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                Semua fitur di Paket Sederhana
              </li>
              <li className="flex gap-3 text-slate-300 text-sm">
                <svg className="w-5 h-5 text-primary flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                Transaksi Tak Terbatas (Unlimited)
              </li>
              <li className="flex gap-3 text-slate-300 text-sm">
                <svg className="w-5 h-5 text-primary flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                Pencatatan Hutang & Piutang Pelanggan
              </li>
              <li className="flex gap-3 text-slate-300 text-sm">
                <svg className="w-5 h-5 text-primary flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                Laporan Komprehensif (Bulanan & Tahunan)
              </li>
              <li className="flex gap-3 text-slate-300 text-sm">
                <svg className="w-5 h-5 text-primary flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                Prioritas Support 24/7
              </li>
            </ul>
          </div>
          
        </div>
      </div>
    </div>
  );
}

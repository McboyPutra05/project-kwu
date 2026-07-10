const features = [
  {
    title: 'Pencatatan Otomatis',
    description: 'Catat pemasukan dan pengeluaran harian hanya dengan mengirim pesan singkat ke bot WhatsApp.',
    icon: (
      <svg className="w-6 h-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
    ),
    bgColor: 'bg-blue-100'
  },
  {
    title: 'Manajemen Hutang',
    description: 'Kelola hutang dan piutang pelanggan dengan rapi tanpa perlu mengingat manual.',
    icon: (
      <svg className="w-6 h-6 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    ),
    bgColor: 'bg-purple-100'
  },
  {
    title: 'Laporan Finansial',
    description: 'Dapatkan rekapitulasi keuangan Anda dalam format file Excel secara instan kapan saja.',
    icon: (
      <svg className="w-6 h-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
    ),
    bgColor: 'bg-green-100'
  },
  {
    title: 'Akses 24/7',
    description: 'FinanceBot selalu aktif. Catat pengeluaran jam berapa pun dari smartphone Anda tanpa batasan.',
    icon: (
      <svg className="w-6 h-6 text-orange-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    ),
    bgColor: 'bg-orange-100'
  }
];

export default function Features() {
  return (
    <div id="features" className="py-24 bg-darkSlate">
      <div className="max-w-7xl mx-auto px-6 lg:px-8 flex flex-col lg:flex-row gap-16 items-center">
        
        {/* Left Side: Text */}
        <div className="w-full lg:w-5/12 text-center lg:text-left">
          <div className="inline-flex items-center px-3 py-1 rounded border border-slate-700 bg-slate-800 text-slate-300 text-xs font-bold tracking-widest uppercase mb-6">
            Features
          </div>
          <h2 className="text-4xl md:text-5xl font-bold text-white leading-tight mb-6">
            Best Feature We<br className="hidden lg:block"/> Offer For You
          </h2>
          <p className="text-slate-400 text-lg leading-relaxed mb-8">
            FinanceBot menawarkan pengalaman pencatatan keuangan UMKM yang sangat kaya fitur namun tetap ramah pengguna, langsung dari WhatsApp Anda.
          </p>
          <a href="#" className="inline-flex bg-primary hover:bg-primaryHover text-white px-8 py-3.5 rounded-full text-base font-semibold transition-colors">
            Learn More
          </a>
        </div>
        
        {/* Right Side: Grid Cards */}
        <div className="w-full lg:w-7/12">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 relative">
            {features.map((feat, idx) => (
              <div 
                key={idx} 
                className={`bg-white rounded-3xl p-8 shadow-xl hover:shadow-2xl hover:-translate-y-1 transition-all duration-300 ${idx === 1 || idx === 3 ? 'sm:translate-y-8' : ''}`}
              >
                <div className={`w-12 h-12 ${feat.bgColor} rounded-xl flex items-center justify-center mb-6`}>
                  {feat.icon}
                </div>
                <h3 className="text-lg font-bold text-slate-900 mb-3">{feat.title}</h3>
                <p className="text-sm text-slate-500 leading-relaxed">
                  {feat.description}
                </p>
              </div>
            ))}
          </div>
        </div>
        
      </div>
    </div>
  );
}

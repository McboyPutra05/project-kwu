export default function Hero() {
  return (
    <div className="relative pt-32 pb-20 lg:pt-48 lg:pb-32 overflow-hidden bg-lightGray">
      <div className="max-w-7xl mx-auto px-6 lg:px-8 relative z-10 flex flex-col lg:flex-row items-center gap-12 lg:gap-8">
        
        {/* Left Side: Text */}
        <div className="flex-1 text-center lg:text-left">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-yellow-50 text-yellow-800 text-xs font-bold tracking-wider uppercase mb-6 shadow-sm border border-yellow-100">
            <span className="text-yellow-500">⚡</span> Kelola Bisnis Lebih Mudah
          </div>
          
          <h1 className="text-5xl md:text-6xl lg:text-7xl font-extrabold tracking-tight text-slate-900 mb-6 leading-[1.1]">
            Catat dan Analisis <br className="hidden md:block"/>
            Keuangan <span className="text-primary">UMKM</span>
          </h1>
          
          <p className="mt-4 text-lg md:text-xl text-slate-600 max-w-2xl mx-auto lg:mx-0 mb-10 leading-relaxed">
            Tidak perlu install aplikasi tambahan. Cukup gunakan WhatsApp untuk mencatat pengeluaran, pemasukan, hingga hutang harian secara otomatis dan praktis.
          </p>
          
          <div className="flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-4">
            <a href="#" className="w-full sm:w-auto bg-primary hover:bg-primaryHover text-white px-8 py-4 rounded-full text-base font-semibold transition-all duration-300 shadow-lg shadow-primary/30 flex items-center justify-center gap-2">
              Mulai Sekarang
            </a>
            <a href="#features" className="w-full sm:w-auto bg-white hover:bg-gray-50 text-slate-700 border border-slate-200 px-8 py-4 rounded-full text-base font-semibold transition-all duration-300 flex items-center justify-center gap-2 shadow-sm">
              <svg className="w-5 h-5 text-primary" fill="currentColor" viewBox="0 0 20 20"><path d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clipRule="evenodd" fillRule="evenodd"></path></svg>
              Lihat Demo
            </a>
          </div>
        </div>

        {/* Right Side: CSS Phone Mockup */}
        <div className="flex-1 flex justify-center lg:justify-end relative w-full mt-12 lg:mt-0 perspective-1000">
          {/* Decorative Blob Behind Phone */}
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-primary/20 rounded-full mix-blend-multiply filter blur-[80px] opacity-70"></div>
          
          <div className="relative mx-auto border-gray-800 dark:border-gray-800 bg-gray-800 border-[14px] rounded-[2.5rem] h-[600px] w-[300px] shadow-2xl transform rotate-y-[-10deg] rotate-x-[5deg] hover:rotate-0 transition-transform duration-700 ease-out z-10 bg-white">
            <div className="w-[148px] h-[18px] bg-gray-800 absolute top-0 left-1/2 -translate-x-1/2 rounded-b-[1rem] z-20"></div>
            <div className="h-[46px] w-[3px] bg-gray-800 absolute -left-[17px] top-[124px] rounded-l-lg"></div>
            <div className="h-[46px] w-[3px] bg-gray-800 absolute -left-[17px] top-[178px] rounded-l-lg"></div>
            <div className="h-[64px] w-[3px] bg-gray-800 absolute -right-[17px] top-[142px] rounded-r-lg"></div>
            
            {/* Phone Screen Content (WhatsApp Chat UI) */}
            <div className="rounded-[2rem] overflow-hidden w-[272px] h-[572px] bg-[#E5DDD5] relative flex flex-col relative z-10">
              {/* WA Header */}
              <div className="bg-[#075E54] text-white px-4 py-3 flex items-center gap-3 pt-8">
                <div className="w-8 h-8 bg-white rounded-full flex items-center justify-center text-primary font-bold text-xs">FB</div>
                <div>
                  <h3 className="text-sm font-bold leading-tight">FinanceBot UMKM</h3>
                  <p className="text-[10px] text-green-100">Online</p>
                </div>
              </div>
              
              {/* WA Body */}
              <div className="flex-1 p-3 flex flex-col gap-3 text-sm overflow-hidden" style={{ backgroundImage: "url('https://user-images.githubusercontent.com/15075759/28719144-86dc0f70-73b1-11e7-911d-60d70fcded21.png')", backgroundSize: 'cover' }}>
                <div className="bg-white p-2 rounded-lg rounded-tl-none self-start max-w-[85%] shadow-sm">
                  <p className="text-gray-800">Silakan pilih menu:<br/>1. Catat Pemasukan<br/>2. Catat Pengeluaran</p>
                  <p className="text-[9px] text-gray-400 text-right mt-1">10:00</p>
                </div>
                
                <div className="bg-[#DCF8C6] p-2 rounded-lg rounded-tr-none self-end max-w-[85%] shadow-sm">
                  <p className="text-gray-800">1</p>
                  <p className="text-[9px] text-gray-500 text-right mt-1">10:01 ✓✓</p>
                </div>
                
                <div className="bg-[#DCF8C6] p-2 rounded-lg rounded-tr-none self-end max-w-[85%] shadow-sm">
                  <p className="text-gray-800">1 porsi nasi goreng, 15000</p>
                  <p className="text-[9px] text-gray-500 text-right mt-1">10:02 ✓✓</p>
                </div>
                
                <div className="bg-white p-2 rounded-lg rounded-tl-none self-start max-w-[85%] shadow-sm">
                  <p className="text-gray-800">Pemasukan berhasil dicatat!<br/><br/>🟢 <b>+ Rp 15.000</b><br/>📝 1 porsi nasi goreng</p>
                  <p className="text-[9px] text-gray-400 text-right mt-1">10:02</p>
                </div>
              </div>
              
              {/* WA Input */}
              <div className="bg-gray-100 p-2 flex items-center gap-2">
                <div className="flex-1 bg-white rounded-full px-4 py-2 text-gray-400 text-xs">
                  Ketik pesan...
                </div>
                <div className="w-8 h-8 bg-[#00897B] rounded-full flex items-center justify-center text-white">
                  ▶
                </div>
              </div>
            </div>
          </div>
          
          {/* Floating Cards over phone */}
          <div className="absolute -left-6 lg:-left-12 bottom-32 bg-white p-4 rounded-xl shadow-xl shadow-slate-200/50 border border-slate-100 z-30 animate-bounce" style={{ animationDuration: '3s' }}>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center text-green-600 font-bold">
                Rp
              </div>
              <div>
                <p className="text-xs text-slate-500 font-medium">Total Pemasukan</p>
                <p className="text-lg font-bold text-slate-900">+3.500.000</p>
              </div>
            </div>
          </div>
          
        </div>
        
      </div>
    </div>
  );
}

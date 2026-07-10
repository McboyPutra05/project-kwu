export default function HowItWorks() {
  const steps = [
    { num: '01', title: 'Simpan Nomor', desc: 'Simpan nomor WhatsApp FinanceBot di kontak Anda.' },
    { num: '02', title: 'Kirim Pesan', desc: 'Ketik "Halo" atau "Menu" untuk memulai percakapan.' },
    { num: '03', title: 'Pilih Menu', desc: 'Pilih opsi 1-4 untuk mencatat atau melihat laporan.' },
    { num: '04', title: 'Terima Laporan', desc: 'Dapatkan rekap finansial dalam bentuk file Excel.' }
  ];

  return (
    <div id="how-it-works" className="py-24 bg-dark">
      <div className="max-w-7xl mx-auto px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">Cara Kerja Super Mudah</h2>
          <p className="text-gray-400 max-w-2xl mx-auto">Tanpa perlu install aplikasi berat, cukup gunakan WhatsApp yang sudah ada di HP Anda.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {steps.map((step, idx) => (
            <div key={idx} className="relative p-6 bg-[#161622] rounded-2xl border border-gray-800">
              <div className="text-5xl font-black text-gray-800 mb-4">{step.num}</div>
              <h3 className="text-lg font-bold text-white mb-2">{step.title}</h3>
              <p className="text-sm text-gray-400">{step.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

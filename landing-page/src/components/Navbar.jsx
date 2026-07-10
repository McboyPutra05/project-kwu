export default function Navbar() {
  return (
    <nav className="fixed w-full z-50 bg-white/80 backdrop-blur-lg border-b border-gray-100">
      <div className="max-w-7xl mx-auto px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          <div className="flex-shrink-0">
            <span className="text-2xl font-black tracking-tight text-primary italic">FinanceBot</span>
          </div>
          <div className="hidden md:flex items-center space-x-10">
            <a href="#features" className="text-slate-600 hover:text-primary transition-colors text-sm font-semibold">Features</a>
            <a href="#how-it-works" className="text-slate-600 hover:text-primary transition-colors text-sm font-semibold">How It Works</a>
            <a href="#pricing" className="text-slate-600 hover:text-primary transition-colors text-sm font-semibold">Pricing</a>
            <a href="#" className="bg-primary hover:bg-primaryHover text-white px-6 py-2.5 rounded-full text-sm font-semibold transition-all duration-300 shadow-md shadow-primary/30">
              Register
            </a>
          </div>
        </div>
      </div>
    </nav>
  );
}

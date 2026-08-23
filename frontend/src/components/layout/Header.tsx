export default function Header() {

  return (
    <header className="h-16 bg-slate-950 border-b border-slate-800 flex items-center justify-between px-8">


      <div>

        <h2 className="text-lg font-semibold text-white">
          Financial Risk Monitoring
        </h2>

        <p className="text-xs text-slate-400">
          AI Powered Fraud Investigation Platform
        </p>

      </div>



      <div className="flex items-center gap-3">

        <div className="h-2 w-2 rounded-full bg-green-400">
        </div>

        <span className="text-sm text-slate-300">
          Backend Connected
        </span>

      </div>


    </header>
  );
}
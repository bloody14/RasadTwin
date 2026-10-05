import React, { useEffect, useState } from 'react';
import { Hexagon, Server, CheckCircle2 } from 'lucide-react';

export default function CommandHeader({ offline }) {
  const [time, setTime] = useState(new Date());
  useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <header className="bg-[#0f1511] border-b border-[#2a362c] text-white p-3 flex justify-between items-center z-10 relative shadow-md shrink-0">
      <div className="flex items-center gap-4">
        <Hexagon className="w-10 h-10 text-[#a3b18a] stroke-[1.5]" />
        <div>
          <h1 className="text-2xl font-bold tracking-widest text-white leading-tight">RASADTWIN</h1>
          <div className="text-[10px] text-[#84a59d] uppercase tracking-wider font-mono">Predictive Logistics Digital Twin</div>
        </div>
      </div>
      
      <div className="flex flex-col justify-center border-l border-[#2a362c] pl-6 ml-4 hidden md:flex">
        <h2 className="text-xl font-bold tracking-wide text-white">LOGISTICS COMMAND CENTRE</h2>
        <div className="text-xs text-[#a3b18a]">Uncertainty-Aware Predictive Logistics for Forward Formations</div>
      </div>

      <div className="flex-1"></div>

      <div className="flex items-center gap-4">
        {offline ? (
          <div className="flex items-center gap-3 bg-[#1c231e] border border-[#e63946] px-3 py-1.5 rounded-sm">
            <Server className="w-5 h-5 text-[#e63946]" />
            <div>
              <div className="text-[10px] text-[#e63946] font-bold tracking-widest uppercase leading-tight">OFFLINE MODE</div>
              <div className="text-[9px] text-[#e63946]/70">Connection Lost</div>
            </div>
          </div>
        ) : (
          <div className="flex items-center gap-3 bg-[#1c231e] border border-[#d4a373] px-3 py-1.5 rounded-sm">
            <Server className="w-5 h-5 text-[#d4a373]" />
            <div>
              <div className="text-[10px] text-[#d4a373] font-bold tracking-widest uppercase leading-tight">LOCAL MODE</div>
              <div className="text-[9px] text-gray-400">Local Engine Active</div>
            </div>
          </div>
        )}
        
        <div className="flex items-center gap-3 bg-[#1c231e] border border-[#2a362c] px-3 py-1.5 rounded-sm">
          <div className={`w-3 h-3 rounded-full ${offline ? 'bg-[#e63946] shadow-[0_0_8px_#e63946]' : 'bg-[#52b788] shadow-[0_0_8px_#52b788]'}`}></div>
          <div>
            <div className={`text-[10px] font-bold tracking-widest uppercase leading-tight ${offline ? 'text-[#e63946]' : 'text-[#52b788]'}`}>
              {offline ? 'SYSTEM DEGRADED' : 'SYSTEM NOMINAL'}
            </div>
            <div className="text-[9px] text-gray-400">{offline ? 'Backend Unreachable' : 'All Services Operational'}</div>
          </div>
        </div>

        <div className="text-right ml-4 border-l border-[#2a362c] pl-4">
          <div className="text-xs text-white">{time.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })}</div>
          <div className="text-sm font-mono text-white font-bold">{time.toLocaleTimeString('en-GB')}</div>
        </div>
      </div>
    </header>
  );
}

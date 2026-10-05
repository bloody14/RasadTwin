import React from 'react';

export default function RiskMeter({ riskData }) {
  if (!riskData) return null;
  
  const dos = riskData.days_of_supply;
  const target = 5.8;
  const pct = Math.min(100, Math.max(0, (dos / 10) * 100));
  
  return (
    <div className="bg-command-panel border border-olive-deep p-3">
      <div className="flex justify-between items-end mb-2">
        <h3 className="text-[10px] text-neutral-gray uppercase tracking-widest">INVENTORY STATUS</h3>
        <span className="text-[10px] text-sand-field font-mono">TARGET: {target}d</span>
      </div>
      
      <div className="relative h-2 bg-command-black border border-olive-muted w-full mb-4">
        {/* Safe zone */}
        <div className="absolute left-[58%] right-0 top-0 bottom-0 bg-olive-military/30"></div>
        {/* Watch zone */}
        <div className="absolute left-[25%] right-[42%] top-0 bottom-0 bg-accent-amber/20"></div>
        {/* Critical zone */}
        <div className="absolute left-0 w-1/4 top-0 bottom-0 bg-accent-critical/20"></div>
        
        {/* Current Marker */}
        <div className="absolute top-0 bottom-0 w-1 bg-neutral-white transition-all duration-500 shadow-[0_0_8px_rgba(255,255,255,0.8)]" style={{ left: `${pct}%` }}></div>
        {/* Target Marker */}
        <div className="absolute top-0 bottom-0 w-0.5 bg-accent-blue" style={{ left: '58%' }}></div>
      </div>
      
      <div className="flex justify-between text-[9px] font-mono text-neutral-gray">
        <span className="text-accent-critical">CRITICAL</span>
        <span className="text-accent-warning">WATCH</span>
        <span className="text-accent-green">SAFE</span>
      </div>
    </div>
  );
}

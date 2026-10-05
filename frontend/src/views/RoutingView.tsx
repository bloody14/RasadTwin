import React from 'react';
import { GitMerge } from 'lucide-react';

export default function RoutingView({ routes }: any) {
  const riskColor = (r: string) => r === 'High' ? 'text-[#e63946]' : r === 'Medium' ? 'text-[#d4a373]' : 'text-[#52b788]';

  return (
    <div className="flex-1 bg-[#0b0f0c] border border-[#2a362c] rounded p-4 overflow-y-auto custom-scrollbar">
      <h2 className="text-sm font-bold tracking-widest text-white uppercase mb-4 flex items-center gap-2"><GitMerge className="w-4 h-4 text-[#457b9d]" /> ROUTE NETWORK</h2>
      <table className="w-full text-[10px]">
        <thead>
          <tr className="text-gray-500 uppercase tracking-widest border-b border-[#2a362c]">
            <th className="text-left py-2 px-2">Route</th>
            <th className="text-left py-2 px-2">Source</th>
            <th className="text-left py-2 px-2">Target</th>
            <th className="text-left py-2 px-2">Mode</th>
            <th className="text-right py-2 px-2">Distance</th>
            <th className="text-right py-2 px-2">Nominal ETA</th>
            <th className="text-right py-2 px-2">Robust ETA</th>
            <th className="text-right py-2 px-2">Risk</th>
          </tr>
        </thead>
        <tbody>
          {routes.map((r:any) => (
            <tr key={r.id} className="border-b border-[#2a362c]/50 hover:bg-[#1c231e]">
              <td className="py-2 px-2 font-mono font-bold text-white">{r.id}</td>
              <td className="py-2 px-2 text-gray-400">{r.source}</td>
              <td className="py-2 px-2 text-gray-400">{r.target}</td>
              <td className="py-2 px-2 text-white">{r.mode}</td>
              <td className="py-2 px-2 text-right font-mono text-gray-400">{r.distance_km} km</td>
              <td className="py-2 px-2 text-right font-mono text-[#457b9d]">{r.eta_hrs}h</td>
              <td className="py-2 px-2 text-right font-mono text-[#d4a373]">{r.robust_eta_hrs}h</td>
              <td className={`py-2 px-2 text-right font-bold uppercase ${riskColor(r.risk)}`}>{r.risk}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

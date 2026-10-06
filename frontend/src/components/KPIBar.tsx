import React from 'react';
import { Activity, Route, ShieldAlert, Package, Wifi } from 'lucide-react';

export default function KPIBar({ systemState, posts, routes, whatIf, decision }: any) {
  const atRisk = posts.filter((p:any) => p.risk === 'High').length;
  const pending = whatIf && !decision ? 1 : 0;
  
  const getSystemStateColor = () => {
    switch (systemState) {
      case 'NORMAL': return 'text-[#52b788]';
      case 'DISRUPTION_DETECTED': return 'text-[#e63946]';
      case 'HUMAN_REVIEW': return 'text-[#d4a373]';
      case 'PLAN_UPDATED': return 'text-[#6D9FB3]';
      default: return 'text-gray-400';
    }
  };

  return (
    <div className="flex gap-2 shrink-0 mb-2">
      <div className="bg-[#0b0f0c] border border-[#2a362c] rounded px-4 py-2 flex items-center justify-between w-64">
        <div>
          <div className="text-[9px] text-gray-500 font-bold tracking-widest uppercase">SYSTEM STATE</div>
          <div className={`text-xs font-mono font-bold mt-1 ${getSystemStateColor()}`}>{systemState.replace('_', ' ')}</div>
        </div>
        <Activity className={`w-5 h-5 ${getSystemStateColor()}`} />
      </div>
      
      <div className="flex-1 grid grid-cols-4 gap-2">
        <div className="bg-[#0b0f0c] border border-[#2a362c] rounded px-4 py-2 flex items-center justify-between">
          <div><div className="text-[9px] text-gray-500 font-bold tracking-widest uppercase">Active Posts</div><div className="text-sm font-mono text-white mt-1">{posts.length}</div></div>
          <Package className="w-4 h-4 text-gray-600" />
        </div>
        <div className="bg-[#0b0f0c] border border-[#2a362c] rounded px-4 py-2 flex items-center justify-between">
          <div><div className="text-[9px] text-[#e63946] font-bold tracking-widest uppercase">At Risk</div><div className="text-sm font-mono text-[#e63946] mt-1">{atRisk}</div></div>
          <ShieldAlert className="w-4 h-4 text-[#e63946]" />
        </div>
        <div className="bg-[#0b0f0c] border border-[#2a362c] rounded px-4 py-2 flex items-center justify-between">
          <div><div className="text-[9px] text-gray-500 font-bold tracking-widest uppercase">Active Routes</div><div className="text-sm font-mono text-white mt-1">{routes.length}</div></div>
          <Route className="w-4 h-4 text-gray-600" />
        </div>
        <div className="bg-[#0b0f0c] border border-[#d4a373]/30 rounded px-4 py-2 flex items-center justify-between">
          <div><div className="text-[9px] text-[#d4a373] font-bold tracking-widest uppercase">Decisions Pending</div><div className="text-sm font-mono text-[#d4a373] mt-1">{pending}</div></div>
          <Activity className="w-4 h-4 text-[#d4a373]" />
        </div>
      </div>
    </div>
  );
}

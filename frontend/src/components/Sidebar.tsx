import React from 'react';
import { LayoutDashboard, MapPin, TrendingUp, PackageSearch, GitMerge, Settings2, ShieldCheck, ListTodo } from 'lucide-react';

export default function Sidebar({ activeView, setActiveView }) {
  const items = [
    { id: 'COMMAND', icon: LayoutDashboard, label: 'COMMAND' },
    { id: 'POSTS', icon: MapPin, label: 'POSTS' },
    { id: 'FORECAST', icon: TrendingUp, label: 'FORECAST' },
    { id: 'INVENTORY', icon: PackageSearch, label: 'INVENTORY' },
    { id: 'ROUTING', icon: GitMerge, label: 'ROUTING' },
    { id: 'WHAT_IF', icon: Settings2, label: 'WHAT-IF' },
    { id: 'DECISIONS', icon: ShieldCheck, label: 'DECISIONS' },
    { id: 'AUDIT', icon: ListTodo, label: 'AUDIT' },
  ];

  return (
    <div className="w-[200px] bg-[#0b0f0c] border border-[#2a362c] flex flex-col justify-between shrink-0 rounded">
      <div className="py-2">
        {items.map((it) => (
          <button key={it.id} onClick={() => setActiveView(it.id)} className={`w-full flex items-center gap-4 px-6 py-4 transition-colors ${activeView === it.id ? 'bg-[#d4a373]/10 text-[#d4a373] border-l-2 border-[#d4a373]' : 'text-gray-400 hover:bg-[#1c231e] hover:text-white border-l-2 border-transparent'}`}>
            <it.icon className="w-5 h-5 shrink-0" />
            <span className="text-[11px] font-bold tracking-widest uppercase">{it.label}</span>
          </button>
        ))}
      </div>
      
      <div className="p-6 border-t border-[#2a362c]">
        <div className="text-sm font-bold text-white mb-1">NexRoute</div>
        <div className="text-[10px] text-gray-400 font-mono space-y-1">
          <div>SIH26251 | Indian Army</div>
          <div className="text-[#84a59d]">Synthetic Environment</div>
          <div className="text-gray-500">No Real Operational Data</div>
        </div>
      </div>
    </div>
  );
}

import React from 'react';
import { Activity, AlertTriangle, ShieldCheck } from 'lucide-react';

export default function KPIBar({ posts, routes, whatIf, decision }: any) {
  const fPosts = posts.filter((p:any) => p.type === 'forward_post');
  const atRisk = fPosts.filter((p:any) => p.risk === 'High').length;
  const watch = fPosts.filter((p:any) => p.dos < 7).length;

  const disruptions = whatIf && !decision ? 1 : 0;
  const pendingDecisions = whatIf && !decision ? 1 : 0;

  return (
    <div className="bg-[#0b0f0c] border border-[#2a362c] rounded flex items-center shrink-0">
      <div className="flex-1 flex divide-x divide-[#2a362c]">
        <div className="px-6 py-3 flex-1">
          <div className="text-[9px] text-gray-500 uppercase tracking-widest font-bold mb-1">Forward Posts</div>
          <div className="text-xl font-mono text-white">{fPosts.length}</div>
        </div>
        <div className="px-6 py-3 flex-1">
          <div className="text-[9px] text-[#e63946] uppercase tracking-widest font-bold mb-1 flex items-center gap-1"><AlertTriangle className="w-3 h-3"/> At Risk</div>
          <div className="text-xl font-mono text-[#e63946]">{atRisk}</div>
        </div>
        <div className="px-6 py-3 flex-1">
          <div className="text-[9px] text-[#d4a373] uppercase tracking-widest font-bold mb-1">Stock-out Watch</div>
          <div className="text-xl font-mono text-[#d4a373]">{watch}</div>
        </div>
        <div className="px-6 py-3 flex-1 bg-[#131915]">
          <div className="text-[9px] text-gray-400 uppercase tracking-widest font-bold mb-1">Disruptions</div>
          <div className={`text-xl font-mono ${disruptions > 0 ? 'text-[#e63946]' : 'text-white'}`}>{disruptions}</div>
        </div>
        <div className={`px-6 py-3 flex-1 transition-colors ${pendingDecisions > 0 ? 'bg-[#d4a373]/10 border-b-2 border-[#d4a373]' : ''}`}>
          <div className="text-[9px] text-gray-400 uppercase tracking-widest font-bold mb-1">Decisions Pending</div>
          <div className={`text-xl font-mono ${pendingDecisions > 0 ? 'text-[#d4a373]' : 'text-white'}`}>{pendingDecisions}</div>
        </div>
      </div>
    </div>
  );
}

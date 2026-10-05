import React from 'react';
import { ShieldCheck } from 'lucide-react';

export default function DecisionsView({ audits }: any) {
  const decisions = audits.filter((a:any) => a.action?.startsWith('HITL'));

  return (
    <div className="flex-1 bg-[#0b0f0c] border border-[#2a362c] rounded p-4 overflow-y-auto custom-scrollbar">
      <h2 className="text-sm font-bold tracking-widest text-white uppercase mb-4 flex items-center gap-2"><ShieldCheck className="w-4 h-4 text-[#52b788]" /> HITL DECISIONS</h2>
      {decisions.length === 0 ? (
        <div className="text-gray-500 text-xs text-center py-8 border border-dashed border-[#2a362c] rounded">No HITL decisions recorded yet. Run a What-If scenario from COMMAND view.</div>
      ) : (
        <div className="space-y-2">
          {decisions.map((d:any, i:number) => (
            <div key={i} className="bg-[#131915] border border-[#2a362c] p-3 rounded flex justify-between items-center">
              <div>
                <div className="text-xs font-bold text-white">{d.action}</div>
                <div className="text-[10px] text-gray-400">{d.scenario} → {d.decision}</div>
                <div className="text-[9px] text-gray-500">{d.reason}</div>
              </div>
              <div className="text-right">
                <div className="text-[10px] text-gray-500">{new Date(d.timestamp).toLocaleString()}</div>
                <div className="text-[9px] text-[#457b9d]">{d.user}</div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

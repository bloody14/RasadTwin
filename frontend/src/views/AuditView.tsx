import React from 'react';
import { ListTodo } from 'lucide-react';

export default function AuditView({ audits }: any) {
  return (
    <div className="flex-1 bg-[#0b0f0c] border border-[#2a362c] rounded p-4 overflow-y-auto custom-scrollbar">
      <h2 className="text-sm font-bold tracking-widest text-white uppercase mb-4 flex items-center gap-2"><ListTodo className="w-4 h-4 text-[#d4a373]" /> FULL AUDIT TIMELINE</h2>
      {audits.length === 0 ? (
        <div className="text-gray-500 text-xs text-center py-8 border border-dashed border-[#2a362c] rounded">No audit events yet. Perform actions in the COMMAND view.</div>
      ) : (
        <div className="space-y-1 font-mono text-[10px]">
          {audits.map((a:any, i:number) => (
            <div key={i} className={`flex gap-3 px-2 py-1.5 rounded ${a.user === 'COMMANDER' ? 'bg-[#1c231e] text-white' : 'text-gray-400'}`}>
              <span className={a.user === 'COMMANDER' ? 'text-[#52b788]' : 'text-[#d4a373]'}>▶</span>
              <span className="w-36 text-gray-500 shrink-0">{new Date(a.timestamp).toLocaleString()}</span>
              <span className={`w-20 shrink-0 ${a.user === 'COMMANDER' ? 'text-[#457b9d]' : 'text-gray-500'}`}>{a.user}</span>
              <span className="w-24 shrink-0 text-white">{a.action}</span>
              <span className="truncate">{a.decision} — {a.scenario}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

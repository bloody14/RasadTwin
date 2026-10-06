import React from 'react';

export default function AuditView({ audits }: any) {
  return (
    <div className="h-full bg-[#0b0f0c] border border-[#2a362c] rounded flex flex-col overflow-hidden">
      <div className="p-4 border-b border-[#2a362c] flex justify-between items-center bg-[#131915]">
        <h2 className="text-sm font-bold tracking-widest text-white uppercase">SYSTEM AUDIT LEDGER</h2>
      </div>
      <div className="flex-1 overflow-auto p-4 custom-scrollbar">
        <table className="w-full text-left text-xs">
          <thead>
            <tr className="text-gray-500 border-b border-[#2a362c]">
              <th className="pb-2 font-normal uppercase tracking-wider">Timestamp</th>
              <th className="pb-2 font-normal uppercase tracking-wider">Actor</th>
              <th className="pb-2 font-normal uppercase tracking-wider">Event</th>
              <th className="pb-2 font-normal uppercase tracking-wider">Scenario</th>
              <th className="pb-2 font-normal uppercase tracking-wider">Detail</th>
            </tr>
          </thead>
          <tbody>
            {audits.map((a:any, i:number) => (
              <tr key={i} className="border-b border-[#1c231e] hover:bg-[#1c231e]/50">
                <td className="py-2 font-mono text-gray-400 whitespace-nowrap">{new Date(a.timestamp).toLocaleString()}</td>
                <td className={`py-2 ${a.user === 'COMMANDER' ? 'text-[#457b9d] font-bold' : 'text-gray-500'}`}>{a.user}</td>
                <td className="py-2 font-mono text-white">{a.action}</td>
                <td className="py-2 text-gray-400">{a.scenario || '-'}</td>
                <td className="py-2 text-gray-300">
                  {a.user_action === 'APPROVE' ? `APPROVED ${a.selected_scope}` : 
                   a.user_action === 'REJECT' ? `REJECTED -> PLAN RETAINED` :
                   a.user_action === 'OVERRIDE' ? `OVERRIDE -> ${a.selected_scope}` :
                   a.reason || '-'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

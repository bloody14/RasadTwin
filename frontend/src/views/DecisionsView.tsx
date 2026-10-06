import React from 'react';

export default function DecisionsView({ audits }: any) {
  const hitl = audits.filter((a:any) => a.action.startsWith('HITL'));
  return (
    <div className="h-full bg-[#0b0f0c] border border-[#2a362c] rounded flex flex-col overflow-hidden">
      <div className="p-4 border-b border-[#2a362c] flex justify-between items-center bg-[#131915]">
        <h2 className="text-sm font-bold tracking-widest text-white uppercase">HUMAN DECISIONS</h2>
      </div>
      <div className="flex-1 overflow-auto p-4 custom-scrollbar">
        <table className="w-full text-left text-xs">
          <thead>
            <tr className="text-gray-500 border-b border-[#2a362c]">
              <th className="pb-2 font-normal uppercase tracking-wider">Time</th>
              <th className="pb-2 font-normal uppercase tracking-wider">Scenario</th>
              <th className="pb-2 font-normal uppercase tracking-wider">System Rec</th>
              <th className="pb-2 font-normal uppercase tracking-wider">User Action</th>
              <th className="pb-2 font-normal uppercase tracking-wider">Selected Scope</th>
              <th className="pb-2 font-normal uppercase tracking-wider">Actor</th>
            </tr>
          </thead>
          <tbody>
            {hitl.map((d:any, i:number) => (
              <tr key={i} className="border-b border-[#1c231e] hover:bg-[#1c231e]/50">
                <td className="py-3 font-mono text-gray-400">{new Date(d.timestamp).toLocaleTimeString()}</td>
                <td className="py-3 text-white uppercase">{d.scenario}</td>
                <td className="py-3 text-[#d4a373] uppercase font-bold">{d.system_recommendation}</td>
                <td className="py-3 text-[#52b788] uppercase font-bold">{d.user_action}</td>
                <td className="py-3 text-[#6D9FB3] uppercase font-bold">{d.selected_scope}</td>
                <td className="py-3 text-gray-500">{d.user}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

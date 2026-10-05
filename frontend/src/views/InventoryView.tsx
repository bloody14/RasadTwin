import React from 'react';
import { PackageSearch } from 'lucide-react';

export default function InventoryView({ posts }: any) {
  const riskColor = (r: string) => r === 'High' ? 'text-[#e63946]' : r === 'Medium' ? 'text-[#d4a373]' : 'text-[#52b788]';

  return (
    <div className="flex-1 bg-[#0b0f0c] border border-[#2a362c] rounded p-4 overflow-y-auto custom-scrollbar">
      <h2 className="text-sm font-bold tracking-widest text-white uppercase mb-4 flex items-center gap-2"><PackageSearch className="w-4 h-4 text-[#d4a373]" /> INVENTORY STATUS</h2>
      <table className="w-full text-[10px]">
        <thead>
          <tr className="text-gray-500 uppercase tracking-widest border-b border-[#2a362c]">
            <th className="text-left py-2 px-2">Post</th>
            <th className="text-left py-2 px-2">Name</th>
            <th className="text-left py-2 px-2">Type</th>
            <th className="text-right py-2 px-2">Days of Supply</th>
            <th className="text-right py-2 px-2">Priority</th>
            <th className="text-right py-2 px-2">Risk</th>
          </tr>
        </thead>
        <tbody>
          {posts.map((p:any) => (
            <tr key={p.id} className="border-b border-[#2a362c]/50 hover:bg-[#1c231e]">
              <td className="py-2 px-2 font-mono font-bold text-white">{p.id.replace('FP-00','F-0')}</td>
              <td className="py-2 px-2 text-gray-400">{p.name}</td>
              <td className="py-2 px-2 text-gray-500 uppercase">{p.type.replace('_',' ')}</td>
              <td className={`py-2 px-2 text-right font-mono font-bold ${p.dos < 5 ? 'text-[#e63946]' : 'text-white'}`}>{p.dos}</td>
              <td className="py-2 px-2 text-right font-mono text-gray-400">{p.priority}</td>
              <td className={`py-2 px-2 text-right font-bold uppercase ${riskColor(p.risk)}`}>{p.risk}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="mt-4 text-[8px] text-gray-600 text-center uppercase tracking-widest">All data is synthetic — no real operational information</div>
    </div>
  );
}

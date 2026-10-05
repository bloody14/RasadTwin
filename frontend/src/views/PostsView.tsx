import React from 'react';
import { AlertTriangle, CheckCircle, MapPin } from 'lucide-react';

export default function PostsView({ posts, selectPost, selectedPost }: any) {
  const riskColor = (r: string) => r === 'High' ? 'text-[#e63946]' : r === 'Medium' ? 'text-[#d4a373]' : 'text-[#52b788]';
  const riskBg = (r: string) => r === 'High' ? 'bg-[#e63946]/10 border-[#e63946]/40' : r === 'Medium' ? 'bg-[#d4a373]/10 border-[#d4a373]/40' : 'bg-[#131915] border-[#2a362c]';

  return (
    <div className="flex-1 bg-[#0b0f0c] border border-[#2a362c] rounded p-4 overflow-y-auto custom-scrollbar">
      <h2 className="text-sm font-bold tracking-widest text-white uppercase mb-4 flex items-center gap-2"><MapPin className="w-4 h-4 text-[#d4a373]" /> ALL SYNTHETIC POSTS</h2>
      <div className="grid grid-cols-3 gap-3">
        {posts.map((p: any) => (
          <button key={p.id} onClick={() => selectPost(p)} className={`text-left p-3 rounded border transition-all ${selectedPost?.id === p.id ? 'border-[#d4a373] bg-[#d4a373]/10' : riskBg(p.risk)} hover:border-[#d4a373]/60`}>
            <div className="flex justify-between items-start mb-2">
              <div className="text-lg font-mono font-bold text-white">{p.id.replace('FP-00','F-0')}</div>
              <div className={`text-[9px] font-bold uppercase tracking-widest px-2 py-0.5 rounded ${riskColor(p.risk)} ${p.risk === 'High' ? 'bg-[#e63946]/20' : ''}`}>{p.risk}</div>
            </div>
            <div className="text-[10px] text-gray-400 mb-1">{p.name}</div>
            <div className="text-[9px] text-gray-500 uppercase">{p.type.replace('_',' ')}</div>
            <div className="flex justify-between mt-2 text-[10px]">
              <span className="text-gray-500">DoS</span>
              <span className={`font-mono font-bold ${p.dos < 5 ? 'text-[#e63946]' : 'text-white'}`}>{p.dos} days</span>
            </div>
          </button>
        ))}
      </div>
      <div className="mt-4 text-[9px] text-gray-600 text-center">Click a post to inspect it in COMMAND view</div>
    </div>
  );
}

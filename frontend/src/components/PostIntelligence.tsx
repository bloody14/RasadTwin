import React, { useState } from 'react';
import { ShieldAlert, Package, Activity, Loader2, GitMerge } from 'lucide-react';
import { AreaChart, Area, ResponsiveContainer, XAxis, Tooltip } from 'recharts';

export default function PostIntelligence({ post, riskData, forecast, routes, isLoading }: any) {
  const [tab, setTab] = useState('RISK');

  if (isLoading) {
    return (
      <div className="w-[320px] bg-[#0b0f0c] border border-[#2a362c] rounded p-4 flex flex-col items-center justify-center shrink-0">
         <Loader2 className="w-8 h-8 text-[#d4a373] animate-spin mb-4" />
         <h3 className="text-xs text-[#d4a373] tracking-widest uppercase font-bold">Fetching Post Intelligence...</h3>
      </div>
    );
  }

  if (!post || !riskData || !forecast) {
    return (
      <div className="w-[320px] bg-[#0b0f0c] border border-[#2a362c] rounded p-4 flex flex-col items-center justify-center shrink-0 text-center">
         <h3 className="text-xs text-gray-500 tracking-widest uppercase font-bold mb-2">POST INTELLIGENCE</h3>
         <p className="text-[10px] text-gray-600">Select a post on the map to load intelligence.</p>
      </div>
    );
  }

  const postRoutes = routes.filter((r:any) => r.target === post.id);
  const chartData = [...(forecast.history || []), ...(forecast.future || [])].map((d:any) => ({
    name: d.day, actual: d.demand, forecast: d.forecast
  }));

  return (
    <div className="w-[320px] bg-[#0b0f0c] border border-[#2a362c] rounded flex flex-col shrink-0 overflow-hidden">
      <div className="p-4 border-b border-[#2a362c] relative">
        <div className="absolute top-0 right-0 bg-[#d4a373]/20 text-[#d4a373] text-[8px] font-bold px-2 py-0.5 rounded-bl tracking-widest">CURRENT PLAN</div>
        <div className="flex items-start justify-between mt-2">
          <div>
            <h2 className="text-xl font-mono font-bold text-white">{post.id.replace('FP-00', 'F-0')}</h2>
            <div className="text-[10px] text-gray-400 uppercase tracking-widest">{post.name} • {post.type.replace('_',' ')}</div>
          </div>
          <div className={`px-2 py-1 rounded text-[10px] font-bold uppercase tracking-widest ${post.risk === 'High' ? 'bg-[#e63946]/20 text-[#e63946]' : 'bg-[#52b788]/20 text-[#52b788]'}`}>
            {post.risk === 'High' ? 'AT RISK' : 'NOMINAL'}
          </div>
        </div>
      </div>

      <div className="flex border-b border-[#2a362c] text-[10px] font-bold tracking-widest uppercase">
        {['RISK', 'FORECAST', 'ROUTES'].map(t => (
          <button key={t} onClick={() => setTab(t)} className={`flex-1 py-2 text-center transition-colors ${tab === t ? 'text-[#d4a373] border-b-2 border-[#d4a373]' : 'text-gray-500 hover:text-gray-300'}`}>
            {t}
          </button>
        ))}
      </div>

      <div className="p-4 flex-1 overflow-y-auto custom-scrollbar">
        {tab === 'RISK' && (
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-2">
              <div className="bg-[#131915] p-3 rounded border border-[#2a362c]">
                <div className="text-[9px] text-gray-500 uppercase mb-1">Days of Supply</div>
                <div className={`text-lg font-mono font-bold ${riskData.days_of_supply < 7 ? 'text-[#e63946]' : 'text-white'}`}>{riskData.days_of_supply}.0 days</div>
              </div>
              <div className="bg-[#131915] p-3 rounded border border-[#2a362c]">
                <div className="text-[9px] text-gray-500 uppercase mb-1">Stock-out Risk</div>
                <div className={`text-lg font-mono font-bold ${riskData.stock_out_risk === '85%' ? 'text-[#e63946]' : 'text-white'}`}>{riskData.stock_out_risk}</div>
              </div>
            </div>

            <div>
              <div className="text-[10px] text-[#d4a373] font-bold uppercase tracking-widest mb-2">Why At Risk?</div>
              <div className="space-y-1">
                {(riskData.explainability || []).map((ex:any, i:number) => (
                  <div key={i} className="flex justify-between items-center text-[10px] bg-[#131915] px-2 py-1.5 rounded">
                    <span className="text-gray-400">{ex.feature}</span>
                    <span className="text-white font-mono">{ex.description}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {tab === 'FORECAST' && (
          <div className="space-y-4">
            <div className="text-[9px] text-gray-500 uppercase tracking-widest flex justify-between">
              <span>Historical</span>
              <span className="text-[#457b9d]">Predicted Demand</span>
            </div>
            <div className="h-32 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={chartData}>
                  <XAxis dataKey="name" hide />
                  <Tooltip contentStyle={{ backgroundColor: '#131915', borderColor: '#2a362c', fontSize: '10px' }} />
                  <Area type="monotone" dataKey="actual" stroke="#6b7280" fill="none" strokeWidth={2} />
                  <Area type="monotone" dataKey="forecast" stroke="#457b9d" fill="#457b9d" fillOpacity={0.2} strokeWidth={2} strokeDasharray="3 3" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
            <div className="text-[9px] text-gray-500 text-center">Nominal Coverage: {forecast.nominal_coverage}</div>
          </div>
        )}

        {tab === 'ROUTES' && (
          <div className="space-y-2">
            {postRoutes.map((r:any) => (
              <div key={r.id} className="bg-[#131915] p-3 rounded border border-[#2a362c]">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-[10px] text-gray-400 font-mono">{r.source} → {r.target}</span>
                  <span className="text-[9px] text-white font-bold bg-[#1c231e] px-1.5 py-0.5 rounded">{r.mode}</span>
                </div>
                <div className="flex justify-between text-[10px]">
                  <span className="text-gray-500">Nominal ETA</span>
                  <span className="font-mono text-white">{r.eta_hrs} hrs</span>
                </div>
                <div className="flex justify-between text-[10px] mt-1">
                  <span className="text-gray-500">Robust ETA</span>
                  <span className="font-mono text-[#d4a373]">{r.robust_eta_hrs} hrs</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

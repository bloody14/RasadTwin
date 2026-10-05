import React from 'react';
import { TrendingUp } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function ForecastView({ selectedPost, forecast }: any) {
  if (!selectedPost || !forecast) return (
    <div className="flex-1 bg-[#0b0f0c] border border-[#2a362c] rounded flex items-center justify-center text-gray-500 text-xs uppercase tracking-widest">Select a post from POSTS view first</div>
  );

  const chartData = [
    ...(forecast.history || []).map((d:any) => ({ name: d.day, actual: d.demand })),
    ...(forecast.future || []).map((d:any) => ({ name: d.day, forecast: d.forecast, lower: d.lower, upper: d.upper })),
  ];

  return (
    <div className="flex-1 bg-[#0b0f0c] border border-[#2a362c] rounded p-4 overflow-y-auto custom-scrollbar">
      <h2 className="text-sm font-bold tracking-widest text-white uppercase mb-2 flex items-center gap-2"><TrendingUp className="w-4 h-4 text-[#457b9d]" /> FORECAST — {selectedPost.id.replace('FP-00','F-0')}</h2>
      <div className="text-[10px] text-gray-500 mb-4">{selectedPost.name} • Nominal Coverage: {forecast.nominal_coverage || '90%'}</div>

      <div className="flex gap-4 mb-2 text-[9px] text-gray-400 uppercase tracking-widest">
        <span className="flex items-center gap-1"><div className="w-2 h-2 bg-gray-500"></div> Historical</span>
        <span className="flex items-center gap-1"><div className="w-2 h-2 bg-[#457b9d]"></div> Forecast</span>
        <span className="flex items-center gap-1"><div className="w-2 h-2 bg-[#457b9d]/30 border border-[#457b9d]"></div> Uncertainty</span>
      </div>
      <div className="h-64 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
            <CartesianGrid stroke="#2a362c" strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="name" tick={{fontSize: 10, fill: '#6b7280'}} axisLine={false} tickLine={false} />
            <YAxis tick={{fontSize: 10, fill: '#6b7280'}} axisLine={false} tickLine={false} />
            <Tooltip contentStyle={{ backgroundColor: '#131915', borderColor: '#2a362c', fontSize: '11px', color: '#fff' }} />
            <Area type="monotone" dataKey="upper" stroke="none" fill="#457b9d" fillOpacity={0.15} />
            <Area type="monotone" dataKey="lower" stroke="none" fill="#0b0f0c" fillOpacity={1} />
            <Area type="monotone" dataKey="actual" stroke="#6b7280" strokeWidth={2} fill="none" dot={{r:3, fill:'#6b7280'}} />
            <Area type="monotone" dataKey="forecast" stroke="#457b9d" strokeWidth={2} fill="none" dot={{r:3, fill:'#457b9d'}} strokeDasharray="4 4" />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      <div className="grid grid-cols-7 gap-2 mt-4">
        {(forecast.future || []).map((d:any, i:number) => (
          <div key={i} className="bg-[#131915] border border-[#2a362c] p-2 rounded text-center">
            <div className="text-[9px] text-gray-500">{d.day}</div>
            <div className="text-sm font-mono text-[#457b9d] font-bold">{d.forecast}</div>
            <div className="text-[8px] text-gray-600">[{d.lower}–{d.upper}]</div>
          </div>
        ))}
      </div>
    </div>
  );
}

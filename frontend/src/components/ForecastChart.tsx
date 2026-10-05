import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ComposedChart, Area } from 'recharts';

export default function ForecastChart({ forecast }) {
  if (!forecast) return <div className="text-xs text-neutral-gray font-mono">Loading forecast...</div>;

  const chartData = [
    ...forecast.history.map(d => ({ name: d.day, actual: d.demand })),
    ...forecast.future.map(d => ({ name: d.day, forecast: d.forecast, lower: d.lower, upper: d.upper }))
  ];

  return (
    <div className="bg-command-panel border border-olive-deep p-3">
      <h3 className="text-[10px] text-neutral-gray uppercase tracking-widest mb-3">DEMAND FORECAST (NEXT 7 DAYS)</h3>
      <div className="h-48 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={chartData} margin={{ top: 5, right: 0, left: -20, bottom: 0 }}>
            <CartesianGrid stroke="#2F3D31" strokeDasharray="2 2" vertical={false} />
            <XAxis dataKey="name" tick={{fontSize: 10, fill: '#9AA39A', fontFamily: 'monospace'}} axisLine={{stroke: '#46543A'}} tickLine={false} />
            <YAxis tick={{fontSize: 10, fill: '#9AA39A', fontFamily: 'monospace'}} axisLine={{stroke: '#46543A'}} tickLine={false} />
            <Tooltip 
              contentStyle={{ backgroundColor: '#1A211C', border: '1px solid #46543A', borderRadius: '0', fontSize: '12px', fontFamily: 'monospace', color: '#E9ECE7' }}
              itemStyle={{ color: '#E9ECE7' }}
            />
            {/* Uncertainty Band */}
            <Area type="step" dataKey="upper" stroke="none" fill="#6D9FB3" fillOpacity={0.15} />
            <Area type="step" dataKey="lower" stroke="none" fill="#1A211C" fillOpacity={1} />
            
            <Line type="step" dataKey="actual" stroke="#9AA39A" strokeWidth={1} dot={{r: 2, fill: '#9AA39A', strokeWidth: 0}} isAnimationActive={false} />
            <Line type="step" dataKey="forecast" stroke="#D6A63C" strokeWidth={2} strokeDasharray="4 4" dot={{r: 2, fill: '#D6A63C', strokeWidth: 0}} isAnimationActive={false} />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
      <div className="flex justify-between items-center mt-2">
        <div className="flex gap-3">
          <div className="flex items-center gap-1 text-[9px] text-neutral-gray font-mono"><div className="w-2 h-0.5 bg-neutral-gray"></div> ACTUAL</div>
          <div className="flex items-center gap-1 text-[9px] text-neutral-gray font-mono"><div className="w-2 h-0.5 bg-accent-amber border border-dashed"></div> PRED</div>
        </div>
        <div className="text-[9px] text-accent-blue font-mono bg-accent-blue/10 px-1">UNCERTAINTY BAND: 80%</div>
      </div>
    </div>
  );
}

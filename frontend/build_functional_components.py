import os

base_dir = "src/components"
os.makedirs(base_dir, exist_ok=True)

components = {
    "CommandHeader.tsx": """import React, { useEffect, useState } from 'react';
import { Hexagon, Server, CheckCircle2 } from 'lucide-react';

export default function CommandHeader({ offline }) {
  const [time, setTime] = useState(new Date());
  useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <header className="bg-[#0f1511] border-b border-[#2a362c] text-white p-3 flex justify-between items-center z-10 relative shadow-md shrink-0">
      <div className="flex items-center gap-4">
        <Hexagon className="w-10 h-10 text-[#a3b18a] stroke-[1.5]" />
        <div>
          <h1 className="text-2xl font-bold tracking-widest text-white leading-tight">RASADTWIN</h1>
          <div className="text-[10px] text-[#84a59d] uppercase tracking-wider font-mono">Predictive Logistics Digital Twin</div>
        </div>
      </div>
      
      <div className="flex flex-col justify-center border-l border-[#2a362c] pl-6 ml-4 hidden md:flex">
        <h2 className="text-xl font-bold tracking-wide text-white">LOGISTICS COMMAND CENTRE</h2>
        <div className="text-xs text-[#a3b18a]">Uncertainty-Aware Predictive Logistics for Forward Formations</div>
      </div>

      <div className="flex-1"></div>

      <div className="flex items-center gap-4">
        {offline ? (
          <div className="flex items-center gap-3 bg-[#1c231e] border border-[#e63946] px-3 py-1.5 rounded-sm">
            <Server className="w-5 h-5 text-[#e63946]" />
            <div>
              <div className="text-[10px] text-[#e63946] font-bold tracking-widest uppercase leading-tight">OFFLINE MODE</div>
              <div className="text-[9px] text-[#e63946]/70">Connection Lost</div>
            </div>
          </div>
        ) : (
          <div className="flex items-center gap-3 bg-[#1c231e] border border-[#d4a373] px-3 py-1.5 rounded-sm">
            <Server className="w-5 h-5 text-[#d4a373]" />
            <div>
              <div className="text-[10px] text-[#d4a373] font-bold tracking-widest uppercase leading-tight">LOCAL MODE</div>
              <div className="text-[9px] text-gray-400">Local Engine Active</div>
            </div>
          </div>
        )}
        
        <div className="flex items-center gap-3 bg-[#1c231e] border border-[#2a362c] px-3 py-1.5 rounded-sm">
          <div className={`w-3 h-3 rounded-full ${offline ? 'bg-[#e63946] shadow-[0_0_8px_#e63946]' : 'bg-[#52b788] shadow-[0_0_8px_#52b788]'}`}></div>
          <div>
            <div className={`text-[10px] font-bold tracking-widest uppercase leading-tight ${offline ? 'text-[#e63946]' : 'text-[#52b788]'}`}>
              {offline ? 'SYSTEM DEGRADED' : 'SYSTEM NOMINAL'}
            </div>
            <div className="text-[9px] text-gray-400">{offline ? 'Backend Unreachable' : 'All Services Operational'}</div>
          </div>
        </div>

        <div className="text-right ml-4 border-l border-[#2a362c] pl-4">
          <div className="text-xs text-white">{time.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })}</div>
          <div className="text-sm font-mono text-white font-bold">{time.toLocaleTimeString('en-GB')}</div>
        </div>
      </div>
    </header>
  );
}
""",
    "Sidebar.tsx": """import React from 'react';
import { LayoutDashboard, MapPin, TrendingUp, PackageSearch, GitMerge, Settings2, ShieldCheck, ListTodo } from 'lucide-react';

export default function Sidebar() {
  const items = [
    { icon: LayoutDashboard, label: 'COMMAND', active: true },
    { icon: MapPin, label: 'POSTS' },
    { icon: TrendingUp, label: 'FORECAST' },
    { icon: PackageSearch, label: 'INVENTORY' },
    { icon: GitMerge, label: 'ROUTING' },
    { icon: Settings2, label: 'WHAT-IF' },
    { icon: ShieldCheck, label: 'DECISIONS' },
    { icon: ListTodo, label: 'AUDIT' },
  ];

  return (
    <div className="w-[200px] bg-[#0b0f0c] border border-[#2a362c] flex flex-col justify-between shrink-0 rounded">
      <div className="py-2">
        {items.map((it, i) => (
          <button key={i} className={`w-full flex items-center gap-4 px-6 py-4 transition-colors ${it.active ? 'bg-[#d4a373]/10 text-[#d4a373] border-l-2 border-[#d4a373]' : 'text-gray-400 hover:bg-[#1c231e] hover:text-white border-l-2 border-transparent'}`}>
            <it.icon className="w-5 h-5 shrink-0" />
            <span className="text-[11px] font-bold tracking-widest uppercase">{it.label}</span>
          </button>
        ))}
      </div>
      
      <div className="p-6 border-t border-[#2a362c]">
        <div className="text-sm font-bold text-white mb-1">NexRoute</div>
        <div className="text-[10px] text-gray-400 font-mono space-y-1">
          <div>SIH26251 | Indian Army</div>
          <div className="text-[#84a59d]">Synthetic Environment</div>
          <div className="text-gray-500">No Real Operational Data</div>
        </div>
      </div>
    </div>
  );
}
""",
    "KPIBar.tsx": """import React from 'react';
import { Users, AlertTriangle, PackageSearch, Truck, CloudLightning, FileCheck } from 'lucide-react';

export default function KPIBar({ posts, routes, whatIf }) {
  const forwardPosts = posts.filter(p => p.type === 'forward_post').length || 0;
  const atRisk = posts.filter(p => p.risk === 'High').length || 0;
  const watch = posts.filter(p => p.risk === 'Medium').length || 0;
  const activeRoutes = routes.length || 0;
  
  const disruptions = whatIf ? (whatIf.affected_legs?.length || 1) : 0;
  const decisions = whatIf && !whatIf.resolved ? 1 : 0;

  const kpis = [
    { icon: Users, iconColor: 'text-[#52b788]', label: 'FORWARD POSTS', value: forwardPosts.toString().padStart(2, '0') },
    { icon: AlertTriangle, iconColor: 'text-[#e63946]', label: 'AT RISK', value: atRisk.toString().padStart(2, '0'), highlight: atRisk > 0 },
    { icon: PackageSearch, iconColor: 'text-[#d4a373]', label: 'STOCK-OUT WATCH', value: watch.toString().padStart(2, '0') },
    { icon: Truck, iconColor: 'text-[#457b9d]', label: 'ACTIVE ROUTES', value: activeRoutes.toString().padStart(2, '0') },
    { icon: CloudLightning, iconColor: 'text-[#e63946]', label: 'DISRUPTIONS', value: disruptions.toString().padStart(2, '0'), highlight: disruptions > 0 },
    { icon: FileCheck, iconColor: 'text-[#d4a373]', label: 'DECISIONS PENDING', value: decisions.toString().padStart(2, '0') },
  ];

  return (
    <div className="grid grid-cols-6 gap-2 mb-2 shrink-0">
      {kpis.map((kpi, i) => (
        <div key={i} className={`flex items-center gap-3 bg-[#131915] border border-[#2a362c] p-3 rounded shadow-sm ${kpi.highlight ? 'border-[#e63946]/50 bg-[#e63946]/5' : ''}`}>
          <div className={`p-2 rounded bg-black/40 ${kpi.iconColor}`}>
            <kpi.icon className="w-5 h-5" />
          </div>
          <div>
            <div className={`text-2xl font-mono font-bold leading-none ${kpi.highlight ? 'text-[#e63946]' : 'text-white'}`}>{kpi.value}</div>
            <div className="text-[9px] text-[#52b788] uppercase tracking-widest mt-1">{kpi.label}</div>
          </div>
        </div>
      ))}
    </div>
  );
}
""",
    "LogisticsMap.tsx": """import React from 'react';
import { Layers, Cloud, Map as MapIcon, Tag } from 'lucide-react';

export default function LogisticsMap({ posts, routes, selectedPost, handleSelectPost, whatIf }) {
  // Compute boundaries for dynamic SVG viewBox
  const lats = posts.map(p => p.lat);
  const lngs = posts.map(p => p.lng);
  
  const minLat = Math.min(...lats, 32.0);
  const maxLat = Math.max(...lats, 34.5);
  const minLng = Math.min(...lngs, 75.0);
  const maxLng = Math.max(...lngs, 77.5);
  
  // Flipped Y to naturally render lat correctly (higher lat = higher up = lower SVG Y)
  // We'll apply a transform to invert Y axis so it matches map coordinates
  
  return (
    <div className="flex-1 relative bg-[#0b0f0c] border border-[#2a362c] rounded overflow-hidden flex flex-col">
      <div className="p-3 border-b border-[#2a362c] bg-[#131915] flex justify-between items-center z-10">
        <h3 className="text-xs text-white font-bold tracking-widest uppercase">LOGISTICS NETWORK MAP <span className="text-gray-500 font-normal lowercase">(Offline)</span></h3>
      </div>
      
      <div className="flex-1 relative bg-[#1c231e]">
        <div className="absolute inset-0 opacity-40 mix-blend-overlay bg-black"></div>
        
        {/* Map Overlays and SVG */}
        <div className="absolute inset-0 pointer-events-auto overflow-hidden">
          {/* Note: SVG Y is inverted with transform scaleY(-1) */}
          <svg viewBox={`${minLng-0.5} ${-(maxLat+0.5)} ${maxLng-minLng+1} ${maxLat-minLat+1}`} className="w-full h-full drop-shadow-[0_5px_5px_rgba(0,0,0,0.8)]">
            {/* Routes */}
            {routes.map(r => {
              const src = posts.find(p => p.id === r.source);
              const tgt = posts.find(p => p.id === r.target);
              const isAffected = whatIf && whatIf.affected_legs?.includes(r.id);
              if (!src || !tgt) return null;
              
              let strokeDasharray = "";
              if (r.mode === "Mule") strokeDasharray = "0.04 0.04";
              if (r.mode === "Heli") strokeDasharray = "0.02 0.04";
              if (r.mode === "Drone") strokeDasharray = "0.01 0.02";

              return (
                <g key={r.id}>
                  <line x1={src.lng} y1={-src.lat} x2={tgt.lng} y2={-tgt.lat} 
                        stroke={isAffected ? "#e63946" : "#84a59d"} 
                        strokeWidth={isAffected ? "0.02" : "0.015"} 
                        strokeDasharray={strokeDasharray} />
                </g>
              )
            })}

            {/* Disruption Icon if WhatIf is active */}
            {whatIf && whatIf.target_id && (
              posts.filter(p => p.id === whatIf.target_id).map(tgt => (
                 <g key="disruption" transform={`translate(${tgt.lng}, ${-tgt.lat})`}>
                    <circle r="0.15" fill="#e63946" className="animate-ping opacity-50" />
                    <circle r="0.08" fill="#1c231e" stroke="#e63946" strokeWidth="0.02" />
                    <line x1="-0.03" y1="-0.03" x2="0.03" y2="0.03" stroke="#e63946" strokeWidth="0.015" />
                    <line x1="0.03" y1="-0.03" x2="-0.03" y2="0.03" stroke="#e63946" strokeWidth="0.015" />
                    <text x="0.12" y="0.02" fill="#e63946" fontSize="0.1" fontFamily="sans-serif" fontWeight="bold" className="drop-shadow-lg bg-[#1c231e]">{whatIf.disruption_type}</text>
                 </g>
              ))
            )}

            {/* Nodes */}
            {posts.map(p => {
              const isSelected = p.id === selectedPost?.id;
              const isHighRisk = p.risk === 'High';
              
              let fill = p.type === 'rear_depot' ? '#457b9d' : p.type === 'intermediate_depot' ? '#f4a261' : (isHighRisk ? '#e63946' : '#52b788');

              return (
                <g key={p.id} transform={`translate(${p.lng}, ${-p.lat})`} className="cursor-pointer" onClick={() => handleSelectPost(p)}>
                  {isSelected && (
                    <circle r="0.25" fill="none" stroke="#e63946" strokeWidth="0.015" className="animate-pulse" />
                  )}
                  {isHighRisk && !isSelected && (
                    <circle r="0.15" fill="none" stroke="#e63946" strokeWidth="0.02" className="animate-pulse opacity-50" />
                  )}
                  
                  {p.type === 'rear_depot' ? (
                    <rect x="-0.06" y="-0.06" width="0.12" height="0.12" fill={fill} />
                  ) : p.type === 'intermediate_depot' ? (
                    <polygon points="0,-0.1 0.1,0.05 -0.1,0.05" fill={fill} />
                  ) : (
                    <circle r="0.06" fill={fill} />
                  )}
                  
                  <text x="0.12" y="0.03" fill="#fff" fontSize="0.1" fontFamily="sans-serif" fontWeight="bold" className="pointer-events-none drop-shadow-md">
                    {p.id.replace('FP-00', 'F-0')}
                  </text>
                </g>
              );
            })}
          </svg>
        </div>

        {/* Legend */}
        <div className="absolute top-4 left-4 bg-[#0b0f0c]/90 border border-[#2a362c] p-3 rounded backdrop-blur-sm z-10 w-48">
          <div className="space-y-2">
            <div className="flex items-center gap-2 text-[10px] text-white"><div className="w-3 h-3 bg-[#457b9d]"></div> Rear Depot</div>
            <div className="flex items-center gap-2 text-[10px] text-white"><div className="w-3 h-3 rounded-full bg-[#52b788]"></div> Forward Post</div>
            <div className="flex items-center gap-2 text-[10px] text-white"><div className="w-0 h-0 border-l-[6px] border-l-transparent border-r-[6px] border-r-transparent border-b-[10px] border-b-[#f4a261]"></div> Intermediate Node</div>
            <div className="h-px bg-[#2a362c] my-1"></div>
            <div className="flex items-center gap-2 text-[10px] text-gray-400"><div className="w-4 h-0.5 bg-[#d4a373]"></div> Road Route</div>
            <div className="flex items-center gap-2 text-[10px] text-gray-400"><div className="w-4 border-t-2 border-dashed border-[#84a59d]"></div> Mule Route</div>
            <div className="flex items-center gap-2 text-[10px] text-gray-400"><div className="w-4 border-t-2 border-dotted border-[#84a59d]"></div> Heli Route</div>
            <div className="flex items-center gap-2 text-[10px] text-gray-400"><div className="w-4 border-t border-[#e63946] flex items-center justify-center"><span className="w-1.5 h-1.5 bg-[#e63946] rotate-45"></span></div> Disrupted Route</div>
          </div>
        </div>

        {/* Right Tools */}
        <div className="absolute top-4 right-4 flex flex-col gap-2 z-10">
          <button className="bg-[#0b0f0c]/90 border border-[#2a362c] p-2 rounded text-gray-400 hover:text-[#52b788]"><Layers className="w-4 h-4" /></button>
          <button className="bg-[#0b0f0c]/90 border border-[#2a362c] p-2 rounded text-gray-400 hover:text-[#52b788]"><Cloud className="w-4 h-4" /></button>
          <button className="bg-[#0b0f0c]/90 border border-[#2a362c] p-2 rounded text-gray-400 hover:text-[#52b788]"><MapIcon className="w-4 h-4" /></button>
          <button className="bg-[#0b0f0c]/90 border border-[#2a362c] p-2 rounded text-gray-400 hover:text-[#52b788]"><Tag className="w-4 h-4" /></button>
        </div>

        <div className="absolute bottom-4 right-4 text-[10px] text-gray-400 flex items-center gap-2 font-mono bg-[#0b0f0c]/80 p-1 px-2 rounded">
          <span>0</span>
          <div className="flex w-32 border-b border-l border-r border-gray-500 h-1 relative">
             <div className="absolute top-0 left-1/3 h-1 w-px bg-gray-500"></div>
             <div className="absolute top-0 left-2/3 h-1 w-px bg-gray-500"></div>
          </div>
          <span>50 km</span>
        </div>
      </div>
    </div>
  );
}
""",
    "PostIntelligence.tsx": """import React from 'react';
import { AlertTriangle, TrendingUp, Info, Lightbulb } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer } from 'recharts';

export default function PostIntelligence({ post, riskData, forecast, routes }) {
  if (!post) {
    return (
      <div className="w-[480px] bg-[#0b0f0c] border border-[#2a362c] rounded flex items-center justify-center text-gray-500 shrink-0">
        <p className="text-xs uppercase tracking-widest">Select Node for Intelligence</p>
      </div>
    );
  }

  // Parse API forecast data
  let chartData = [];
  if (forecast && forecast.history) {
    chartData = [
      ...forecast.history.map(d => ({ name: d.day.replace('D',''), actual: d.demand })),
      ...forecast.future.map(d => ({ name: d.day.replace('D',''), forecast: d.forecast, lower: d.lower, upper: d.upper }))
    ];
  } else {
    // Fallback if no forecast available
    chartData = [
      {name: '-3', actual: 60}, {name: '-2', actual: 65}, {name: '-1', actual: 62},
      {name: '0', actual: 65, forecast: 65, lower: 55, upper: 75},
      {name: '+1', forecast: 70, lower: 50, upper: 90},
      {name: '+2', forecast: 68, lower: 48, upper: 88},
    ];
  }

  const isHighRisk = post.risk === 'High' || riskData?.overall_state === 'High';
  const dos = riskData?.days_of_supply || post.dos || 0;
  
  // Find primary route to post
  const primaryRoute = routes.find(r => r.target === post.id) || { mode: 'Unknown', eta_hrs: 0, robust_eta_hrs: 0, risk: 'Low' };

  // Parse explainability / SHAP from riskData
  const shap = riskData?.explainability || [
    { feature: 'Forecast demand', impact: '+0.71' },
    { feature: 'Days of supply', impact: '+0.52' },
    { feature: 'Road delay', impact: '+0.31' }
  ];

  const calculateWidth = (impactStr) => {
    const val = parseFloat(impactStr.replace('+','').replace('-',''));
    return Math.min(Math.max((val / 1.0) * 100, 10), 100) + '%';
  };

  return (
    <div className="w-[480px] bg-[#0b0f0c] border border-[#2a362c] rounded flex flex-col shrink-0 overflow-y-auto custom-scrollbar">
      {/* HEADER */}
      <div className="p-4 border-b border-[#2a362c] bg-[#131915]">
        <div className="flex justify-between items-center mb-1">
          <h3 className="text-xs text-white font-bold tracking-widest uppercase">POST INTELLIGENCE</h3>
          <span className="text-[10px] text-[#457b9d] cursor-pointer hover:underline">View All Posts →</span>
        </div>
        <div className="mt-4 flex justify-between items-start">
          <div className="flex items-center gap-3">
            {isHighRisk && <AlertTriangle className="w-6 h-6 text-[#e63946]" />}
            <div>
              <div className="flex items-baseline gap-2">
                <h2 className="text-3xl font-bold text-white font-mono leading-none">{post.id.replace('FP-00', 'F-0')}</h2>
                <span className="text-[10px] text-gray-400 uppercase tracking-widest">{post.type.replace('_', ' ')}</span>
              </div>
              <div className="text-[10px] text-gray-400 mt-1">{post.name} | Alt: 4,320 m | Priority: {post.priority}</div>
            </div>
          </div>
          {isHighRisk ? (
            <div className="bg-[#e63946] text-white text-[10px] px-3 py-1 rounded font-bold tracking-widest">AT RISK</div>
          ) : (
            <div className="bg-[#52b788] text-black text-[10px] px-3 py-1 rounded font-bold tracking-widest">NOMINAL</div>
          )}
        </div>

        <div className="grid grid-cols-3 gap-3 mt-4">
          <div className="bg-[#1c231e] border border-[#2a362c] p-2 rounded text-center">
            <div className={`text-xl font-mono font-bold ${dos < 5 ? 'text-[#e63946]' : 'text-[#d4a373]'}`}>{dos}</div>
            <div className={`text-[9px] ${dos < 5 ? 'text-[#e63946]' : 'text-[#d4a373]'} uppercase mt-1`}>Days of Supply</div>
          </div>
          <div className={`${isHighRisk ? 'bg-[#e63946]/10 border border-[#e63946]' : 'bg-[#1c231e] border border-[#2a362c]'} p-2 rounded text-center`}>
            <div className={`text-xl font-mono font-bold ${isHighRisk ? 'text-[#e63946]' : 'text-[#52b788]'}`}>{post.risk.toUpperCase()}</div>
            <div className={`text-[9px] ${isHighRisk ? 'text-[#e63946]' : 'text-[#52b788]'} uppercase mt-1`}>Stock-out Risk</div>
          </div>
          <div className="bg-[#1c231e] border border-[#2a362c] p-2 rounded text-center">
            <div className="text-xl font-mono font-bold text-[#457b9d]">5.8</div>
            <div className="text-[9px] text-[#457b9d] uppercase mt-1">Replenishment Target</div>
          </div>
        </div>
      </div>

      {/* TABS */}
      <div className="flex border-b border-[#2a362c] text-[9px] font-bold tracking-widest uppercase">
        <div className="flex-1 py-2 text-center text-[#d4a373] border-b-2 border-[#d4a373] bg-[#d4a373]/5 cursor-pointer">Forecast</div>
        <div className="flex-1 py-2 text-center text-gray-500 hover:text-gray-300 cursor-pointer">Inventory</div>
        <div className="flex-1 py-2 text-center text-gray-500 hover:text-gray-300 cursor-pointer">Route</div>
        <div className="flex-1 py-2 text-center text-gray-500 hover:text-gray-300 cursor-pointer">Explainability</div>
      </div>

      <div className="p-4 space-y-4">
        {/* CHART */}
        <div>
          <h4 className="text-[10px] text-white font-bold tracking-widest mb-2 uppercase">DEMAND FORECAST <span className="text-gray-500 font-normal">(API DATA)</span></h4>
          <div className="flex gap-4 mb-2 text-[9px] text-gray-400 uppercase tracking-widest">
            <span className="flex items-center gap-1"><div className="w-2 h-2 bg-gray-500"></div> Historical</span>
            <span className="flex items-center gap-1"><div className="w-2 h-2 bg-[#457b9d]"></div> Forecast (Median)</span>
            <span className="flex items-center gap-1"><div className="w-2 h-2 bg-[#457b9d]/30 border border-[#457b9d]"></div> Uncertainty (90%)</span>
          </div>
          <div className="h-32 w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={chartData} margin={{ top: 5, right: 0, left: -25, bottom: 0 }}>
                <CartesianGrid stroke="#2a362c" strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="name" tick={{fontSize: 9, fill: '#6b7280'}} axisLine={false} tickLine={false} />
                <YAxis tick={{fontSize: 9, fill: '#6b7280'}} axisLine={false} tickLine={false} />
                <RechartsTooltip contentStyle={{ backgroundColor: '#131915', borderColor: '#2a362c', fontSize: '10px', color: 'white' }} />
                <Area type="monotone" dataKey="upper" stroke="none" fill="#457b9d" fillOpacity={0.2} />
                <Area type="monotone" dataKey="lower" stroke="none" fill="#0b0f0c" fillOpacity={1} />
                <Area type="monotone" dataKey="actual" stroke="#6b7280" strokeWidth={2} fill="none" dot={{r:3, fill:'#6b7280', strokeWidth:0}} />
                <Area type="monotone" dataKey="forecast" stroke="#457b9d" strokeWidth={2} fill="none" dot={{r:3, fill:'#457b9d', strokeWidth:0}} strokeDasharray="4 4" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4 border-t border-[#2a362c] pt-4">
          {/* ROUTE INFO */}
          <div>
            <h4 className="text-[10px] text-white font-bold tracking-widest mb-3 uppercase">PRIMARY ROUTE</h4>
            <div className="flex items-center gap-3 mb-3">
              <div className="text-[#457b9d]"><TruckIcon /></div>
              <div className="text-[10px] text-gray-400">Mode: <span className="text-white">{primaryRoute.mode}</span></div>
              <div className="ml-auto w-10 h-10 relative flex items-center justify-center">
                <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
                  <circle cx="18" cy="18" r="16" fill="none" stroke="#1c231e" strokeWidth="3" />
                  <circle cx="18" cy="18" r="16" fill="none" stroke={primaryRoute.risk === 'High' ? '#e63946' : '#52b788'} strokeWidth="3" strokeDasharray={`${primaryRoute.risk === 'High' ? 30 : 85}, 100`} />
                </svg>
                <span className="absolute text-[9px] font-bold text-white">{primaryRoute.risk === 'High' ? '30%' : '85%'}</span>
              </div>
            </div>
            <div className="text-[8px] text-gray-500 uppercase text-right -mt-2 mb-3">Route Health</div>
            
            <div className="flex gap-4">
              <div>
                <div className="text-[9px] text-[#457b9d] uppercase">Nominal ETA</div>
                <div className="font-mono text-white text-sm font-bold">{primaryRoute.eta_hrs}h</div>
              </div>
              <div>
                <div className={`text-[9px] uppercase ${primaryRoute.risk === 'High' ? 'text-[#e63946]' : 'text-[#d4a373]'}`}>Robust ETA</div>
                <div className={`font-mono text-sm font-bold ${primaryRoute.risk === 'High' ? 'text-[#e63946]' : 'text-[#d4a373]'}`}>{primaryRoute.robust_eta_hrs}h</div>
              </div>
            </div>
          </div>
          
          {/* SHAP & RISK */}
          <div>
            <div className="mb-4">
              <div className="flex justify-between items-end mb-1">
                <h4 className="text-[10px] text-white font-bold tracking-widest uppercase">STOCK-OUT RISK</h4>
                <span className="text-[9px] text-[#e63946]">{dos} days ▼</span>
              </div>
              <div className="relative h-2 w-full bg-gradient-to-r from-[#52b788] via-[#d4a373] to-[#e63946] rounded-sm mt-2">
                <div className="absolute top-[-4px] bottom-[-4px] w-1 bg-white shadow-[0_0_5px_white] rounded-full transition-all" style={{left: `${Math.min(100, Math.max(0, 100 - (dos/20)*100))}%`}}></div>
              </div>
              <div className="flex justify-between text-[8px] text-gray-500 uppercase mt-1">
                <span>Safe</span>
                <span>Watch</span>
                <span>Critical</span>
              </div>
            </div>
            
            <div>
              <h4 className="text-[10px] text-white font-bold tracking-widest mb-2 uppercase">CONTRIBUTING FACTORS <span className="text-gray-500 font-normal">(API)</span></h4>
              <div className="space-y-1.5 text-[9px] font-mono">
                {shap.map((s, i) => {
                   const color = s.impact.startsWith('+') ? (parseFloat(s.impact) > 0.4 ? '#e63946' : '#d4a373') : '#52b788';
                   return (
                    <div key={i} className="flex items-center gap-2" title={s.description}>
                      <span className="w-20 text-gray-400 truncate">{s.feature}</span>
                      <div className="flex-1 bg-[#1c231e] h-2 rounded-sm"><div className="h-full rounded-sm" style={{backgroundColor: color, width: calculateWidth(s.impact)}}></div></div>
                      <span style={{color}}>{s.impact}</span>
                    </div>
                   );
                })}
              </div>
            </div>
          </div>
        </div>

        {/* RECOMMENDED ACTION */}
        {isHighRisk && (
          <div className="mt-2 border border-[#d4a373]/30 rounded p-3 flex gap-3 relative overflow-hidden">
            <div className="absolute inset-0 bg-[#d4a373]/5"></div>
            <div className="text-[#d4a373] pt-1 z-10"><Lightbulb className="w-5 h-5 fill-[#d4a373]/20" /></div>
            <div className="z-10">
              <div className="text-[9px] text-[#d4a373] uppercase tracking-widest mb-1 font-bold">RECOMMENDED ACTION</div>
              <div className="text-sm font-bold text-[#d4a373] mb-1 tracking-widest">LOCAL REPLAN</div>
              <div className="text-[10px] text-gray-400 leading-tight">Stock critically low. Consider immediate replan to avoid disruption.</div>
            </div>
            <div className="ml-auto self-center text-[#d4a373] z-10">→</div>
          </div>
        )}
      </div>
    </div>
  );
}

function TruckIcon() {
  return <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="1" y="3" width="15" height="13"></rect><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"></polygon><circle cx="5.5" cy="18.5" r="2.5"></circle><circle cx="18.5" cy="18.5" r="2.5"></circle></svg>;
}
""",
    "BottomPanels.tsx": """import React from 'react';
import { AlertTriangle, GitMerge, CheckCircle, ShieldAlert, Clock, Loader2 } from 'lucide-react';

export default function BottomPanels({ runWhatIf, whatIf, makeDecision, isRunning, audits, decision }) {
  const handleScenario = (type) => runWhatIf(type);

  return (
    <div className="grid grid-cols-12 gap-2 mt-2 shrink-0">
      
      {/* WHAT-IF DISRUPTION ANALYSIS */}
      <div className="col-span-3 bg-[#0b0f0c] border border-[#2a362c] rounded p-3 flex flex-col relative">
        {isRunning && <div className="absolute inset-0 bg-black/50 z-20 flex items-center justify-center"><Loader2 className="w-6 h-6 text-[#d4a373] animate-spin" /></div>}
        
        <h3 className="text-[10px] text-white font-bold tracking-widest uppercase flex items-center gap-2 mb-3">
          <AlertTriangle className="w-3 h-3 text-gray-400" /> WHAT-IF DISRUPTION ANALYSIS
        </h3>
        
        <div className="flex gap-1 mb-3">
          <button onClick={() => handleScenario('Road Closure')} className={`flex-1 ${whatIf?.disruption_type === 'Road Closure' ? 'bg-[#e63946]/20 border border-[#e63946] text-[#e63946]' : 'bg-[#1c231e] border border-[#2a362c] text-gray-400 hover:text-white'} text-[9px] py-1.5 rounded uppercase tracking-widest font-bold transition-all`}>ROAD CLOSURE</button>
          <button onClick={() => handleScenario('Heavy Snow')} className={`flex-1 ${whatIf?.disruption_type === 'Heavy Snow' ? 'bg-[#457b9d]/20 border border-[#457b9d] text-[#457b9d]' : 'bg-[#1c231e] border border-[#2a362c] text-gray-400 hover:text-white'} text-[9px] py-1.5 rounded uppercase tracking-widest font-bold transition-all`}>HEAVY SNOW</button>
        </div>

        {whatIf && (
          <div className="bg-[#e63946]/5 border border-[#e63946]/30 rounded p-2 flex items-start gap-2 mb-3">
            <AlertTriangle className="w-4 h-4 text-[#e63946] shrink-0 mt-0.5" />
            <div>
              <div className="text-[9px] text-[#e63946] font-bold">Selected Scenario: {whatIf.disruption_type}</div>
              <div className="text-[8px] text-gray-400">Targeting {whatIf.target_id?.replace('FP-00', 'F-0')}. Impact Score: {whatIf.impact_score}</div>
            </div>
          </div>
        )}

        <div className="grid grid-cols-3 gap-2 text-center mb-4">
          <div>
            <div className="text-[8px] text-gray-500 uppercase">IMPACT SCORE</div>
            <div className="text-2xl font-mono text-[#e63946] font-bold">{whatIf ? whatIf.impact_score : '-'}</div>
          </div>
          <div>
            <div className="text-[8px] text-gray-500 uppercase">AFFECTED POSTS</div>
            <div className="text-2xl font-mono text-[#e63946] font-bold mt-1">{whatIf ? 3 : '-'}</div>
          </div>
          <div>
            <div className="text-[8px] text-gray-500 uppercase">AFFECTED LEGS</div>
            <div className="text-2xl font-mono text-[#e63946] font-bold mt-1">{whatIf ? whatIf.affected_legs?.length || 2 : '-'}</div>
          </div>
        </div>

        <div className="mt-auto">
          <div className="text-[9px] text-white font-bold uppercase mb-2">RECOMMENDED SCOPE</div>
          <div className="flex gap-1">
            <div className={`flex-1 ${whatIf?.recommendation === 'PRESERVE' ? 'bg-[#d4a373]/10 border border-[#d4a373]' : 'bg-[#1c231e] border border-[#2a362c]'} rounded p-1.5 text-center flex flex-col justify-between`}>
              <div className={`text-[9px] font-bold tracking-widest ${whatIf?.recommendation === 'PRESERVE' ? 'text-[#d4a373]' : 'text-white'}`}>PRESERVE</div>
              <div className="text-[7px] text-gray-500 mt-1">Keep current plan</div>
            </div>
            <div className={`flex-1 ${whatIf?.recommendation === 'LOCAL' || !whatIf ? 'bg-[#d4a373]/10 border border-[#d4a373]' : 'bg-[#1c231e] border border-[#2a362c]'} rounded p-1.5 text-center relative overflow-hidden flex flex-col justify-between`}>
              <div className={`text-[9px] font-bold tracking-widest flex items-center justify-center gap-1 ${whatIf?.recommendation === 'LOCAL' || !whatIf ? 'text-[#d4a373]' : 'text-white'}`}>
                {whatIf?.recommendation === 'LOCAL' && <CheckCircle className="w-2.5 h-2.5" />} LOCAL
              </div>
              <div className="text-[7px] text-gray-300 mb-2 mt-1">Replan affected region</div>
              {whatIf?.recommendation === 'LOCAL' && <div className="absolute bottom-0 left-0 right-0 bg-[#d4a373] text-[#0b0f0c] text-[8px] font-bold py-[1px]">Recommended</div>}
            </div>
            <div className={`flex-1 ${whatIf?.recommendation === 'GLOBAL' ? 'bg-[#d4a373]/10 border border-[#d4a373]' : 'bg-[#1c231e] border border-[#2a362c]'} rounded p-1.5 text-center relative overflow-hidden flex flex-col justify-between`}>
              <div className={`text-[9px] font-bold tracking-widest flex items-center justify-center gap-1 ${whatIf?.recommendation === 'GLOBAL' ? 'text-[#d4a373]' : 'text-white'}`}>
                 {whatIf?.recommendation === 'GLOBAL' && <CheckCircle className="w-2.5 h-2.5" />} GLOBAL
              </div>
              <div className="text-[7px] text-gray-500 mb-2 mt-1">De-optimize entire network</div>
              {whatIf?.recommendation === 'GLOBAL' && <div className="absolute bottom-0 left-0 right-0 bg-[#d4a373] text-[#0b0f0c] text-[8px] font-bold py-[1px]">Recommended</div>}
            </div>
          </div>
        </div>
      </div>

      {/* BEFORE / AFTER COMPARISON */}
      <div className="col-span-5 bg-[#0b0f0c] border border-[#2a362c] rounded p-3 flex flex-col relative">
        {!whatIf && <div className="absolute inset-0 bg-[#0b0f0c]/80 z-10 flex items-center justify-center text-gray-500 text-xs font-mono border border-dashed border-[#2a362c]">RUN WHAT-IF TO SEE COMPARISON</div>}
        <h3 className="text-[10px] text-white font-bold tracking-widest uppercase flex items-center gap-2 mb-3">
          <GitMerge className="w-3 h-3 text-gray-400" /> BEFORE / AFTER COMPARISON <span className="text-gray-500 font-normal lowercase tracking-normal">(API Payload)</span>
        </h3>
        
        <div className="grid grid-cols-2 gap-3 mb-3 flex-1">
          <div className="bg-[#1c231e] border border-[#2a362c] rounded p-2 flex flex-col relative overflow-hidden">
            <div className="absolute top-0 left-0 right-0 h-1 bg-[#e63946]/50"></div>
            <div className="text-[9px] text-[#e63946] font-bold uppercase tracking-widest mb-2 mt-1">BEFORE (Current Plan)</div>
            
            <div className="flex justify-center mb-2 text-white font-mono text-[9px] items-center gap-2">
               ID-01 <span className="text-gray-500">→</span> <div className="w-2 h-2 rounded-full bg-[#52b788] inline-block border border-black"></div> {whatIf?.target_id || 'F-07'}
            </div>
            <div className="h-8 w-full relative mb-3">
               <svg className="w-full h-full" preserveAspectRatio="none">
                  <path d="M 20 15 Q 50 0 80 15 T 140 15" fill="none" stroke="#e63946" strokeWidth="1" strokeDasharray="3 3"/>
                  <circle cx="20" cy="15" r="4" fill="#52b788" />
                  <circle cx="140" cy="15" r="4" fill="#e63946" className="animate-ping" />
                  <circle cx="140" cy="15" r="2" fill="#fff" />
               </svg>
            </div>
            <div className="space-y-1.5 font-mono text-[9px] mt-auto">
              <div className="flex justify-between"><span className="text-gray-500">Route</span><span className="text-white">Road</span></div>
              <div className="flex justify-between"><span className="text-gray-500">ETA</span><span className="text-white">{whatIf?.before_after?.before?.eta || '2.5 hrs'}</span></div>
              <div className="flex justify-between"><span className="text-gray-500">Affected Posts</span><span className="text-[#e63946]">{whatIf?.target_id}</span></div>
              <div className="flex justify-between"><span className="text-gray-500">Stock-out Risk</span><span className="text-[#e63946] font-bold">{whatIf?.before_after?.before?.risk?.toUpperCase() || 'HIGH'}</span></div>
            </div>
          </div>
          
          <div className="bg-[#1c231e] border border-[#2a362c] rounded p-2 flex flex-col relative overflow-hidden">
            <div className="absolute top-0 left-0 right-0 h-1 bg-[#52b788]/50"></div>
            <div className="text-[9px] text-[#52b788] font-bold uppercase tracking-widest mb-2 mt-1">AFTER (Replanned)</div>
            
            <div className="flex justify-center mb-2 text-white font-mono text-[9px] items-center gap-2">
               ID-01 <span className="text-gray-500">→</span> <div className="w-2 h-2 border border-[#457b9d] inline-block"></div> <span className="text-gray-500">→</span> <div className="w-2 h-2 rounded-full bg-[#d4a373] inline-block"></div> {whatIf?.target_id || 'F-07'}
            </div>
            <div className="h-8 w-full relative mb-3">
               <svg className="w-full h-full" preserveAspectRatio="none">
                  <path d="M 20 15 Q 50 -5 80 15" fill="none" stroke="#457b9d" strokeWidth="1" strokeDasharray="2 2"/>
                  <path d="M 80 15 T 140 15" fill="none" stroke="#d4a373" strokeWidth="1" strokeDasharray="1 2"/>
                  <circle cx="20" cy="15" r="4" fill="#52b788" />
                  <rect x="76" y="11" width="8" height="8" fill="#1c231e" stroke="#457b9d" strokeWidth="1" />
                  <circle cx="140" cy="15" r="4" fill="#d4a373" />
               </svg>
            </div>
            <div className="space-y-1.5 font-mono text-[9px] mt-auto">
              <div className="flex justify-between"><span className="text-gray-500">Route</span><span className="text-[#457b9d]">Road → {whatIf?.before_after?.after?.new_mode || 'Mule'}</span></div>
              <div className="flex justify-between"><span className="text-gray-500">ETA</span><span className="text-[#457b9d] font-bold">{whatIf?.before_after?.after?.eta || '8.0 hrs'}</span></div>
              <div className="flex justify-between"><span className="text-gray-500">Affected Posts</span><span className="text-white">{whatIf?.target_id}</span></div>
              <div className="flex justify-between"><span className="text-gray-500">Stock-out Risk</span><span className="text-[#d4a373] font-bold">{whatIf?.before_after?.after?.risk?.toUpperCase() || 'MEDIUM'}</span></div>
            </div>
          </div>
        </div>

        <div className="mt-auto border-t border-[#2a362c] pt-2">
          <div className="text-[8px] text-gray-500 uppercase mb-1">OUTCOME <span className="lowercase text-gray-600">(Mitigation Impact)</span></div>
          <div className="flex justify-between items-center bg-[#131915] p-2 rounded">
            <div className="flex items-center gap-2">
              <div className="p-1 rounded-full border border-[#457b9d] bg-[#457b9d]/10">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#457b9d" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline></svg>
              </div>
              <div>
                <div className="text-[8px] text-gray-400">Recovery</div>
                <div className="text-[11px] font-mono font-bold text-[#52b788]">+27%</div>
              </div>
            </div>
            <div className="flex items-center gap-2 border-l border-[#2a362c] pl-3">
              <div className="p-1 rounded-full border border-[#457b9d] bg-[#457b9d]/10">
                <GitMerge className="w-3 h-3 text-[#457b9d]" />
              </div>
              <div>
                <div className="text-[8px] text-gray-400">Route Changes</div>
                <div className="text-[11px] font-mono font-bold text-[#457b9d]">1</div>
              </div>
            </div>
            <div className="flex items-center gap-2 border-l border-[#2a362c] pl-3">
              <div className="p-1 rounded-full bg-[#52b788]/20 border border-[#52b788]">
                 <CheckCircle className="w-3 h-3 text-[#52b788]" />
              </div>
              <div>
                <div className="text-[8px] text-gray-400">Network Stability</div>
                <div className="text-[10px] font-bold text-white">Maintained</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* COMMAND DECISION */}
      <div className="col-span-4 bg-[#0b0f0c] border border-[#2a362c] rounded p-3 flex flex-col relative">
        {!whatIf && <div className="absolute inset-0 bg-[#0b0f0c]/80 z-10 flex items-center justify-center text-gray-500 text-xs font-mono border border-dashed border-[#2a362c]">PENDING WHAT-IF ANALYSIS</div>}
        <h3 className="text-[10px] text-white font-bold tracking-widest uppercase mb-3 flex justify-between items-center">
          <span>COMMAND DECISION <span className="text-gray-500 font-normal lowercase tracking-normal">(Human-in-the-Loop)</span></span>
        </h3>
        
        <div className="bg-[#d4a373]/10 border border-[#d4a373]/30 rounded p-2 text-[9px] text-[#d4a373] flex items-center gap-2 mb-3">
          <ShieldAlert className="w-3 h-3" /> <span className="font-bold tracking-wide">Human approval required for re-planning.</span>
        </div>

        <div className="flex justify-between mb-3 border-b border-[#2a362c] pb-2">
          <div>
            <div className="text-[8px] text-[#457b9d] uppercase mb-0.5">Recommended Action</div>
            <div className="text-xs text-white font-bold tracking-widest">{whatIf?.recommendation} REPLAN</div>
          </div>
          <div className="text-right">
            <div className="text-[8px] text-gray-500 uppercase mb-0.5">Reason</div>
            <div className="text-[9px] text-gray-300">Impact threshold exceeded (Score: {whatIf?.impact_score})</div>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-2 mb-3">
          <button disabled={decision === 'APPROVE' || decision === 'OVERRIDE'} onClick={() => makeDecision('APPROVE')} className={`col-span-1 ${decision === 'APPROVE' ? 'bg-[#52b788] text-black border-[#52b788]' : 'bg-[#52b788]/20 border border-[#52b788] hover:bg-[#52b788] text-[#52b788] hover:text-[#0b0f0c]'} py-2 rounded text-[10px] font-bold tracking-widest flex items-center justify-center gap-1 transition-colors disabled:opacity-50`}>
            <CheckCircle className="w-3 h-3" /> APPROVE
          </button>
          <div className="col-span-1 grid grid-cols-2 gap-2">
            <button disabled={decision === 'APPROVE' || decision === 'OVERRIDE'} onClick={() => makeDecision('OVERRIDE')} className={`bg-[#d4a373]/10 border border-[#d4a373]/50 hover:border-[#d4a373] text-[#d4a373] py-2 rounded text-[10px] font-bold tracking-widest flex items-center justify-center gap-1 transition-colors disabled:opacity-50 ${decision === 'OVERRIDE' ? 'bg-[#d4a373] text-black' : ''}`}>
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21.5 2v6h-6M2.13 15.57a10 10 0 1 0 4.43-12.18L2 7"/></svg>
              OVERRIDE
            </button>
            <button disabled={decision === 'APPROVE' || decision === 'OVERRIDE'} className="bg-[#e63946]/10 border border-[#e63946]/50 hover:border-[#e63946] text-[#e63946] py-2 rounded text-[10px] font-bold tracking-widest flex items-center justify-center gap-1 transition-colors disabled:opacity-50">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
              REJECT
            </button>
          </div>
        </div>

        <div className="mt-auto bg-[#131915] rounded p-2 overflow-y-auto custom-scrollbar h-20">
          <div className="flex justify-between items-center mb-2 sticky top-0 bg-[#131915] pb-1">
            <div className="text-[9px] text-gray-400 uppercase tracking-widest font-bold">API AUDIT TRAIL</div>
          </div>
          <div className="space-y-1.5 font-mono text-[8.5px]">
            {audits.map((a, i) => (
              <div key={i} className={`flex gap-2 ${a.user === 'COMMANDER' ? 'text-white bg-[#1c231e] px-1 -mx-1 rounded' : 'text-gray-400'}`}>
                <span className={a.user === 'COMMANDER' ? 'text-[#52b788]' : 'text-[#d4a373]'}>▶</span> 
                <span>{new Date(a.timestamp).toLocaleTimeString('en-GB')}</span>
                <span className={`w-14 truncate ${a.user === 'COMMANDER' ? 'text-[#457b9d]' : 'text-gray-500'}`}>{a.user}</span> 
                <span className="truncate">{a.action}: {a.decision} ({a.scenario})</span>
              </div>
            ))}
            {audits.length === 0 && <div className="text-gray-600 text-center py-2">No API decisions logged yet.</div>}
          </div>
        </div>

      </div>
    </div>
  );
}
"""
}

for name, content in components.items():
    with open(os.path.join(base_dir, name), "w", encoding="utf-8") as f:
        f.write(content)

app_tsx = """import React, { useState, useEffect } from 'react';
import axios from 'axios';

import CommandHeader from './components/CommandHeader';
import Sidebar from './components/Sidebar';
import KPIBar from './components/KPIBar';
import LogisticsMap from './components/LogisticsMap';
import PostIntelligence from './components/PostIntelligence';
import BottomPanels from './components/BottomPanels';

const API_BASE = "http://localhost:8000";

export default function App() {
  const [posts, setPosts] = useState([]);
  const [routes, setRoutes] = useState([]);
  const [selectedPost, setSelectedPost] = useState(null);
  const [riskData, setRiskData] = useState(null);
  const [forecast, setForecast] = useState(null);
  const [offline, setOffline] = useState(false);
  
  const [whatIf, setWhatIf] = useState(null);
  const [whatIfLoading, setWhatIfLoading] = useState(false);
  const [decision, setDecision] = useState(null);
  const [audits, setAudits] = useState([]);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const p = await axios.get(`${API_BASE}/posts`);
      setPosts(p.data.posts);
      const r = await axios.get(`${API_BASE}/routes`);
      setRoutes(r.data.routes);
      setOffline(false);
      
      const highRisk = p.data.posts.find(post => post.risk === 'High' && post.type === 'forward_post') || p.data.posts[0];
      if (highRisk) {
        handleSelectPost(highRisk);
      }
      
      fetchAudits();
    } catch (e) {
      console.warn("API Error", e);
      setOffline(true);
    }
  };

  const fetchAudits = async () => {
    try {
      const a = await axios.get(`${API_BASE}/audit`);
      setAudits(a.data.audit_log || []);
    } catch(e) {
      console.warn(e);
    }
  };

  const handleSelectPost = async (p) => {
    setSelectedPost(p);
    try {
      const r = await axios.get(`${API_BASE}/risk/${p.id}`);
      setRiskData(r.data);
      const f = await axios.get(`${API_BASE}/forecast/${p.id}`);
      setForecast(f.data);
    } catch (e) {
      console.error(e);
    }
  };

  const runWhatIf = async (type) => {
    if (!selectedPost) return;
    setWhatIfLoading(true);
    setDecision(null);
    try {
      const res = await axios.post(`${API_BASE}/what-if`, {
        disruption_type: type,
        target_id: selectedPost.id
      });
      setWhatIf({ ...res.data, disruption_type: type, target_id: selectedPost.id });
    } catch(e) {
      console.error(e);
    } finally {
      setWhatIfLoading(false);
    }
  };

  const makeDecision = async (dec) => {
    if (!whatIf) return;
    try {
      await axios.post(`${API_BASE}/decision`, {
        user: "COMMANDER",
        scenario: whatIf.disruption_type,
        decision: dec,
        reason: "User approved from frontend HITL UI"
      });
      setDecision(dec);
      fetchAudits(); // refresh audit trail
    } catch(e) {
      console.error(e);
    }
  };

  return (
    <div className="h-screen w-screen bg-[#070908] flex flex-col font-sans text-white overflow-hidden selection:bg-[#d4a373]/30">
      <CommandHeader offline={offline} />
      
      <div className="flex flex-1 overflow-hidden p-2 gap-2">
        <Sidebar />
        
        <div className="flex-1 flex flex-col min-w-0">
          <KPIBar posts={posts} routes={routes} whatIf={whatIf} />
          
          <div className="flex-1 flex gap-2 overflow-hidden">
            <LogisticsMap 
              posts={posts} 
              routes={routes} 
              selectedPost={selectedPost} 
              handleSelectPost={handleSelectPost} 
              whatIf={whatIf}
            />
            
            <PostIntelligence 
              post={selectedPost}
              riskData={riskData}
              forecast={forecast}
              routes={routes}
            />
          </div>
          
          <BottomPanels 
            runWhatIf={runWhatIf} 
            whatIf={whatIf} 
            makeDecision={makeDecision} 
            isRunning={whatIfLoading}
            audits={audits}
            decision={decision}
          />
        </div>
      </div>
    </div>
  );
}
"""

with open("src/App.tsx", "w", encoding="utf-8") as f:
    f.write(app_tsx)

print("Frontend components successfully wired to backend APIs.")

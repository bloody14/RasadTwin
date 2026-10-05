import os

base_dir = "src/components"
os.makedirs(base_dir, exist_ok=True)

components = {
    "CommandHeader.tsx": """import React from 'react';
import { Hexagon, Server, CheckCircle2 } from 'lucide-react';

export default function CommandHeader({ offline }) {
  return (
    <header className="bg-[#0f1511] border-b border-[#2a362c] text-white p-3 flex justify-between items-center z-10 relative shadow-md shrink-0">
      <div className="flex items-center gap-4">
        <Hexagon className="w-10 h-10 text-[#a3b18a] stroke-[1.5]" />
        <div>
          <h1 className="text-2xl font-bold tracking-widest text-white leading-tight">RASADTWIN</h1>
          <div className="text-[10px] text-[#84a59d] uppercase tracking-wider font-mono">Predictive Logistics Digital Twin</div>
        </div>
      </div>
      
      <div className="flex flex-col justify-center border-l border-[#2a362c] pl-6 ml-4">
        <h2 className="text-xl font-bold tracking-wide text-white">LOGISTICS COMMAND CENTRE</h2>
        <div className="text-xs text-[#a3b18a]">Uncertainty-Aware Predictive Logistics for Forward Formations</div>
      </div>

      <div className="flex-1"></div>

      <div className="flex items-center gap-4">
        <div className="flex items-center gap-3 bg-[#1c231e] border border-[#d4a373] px-3 py-1.5 rounded-sm">
          <Server className="w-5 h-5 text-[#d4a373]" />
          <div>
            <div className="text-[10px] text-[#d4a373] font-bold tracking-widest uppercase leading-tight">OFFLINE MODE</div>
            <div className="text-[9px] text-gray-400">Local Engine Active</div>
          </div>
        </div>
        
        <div className="flex items-center gap-3 bg-[#1c231e] border border-[#2a362c] px-3 py-1.5 rounded-sm">
          <div className="w-3 h-3 rounded-full bg-[#52b788] shadow-[0_0_8px_#52b788]"></div>
          <div>
            <div className="text-[10px] text-[#52b788] font-bold tracking-widest uppercase leading-tight">SYSTEM NOMINAL</div>
            <div className="text-[9px] text-gray-400">All Services Operational</div>
          </div>
        </div>

        <div className="text-right ml-4 border-l border-[#2a362c] pl-4">
          <div className="text-xs text-white">17 Nov 2025</div>
          <div className="text-sm font-mono text-white font-bold">16:42:18</div>
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
  const kpis = [
    { icon: Users, iconColor: 'text-[#52b788]', label: 'FORWARD POSTS', value: '12' },
    { icon: AlertTriangle, iconColor: 'text-[#e63946]', label: 'AT RISK', value: '03', highlight: true },
    { icon: PackageSearch, iconColor: 'text-[#d4a373]', label: 'STOCK-OUT WATCH', value: '02' },
    { icon: Truck, iconColor: 'text-[#457b9d]', label: 'ACTIVE ROUTES', value: '09' },
    { icon: CloudLightning, iconColor: 'text-[#e63946]', label: 'DISRUPTIONS', value: '01', highlight: true },
    { icon: FileCheck, iconColor: 'text-[#d4a373]', label: 'DECISIONS PENDING', value: '02' },
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
  return (
    <div className="flex-1 relative bg-[#0b0f0c] border border-[#2a362c] rounded overflow-hidden flex flex-col">
      <div className="p-3 border-b border-[#2a362c] bg-[#131915] flex justify-between items-center z-10">
        <h3 className="text-xs text-white font-bold tracking-widest uppercase">LOGISTICS NETWORK MAP <span className="text-gray-500 font-normal lowercase">(Offline)</span></h3>
      </div>
      
      <div className="flex-1 relative bg-[#1c231e]">
        <div className="absolute inset-0 opacity-40 mix-blend-overlay bg-black"></div>
        
        {/* Map Overlays and SVG */}
        <div className="absolute inset-0 pointer-events-auto">
          <svg viewBox="73 30 5 5" className="w-full h-full drop-shadow-[0_5px_5px_rgba(0,0,0,0.8)]">
            {/* Routes */}
            {routes.map(r => {
              const src = posts.find(p => p.id === r.source);
              const tgt = posts.find(p => p.id === r.target);
              const isAffected = r.target === 'F-07' || r.source === 'F-07';
              if (!src || !tgt) return null;
              
              let strokeDasharray = "";
              if (r.mode === "Mule") strokeDasharray = "0.04 0.04";
              if (r.mode === "Heli") strokeDasharray = "0.02 0.04";
              if (r.mode === "Drone") strokeDasharray = "0.01 0.02";

              return (
                <g key={r.id}>
                  <line x1={src.lng} y1={src.lat} x2={tgt.lng} y2={tgt.lat} 
                        stroke={isAffected ? "#e63946" : "#84a59d"} 
                        strokeWidth={isAffected ? "0.02" : "0.015"} 
                        strokeDasharray={strokeDasharray} />
                </g>
              )
            })}

            {/* Disruption Icon */}
            <g transform="translate(76.2, 32.5)">
              <circle r="0.1" fill="#e63946" className="animate-ping opacity-50" />
              <circle r="0.05" fill="#1c231e" stroke="#e63946" strokeWidth="0.02" />
              <line x1="-0.02" y1="-0.02" x2="0.02" y2="0.02" stroke="#e63946" strokeWidth="0.01" />
              <line x1="0.02" y1="-0.02" x2="-0.02" y2="0.02" stroke="#e63946" strokeWidth="0.01" />
              <text x="0.08" y="0.02" fill="#e63946" fontSize="0.08" fontFamily="sans-serif" fontWeight="bold" className="drop-shadow-lg bg-[#1c231e]">PASS-01 (CLOSED)</text>
            </g>

            {/* Nodes */}
            {posts.map(p => {
              const isSelected = p.id === selectedPost?.id || p.id === 'F-07';
              const isHighRisk = p.risk === 'High' || p.id === 'F-07';
              
              let fill = p.type === 'rear_depot' ? '#457b9d' : p.type === 'intermediate_depot' ? '#f4a261' : (isHighRisk ? '#e63946' : '#52b788');

              return (
                <g key={p.id} transform={`translate(${p.lng}, ${p.lat})`} className="cursor-pointer" onClick={() => handleSelectPost(p)}>
                  {isSelected && (
                    <circle r="0.25" fill="none" stroke="#e63946" strokeWidth="0.01" className="animate-pulse" />
                  )}
                  {isHighRisk && (
                    <circle r="0.15" fill="none" stroke="#e63946" strokeWidth="0.02" className="animate-pulse opacity-50" />
                  )}
                  
                  {p.type === 'rear_depot' ? (
                    <rect x="-0.05" y="-0.05" width="0.1" height="0.1" fill={fill} />
                  ) : p.type === 'intermediate_depot' ? (
                    <polygon points="0,-0.08 0.08,0.04 -0.08,0.04" fill={fill} />
                  ) : (
                    <circle r="0.05" fill={fill} />
                  )}
                  
                  <text x="0.1" y="0.03" fill="#fff" fontSize="0.08" fontFamily="sans-serif" fontWeight="bold" className="pointer-events-none drop-shadow-md">
                    {p.id}
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

        <div className="absolute bottom-4 right-4 text-[10px] text-gray-400 flex items-center gap-2 font-mono">
          <span>0</span>
          <div className="flex w-32 border-b border-l border-r border-gray-500 h-1 relative">
             <div className="absolute top-0 left-1/3 h-1 w-px bg-gray-500"></div>
             <div className="absolute top-0 left-2/3 h-1 w-px bg-gray-500"></div>
          </div>
          <span>30 km</span>
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
    post = { id: 'F-07', name: 'Forward Post F-07' };
  }

  const chartData = [
    {name: 'Nov 17', actual: 60},
    {name: '18', actual: 65, forecast: 65, lower: 55, upper: 75},
    {name: '19', forecast: 70, lower: 50, upper: 90},
    {name: '20', forecast: 68, lower: 48, upper: 88},
    {name: '21', forecast: 72, lower: 52, upper: 92},
    {name: '22', forecast: 75, lower: 55, upper: 95},
    {name: '23', forecast: 80, lower: 60, upper: 100},
    {name: '24', forecast: 78, lower: 58, upper: 98},
  ];

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
            <AlertTriangle className="w-6 h-6 text-[#e63946]" />
            <div>
              <div className="flex items-baseline gap-2">
                <h2 className="text-3xl font-bold text-white font-mono leading-none">F-07</h2>
                <span className="text-[10px] text-gray-400 uppercase tracking-widest">FORWARD POST</span>
              </div>
              <div className="text-[10px] text-gray-400 mt-1">Alt: 4,320 m | Region: North | Type: Infantry Post</div>
            </div>
          </div>
          <div className="bg-[#e63946] text-white text-[10px] px-3 py-1 rounded font-bold tracking-widest">AT RISK</div>
        </div>

        <div className="grid grid-cols-3 gap-3 mt-4">
          <div className="bg-[#1c231e] border border-[#2a362c] p-2 rounded text-center">
            <div className="text-xl font-mono font-bold text-[#e63946]">2.4</div>
            <div className="text-[9px] text-[#e63946] uppercase mt-1">Days of Supply</div>
          </div>
          <div className="bg-[#e63946]/10 border border-[#e63946] p-2 rounded text-center">
            <div className="text-xl font-mono font-bold text-[#e63946]">HIGH</div>
            <div className="text-[9px] text-[#e63946] uppercase mt-1">Stock-out Risk</div>
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
        <div className="flex-1 py-2 text-center text-gray-500 hover:text-gray-300 cursor-pointer">Weather</div>
        <div className="flex-1 py-2 text-center text-gray-500 hover:text-gray-300 cursor-pointer">Explainability</div>
      </div>

      <div className="p-4 space-y-4">
        {/* CHART */}
        <div>
          <h4 className="text-[10px] text-white font-bold tracking-widest mb-2 uppercase">DEMAND FORECAST <span className="text-gray-500 font-normal">(NEXT 7 DAYS)</span></h4>
          <div className="flex gap-4 mb-2 text-[9px] text-gray-400 uppercase tracking-widest">
            <span className="flex items-center gap-1"><div className="w-2 h-2 bg-gray-500"></div> Historical</span>
            <span className="flex items-center gap-1"><div className="w-2 h-2 bg-[#457b9d]"></div> Forecast (Median)</span>
            <span className="flex items-center gap-1"><div className="w-2 h-2 bg-[#457b9d]/30 border border-[#457b9d]"></div> Uncertainty (80%)</span>
          </div>
          <div className="h-32 w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={chartData} margin={{ top: 5, right: 0, left: -25, bottom: 0 }}>
                <CartesianGrid stroke="#2a362c" strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="name" tick={{fontSize: 9, fill: '#6b7280'}} axisLine={false} tickLine={false} />
                <YAxis tick={{fontSize: 9, fill: '#6b7280'}} axisLine={false} tickLine={false} domain={[0, 120]} ticks={[0, 40, 80, 120]} />
                <RechartsTooltip contentStyle={{ backgroundColor: '#131915', borderColor: '#2a362c', fontSize: '10px' }} />
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
            <h4 className="text-[10px] text-white font-bold tracking-widest mb-3 uppercase">ROUTE TO F-07</h4>
            <div className="flex items-center gap-3 mb-3">
              <div className="text-[#457b9d]"><TruckIcon /></div>
              <div className="text-[10px] text-gray-400">Mode: <span className="text-white">Road → Mule</span></div>
              <div className="ml-auto w-10 h-10 relative flex items-center justify-center">
                <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
                  <circle cx="18" cy="18" r="16" fill="none" stroke="#1c231e" strokeWidth="3" />
                  <circle cx="18" cy="18" r="16" fill="none" stroke="#52b788" strokeWidth="3" strokeDasharray="78, 100" />
                </svg>
                <span className="absolute text-[10px] font-bold text-white">78%</span>
              </div>
            </div>
            <div className="text-[8px] text-gray-500 uppercase text-right -mt-2 mb-3">Route Health</div>
            
            <div className="flex gap-4">
              <div>
                <div className="text-[9px] text-[#457b9d] uppercase">Nominal ETA</div>
                <div className="font-mono text-white text-sm font-bold">04:52</div>
              </div>
              <div>
                <div className="text-[9px] text-[#e63946] uppercase">Robust ETA</div>
                <div className="font-mono text-[#e63946] text-sm font-bold">05:41 <span className="text-[9px]">(+49 min)</span></div>
              </div>
            </div>
          </div>
          
          {/* SHAP & RISK */}
          <div>
            <div className="mb-4">
              <div className="flex justify-between items-end mb-1">
                <h4 className="text-[10px] text-white font-bold tracking-widest uppercase">STOCK-OUT RISK</h4>
                <span className="text-[9px] text-[#e63946]">2.4 days ▼</span>
              </div>
              <div className="relative h-2 w-full bg-gradient-to-r from-[#52b788] via-[#d4a373] to-[#e63946] rounded-sm mt-2">
                <div className="absolute top-[-4px] bottom-[-4px] w-1 bg-white shadow-[0_0_5px_white] left-[85%] rounded-full"></div>
              </div>
              <div className="flex justify-between text-[8px] text-gray-500 uppercase mt-1">
                <span>Safe</span>
                <span>Watch</span>
                <span>Critical</span>
              </div>
              <div className="flex justify-between text-[8px] text-gray-500 mt-0.5">
                <span>0</span>
                <span>5</span>
                <span>10</span>
                <span>15</span>
              </div>
            </div>
            
            <div>
              <h4 className="text-[10px] text-white font-bold tracking-widest mb-2 uppercase">TOP CONTRIBUTING FACTORS <span className="text-gray-500 font-normal">(SHAP)</span></h4>
              <div className="space-y-1.5 text-[9px] font-mono">
                <div className="flex items-center gap-2">
                  <span className="w-20 text-gray-400 truncate">Forecast demand</span>
                  <div className="flex-1 bg-[#1c231e] h-2 rounded-sm"><div className="bg-[#e63946] h-full rounded-sm" style={{width:'71%'}}></div></div>
                  <span className="text-[#e63946]">+0.71</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="w-20 text-gray-400 truncate">Days of supply</span>
                  <div className="flex-1 bg-[#1c231e] h-2 rounded-sm"><div className="bg-[#d4a373] h-full rounded-sm" style={{width:'52%'}}></div></div>
                  <span className="text-[#d4a373]">+0.52</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="w-20 text-gray-400 truncate">Road delay</span>
                  <div className="flex-1 bg-[#1c231e] h-2 rounded-sm"><div className="bg-[#d4a373] h-full rounded-sm" style={{width:'31%'}}></div></div>
                  <span className="text-[#d4a373]">+0.31</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="w-20 text-gray-400 truncate">Weather impact</span>
                  <div className="flex-1 bg-[#1c231e] h-2 rounded-sm"><div className="bg-[#457b9d] h-full rounded-sm" style={{width:'18%'}}></div></div>
                  <span className="text-[#457b9d]">+0.18</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* RECOMMENDED ACTION */}
        <div className="mt-2 border border-[#d4a373]/30 rounded p-3 flex gap-3 relative overflow-hidden">
          <div className="absolute inset-0 bg-[#d4a373]/5"></div>
          <div className="text-[#d4a373] pt-1 z-10"><Lightbulb className="w-5 h-5 fill-[#d4a373]/20" /></div>
          <div className="z-10">
            <div className="text-[9px] text-[#d4a373] uppercase tracking-widest mb-1 font-bold">RECOMMENDED ACTION</div>
            <div className="text-sm font-bold text-[#d4a373] mb-1 tracking-widest">LOCAL REPLAN</div>
            <div className="text-[10px] text-gray-400 leading-tight">Closure affects 3 downstream posts<br/>but does not compromise the wider network.</div>
          </div>
          <div className="ml-auto self-center text-[#d4a373] z-10">→</div>
        </div>
      </div>
    </div>
  );
}

function TruckIcon() {
  return <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="1" y="3" width="15" height="13"></rect><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"></polygon><circle cx="5.5" cy="18.5" r="2.5"></circle><circle cx="18.5" cy="18.5" r="2.5"></circle></svg>;
}
""",
    "BottomPanels.tsx": """import React from 'react';
import { AlertTriangle, GitMerge, CheckCircle, ShieldAlert } from 'lucide-react';

export default function BottomPanels({ runWhatIf, whatIf, makeDecision }) {
  return (
    <div className="grid grid-cols-12 gap-2 mt-2 shrink-0">
      
      {/* WHAT-IF DISRUPTION ANALYSIS */}
      <div className="col-span-3 bg-[#0b0f0c] border border-[#2a362c] rounded p-3 flex flex-col">
        <h3 className="text-[10px] text-white font-bold tracking-widest uppercase flex items-center gap-2 mb-3">
          <AlertTriangle className="w-3 h-3 text-gray-400" /> WHAT-IF DISRUPTION ANALYSIS
        </h3>
        
        <div className="flex gap-1 mb-3">
          <button className="flex-1 bg-[#e63946]/20 border border-[#e63946] text-[#e63946] text-[9px] py-1.5 rounded uppercase tracking-widest font-bold">ROAD CLOSURE</button>
          <button className="flex-1 bg-[#1c231e] border border-[#2a362c] text-gray-400 hover:text-white text-[9px] py-1.5 rounded uppercase tracking-widest">HEAVY SNOW</button>
          <button className="flex-1 bg-[#1c231e] border border-[#2a362c] text-gray-400 hover:text-white text-[9px] py-1.5 rounded uppercase tracking-widest">HELI GROUNDING</button>
        </div>

        <div className="bg-[#e63946]/5 border border-[#e63946]/30 rounded p-2 flex items-start gap-2 mb-3">
          <AlertTriangle className="w-4 h-4 text-[#e63946] shrink-0 mt-0.5" />
          <div>
            <div className="text-[9px] text-[#e63946] font-bold">Selected Scenario: Road Closure</div>
            <div className="text-[8px] text-gray-400">Simulating impact on logistics network...</div>
          </div>
        </div>

        <div className="grid grid-cols-3 gap-2 text-center mb-4">
          <div>
            <div className="text-[8px] text-gray-500 uppercase">IMPACT SCORE</div>
            <div className="text-2xl font-mono text-[#e63946] font-bold">64</div>
            <div className="text-[8px] text-[#e63946]">(Moderate-High)</div>
          </div>
          <div>
            <div className="text-[8px] text-gray-500 uppercase">AFFECTED POSTS</div>
            <div className="text-2xl font-mono text-[#e63946] font-bold mt-1">3</div>
          </div>
          <div>
            <div className="text-[8px] text-gray-500 uppercase">AFFECTED LEGS</div>
            <div className="text-2xl font-mono text-[#e63946] font-bold mt-1">2</div>
          </div>
        </div>

        <div className="mt-auto">
          <div className="text-[9px] text-white font-bold uppercase mb-2">RECOMMENDED SCOPE</div>
          <div className="flex gap-1">
            <div className="flex-1 bg-[#1c231e] border border-[#2a362c] rounded p-1.5 text-center">
              <div className="text-[9px] text-white font-bold tracking-widest">PRESERVE</div>
              <div className="text-[7px] text-gray-500 mt-1">Keep current plan</div>
            </div>
            <div className="flex-1 bg-[#d4a373]/10 border border-[#d4a373] rounded p-1.5 text-center relative overflow-hidden flex flex-col justify-between">
              <div className="text-[9px] text-[#d4a373] font-bold tracking-widest flex items-center justify-center gap-1">
                <CheckCircle className="w-2.5 h-2.5" /> LOCAL
              </div>
              <div className="text-[7px] text-gray-300 mb-3 mt-1">Replan affected region</div>
              <div className="absolute bottom-0 left-0 right-0 bg-[#d4a373] text-[#0b0f0c] text-[8px] font-bold py-0.5">Recommended</div>
            </div>
            <div className="flex-1 bg-[#1c231e] border border-[#2a362c] rounded p-1.5 text-center">
              <div className="text-[9px] text-white font-bold tracking-widest">GLOBAL</div>
              <div className="text-[7px] text-gray-500 mt-1">De-optimize complete network</div>
            </div>
          </div>
        </div>
      </div>

      {/* BEFORE / AFTER COMPARISON */}
      <div className="col-span-5 bg-[#0b0f0c] border border-[#2a362c] rounded p-3 flex flex-col">
        <h3 className="text-[10px] text-white font-bold tracking-widest uppercase flex items-center gap-2 mb-3">
          <GitMerge className="w-3 h-3 text-gray-400" /> BEFORE / AFTER COMPARISON <span className="text-gray-500 font-normal lowercase tracking-normal">(Synthetic Scenario)</span>
        </h3>
        
        <div className="grid grid-cols-2 gap-3 mb-3 flex-1">
          <div className="bg-[#1c231e] border border-[#2a362c] rounded p-2 flex flex-col relative overflow-hidden">
            <div className="absolute top-0 left-0 right-0 h-1 bg-[#e63946]/50"></div>
            <div className="text-[9px] text-[#e63946] font-bold uppercase tracking-widest mb-2 mt-1">BEFORE (Current Plan)</div>
            
            <div className="flex justify-center mb-2 text-white font-mono text-[9px] items-center gap-2">
               D-01 <span className="text-gray-500">→</span> <div className="w-2 h-2 rounded-full bg-[#52b788] inline-block border border-black"></div> F-07
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
              <div className="flex justify-between"><span className="text-gray-500">ETA</span><span className="text-white">04:52</span></div>
              <div className="flex justify-between"><span className="text-gray-500">Affected Posts</span><span className="text-[#e63946]">F-07, F-08</span></div>
              <div className="flex justify-between"><span className="text-gray-500">Stock-out Risk</span><span className="text-[#e63946] font-bold">HIGH</span></div>
            </div>
          </div>
          
          <div className="bg-[#1c231e] border border-[#2a362c] rounded p-2 flex flex-col relative overflow-hidden">
            <div className="absolute top-0 left-0 right-0 h-1 bg-[#52b788]/50"></div>
            <div className="text-[9px] text-[#52b788] font-bold uppercase tracking-widest mb-2 mt-1">AFTER (Replanned)</div>
            
            <div className="flex justify-center mb-2 text-white font-mono text-[9px] items-center gap-2">
               D-01 <span className="text-gray-500">→</span> <div className="w-2 h-2 border border-[#457b9d] inline-block"></div> <span className="text-gray-500">→</span> <div className="w-2 h-2 rounded-full bg-[#d4a373] inline-block"></div> F-07
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
              <div className="flex justify-between"><span className="text-gray-500">Route</span><span className="text-[#457b9d]">Road → Mule</span></div>
              <div className="flex justify-between"><span className="text-gray-500">ETA</span><span className="text-[#457b9d] font-bold">05:21 (+29 min)</span></div>
              <div className="flex justify-between"><span className="text-gray-500">Affected Posts</span><span className="text-white">F-07</span></div>
              <div className="flex justify-between"><span className="text-gray-500">Stock-out Risk</span><span className="text-[#d4a373] font-bold">MEDIUM</span></div>
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
            <div className="bg-[#52b788]/10 border border-[#52b788] text-[#52b788] text-[7px] px-1 py-0.5 rounded flex items-center gap-1 font-bold">
              <CheckCircle className="w-2 h-2" /> Synthetic Results<br/>(Demo Data)
            </div>
          </div>
        </div>
      </div>

      {/* COMMAND DECISION */}
      <div className="col-span-4 bg-[#0b0f0c] border border-[#2a362c] rounded p-3 flex flex-col">
        <h3 className="text-[10px] text-white font-bold tracking-widest uppercase mb-3 flex justify-between items-center">
          <span>COMMAND DECISION <span className="text-gray-500 font-normal lowercase tracking-normal">(Human-in-the-Loop)</span></span>
        </h3>
        
        <div className="bg-[#d4a373]/10 border border-[#d4a373]/30 rounded p-2 text-[9px] text-[#d4a373] flex items-center gap-2 mb-3">
          <ShieldAlert className="w-3 h-3" /> <span className="font-bold tracking-wide">Human approval required for re-planning.</span>
        </div>

        <div className="flex justify-between mb-3 border-b border-[#2a362c] pb-2">
          <div>
            <div className="text-[8px] text-[#457b9d] uppercase mb-0.5">Recommended Action</div>
            <div className="text-xs text-white font-bold tracking-widest">LOCAL REPLAN</div>
          </div>
          <div className="text-right">
            <div className="text-[8px] text-gray-500 uppercase mb-0.5">Reason</div>
            <div className="text-[9px] text-gray-300">Impact threshold exceeded (Score: 64)</div>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-2 mb-3">
          <button className="col-span-1 bg-[#52b788]/20 border border-[#52b788] hover:bg-[#52b788] text-[#52b788] hover:text-[#0b0f0c] py-2 rounded text-[10px] font-bold tracking-widest flex items-center justify-center gap-1 transition-colors">
            <CheckCircle className="w-3 h-3" /> APPROVE
          </button>
          <div className="col-span-1 grid grid-cols-2 gap-2">
            <button className="bg-[#d4a373]/10 border border-[#d4a373]/50 hover:border-[#d4a373] text-[#d4a373] py-2 rounded text-[10px] font-bold tracking-widest flex items-center justify-center gap-1 transition-colors">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21.5 2v6h-6M2.13 15.57a10 10 0 1 0 4.43-12.18L2 7"/></svg>
              OVERRIDE
            </button>
            <button className="bg-[#e63946]/10 border border-[#e63946]/50 hover:border-[#e63946] text-[#e63946] py-2 rounded text-[10px] font-bold tracking-widest flex items-center justify-center gap-1 transition-colors">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
              REJECT
            </button>
          </div>
        </div>

        <div className="mt-auto bg-[#131915] rounded p-2">
          <div className="flex justify-between items-center mb-2">
            <div className="text-[9px] text-gray-400 uppercase tracking-widest font-bold">AUDIT TRAIL <span className="text-gray-600 lowercase font-normal">(Recent Events)</span></div>
            <div className="text-[8px] text-[#457b9d] cursor-pointer hover:underline">View All →</div>
          </div>
          <div className="space-y-1.5 font-mono text-[8.5px]">
            <div className="flex gap-2 text-gray-400"><span className="text-[#d4a373]">▶</span> 16:42:18 <span className="w-12 text-gray-500">SYSTEM</span> <span className="truncate">Road closure detected on Pass-01</span></div>
            <div className="flex gap-2 text-gray-400"><span className="text-[#d4a373]">▶</span> 16:42:19 <span className="w-12 text-gray-500">ENGINE</span> <span className="truncate">Impact score = 64 (LOCAL recommended)</span></div>
            <div className="flex gap-2 text-white bg-[#1c231e] px-1 -mx-1 rounded"><span className="text-[#52b788]">▶</span> 16:42:22 <span className="w-12 text-[#457b9d]">COMMANDER</span> <span className="truncate">Approved LOCAL replan</span></div>
            <div className="flex gap-2 text-gray-400"><span className="text-[#d4a373]">▶</span> 16:42:23 <span className="w-12 text-gray-500">SYSTEM</span> <span className="truncate">New route generated (Road → Mule)</span></div>
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
  const [decision, setDecision] = useState(null);

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
      
      // Auto-select first High risk post for visual demo to match the image
      const highRisk = p.data.posts.find(post => post.id === 'F-07' || post.risk === 'High');
      if (highRisk) {
        handleSelectPost(highRisk);
        setWhatIf(true); // Mock What-If activated to show bottom panels
      }
    } catch (e) {
      console.warn("API Error", e);
      setOffline(true);
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

  const runWhatIf = async (type) => {};
  const makeDecision = async (dec) => {};

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
          
          <BottomPanels runWhatIf={runWhatIf} whatIf={whatIf} makeDecision={makeDecision} />
        </div>
      </div>
    </div>
  );
}
"""

with open("src/App.tsx", "w", encoding="utf-8") as f:
    f.write(app_tsx)

print("Frontend components regenerated matching detailed image.")

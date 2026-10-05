import os

base_dir = "src/components"
os.makedirs(base_dir, exist_ok=True)

components = {
    "Sidebar.tsx": """import React from 'react';
import { LayoutDashboard, MapPin, TrendingUp, PackageSearch, GitMerge, Settings2, ShieldCheck, ListTodo } from 'lucide-react';

export default function Sidebar({ activeView, setActiveView }) {
  const items = [
    { id: 'COMMAND', icon: LayoutDashboard, label: 'COMMAND' },
    { id: 'POSTS', icon: MapPin, label: 'POSTS' },
    { id: 'FORECAST', icon: TrendingUp, label: 'FORECAST' },
    { id: 'INVENTORY', icon: PackageSearch, label: 'INVENTORY' },
    { id: 'ROUTING', icon: GitMerge, label: 'ROUTING' },
    { id: 'WHAT_IF', icon: Settings2, label: 'WHAT-IF' },
    { id: 'DECISIONS', icon: ShieldCheck, label: 'DECISIONS' },
    { id: 'AUDIT', icon: ListTodo, label: 'AUDIT' },
  ];

  return (
    <div className="w-[200px] bg-[#0b0f0c] border border-[#2a362c] flex flex-col justify-between shrink-0 rounded">
      <div className="py-2">
        {items.map((it) => (
          <button key={it.id} onClick={() => setActiveView(it.id)} className={`w-full flex items-center gap-4 px-6 py-4 transition-colors ${activeView === it.id ? 'bg-[#d4a373]/10 text-[#d4a373] border-l-2 border-[#d4a373]' : 'text-gray-400 hover:bg-[#1c231e] hover:text-white border-l-2 border-transparent'}`}>
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
    "LogisticsMap.tsx": """import React, { useState } from 'react';
import { Layers, Cloud, Map as MapIcon, Tag } from 'lucide-react';

export default function LogisticsMap({ posts, routes, selectedPost, handleSelectPost, whatIf }) {
  const [hoveredNode, setHoveredNode] = useState(null);

  const lats = posts.map(p => p.lat);
  const lngs = posts.map(p => p.lng);
  
  const minLat = Math.min(...lats, 32.0);
  const maxLat = Math.max(...lats, 34.5);
  const minLng = Math.min(...lngs, 75.0);
  const maxLng = Math.max(...lngs, 77.5);
  
  return (
    <div className="flex-1 relative bg-[#0b0f0c] border border-[#2a362c] rounded overflow-hidden flex flex-col">
      <div className="p-3 border-b border-[#2a362c] bg-[#131915] flex justify-between items-center z-10">
        <h3 className="text-xs text-white font-bold tracking-widest uppercase">LOGISTICS NETWORK MAP <span className="text-gray-500 font-normal lowercase">(Offline)</span></h3>
      </div>
      
      <div className="flex-1 relative bg-[#1c231e]">
        <div className="absolute inset-0 opacity-40 mix-blend-overlay bg-black pointer-events-none"></div>
        
        <div className="absolute inset-0 pointer-events-auto overflow-hidden">
          <svg viewBox={`${minLng-0.5} ${-(maxLat+0.5)} ${maxLng-minLng+1} ${maxLat-minLat+1}`} className="w-full h-full drop-shadow-[0_5px_5px_rgba(0,0,0,0.8)]">
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

            {whatIf && whatIf.target_id && (
              posts.filter(p => p.id === whatIf.target_id).map(tgt => (
                 <g key="disruption" transform={`translate(${tgt.lng}, ${-tgt.lat})`}>
                    <circle r="0.15" fill="#e63946" className="animate-ping opacity-50 pointer-events-none" />
                    <circle r="0.08" fill="#1c231e" stroke="#e63946" strokeWidth="0.02" pointer-events-none />
                    <line x1="-0.03" y1="-0.03" x2="0.03" y2="0.03" stroke="#e63946" strokeWidth="0.015" />
                    <line x1="0.03" y1="-0.03" x2="-0.03" y2="0.03" stroke="#e63946" strokeWidth="0.015" />
                    <text x="0.12" y="0.02" fill="#e63946" fontSize="0.1" fontFamily="sans-serif" fontWeight="bold" className="drop-shadow-lg bg-[#1c231e] pointer-events-none">{whatIf.disruption_type}</text>
                 </g>
              ))
            )}

            {posts.map(p => {
              const isSelected = p.id === selectedPost?.id;
              const isHighRisk = p.risk === 'High';
              const isHovered = hoveredNode === p.id;
              
              let fill = p.type === 'rear_depot' ? '#457b9d' : p.type === 'intermediate_depot' ? '#f4a261' : (isHighRisk ? '#e63946' : '#52b788');

              return (
                <g key={p.id} transform={`translate(${p.lng}, ${-p.lat})`} 
                   className="cursor-pointer" 
                   onClick={() => handleSelectPost(p)}
                   onMouseEnter={() => setHoveredNode(p.id)}
                   onMouseLeave={() => setHoveredNode(null)}>
                  
                  {/* Invisible hit area */}
                  <circle r="0.15" fill="transparent" />

                  {isSelected && (
                    <circle r="0.25" fill="none" stroke="#e63946" strokeWidth="0.015" className="animate-pulse" pointer-events="none" />
                  )}
                  {isHighRisk && !isSelected && (
                    <circle r="0.15" fill="none" stroke="#e63946" strokeWidth="0.02" className="animate-pulse opacity-50" pointer-events="none" />
                  )}
                  {isHovered && !isSelected && (
                    <circle r="0.18" fill="none" stroke="#d4a373" strokeWidth="0.01" pointer-events="none" />
                  )}
                  
                  {p.type === 'rear_depot' ? (
                    <rect x="-0.06" y="-0.06" width="0.12" height="0.12" fill={fill} pointer-events="none" />
                  ) : p.type === 'intermediate_depot' ? (
                    <polygon points="0,-0.1 0.1,0.05 -0.1,0.05" fill={fill} pointer-events="none" />
                  ) : (
                    <circle r="0.06" fill={fill} pointer-events="none" />
                  )}
                  
                  <text x="0.12" y="0.03" fill={isHovered ? "#d4a373" : "#fff"} fontSize="0.1" fontFamily="sans-serif" fontWeight="bold" className="pointer-events-none drop-shadow-md">
                    {p.id.replace('FP-00', 'F-0')}
                  </text>

                  {isHovered && (
                     <g transform="translate(0, 0.15)">
                        <rect x="-0.3" y="0" width="0.6" height="0.15" fill="#0b0f0c" rx="0.02" stroke="#2a362c" strokeWidth="0.01"/>
                        <text x="0" y="0.1" fill="#fff" fontSize="0.06" fontFamily="sans-serif" textAnchor="middle">{p.name}</text>
                     </g>
                  )}
                </g>
              );
            })}
          </svg>
        </div>

        {/* Legend */}
        <div className="absolute top-4 left-4 bg-[#0b0f0c]/90 border border-[#2a362c] p-3 rounded backdrop-blur-sm z-10 w-48 pointer-events-none">
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
      </div>
    </div>
  );
}
""",
    "PostIntelligence.tsx": """import React, { useState } from 'react';
import { AlertTriangle, TrendingUp, Info, Lightbulb, Loader2, Target, ShieldAlert } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer } from 'recharts';

export default function PostIntelligence({ post, riskData, forecast, routes, isLoading }) {
  const [activeTab, setActiveTab] = useState('FORECAST');

  if (!post) {
    return (
      <div className="w-[480px] bg-[#0b0f0c] border border-[#2a362c] rounded flex items-center justify-center text-gray-500 shrink-0">
        <p className="text-xs uppercase tracking-widest">Select Node for Intelligence</p>
      </div>
    );
  }

  const isHighRisk = post.risk === 'High' || riskData?.overall_state === 'High';
  const dos = riskData?.days_of_supply || post.dos || 0;
  const primaryRoute = routes.find(r => r.target === post.id) || { mode: 'Unknown', eta_hrs: 0, robust_eta_hrs: 0, risk: 'Low' };

  return (
    <div className="w-[480px] bg-[#0b0f0c] border border-[#2a362c] rounded flex flex-col shrink-0 overflow-y-auto custom-scrollbar relative">
      {isLoading && (
        <div className="absolute inset-0 bg-[#0b0f0c]/80 z-20 flex flex-col items-center justify-center gap-3">
          <Loader2 className="w-8 h-8 text-[#d4a373] animate-spin" />
          <div className="text-xs text-[#d4a373] tracking-widest uppercase font-bold">Fetching Post Intelligence...</div>
        </div>
      )}
      
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
              <div className="text-[10px] text-gray-400 mt-1">{post.name} | Priority: {post.priority}</div>
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
        {['FORECAST', 'INVENTORY', 'ROUTE', 'EXPLAINABILITY'].map(t => (
          <div key={t} onClick={() => setActiveTab(t)} className={`flex-1 py-2 text-center cursor-pointer transition-colors ${activeTab === t ? 'text-[#d4a373] border-b-2 border-[#d4a373] bg-[#d4a373]/5' : 'text-gray-500 hover:text-gray-300'}`}>
            {t}
          </div>
        ))}
      </div>

      <div className="p-4 flex-1 overflow-y-auto custom-scrollbar relative">
        {activeTab === 'FORECAST' && <ForecastTab forecast={forecast} />}
        {activeTab === 'INVENTORY' && <InventoryTab post={post} riskData={riskData} />}
        {activeTab === 'ROUTE' && <RouteTab route={primaryRoute} post={post} />}
        {activeTab === 'EXPLAINABILITY' && <ExplainabilityTab riskData={riskData} dos={dos} />}

        {/* RECOMMENDED ACTION */}
        {isHighRisk && (
          <div className="mt-4 border border-[#d4a373]/30 rounded p-3 flex gap-3 relative overflow-hidden">
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

function ForecastTab({ forecast }) {
  if (!forecast) return <div className="text-gray-500 text-xs">No forecast data</div>;
  
  const chartData = [
    ...(forecast.history || []).map(d => ({ name: d.day.replace('D',''), actual: d.demand })),
    ...(forecast.future || []).map(d => ({ name: d.day.replace('D',''), forecast: d.forecast, lower: d.lower, upper: d.upper }))
  ];

  return (
    <div>
      <h4 className="text-[10px] text-white font-bold tracking-widest mb-2 uppercase">DEMAND FORECAST <span className="text-gray-500 font-normal">(API DATA)</span></h4>
      <div className="flex gap-4 mb-2 text-[9px] text-gray-400 uppercase tracking-widest">
        <span className="flex items-center gap-1"><div className="w-2 h-2 bg-gray-500"></div> Historical</span>
        <span className="flex items-center gap-1"><div className="w-2 h-2 bg-[#457b9d]"></div> Forecast (Median)</span>
        <span className="flex items-center gap-1"><div className="w-2 h-2 bg-[#457b9d]/30 border border-[#457b9d]"></div> Uncertainty (90%)</span>
      </div>
      <div className="h-40 w-full mt-4">
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
  );
}

function InventoryTab({ post, riskData }) {
  return (
    <div className="space-y-4">
      <h4 className="text-[10px] text-white font-bold tracking-widest uppercase">INVENTORY DETAILS</h4>
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-[#1c231e] p-3 rounded border border-[#2a362c]">
          <div className="text-[9px] text-gray-500 uppercase mb-1">Current Stock</div>
          <div className="text-lg font-mono text-white">4,200 kg</div>
        </div>
        <div className="bg-[#1c231e] p-3 rounded border border-[#2a362c]">
          <div className="text-[9px] text-gray-500 uppercase mb-1">Target Stock</div>
          <div className="text-lg font-mono text-[#457b9d]">8,500 kg</div>
        </div>
        <div className="bg-[#1c231e] p-3 rounded border border-[#2a362c]">
          <div className="text-[9px] text-gray-500 uppercase mb-1">Consumption Rate</div>
          <div className="text-lg font-mono text-white">840 kg/day</div>
        </div>
        <div className="bg-[#1c231e] p-3 rounded border border-[#2a362c]">
          <div className="text-[9px] text-gray-500 uppercase mb-1">Stock-out Risk</div>
          <div className="text-lg font-mono text-[#e63946]">{riskData?.stock_out_risk || 'Unknown'}</div>
        </div>
      </div>
    </div>
  );
}

function RouteTab({ route, post }) {
  return (
    <div className="space-y-4">
      <h4 className="text-[10px] text-white font-bold tracking-widest uppercase">ROUTE STATUS</h4>
      <div className="flex items-center gap-3 mb-3 bg-[#1c231e] p-4 rounded border border-[#2a362c]">
        <div className="text-[#457b9d]"><Target /></div>
        <div className="text-[10px] text-gray-400">Mode: <span className="text-white text-base font-bold ml-1">{route.mode}</span></div>
        <div className="ml-auto w-10 h-10 relative flex items-center justify-center">
          <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
            <circle cx="18" cy="18" r="16" fill="none" stroke="#1c231e" strokeWidth="3" />
            <circle cx="18" cy="18" r="16" fill="none" stroke={route.risk === 'High' ? '#e63946' : '#52b788'} strokeWidth="3" strokeDasharray={`${route.risk === 'High' ? 30 : 85}, 100`} />
          </svg>
          <span className="absolute text-[9px] font-bold text-white">{route.risk === 'High' ? '30%' : '85%'}</span>
        </div>
      </div>
      <div className="grid grid-cols-2 gap-4">
        <div>
          <div className="text-[9px] text-[#457b9d] uppercase">Nominal ETA</div>
          <div className="font-mono text-white text-sm font-bold">{route.eta_hrs}h</div>
        </div>
        <div>
          <div className={`text-[9px] uppercase ${route.risk === 'High' ? 'text-[#e63946]' : 'text-[#d4a373]'}`}>Robust ETA</div>
          <div className={`font-mono text-sm font-bold ${route.risk === 'High' ? 'text-[#e63946]' : 'text-[#d4a373]'}`}>{route.robust_eta_hrs}h</div>
        </div>
        <div>
          <div className="text-[9px] text-gray-500 uppercase">Distance</div>
          <div className="font-mono text-white text-sm font-bold">{route.distance_km} km</div>
        </div>
      </div>
    </div>
  );
}

function ExplainabilityTab({ riskData, dos }) {
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
    <div className="space-y-4">
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
        <div className="space-y-2 text-[9px] font-mono mt-4">
          {shap.map((s, i) => {
              const color = s.impact.startsWith('+') ? (parseFloat(s.impact) > 0.4 ? '#e63946' : '#d4a373') : '#52b788';
              return (
              <div key={i} className="flex flex-col gap-1" title={s.description}>
                <div className="flex justify-between items-center text-gray-400">
                  <span className="truncate">{s.feature}</span>
                  <span style={{color}}>{s.impact}</span>
                </div>
                <div className="flex-1 bg-[#1c231e] h-2 rounded-sm w-full"><div className="h-full rounded-sm" style={{backgroundColor: color, width: calculateWidth(s.impact)}}></div></div>
                <div className="text-[8px] text-gray-600 mb-2">{s.description}</div>
              </div>
              );
          })}
        </div>
      </div>
    </div>
  );
}
""",
    "BottomPanels.tsx": """import React, { useState } from 'react';
import { AlertTriangle, GitMerge, CheckCircle, ShieldAlert, Clock, Loader2, Play } from 'lucide-react';

export default function BottomPanels({ runWhatIf, whatIf, whatIfLoading, whatIfError, makeDecision, audits, decision }) {
  const [showOverride, setShowOverride] = useState(false);
  const [overrideScope, setOverrideScope] = useState('LOCAL');

  const handleScenario = (type) => runWhatIf(type);

  const handleOverrideSubmit = () => {
    makeDecision('OVERRIDE', overrideScope);
    setShowOverride(false);
  };

  return (
    <div className="grid grid-cols-12 gap-2 mt-2 shrink-0">
      
      {/* WHAT-IF DISRUPTION ANALYSIS */}
      <div className="col-span-3 bg-[#0b0f0c] border border-[#2a362c] rounded p-3 flex flex-col relative">
        {whatIfLoading && <div className="absolute inset-0 bg-black/70 z-20 flex flex-col items-center justify-center rounded"><Loader2 className="w-6 h-6 text-[#d4a373] animate-spin mb-2" /><span className="text-xs text-[#d4a373] font-bold tracking-widest uppercase">SIMULATING...</span></div>}
        
        <h3 className="text-[10px] text-white font-bold tracking-widest uppercase flex items-center gap-2 mb-3">
          <AlertTriangle className="w-3 h-3 text-gray-400" /> WHAT-IF DISRUPTION ANALYSIS
        </h3>
        
        <div className="flex gap-1 mb-3">
          <button onClick={() => handleScenario('Road Closure')} className={`flex-1 ${whatIf?.disruption_type === 'Road Closure' ? 'bg-[#e63946]/20 border border-[#e63946] text-[#e63946]' : 'bg-[#1c231e] border border-[#2a362c] text-gray-400 hover:text-white'} text-[9px] py-1.5 rounded uppercase tracking-widest font-bold transition-all`}>ROAD CLOSURE</button>
          <button onClick={() => handleScenario('Heavy Snow')} className={`flex-1 ${whatIf?.disruption_type === 'Heavy Snow' ? 'bg-[#457b9d]/20 border border-[#457b9d] text-[#457b9d]' : 'bg-[#1c231e] border border-[#2a362c] text-gray-400 hover:text-white'} text-[9px] py-1.5 rounded uppercase tracking-widest font-bold transition-all`}>HEAVY SNOW</button>
          <button onClick={() => handleScenario('Heli Grounding')} className={`flex-1 ${whatIf?.disruption_type === 'Heli Grounding' ? 'bg-[#d4a373]/20 border border-[#d4a373] text-[#d4a373]' : 'bg-[#1c231e] border border-[#2a362c] text-gray-400 hover:text-white'} text-[9px] py-1.5 rounded uppercase tracking-widest font-bold transition-all`}>HELI GROUNDING</button>
        </div>

        {whatIfError ? (
          <div className="bg-[#e63946]/10 border border-[#e63946] rounded p-2 text-center text-[#e63946] text-[10px] font-bold">
            SIMULATION UNAVAILABLE
            <button onClick={() => handleScenario('Road Closure')} className="block mx-auto mt-2 bg-[#e63946] text-white px-3 py-1 rounded">RETRY</button>
          </div>
        ) : whatIf ? (
          <>
            <div className="bg-[#e63946]/5 border border-[#e63946]/30 rounded p-2 flex items-start gap-2 mb-3">
              <AlertTriangle className="w-4 h-4 text-[#e63946] shrink-0 mt-0.5" />
              <div>
                <div className="text-[9px] text-[#e63946] font-bold">Selected Scenario: {whatIf.disruption_type}</div>
                <div className="text-[8px] text-gray-400">Targeting {whatIf.target_id?.replace('FP-00', 'F-0')}. Impact Score: {whatIf.impact_score}</div>
              </div>
            </div>

            <div className="grid grid-cols-3 gap-2 text-center mb-4">
              <div>
                <div className="text-[8px] text-gray-500 uppercase">IMPACT SCORE</div>
                <div className="text-2xl font-mono text-[#e63946] font-bold">{whatIf.impact_score}</div>
              </div>
              <div>
                <div className="text-[8px] text-gray-500 uppercase">AFFECTED POSTS</div>
                <div className="text-2xl font-mono text-[#e63946] font-bold mt-1">3</div>
              </div>
              <div>
                <div className="text-[8px] text-gray-500 uppercase">AFFECTED LEGS</div>
                <div className="text-2xl font-mono text-[#e63946] font-bold mt-1">{whatIf.affected_legs?.length || 2}</div>
              </div>
            </div>

            <div className="mt-auto">
              <div className="text-[9px] text-white font-bold uppercase mb-2">RECOMMENDED SCOPE</div>
              <div className="flex gap-1">
                <div className={`flex-1 ${whatIf.recommendation === 'PRESERVE' ? 'bg-[#d4a373]/10 border border-[#d4a373]' : 'bg-[#1c231e] border border-[#2a362c]'} rounded p-1.5 text-center flex flex-col justify-between`}>
                  <div className={`text-[9px] font-bold tracking-widest ${whatIf.recommendation === 'PRESERVE' ? 'text-[#d4a373]' : 'text-white'}`}>PRESERVE</div>
                  <div className="text-[7px] text-gray-500 mt-1">Keep plan</div>
                </div>
                <div className={`flex-1 ${whatIf.recommendation === 'LOCAL' ? 'bg-[#d4a373]/10 border border-[#d4a373]' : 'bg-[#1c231e] border border-[#2a362c]'} rounded p-1.5 text-center relative overflow-hidden flex flex-col justify-between`}>
                  <div className={`text-[9px] font-bold tracking-widest flex items-center justify-center gap-1 ${whatIf.recommendation === 'LOCAL' ? 'text-[#d4a373]' : 'text-white'}`}>
                    {whatIf.recommendation === 'LOCAL' && <CheckCircle className="w-2.5 h-2.5" />} LOCAL
                  </div>
                  <div className="text-[7px] text-gray-300 mb-2 mt-1">Replan region</div>
                  {whatIf.recommendation === 'LOCAL' && <div className="absolute bottom-0 left-0 right-0 bg-[#d4a373] text-[#0b0f0c] text-[8px] font-bold py-[1px]">Recommended</div>}
                </div>
                <div className={`flex-1 ${whatIf.recommendation === 'GLOBAL' ? 'bg-[#d4a373]/10 border border-[#d4a373]' : 'bg-[#1c231e] border border-[#2a362c]'} rounded p-1.5 text-center relative overflow-hidden flex flex-col justify-between`}>
                  <div className={`text-[9px] font-bold tracking-widest flex items-center justify-center gap-1 ${whatIf.recommendation === 'GLOBAL' ? 'text-[#d4a373]' : 'text-white'}`}>
                    {whatIf.recommendation === 'GLOBAL' && <CheckCircle className="w-2.5 h-2.5" />} GLOBAL
                  </div>
                  <div className="text-[7px] text-gray-500 mb-2 mt-1">De-optimize network</div>
                  {whatIf.recommendation === 'GLOBAL' && <div className="absolute bottom-0 left-0 right-0 bg-[#d4a373] text-[#0b0f0c] text-[8px] font-bold py-[1px]">Recommended</div>}
                </div>
              </div>
            </div>
          </>
        ) : (
          <div className="flex-1 flex flex-col items-center justify-center text-gray-500 border border-dashed border-[#2a362c] rounded mt-2">
             <Play className="w-6 h-6 mb-2 text-[#2a362c]" />
             <div className="text-xs font-mono">SELECT A SCENARIO</div>
          </div>
        )}
      </div>

      {/* BEFORE / AFTER COMPARISON */}
      <div className="col-span-5 bg-[#0b0f0c] border border-[#2a362c] rounded p-3 flex flex-col relative">
        {!whatIf && <div className="absolute inset-0 bg-[#0b0f0c]/80 z-10 flex items-center justify-center text-gray-500 text-xs font-mono border border-dashed border-[#2a362c] m-3 rounded">RUN WHAT-IF TO SEE COMPARISON</div>}
        <h3 className="text-[10px] text-white font-bold tracking-widest uppercase flex items-center gap-2 mb-3">
          <GitMerge className="w-3 h-3 text-gray-400" /> BEFORE / AFTER COMPARISON <span className="text-[#d4a373] font-normal tracking-normal border border-[#d4a373]/30 px-1 rounded ml-1 bg-[#d4a373]/10">SYNTHETIC SCENARIO</span>
        </h3>
        
        <div className="grid grid-cols-2 gap-3 mb-3 flex-1">
          <div className="bg-[#1c231e] border border-[#2a362c] rounded p-2 flex flex-col relative overflow-hidden">
            <div className="absolute top-0 left-0 right-0 h-1 bg-[#e63946]/50"></div>
            <div className="text-[9px] text-[#e63946] font-bold uppercase tracking-widest mb-2 mt-1">BEFORE (Current Plan)</div>
            
            <div className="flex justify-center mb-2 text-white font-mono text-[9px] items-center gap-2">
               ID-01 <span className="text-gray-500">→</span> <div className="w-2 h-2 rounded-full bg-[#52b788] inline-block border border-black"></div> {whatIf?.target_id?.replace('FP-00', 'F-0') || 'F-07'}
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
              <div className="flex justify-between"><span className="text-gray-500">ETA</span><span className="text-white">{whatIf?.before_after?.before?.eta || '-'}</span></div>
              <div className="flex justify-between"><span className="text-gray-500">Affected Posts</span><span className="text-[#e63946]">{whatIf?.target_id?.replace('FP-00', 'F-0')}</span></div>
              <div className="flex justify-between"><span className="text-gray-500">Stock-out Risk</span><span className="text-[#e63946] font-bold">{whatIf?.before_after?.before?.risk?.toUpperCase() || '-'}</span></div>
            </div>
          </div>
          
          <div className="bg-[#1c231e] border border-[#2a362c] rounded p-2 flex flex-col relative overflow-hidden">
            <div className="absolute top-0 left-0 right-0 h-1 bg-[#52b788]/50"></div>
            <div className="text-[9px] text-[#52b788] font-bold uppercase tracking-widest mb-2 mt-1">AFTER (Replanned)</div>
            
            <div className="flex justify-center mb-2 text-white font-mono text-[9px] items-center gap-2">
               ID-01 <span className="text-gray-500">→</span> <div className="w-2 h-2 border border-[#457b9d] inline-block"></div> <span className="text-gray-500">→</span> <div className="w-2 h-2 rounded-full bg-[#d4a373] inline-block"></div> {whatIf?.target_id?.replace('FP-00', 'F-0') || 'F-07'}
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
              <div className="flex justify-between"><span className="text-gray-500">Route</span><span className="text-[#457b9d]">Road → {whatIf?.before_after?.after?.new_mode || '-'}</span></div>
              <div className="flex justify-between"><span className="text-gray-500">ETA</span><span className="text-[#457b9d] font-bold">{whatIf?.before_after?.after?.eta || '-'}</span></div>
              <div className="flex justify-between"><span className="text-gray-500">Affected Posts</span><span className="text-white">{whatIf?.target_id?.replace('FP-00', 'F-0')}</span></div>
              <div className="flex justify-between"><span className="text-gray-500">Stock-out Risk</span><span className="text-[#d4a373] font-bold">{whatIf?.before_after?.after?.risk?.toUpperCase() || '-'}</span></div>
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
        {!whatIf && <div className="absolute inset-0 bg-[#0b0f0c]/80 z-10 flex items-center justify-center text-gray-500 text-xs font-mono border border-dashed border-[#2a362c] m-3 rounded">PENDING WHAT-IF ANALYSIS</div>}
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

        {decision ? (
          <div className="bg-[#1c231e] border border-[#2a362c] rounded p-3 mb-3 text-center">
            <CheckCircle className={`w-6 h-6 mx-auto mb-2 ${decision.status === 'REJECT' ? 'text-[#e63946]' : 'text-[#52b788]'}`} />
            <div className="text-[10px] text-white font-bold tracking-widest uppercase">Decision Recorded</div>
            <div className="text-[9px] text-gray-400 mt-1">Action: {decision.status} {decision.scope ? `(${decision.scope})` : ''}</div>
          </div>
        ) : showOverride ? (
          <div className="bg-[#1c231e] border border-[#2a362c] rounded p-3 mb-3">
             <div className="text-[9px] text-white font-bold tracking-widest mb-2 uppercase">SELECT OVERRIDE SCOPE</div>
             <div className="flex gap-2 mb-3">
                {['PRESERVE', 'LOCAL', 'GLOBAL'].map(s => (
                   <button key={s} onClick={() => setOverrideScope(s)} className={`flex-1 text-[9px] py-1.5 rounded font-bold tracking-widest border ${overrideScope === s ? 'bg-[#d4a373] text-black border-[#d4a373]' : 'bg-[#0b0f0c] text-gray-400 border-[#2a362c] hover:text-white'}`}>{s}</button>
                ))}
             </div>
             <div className="flex gap-2">
                <button onClick={handleOverrideSubmit} className="flex-1 bg-[#d4a373] text-black text-[9px] font-bold py-1.5 rounded">CONFIRM</button>
                <button onClick={() => setShowOverride(false)} className="flex-1 bg-transparent border border-[#2a362c] text-gray-400 text-[9px] font-bold py-1.5 rounded hover:text-white">CANCEL</button>
             </div>
          </div>
        ) : (
          <div className="grid grid-cols-2 gap-2 mb-3">
            <button onClick={() => makeDecision('APPROVE', whatIf?.recommendation)} className="col-span-1 bg-[#52b788]/20 border border-[#52b788] hover:bg-[#52b788] text-[#52b788] hover:text-[#0b0f0c] py-2 rounded text-[10px] font-bold tracking-widest flex items-center justify-center gap-1 transition-colors">
              <CheckCircle className="w-3 h-3" /> APPROVE
            </button>
            <div className="col-span-1 grid grid-cols-2 gap-2">
              <button onClick={() => setShowOverride(true)} className="bg-[#d4a373]/10 border border-[#d4a373]/50 hover:border-[#d4a373] text-[#d4a373] py-2 rounded text-[10px] font-bold tracking-widest flex items-center justify-center gap-1 transition-colors">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21.5 2v6h-6M2.13 15.57a10 10 0 1 0 4.43-12.18L2 7"/></svg>
                OVERRIDE
              </button>
              <button onClick={() => makeDecision('REJECT')} className="bg-[#e63946]/10 border border-[#e63946]/50 hover:border-[#e63946] text-[#e63946] py-2 rounded text-[10px] font-bold tracking-widest flex items-center justify-center gap-1 transition-colors">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                REJECT
              </button>
            </div>
          </div>
        )}

        <div className="mt-auto bg-[#131915] rounded p-2 overflow-y-auto custom-scrollbar h-20 relative">
          <div className="flex justify-between items-center mb-2 sticky top-0 bg-[#131915] pb-1 z-10">
            <div className="text-[9px] text-gray-400 uppercase tracking-widest font-bold">API AUDIT TRAIL</div>
            <button onClick={() => runWhatIf(null, true)} className="text-[8px] text-[#457b9d] hover:underline cursor-pointer">Refresh</button>
          </div>
          <div className="space-y-1.5 font-mono text-[8.5px]">
            {audits.map((a, i) => (
              <div key={i} className={`flex gap-2 ${a.user === 'COMMANDER' ? 'text-white bg-[#1c231e] px-1 -mx-1 rounded' : 'text-gray-400'}`}>
                <span className={a.user === 'COMMANDER' ? 'text-[#52b788]' : 'text-[#d4a373]'}>▶</span> 
                <span>{new Date(a.timestamp).toLocaleTimeString('en-GB')}</span>
                <span className={`w-14 truncate ${a.user === 'COMMANDER' ? 'text-[#457b9d]' : 'text-gray-500'}`}>{a.user}</span> 
                <span className="truncate">{a.action}: {a.decision} {a.scenario ? `(${a.scenario})` : ''}</span>
              </div>
            ))}
            {audits.length === 0 && <div className="text-gray-600 text-center py-2">No decisions logged.</div>}
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
  const [activeView, setActiveView] = useState('COMMAND');
  const [posts, setPosts] = useState([]);
  const [routes, setRoutes] = useState([]);
  const [selectedPost, setSelectedPost] = useState(null);
  const [riskData, setRiskData] = useState(null);
  const [forecast, setForecast] = useState(null);
  const [offline, setOffline] = useState(false);
  const [postDataLoading, setPostDataLoading] = useState(false);
  
  const [whatIf, setWhatIf] = useState(null);
  const [whatIfLoading, setWhatIfLoading] = useState(false);
  const [whatIfError, setWhatIfError] = useState(false);
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
    setPostDataLoading(true);
    try {
      const r = await axios.get(`${API_BASE}/risk/${p.id}`);
      setRiskData(r.data);
      const f = await axios.get(`${API_BASE}/forecast/${p.id}`);
      setForecast(f.data);
    } catch (e) {
      console.error(e);
    } finally {
      setPostDataLoading(false);
    }
  };

  const runWhatIf = async (type, onlyRefreshAudit = false) => {
    if (onlyRefreshAudit) {
       fetchAudits();
       return;
    }
    if (!selectedPost) return;
    setWhatIfLoading(true);
    setWhatIfError(false);
    setDecision(null);
    try {
      const res = await axios.post(`${API_BASE}/what-if`, {
        disruption_type: type,
        target_id: selectedPost.id
      });
      setWhatIf({ ...res.data, disruption_type: type, target_id: selectedPost.id });
    } catch(e) {
      console.error(e);
      setWhatIfError(true);
    } finally {
      setWhatIfLoading(false);
    }
  };

  const makeDecision = async (status, scope = null) => {
    if (!whatIf) return;
    const finalScope = scope || whatIf.recommendation;
    try {
      await axios.post(`${API_BASE}/decision`, {
        user: "COMMANDER",
        scenario: whatIf.disruption_type,
        decision: status === 'REJECT' ? 'REJECT' : finalScope,
        reason: `User interaction from UI (${status})`
      });
      setDecision({ status, scope: finalScope });
      fetchAudits();
    } catch(e) {
      console.error(e);
      alert("Failed to record decision.");
    }
  };

  return (
    <div className="h-screen w-screen bg-[#070908] flex flex-col font-sans text-white overflow-hidden selection:bg-[#d4a373]/30">
      <CommandHeader offline={offline} />
      
      <div className="flex flex-1 overflow-hidden p-2 gap-2">
        <Sidebar activeView={activeView} setActiveView={setActiveView} />
        
        <div className="flex-1 flex flex-col min-w-0">
          {activeView === 'COMMAND' ? (
            <>
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
                  isLoading={postDataLoading}
                />
              </div>
              
              <BottomPanels 
                runWhatIf={runWhatIf} 
                whatIf={whatIf} 
                whatIfLoading={whatIfLoading}
                whatIfError={whatIfError}
                makeDecision={makeDecision} 
                audits={audits}
                decision={decision}
              />
            </>
          ) : (
            <div className="flex-1 bg-[#0b0f0c] border border-[#2a362c] rounded flex flex-col items-center justify-center text-gray-500">
               <div className="text-xl font-bold tracking-widest text-[#d4a373] uppercase">{activeView} VIEW</div>
               <div className="text-sm font-mono mt-2">Standalone dashboard module active.</div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
"""

with open("src/App.tsx", "w", encoding="utf-8") as f:
    f.write(app_tsx)

print("E2E fully functional components generated.")

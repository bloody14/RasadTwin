import os

base_dir = "src/components"
os.makedirs(base_dir, exist_ok=True)

components = {
    "CommandHeader.tsx": """import React from 'react';
import { ShieldAlert, ServerOff } from 'lucide-react';

export default function CommandHeader({ offline }) {
  return (
    <header className="bg-command-black border-b border-olive-deep text-neutral-white p-3 flex justify-between items-center z-10 relative">
      <div className="flex items-center gap-4">
        <ShieldAlert className="w-6 h-6 text-accent-amber" />
        <div>
          <h1 className="text-lg font-bold tracking-widest text-neutral-white">RASADTWIN</h1>
          <div className="text-[10px] text-accent-amber uppercase tracking-wider">Predictive Logistics Digital Twin</div>
        </div>
      </div>
      <div className="flex items-center gap-8">
        <div className="flex flex-col items-center">
          <div className="text-[10px] text-neutral-gray uppercase tracking-widest">Command Overview</div>
        </div>
      </div>
      <div className="flex items-center gap-6">
        {offline ? (
          <div className="flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-accent-warning animate-pulse"></span>
            <span className="text-xs text-accent-warning font-bold tracking-widest uppercase">OFFLINE MODE</span>
          </div>
        ) : (
          <div className="flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-accent-green"></span>
            <span className="text-xs text-accent-green font-bold tracking-widest uppercase">SYSTEM NOMINAL</span>
          </div>
        )}
        <div className="text-xs text-neutral-gray border border-olive-deep px-2 py-1 bg-command-dark">
          SYNTHETIC ENVIRONMENT
        </div>
        <div className="text-xs font-mono text-sand-field">
          {new Date().toISOString().split('T')[1].substring(0, 8)} Z
        </div>
      </div>
    </header>
  );
}
""",
    "Sidebar.tsx": """import React from 'react';
import { Crosshair, Map, BarChart2, Package, GitMerge, HelpCircle, CheckSquare, History } from 'lucide-react';

export default function Sidebar() {
  const items = [
    { icon: Crosshair, label: 'COMMAND', active: true },
    { icon: Map, label: 'POSTS' },
    { icon: BarChart2, label: 'FORECAST' },
    { icon: Package, label: 'INVENTORY' },
    { icon: GitMerge, label: 'ROUTING' },
    { icon: HelpCircle, label: 'WHAT-IF' },
    { icon: CheckSquare, label: 'DECISIONS' },
    { icon: History, label: 'AUDIT' },
  ];

  return (
    <div className="w-16 lg:w-48 bg-command-dark border-r border-olive-deep flex flex-col py-4 shrink-0">
      {items.map((it, i) => (
        <button key={i} className={`flex items-center gap-3 px-4 py-3 hover:bg-olive-deep transition-colors ${it.active ? 'border-l-2 border-accent-amber bg-olive-muted/30 text-sand-warm' : 'border-l-2 border-transparent text-neutral-gray'}`}>
          <it.icon className="w-5 h-5 shrink-0" />
          <span className="hidden lg:block text-xs font-bold tracking-wider">{it.label}</span>
        </button>
      ))}
    </div>
  );
}
""",
    "KPIBar.tsx": """import React from 'react';

export default function KPIBar({ posts, routes, whatIf }) {
  const kpis = [
    { label: 'FORWARD POSTS', value: posts.filter(p => p.type === 'forward_post').length.toString().padStart(2, '0') },
    { label: 'AT RISK', value: posts.filter(p => p.risk === 'High').length.toString().padStart(2, '0'), alert: true },
    { label: 'STOCK-OUT WATCH', value: '02', alert: true },
    { label: 'ACTIVE ROUTES', value: routes.length.toString().padStart(2, '0') },
    { label: 'DISRUPTIONS', value: whatIf ? '01' : '00', alert: !!whatIf },
    { label: 'DECISIONS PENDING', value: whatIf && !whatIf.resolved ? '01' : '00', alert: !!whatIf },
  ];

  return (
    <div className="flex bg-command-panel border-b border-olive-deep divide-x divide-olive-deep shrink-0">
      {kpis.map((kpi, i) => (
        <div key={i} className="flex-1 px-4 py-3 flex flex-col items-center justify-center">
          <div className="text-[10px] text-neutral-gray uppercase tracking-widest mb-1">{kpi.label}</div>
          <div className={`text-xl font-mono font-bold ${kpi.alert ? 'text-accent-amber' : 'text-neutral-white'}`}>
            {kpi.value}
          </div>
        </div>
      ))}
    </div>
  );
}
""",
    "LogisticsMap.tsx": """import React from 'react';

export default function LogisticsMap({ posts, routes, selectedPost, handleSelectPost, whatIf }) {
  return (
    <div className="flex-1 relative bg-command-black overflow-hidden flex items-center justify-center border-r border-olive-deep">
      <div className="absolute inset-0 opacity-20 pointer-events-none" style={{
        backgroundImage: 'radial-gradient(circle at center, #202820 1px, transparent 1px)',
        backgroundSize: '20px 20px'
      }}></div>
      
      <svg viewBox="74 31 4 4" className="w-full h-full drop-shadow-lg max-h-[80vh]">
        {/* Terrain/Contour Mockup */}
        <path d="M 74.5 31.5 Q 75.5 32 76 33 T 77.5 34.5" fill="none" stroke="#202820" strokeWidth="0.01" />
        <path d="M 74 33 Q 75 34 76.5 33.5 T 78 35" fill="none" stroke="#202820" strokeWidth="0.01" />

        {/* Routes */}
        {routes.map(r => {
          const src = posts.find(p => p.id === r.source);
          const tgt = posts.find(p => p.id === r.target);
          const isAffected = whatIf && whatIf.affected_legs.includes(r.id);
          if (!src || !tgt) return null;
          
          let strokeDasharray = "";
          if (r.mode === "Mule") strokeDasharray = "0.05 0.05";
          if (r.mode === "Heli") strokeDasharray = "0.02 0.04";
          if (r.mode === "Drone") strokeDasharray = "0.01 0.02";

          return (
            <g key={r.id}>
              <line x1={src.lng} y1={src.lat} x2={tgt.lng} y2={tgt.lat} 
                    stroke={isAffected ? "#C94C45" : "#46543A"} 
                    strokeWidth={isAffected ? "0.03" : "0.015"} 
                    strokeDasharray={strokeDasharray} />
              
              {/* Route Label - Only show if affected or selected post route */}
              {(isAffected || (selectedPost && (r.target === selectedPost.id || r.source === selectedPost.id))) && (
                <text x={(src.lng + tgt.lng) / 2} y={(src.lat + tgt.lat) / 2 - 0.05} 
                      fill={isAffected ? "#C94C45" : "#C8B98A"} 
                      fontSize="0.06" fontFamily="monospace" textAnchor="middle">
                  {r.id}
                </text>
              )}
            </g>
          )
        })}

        {/* Nodes */}
        {posts.map(p => {
          const isSelected = p.id === selectedPost?.id;
          const isAffected = whatIf && whatIf.affected_legs.some(leg => {
             const r = routes.find(ro => ro.id === leg);
             return r && (r.target === p.id || r.source === p.id);
          });
          
          let fill = p.type === 'rear_depot' ? '#E0D2AA' : p.type === 'intermediate_depot' ? '#6D9FB3' : (p.risk === 'High' ? '#C94C45' : '#6F9C5B');
          let markerSize = p.type === 'rear_depot' ? "0.1" : p.type === 'intermediate_depot' ? "0.08" : "0.06";

          return (
            <g key={p.id} transform={`translate(${p.lng}, ${p.lat})`} className="cursor-pointer" onClick={() => handleSelectPost(p)}>
              {isSelected && (
                <circle r="0.15" fill="none" stroke="#D6A63C" strokeWidth="0.01" className="animate-pulse" />
              )}
              {isAffected && (
                <circle r="0.12" fill="none" stroke="#C94C45" strokeWidth="0.01" className="animate-ping" />
              )}
              
              {p.type === 'rear_depot' ? (
                <rect x="-0.05" y="-0.05" width="0.1" height="0.1" fill={fill} stroke="#0B0F0C" strokeWidth="0.01" />
              ) : p.type === 'intermediate_depot' ? (
                <polygon points="0,-0.08 0.08,0.04 -0.08,0.04" fill={fill} stroke="#0B0F0C" strokeWidth="0.01" />
              ) : (
                <circle r={markerSize} fill={fill} stroke="#0B0F0C" strokeWidth="0.01" />
              )}
              
              <text y="0.12" fill={isSelected ? "#D6A63C" : "#E9ECE7"} fontSize="0.05" fontFamily="monospace" textAnchor="middle" className="pointer-events-none drop-shadow-md">
                {p.name}
              </text>
            </g>
          );
        })}
      </svg>
      
      <div className="absolute bottom-4 right-4 bg-command-panel border border-olive-deep p-3 flex flex-col gap-2">
        <div className="text-[10px] text-neutral-gray uppercase tracking-widest border-b border-olive-deep pb-1 mb-1">LEGEND</div>
        <div className="flex items-center gap-2 text-xs text-neutral-white"><div className="w-3 h-3 bg-sand-warm"></div> REAR DEPOT</div>
        <div className="flex items-center gap-2 text-xs text-neutral-white"><div className="w-0 h-0 border-l-[6px] border-l-transparent border-r-[6px] border-r-transparent border-b-[10px] border-b-accent-blue"></div> INT NODE</div>
        <div className="flex items-center gap-2 text-xs text-neutral-white"><div className="w-3 h-3 rounded-full bg-accent-green"></div> FWD POST</div>
        <div className="flex items-center gap-2 text-xs text-neutral-white mt-1 pt-1 border-t border-olive-deep"><div className="w-4 h-0.5 bg-olive-military"></div> ROAD</div>
        <div className="flex items-center gap-2 text-xs text-neutral-white"><div className="w-4 h-0 border border-dashed border-olive-military"></div> AIR / MULE</div>
      </div>
      
      <div className="absolute top-4 left-4 bg-command-panel/80 border border-olive-deep p-2 text-[10px] text-neutral-gray font-mono">
        NO REAL OPERATIONAL DATA
      </div>
    </div>
  );
}
""",
    "PostIntelligence.tsx": """import React from 'react';
import ForecastChart from './ForecastChart';
import RiskMeter from './RiskMeter';
import ExplainabilityPanel from './ExplainabilityPanel';
import RoutePanel from './RoutePanel';
import WhatIfPanel from './WhatIfPanel';
import { Target } from 'lucide-react';

export default function PostIntelligence({ post, riskData, forecast, routes, runWhatIf, whatIf, makeDecision, decision }) {
  if (!post) {
    return (
      <div className="w-full lg:w-[450px] bg-command-dark flex items-center justify-center text-neutral-gray border-l border-olive-deep p-8 text-center shrink-0">
        <div className="flex flex-col items-center gap-4 opacity-50">
          <Target className="w-12 h-12" />
          <p className="text-sm uppercase tracking-widest">Select Node for Intelligence</p>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full lg:w-[480px] bg-command-dark border-l border-olive-deep flex flex-col h-full overflow-y-auto custom-scrollbar shrink-0">
      {/* HEADER */}
      <div className="p-4 border-b border-olive-deep bg-command-panel sticky top-0 z-10 shadow-md">
        <div className="flex justify-between items-start mb-2">
          <div>
            <div className="text-[10px] text-accent-blue uppercase tracking-widest">FORWARD POST</div>
            <h2 className="text-xl font-bold text-neutral-white font-mono">{post.id} // {post.name}</h2>
          </div>
          <div className="bg-command-dark border border-olive-deep px-2 py-1">
            <div className="text-[9px] text-neutral-gray uppercase">PRIORITY</div>
            <div className="text-xs text-sand-warm font-mono font-bold">{post.priority}</div>
          </div>
        </div>
        <div className="flex gap-4 mt-4">
          <div className="flex-1 bg-command-black border border-olive-deep p-2 text-center">
            <div className="text-[9px] text-neutral-gray uppercase tracking-wider">DAYS OF SUPPLY</div>
            <div className={`text-xl font-mono font-bold ${riskData?.days_of_supply < 3 ? 'text-accent-critical' : riskData?.days_of_supply < 7 ? 'text-accent-warning' : 'text-accent-green'}`}>
              {riskData ? riskData.days_of_supply.toFixed(1) : '--'}
            </div>
          </div>
          <div className="flex-1 bg-command-black border border-olive-deep p-2 text-center">
            <div className="text-[9px] text-neutral-gray uppercase tracking-wider">STOCK-OUT RISK</div>
            <div className={`text-xl font-mono font-bold ${riskData?.stock_out_risk === 'High' ? 'text-accent-critical' : riskData?.stock_out_risk === 'Medium' ? 'text-accent-warning' : 'text-accent-green'}`}>
              {riskData ? riskData.stock_out_risk : '--'}
            </div>
          </div>
        </div>
      </div>

      <div className="p-4 space-y-6">
        <RiskMeter riskData={riskData} />
        <ForecastChart forecast={forecast} />
        <ExplainabilityPanel riskData={riskData} />
        <RoutePanel routes={routes} post={post} />
        <WhatIfPanel runWhatIf={runWhatIf} whatIf={whatIf} makeDecision={makeDecision} decision={decision} />
      </div>
    </div>
  );
}
""",
    "RiskMeter.tsx": """import React from 'react';

export default function RiskMeter({ riskData }) {
  if (!riskData) return null;
  
  const dos = riskData.days_of_supply;
  const target = 5.8;
  const pct = Math.min(100, Math.max(0, (dos / 10) * 100));
  
  return (
    <div className="bg-command-panel border border-olive-deep p-3">
      <div className="flex justify-between items-end mb-2">
        <h3 className="text-[10px] text-neutral-gray uppercase tracking-widest">INVENTORY STATUS</h3>
        <span className="text-[10px] text-sand-field font-mono">TARGET: {target}d</span>
      </div>
      
      <div className="relative h-2 bg-command-black border border-olive-muted w-full mb-4">
        {/* Safe zone */}
        <div className="absolute left-[58%] right-0 top-0 bottom-0 bg-olive-military/30"></div>
        {/* Watch zone */}
        <div className="absolute left-[25%] right-[42%] top-0 bottom-0 bg-accent-amber/20"></div>
        {/* Critical zone */}
        <div className="absolute left-0 w-1/4 top-0 bottom-0 bg-accent-critical/20"></div>
        
        {/* Current Marker */}
        <div className="absolute top-0 bottom-0 w-1 bg-neutral-white transition-all duration-500 shadow-[0_0_8px_rgba(255,255,255,0.8)]" style={{ left: `${pct}%` }}></div>
        {/* Target Marker */}
        <div className="absolute top-0 bottom-0 w-0.5 bg-accent-blue" style={{ left: '58%' }}></div>
      </div>
      
      <div className="flex justify-between text-[9px] font-mono text-neutral-gray">
        <span className="text-accent-critical">CRITICAL</span>
        <span className="text-accent-warning">WATCH</span>
        <span className="text-accent-green">SAFE</span>
      </div>
    </div>
  );
}
""",
    "ForecastChart.tsx": """import React from 'react';
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
""",
    "ExplainabilityPanel.tsx": """import React from 'react';

export default function ExplainabilityPanel({ riskData }) {
  if (!riskData || !riskData.explainability) return null;

  return (
    <div className="bg-command-panel border border-olive-deep p-3">
      <h3 className="text-[10px] text-neutral-gray uppercase tracking-widest mb-3">TOP CONTRIBUTING FACTORS</h3>
      <div className="space-y-3">
        {riskData.explainability.map((ex, i) => (
          <div key={i}>
            <div className="flex justify-between font-mono text-[11px] text-neutral-white mb-1">
              <span>{ex.feature}</span>
              <span className={ex.impact.startsWith('+') ? 'text-accent-critical' : 'text-accent-green'}>{ex.impact}</span>
            </div>
            <div className="w-full bg-command-black h-1 rounded-none overflow-hidden flex border border-olive-muted">
              <div className={`h-full ${ex.impact.startsWith('+') ? 'bg-accent-critical' : 'bg-accent-green'}`} style={{width: '60%'}}></div>
            </div>
          </div>
        ))}
      </div>
      <div className="mt-4 border-t border-olive-deep pt-2">
        <div className="text-[9px] text-neutral-gray uppercase tracking-widest mb-1">SYSTEM RECOMMENDATION</div>
        <div className="text-xs text-sand-warm font-mono border-l-2 border-accent-amber pl-2 py-1 bg-olive-deep/30">
          PRE-POSITION + LOCAL REPLAN
        </div>
      </div>
    </div>
  );
}
""",
    "RoutePanel.tsx": """import React from 'react';

export default function RoutePanel({ routes, post }) {
  const postRoutes = routes.filter(r => r.target === post.id);

  return (
    <div className="bg-command-panel border border-olive-deep p-0">
      <div className="p-3 border-b border-olive-deep flex justify-between items-center">
        <h3 className="text-[10px] text-neutral-gray uppercase tracking-widest">ROUTE HEALTH</h3>
        <span className="text-[10px] text-neutral-white font-mono bg-command-black px-1 border border-olive-muted">{postRoutes.length} ROUTES</span>
      </div>
      <table className="w-full text-left border-collapse">
        <thead>
          <tr className="bg-command-dark text-[9px] text-neutral-gray uppercase font-mono border-b border-olive-deep">
            <th className="p-2 font-normal">ID</th>
            <th className="p-2 font-normal">MODE</th>
            <th className="p-2 font-normal">NOMINAL</th>
            <th className="p-2 font-normal text-accent-amber">ROBUST</th>
          </tr>
        </thead>
        <tbody className="text-xs font-mono text-neutral-white">
          {postRoutes.map((r, i) => (
            <tr key={r.id} className={i !== postRoutes.length - 1 ? 'border-b border-olive-muted/30' : ''}>
              <td className="p-2">{r.id}</td>
              <td className="p-2">{r.mode}</td>
              <td className="p-2 text-neutral-gray">{r.eta_hrs}h</td>
              <td className="p-2 text-accent-amber">{r.robust_eta_hrs}h <span className="text-[9px] text-accent-critical">+{Math.round((r.robust_eta_hrs - r.eta_hrs)*60)}m</span></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
""",
    "WhatIfPanel.tsx": """import React, { useState } from 'react';
import { ShieldAlert, AlertTriangle } from 'lucide-react';

export default function WhatIfPanel({ runWhatIf, whatIf, makeDecision, decision }) {
  const [selectedStage, setSelectedStage] = useState('LOCAL');
  
  return (
    <div className="mt-6 border-t border-olive-deep pt-4">
      <h3 className="text-[10px] text-neutral-gray uppercase tracking-widest mb-3">WHAT-IF SCENARIO</h3>
      <div className="flex gap-2 mb-4">
        <button onClick={() => runWhatIf('Road Closure')} className="flex-1 bg-command-dark border border-olive-muted hover:border-sand-field text-neutral-white text-[10px] py-2 uppercase tracking-wider transition-colors">Road Closure</button>
        <button onClick={() => runWhatIf('Heavy Snow')} className="flex-1 bg-command-dark border border-olive-muted hover:border-sand-field text-neutral-white text-[10px] py-2 uppercase tracking-wider transition-colors">Heavy Snow</button>
        <button onClick={() => runWhatIf('Heli Grounding')} className="flex-1 bg-command-dark border border-olive-muted hover:border-sand-field text-neutral-white text-[10px] py-2 uppercase tracking-wider transition-colors">Heli Grounding</button>
      </div>

      {whatIf && (
        <div className="bg-command-dark border border-accent-critical p-4 mt-4 relative overflow-hidden shadow-[0_0_15px_rgba(201,76,69,0.15)] animate-in fade-in slide-in-from-top-4 duration-300">
          <div className="absolute top-0 right-0 w-16 h-16 bg-accent-critical/10 translate-x-1/2 -translate-y-1/2 rounded-full blur-xl"></div>
          
          <div className="flex justify-between items-start mb-4 relative z-10">
            <div>
              <div className="text-[10px] text-accent-critical uppercase tracking-widest mb-1 flex items-center gap-2">
                <AlertTriangle className="w-3 h-3 text-accent-critical animate-pulse" />
                IMPACT ASSESSMENT
              </div>
              <div className="text-3xl font-mono text-neutral-white font-bold">{whatIf.impact_score} <span className="text-xs text-neutral-gray font-normal">/100 SCORE</span></div>
            </div>
            <div className="text-right font-mono">
              <div className="text-[10px] text-neutral-gray uppercase">AFFECTED POSTS</div>
              <div className="text-lg text-accent-warning">03</div>
            </div>
          </div>

          {/* PRESERVE / LOCAL / GLOBAL */}
          <div className="my-6 relative z-10">
            <div className="text-[10px] text-neutral-gray uppercase tracking-widest mb-2">RECOMMENDED SCOPE</div>
            <div className="flex gap-2">
              {['PRESERVE', 'LOCAL', 'GLOBAL'].map(stage => (
                <div key={stage} 
                     className={`flex-1 border p-2 text-center cursor-pointer transition-colors ${selectedStage === stage ? 'border-accent-amber bg-accent-amber/10 text-accent-amber' : 'border-olive-deep bg-command-black text-neutral-gray opacity-50 hover:bg-olive-muted'}`}
                     onClick={() => setSelectedStage(stage)}>
                  <div className="text-[11px] font-bold tracking-widest">{stage}</div>
                  {stage === 'LOCAL' && selectedStage === stage && <div className="text-[9px] mt-1 font-mono">RECOMMENDED</div>}
                </div>
              ))}
            </div>
            {selectedStage === 'LOCAL' && (
              <div className="mt-2 text-[10px] text-neutral-gray font-mono bg-command-black p-2 border border-olive-deep">
                Reason: Disruption affects 3 downstream posts but does not compromise the wider network. Local replan optimal.
              </div>
            )}
          </div>

          {/* BEFORE / AFTER */}
          <div className="bg-command-black border border-olive-deep p-3 mb-4 relative z-10">
            <div className="text-[9px] text-neutral-gray uppercase text-center mb-3">SYNTHETIC SCENARIO COMPARISON</div>
            <div className="grid grid-cols-2 gap-4">
              <div className="border-r border-olive-deep pr-4">
                <div className="text-[10px] text-accent-critical font-bold mb-2 uppercase tracking-widest">CURRENT PLAN</div>
                <div className="font-mono text-xs space-y-1">
                  <div className="flex justify-between"><span className="text-neutral-gray">Route</span><span className="text-neutral-white">Road</span></div>
                  <div className="flex justify-between"><span className="text-neutral-gray">ETA</span><span className="text-neutral-white">{whatIf.before_after.before.eta}</span></div>
                  <div className="flex justify-between mt-2 pt-2 border-t border-olive-deep"><span className="text-neutral-gray">Risk</span><span className="text-accent-critical font-bold">{whatIf.before_after.before.risk}</span></div>
                </div>
              </div>
              <div>
                <div className="text-[10px] text-accent-green font-bold mb-2 uppercase tracking-widest">MITIGATION</div>
                <div className="font-mono text-xs space-y-1">
                  <div className="flex justify-between"><span className="text-neutral-gray">Route</span><span className="text-accent-blue">{whatIf.before_after.after.new_mode}</span></div>
                  <div className="flex justify-between"><span className="text-neutral-gray">ETA</span><span className="text-neutral-white">{whatIf.before_after.after.eta}</span></div>
                  <div className="flex justify-between mt-2 pt-2 border-t border-olive-deep"><span className="text-neutral-gray">Risk</span><span className="text-accent-warning font-bold">{whatIf.before_after.after.risk}</span></div>
                </div>
              </div>
            </div>
            <div className="mt-3 pt-2 border-t border-olive-deep flex justify-between font-mono text-[10px]">
              <span className="text-neutral-gray">RECOVERY: <span className="text-accent-green">+27%</span></span>
              <span className="text-neutral-gray">CHANGES: <span className="text-neutral-white">1</span></span>
            </div>
          </div>

          {/* HITL DECISION */}
          <div className="pt-2 border-t border-olive-deep relative z-10">
            <div className="text-[10px] text-neutral-gray uppercase tracking-widest mb-3">COMMAND DECISION REQUIRED</div>
            <div className="flex gap-2">
              <button onClick={() => makeDecision('APPROVE')} className="flex-1 bg-olive-military hover:bg-olive-deep border border-accent-green text-neutral-white text-xs py-2 uppercase tracking-widest transition-colors font-bold shadow-[0_0_10px_rgba(111,156,91,0.2)]">APPROVE</button>
              <button onClick={() => makeDecision('OVERRIDE')} className="flex-1 bg-command-black border border-accent-amber hover:bg-accent-amber/10 text-accent-amber text-xs py-2 uppercase tracking-widest transition-colors">OVERRIDE</button>
              <button onClick={() => makeDecision('REJECT')} className="px-4 bg-command-black border border-olive-muted hover:border-accent-critical hover:text-accent-critical text-neutral-gray text-xs py-2 uppercase tracking-widest transition-colors">REJECT</button>
            </div>
            {decision && (
              <div className="mt-3 bg-command-black border-l-2 border-accent-blue p-2 font-mono text-[10px] text-neutral-gray flex justify-between items-center">
                <span>
                  <span className="text-accent-blue font-bold">{new Date().toISOString().split('T')[1].substring(0, 8)} Z</span> - DECISION RECORDED: {decision}
                  <br/>Audit event created successfully.
                </span>
                <ShieldAlert className="w-4 h-4 text-accent-blue" />
              </div>
            )}
          </div>
        </div>
      )}
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
    } catch (e) {
      console.warn("API Error, falling back to offline mode", e);
      setOffline(true);
      // Optional fallback for demo
    }
  };

  const handleSelectPost = async (p) => {
    setSelectedPost(p);
    setWhatIf(null);
    setDecision(null);
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
    try {
      const res = await axios.post(`${API_BASE}/what-if`, {
        disruption_type: type,
        target_id: selectedPost.id
      });
      setWhatIf(res.data);
      setDecision(null);
    } catch (e) {
      console.error(e);
    }
  };

  const makeDecision = async (dec) => {
    try {
      await axios.post(`${API_BASE}/decision`, {
        user: "Commander",
        scenario: "Winter Surge",
        decision: dec,
        reason: "Field override"
      });
      setDecision(dec);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="h-screen w-screen bg-command-black flex flex-col font-sans text-neutral-white overflow-hidden selection:bg-accent-amber/30 selection:text-sand-warm">
      <CommandHeader offline={offline} />
      
      <div className="flex flex-1 overflow-hidden">
        <Sidebar />
        
        <div className="flex-1 flex flex-col min-w-0">
          <KPIBar posts={posts} routes={routes} whatIf={whatIf} />
          
          <div className="flex-1 flex overflow-hidden">
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
              runWhatIf={runWhatIf}
              whatIf={whatIf}
              makeDecision={makeDecision}
              decision={decision}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
"""

with open("src/App.tsx", "w", encoding="utf-8") as f:
    f.write(app_tsx)

index_css = """@tailwind base;
@tailwind components;
@tailwind utilities;

@layer utilities {
  .custom-scrollbar::-webkit-scrollbar {
    width: 6px;
    height: 6px;
  }
  .custom-scrollbar::-webkit-scrollbar-track {
    background: #0B0F0C; 
  }
  .custom-scrollbar::-webkit-scrollbar-thumb {
    background: #202820; 
  }
  .custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background: #46543A; 
  }
}
"""

with open("src/index.css", "w", encoding="utf-8") as f:
    f.write(index_css)

print("Frontend components generated successfully.")

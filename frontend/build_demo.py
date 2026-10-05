import os, textwrap

base = "src"
comp = os.path.join(base, "components")
views = os.path.join(base, "views")
os.makedirs(comp, exist_ok=True)
os.makedirs(views, exist_ok=True)

# ─────────────────────────────────────────────
# App.tsx
# ─────────────────────────────────────────────
open(os.path.join(base, "App.tsx"), "w", encoding="utf-8").write(textwrap.dedent(r'''
import React, { useState, useEffect } from 'react';
import axios from 'axios';

import CommandHeader from './components/CommandHeader';
import Sidebar from './components/Sidebar';
import KPIBar from './components/KPIBar';
import LogisticsMap from './components/LogisticsMap';
import PostIntelligence from './components/PostIntelligence';
import BottomPanels from './components/BottomPanels';
import DemoWalkthrough from './components/DemoWalkthrough';

import PostsView from './views/PostsView';
import ForecastView from './views/ForecastView';
import InventoryView from './views/InventoryView';
import RoutingView from './views/RoutingView';
import DecisionsView from './views/DecisionsView';
import AuditView from './views/AuditView';

const API = "http://localhost:8000";

export default function App() {
  const [activeView, setActiveView] = useState('COMMAND');
  const [posts, setPosts] = useState<any[]>([]);
  const [routes, setRoutes] = useState<any[]>([]);
  const [selectedPost, setSelectedPost] = useState<any>(null);
  const [riskData, setRiskData] = useState<any>(null);
  const [forecast, setForecast] = useState<any>(null);
  const [offline, setOffline] = useState(false);
  const [postLoading, setPostLoading] = useState(false);

  const [whatIf, setWhatIf] = useState<any>(null);
  const [whatIfLoading, setWhatIfLoading] = useState(false);
  const [whatIfError, setWhatIfError] = useState(false);
  const [decision, setDecision] = useState<any>(null);
  const [audits, setAudits] = useState<any[]>([]);

  // Demo walkthrough steps
  const [demoSteps, setDemoSteps] = useState({
    postInspected: false,
    riskReviewed: false,
    disruptionRun: false,
    impactAssessed: false,
    scopeChosen: false,
    decisionMade: false,
    auditReviewed: false,
  });

  useEffect(() => { fetchData(); }, []);

  const fetchData = async () => {
    try {
      const [p, r] = await Promise.all([
        axios.get(`${API}/posts`),
        axios.get(`${API}/routes`),
      ]);
      setPosts(p.data.posts);
      setRoutes(r.data.routes);
      setOffline(false);
      fetchAudits();

      // Auto-select first high-risk forward post (deterministic)
      const highRisk = p.data.posts.find((x:any) => x.risk === 'High' && x.type === 'forward_post');
      if (highRisk) selectPost(highRisk);
    } catch {
      setOffline(true);
    }
  };

  const fetchAudits = async () => {
    try {
      const a = await axios.get(`${API}/audit`);
      setAudits(a.data.logs || []);
    } catch {}
  };

  const selectPost = async (p: any) => {
    setSelectedPost(p);
    setPostLoading(true);
    setDemoSteps(s => ({ ...s, postInspected: true }));
    try {
      const [r, f] = await Promise.all([
        axios.get(`${API}/risk/${p.id}`),
        axios.get(`${API}/forecast/${p.id}`),
      ]);
      setRiskData(r.data);
      setForecast(f.data);
      setDemoSteps(s => ({ ...s, riskReviewed: true }));
    } catch (e) {
      console.error(e);
    } finally {
      setPostLoading(false);
    }
  };

  const runWhatIf = async (type: string) => {
    if (!selectedPost) return;
    setWhatIfLoading(true);
    setWhatIfError(false);
    setDecision(null);
    try {
      const res = await axios.post(`${API}/what-if`, {
        disruption_type: type,
        target_id: selectedPost.id,
      });
      setWhatIf({ ...res.data, disruption_type: type, target_id: selectedPost.id });
      setDemoSteps(s => ({ ...s, disruptionRun: true, impactAssessed: true, scopeChosen: true }));
    } catch {
      setWhatIfError(true);
    } finally {
      setWhatIfLoading(false);
    }
  };

  const makeDecision = async (status: string, scope: string | null = null) => {
    if (!whatIf) return;
    const finalScope = scope || whatIf.recommendation;
    try {
      await axios.post(`${API}/decision`, {
        user: "COMMANDER",
        scenario: whatIf.disruption_type,
        decision: status === 'REJECT' ? 'REJECT' : finalScope,
        reason: `User ${status} via HITL UI`,
      });
      setDecision({ status, scope: finalScope });
      setDemoSteps(s => ({ ...s, decisionMade: true, auditReviewed: true }));
      fetchAudits();
    } catch {
      alert("Failed to record decision.");
    }
  };

  const resetDemo = () => {
    setWhatIf(null);
    setDecision(null);
    setDemoSteps({
      postInspected: !!selectedPost,
      riskReviewed: !!riskData,
      disruptionRun: false,
      impactAssessed: false,
      scopeChosen: false,
      decisionMade: false,
      auditReviewed: false,
    });
    fetchData(); // Reset everything cleanly
  };

  // Sidebar shortcuts
  const handleSidebarNav = (id: string) => {
    if (id === 'WHAT_IF') { setActiveView('COMMAND'); return; }
    setActiveView(id);
  };

  const sharedProps = { posts, routes, selectedPost, selectPost, riskData, forecast, audits, decision };

  return (
    <div className="h-screen w-screen bg-[#070908] flex flex-col font-sans text-white overflow-hidden selection:bg-[#d4a373]/30">
      <CommandHeader offline={offline} />
      <div className="flex flex-1 overflow-hidden p-2 gap-2">
        <Sidebar activeView={activeView} setActiveView={handleSidebarNav} />
        <div className="flex-1 flex flex-col min-w-0 relative">
          {activeView === 'COMMAND' && (
            <>
              <KPIBar posts={posts} routes={routes} whatIf={whatIf} decision={decision} />
              <div className="flex-1 flex gap-2 overflow-hidden relative">
                
                {/* Reset button overlaid on top left */}
                <button onClick={resetDemo} className="absolute top-2 left-2 z-50 bg-[#131915]/80 hover:bg-[#e63946]/20 border border-[#2a362c] hover:border-[#e63946] text-white px-3 py-1.5 rounded text-[10px] font-bold tracking-widest uppercase backdrop-blur transition-all">
                  RESET DEMO
                </button>

                <LogisticsMap posts={posts} routes={routes} selectedPost={selectedPost} handleSelectPost={selectPost} whatIf={whatIf} decision={decision} />
                <PostIntelligence post={selectedPost} riskData={riskData} forecast={forecast} routes={routes} isLoading={postLoading} />
              </div>
              <BottomPanels runWhatIf={runWhatIf} whatIf={whatIf} whatIfLoading={whatIfLoading} whatIfError={whatIfError} makeDecision={makeDecision} audits={audits} decision={decision} fetchAudits={fetchAudits} selectedPost={selectedPost} />
              <DemoWalkthrough steps={demoSteps} />
            </>
          )}
          {activeView === 'POSTS' && <PostsView {...sharedProps} />}
          {activeView === 'FORECAST' && <ForecastView {...sharedProps} />}
          {activeView === 'INVENTORY' && <InventoryView {...sharedProps} />}
          {activeView === 'ROUTING' && <RoutingView {...sharedProps} />}
          {activeView === 'DECISIONS' && <DecisionsView {...sharedProps} />}
          {activeView === 'AUDIT' && <AuditView {...sharedProps} />}
        </div>
      </div>
    </div>
  );
}
'''.lstrip()))

# ─────────────────────────────────────────────
# LogisticsMap.tsx
# ─────────────────────────────────────────────
open(os.path.join(comp, "LogisticsMap.tsx"), "w", encoding="utf-8").write(textwrap.dedent(r'''
import React from 'react';
import { Map, AlertTriangle } from 'lucide-react';

export default function LogisticsMap({ posts, routes, selectedPost, handleSelectPost, whatIf, decision }: any) {
  // Simple projection for offline map bounds
  const padding = 2;
  const lats = posts.map((p: any) => p.lat);
  const lngs = posts.map((p: any) => p.lng);
  const minLat = Math.min(...lats) - padding;
  const maxLat = Math.max(...lats) + padding;
  const minLng = Math.min(...lngs) - padding;
  const maxLng = Math.max(...lngs) + padding;

  const getRiskColor = (risk: string) => {
    if (risk === 'High') return '#e63946';
    if (risk === 'Medium') return '#d4a373';
    return '#52b788';
  };

  const getStatusText = () => {
    if (decision?.status === 'APPROVE') return 'UPDATED PLAN ACTIVE';
    if (whatIf) return 'DISRUPTION SIMULATION';
    return 'CURRENT PLAN';
  };

  return (
    <div className="flex-1 bg-[#0b0f0c] border border-[#2a362c] rounded relative overflow-hidden group">
      <div className="absolute top-4 right-4 z-10 text-right">
        <h2 className="text-sm font-bold tracking-widest text-white uppercase flex items-center gap-2 justify-end">
          LOGISTICS NETWORK MAP <Map className="w-4 h-4 text-[#d4a373]" />
        </h2>
        <div className="text-[10px] text-gray-500 font-mono mt-1">LAT {minLat.toFixed(2)} - {maxLat.toFixed(2)} | LNG {minLng.toFixed(2)} - {maxLng.toFixed(2)}</div>
        <div className={`mt-2 inline-block px-2 py-1 rounded text-[10px] font-bold tracking-widest uppercase border ${decision?.status === 'APPROVE' ? 'bg-[#52b788]/20 border-[#52b788] text-[#52b788]' : whatIf ? 'bg-[#e63946]/20 border-[#e63946] text-[#e63946]' : 'bg-[#1c231e] border-[#2a362c] text-white'}`}>
          {getStatusText()}
        </div>
      </div>

      <svg className="w-full h-full" viewBox={`${minLng} ${-maxLat} ${maxLng - minLng} ${maxLat - minLat}`} preserveAspectRatio="xMidYMid meet">
        {/* Draw nominal routes */}
        {routes.map((r: any) => {
          const source = posts.find((p: any) => p.id === r.source);
          const target = posts.find((p: any) => p.id === r.target);
          if (!source || !target) return null;

          const isDisrupted = !decision && whatIf?.affected_legs?.includes(r.id);
          const isReplaced = decision?.status === 'APPROVE' && whatIf?.affected_legs?.includes(r.id);

          // If replaced and approved, we gray it out completely (or hide it)
          if (isReplaced) return null;

          return (
            <g key={r.id}>
              <line
                x1={source.lng} y1={-source.lat}
                x2={target.lng} y2={-target.lat}
                stroke={isDisrupted ? '#e63946' : '#2a362c'}
                strokeWidth={isDisrupted ? 0.05 : 0.02}
                strokeDasharray={isDisrupted ? "0.1 0.1" : (r.mode !== 'Road' ? "0.05 0.05" : "none")}
                className="transition-all duration-500"
              />
              {isDisrupted && (
                <text x={(source.lng + target.lng)/2} y={-(source.lat + target.lat)/2} fill="#e63946" fontSize="0.15" fontWeight="bold" textAnchor="middle" dy="0.05">X</text>
              )}
            </g>
          );
        })}

        {/* Draw New Replanned Route if Disrupted OR Approved */}
        {(whatIf || decision?.status === 'APPROVE') && whatIf?.before_after?.after?.route && (
           (() => {
             // Mock drawing a new route connecting a rear depot to the affected node
             // The backend sends route changes, we just visually represent a "new" leg to target
             const targetId = whatIf.before_after.after.affected_posts[0];
             const target = posts.find((p:any) => p.id === targetId);
             const alternateSource = posts.find((p:any) => p.type === 'intermediate_depot' && p.id !== 'ID-001') || posts.find((p:any) => p.type === 'intermediate_depot');
             
             if (target && alternateSource) {
               const isActive = decision?.status === 'APPROVE';
               return (
                 <g>
                    <line
                      x1={alternateSource.lng} y1={-alternateSource.lat}
                      x2={target.lng} y2={-target.lat}
                      stroke={isActive ? '#52b788' : '#d4a373'}
                      strokeWidth={isActive ? 0.04 : 0.03}
                      strokeDasharray="0.05 0.05"
                      className="transition-all duration-500"
                    />
                    <text x={(alternateSource.lng + target.lng)/2} y={-(alternateSource.lat + target.lat)/2} fill={isActive ? '#52b788' : '#d4a373'} fontSize="0.08" fontWeight="bold" textAnchor="middle" dy="-0.05">{isActive ? 'UPDATED ROUTE' : 'PROPOSED ALTERNATE'}</text>
                 </g>
               )
             }
             return null;
           })()
        )}

        {/* Draw Posts */}
        {posts.map((p: any) => {
          const isSelected = selectedPost?.id === p.id;
          const isDisruptedPost = !decision && whatIf?.affected_posts?.includes(p.id);
          const color = getRiskColor(p.risk);

          return (
            <g key={p.id} className="cursor-pointer" onClick={() => handleSelectPost(p)}>
              <circle cx={p.lng} cy={-p.lat} r="0.15" fill="transparent" /> {/* Hitbox */}
              {isSelected && <circle cx={p.lng} cy={-p.lat} r="0.08" fill="none" stroke="#d4a373" strokeWidth="0.01" className="animate-pulse" />}
              {isDisruptedPost && <circle cx={p.lng} cy={-p.lat} r="0.06" fill="#e63946" stroke="none" className="animate-ping opacity-50" />}
              <circle cx={p.lng} cy={-p.lat} r="0.03" fill={color} stroke="#070908" strokeWidth="0.01" />
              <text x={p.lng} y={-p.lat} fill="#fff" fontSize="0.05" textAnchor="middle" dy="0.1" className="pointer-events-none font-mono">
                {p.id.replace('FP-00', 'F-0')}
              </text>
            </g>
          );
        })}
      </svg>
      <div className="absolute bottom-4 left-4 text-[9px] text-gray-500 uppercase tracking-widest bg-[#070908]/80 px-2 py-1 rounded backdrop-blur">
        SYNTHETIC ENVIRONMENT • NO REAL OPERATIONAL DATA
      </div>
    </div>
  );
}
'''.lstrip()))

# ─────────────────────────────────────────────
# PostIntelligence.tsx
# ─────────────────────────────────────────────
open(os.path.join(comp, "PostIntelligence.tsx"), "w", encoding="utf-8").write(textwrap.dedent(r'''
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
'''.lstrip()))

# ─────────────────────────────────────────────
# KPIBar.tsx
# ─────────────────────────────────────────────
open(os.path.join(comp, "KPIBar.tsx"), "w", encoding="utf-8").write(textwrap.dedent(r'''
import React from 'react';
import { Activity, AlertTriangle, ShieldCheck } from 'lucide-react';

export default function KPIBar({ posts, routes, whatIf, decision }: any) {
  const fPosts = posts.filter((p:any) => p.type === 'forward_post');
  const atRisk = fPosts.filter((p:any) => p.risk === 'High').length;
  const watch = fPosts.filter((p:any) => p.dos < 7).length;
  
  const disruptions = whatIf && !decision ? 1 : 0;
  const pendingDecisions = whatIf && !decision ? 1 : 0;

  return (
    <div className="bg-[#0b0f0c] border border-[#2a362c] rounded flex items-center shrink-0">
      <div className="flex-1 flex divide-x divide-[#2a362c]">
        <div className="px-6 py-3 flex-1">
          <div className="text-[9px] text-gray-500 uppercase tracking-widest font-bold mb-1">Forward Posts</div>
          <div className="text-xl font-mono text-white">{fPosts.length}</div>
        </div>
        <div className="px-6 py-3 flex-1">
          <div className="text-[9px] text-[#e63946] uppercase tracking-widest font-bold mb-1 flex items-center gap-1"><AlertTriangle className="w-3 h-3"/> At Risk</div>
          <div className="text-xl font-mono text-[#e63946]">{atRisk}</div>
        </div>
        <div className="px-6 py-3 flex-1">
          <div className="text-[9px] text-[#d4a373] uppercase tracking-widest font-bold mb-1">Stock-out Watch</div>
          <div className="text-xl font-mono text-[#d4a373]">{watch}</div>
        </div>
        <div className="px-6 py-3 flex-1 bg-[#131915]">
          <div className="text-[9px] text-gray-400 uppercase tracking-widest font-bold mb-1">Disruptions</div>
          <div className={`text-xl font-mono ${disruptions > 0 ? 'text-[#e63946]' : 'text-white'}`}>{disruptions}</div>
        </div>
        <div className={`px-6 py-3 flex-1 transition-colors ${pendingDecisions > 0 ? 'bg-[#d4a373]/10 border-b-2 border-[#d4a373]' : ''}`}>
          <div className="text-[9px] text-gray-400 uppercase tracking-widest font-bold mb-1">Decisions Pending</div>
          <div className={`text-xl font-mono ${pendingDecisions > 0 ? 'text-[#d4a373]' : 'text-white'}`}>{pendingDecisions}</div>
        </div>
      </div>
    </div>
  );
}
'''.lstrip()))

# ─────────────────────────────────────────────
# BottomPanels.tsx
# ─────────────────────────────────────────────
open(os.path.join(comp, "BottomPanels.tsx"), "w", encoding="utf-8").write(textwrap.dedent(r'''
import React, { useState } from 'react';
import { Settings2, GitMerge, ListTodo, ShieldCheck, CheckCircle, XCircle, Loader2 } from 'lucide-react';

export default function BottomPanels({ runWhatIf, whatIf, whatIfLoading, whatIfError, makeDecision, audits, decision, selectedPost }: any) {
  const [overrideOpen, setOverrideOpen] = useState(false);

  return (
    <div className="h-64 flex gap-2 shrink-0">
      
      {/* WHAT-IF PANEL */}
      <div className="flex-[1.2] bg-[#0b0f0c] border border-[#2a362c] rounded flex flex-col overflow-hidden">
        <div className="p-3 border-b border-[#2a362c] flex justify-between items-center bg-[#131915]">
          <h2 className="text-xs font-bold tracking-widest text-white uppercase flex items-center gap-2"><Settings2 className="w-4 h-4 text-[#d4a373]" /> WHAT-IF DISRUPTION</h2>
        </div>
        <div className="p-4 flex-1 flex flex-col">
          {!selectedPost ? (
             <div className="flex-1 flex items-center justify-center text-xs text-gray-500 uppercase tracking-widest">Select a post to run disruptions</div>
          ) : whatIfLoading ? (
             <div className="flex-1 flex flex-col items-center justify-center">
               <Loader2 className="w-6 h-6 text-[#d4a373] animate-spin mb-3" />
               <div className="text-[10px] text-[#d4a373] font-bold tracking-widest uppercase">SIMULATING DISRUPTION...</div>
             </div>
          ) : decision ? (
             <div className="flex-1 flex flex-col items-center justify-center">
               <CheckCircle className="w-8 h-8 text-[#52b788] mb-2" />
               <div className="text-xs text-[#52b788] font-bold tracking-widest uppercase">PLAN UPDATED</div>
               <div className="text-[10px] text-gray-400 mt-1">Disruption simulation resolved via HITL.</div>
             </div>
          ) : whatIf ? (
             <div className="flex-1 flex flex-col">
               <div className="flex justify-between items-start mb-3">
                 <div>
                   <div className="text-[9px] text-gray-500 uppercase">Scenario</div>
                   <div className="text-sm text-[#e63946] font-bold tracking-widest uppercase">{whatIf.scenario || whatIf.disruption_type}</div>
                 </div>
                 <div className="text-right">
                   <div className="text-[9px] text-gray-500 uppercase">IMPACT SCORE</div>
                   <div className="text-sm font-mono text-[#e63946] font-bold">{whatIf.impact_score} / 100</div>
                 </div>
               </div>
               
               <div className="grid grid-cols-2 gap-2 mb-3">
                 <div className="bg-[#131915] p-2 rounded border border-[#2a362c]">
                   <div className="text-[8px] text-gray-500 uppercase">AFFECTED POSTS</div>
                   <div className="text-xs font-mono text-white mt-1">{(whatIf.affected_posts || []).join(', ')}</div>
                 </div>
                 <div className="bg-[#131915] p-2 rounded border border-[#2a362c]">
                   <div className="text-[8px] text-gray-500 uppercase">AFFECTED LEGS</div>
                   <div className="text-xs font-mono text-[#e63946] mt-1">{(whatIf.affected_legs || []).join(', ')}</div>
                 </div>
               </div>

               <div className="bg-[#1c231e] p-3 rounded border border-[#52b788]/30 flex-1">
                 <div className="text-[9px] text-[#52b788] font-bold uppercase tracking-widest mb-1">SYSTEM RECOMMENDS: {whatIf.recommendation}</div>
                 <div className="text-[10px] text-white leading-tight">{whatIf.reason}</div>
               </div>
             </div>
          ) : (
             <div className="flex-1 flex flex-col justify-center">
               <div className="text-[10px] text-gray-400 mb-3 text-center uppercase tracking-widest">Select scenario for {selectedPost.id.replace('FP-00','F-0')}</div>
               <div className="grid grid-cols-1 gap-2">
                 <button onClick={() => runWhatIf('Road Closure')} className="bg-[#131915] hover:bg-[#1c231e] text-[#d4a373] border border-[#d4a373]/40 hover:border-[#d4a373] py-2 text-[10px] font-bold tracking-widest uppercase rounded transition-all">ROAD CLOSURE</button>
                 <button onClick={() => runWhatIf('Heavy Snow')} className="bg-[#131915] hover:bg-[#1c231e] text-white border border-[#2a362c] hover:border-gray-500 py-2 text-[10px] font-bold tracking-widest uppercase rounded transition-all">HEAVY SNOW</button>
                 <button onClick={() => runWhatIf('Heli Grounding')} className="bg-[#131915] hover:bg-[#1c231e] text-white border border-[#2a362c] hover:border-gray-500 py-2 text-[10px] font-bold tracking-widest uppercase rounded transition-all">HELI GROUNDING</button>
               </div>
             </div>
          )}
        </div>
      </div>

      {/* BEFORE / AFTER PANEL */}
      <div className="flex-[1.5] bg-[#0b0f0c] border border-[#2a362c] rounded flex flex-col overflow-hidden">
        <div className="p-3 border-b border-[#2a362c] flex justify-between items-center bg-[#131915]">
          <h2 className="text-xs font-bold tracking-widest text-white uppercase flex items-center gap-2"><GitMerge className="w-4 h-4 text-[#457b9d]" /> BEFORE / AFTER</h2>
        </div>
        <div className="p-4 flex-1 flex">
          {!whatIf ? (
             <div className="flex-1 flex items-center justify-center text-xs text-gray-500 uppercase tracking-widest">Awaiting Simulation</div>
          ) : (
             <div className="flex-1 flex gap-4">
               {/* BEFORE */}
               <div className="flex-1 flex flex-col">
                 <div className="text-[9px] text-gray-500 font-bold uppercase tracking-widest mb-2 border-b border-[#2a362c] pb-1">CURRENT PLAN</div>
                 <div className="space-y-2 flex-1 text-[10px]">
                   <div className="flex justify-between"><span className="text-gray-500">Route</span><span className="font-mono text-white">{whatIf.before_after.before.route}</span></div>
                   <div className="flex justify-between"><span className="text-gray-500">Mode</span><span className="font-mono text-white">{whatIf.before_after.before.mode}</span></div>
                   <div className="flex justify-between"><span className="text-gray-500">ETA</span><span className="font-mono text-white">{whatIf.before_after.before.eta}</span></div>
                   <div className="flex justify-between"><span className="text-gray-500">Risk</span><span className="font-mono text-[#e63946]">{whatIf.before_after.before.risk}</span></div>
                 </div>
               </div>
               
               {/* AFTER */}
               <div className="flex-1 flex flex-col bg-[#131915] p-2 rounded border border-[#2a362c]">
                 <div className="text-[9px] text-[#52b788] font-bold uppercase tracking-widest mb-2 border-b border-[#2a362c] pb-1">AFTER (Replanned)</div>
                 <div className="space-y-2 flex-1 text-[10px]">
                   <div className="flex justify-between"><span className="text-gray-500">Route</span><span className="font-mono text-[#52b788]">{whatIf.before_after.after.route}</span></div>
                   <div className="flex justify-between"><span className="text-gray-500">Mode</span><span className="font-mono text-[#52b788]">{whatIf.before_after.after.mode || whatIf.before_after.after.new_mode}</span></div>
                   <div className="flex justify-between"><span className="text-gray-500">ETA</span><span className="font-mono text-white">{whatIf.before_after.after.eta}</span></div>
                   <div className="flex justify-between"><span className="text-gray-500">Risk</span><span className="font-mono text-[#d4a373]">{whatIf.before_after.after.risk}</span></div>
                 </div>
               </div>

               {/* METRICS */}
               <div className="flex-1 flex flex-col border-l border-[#2a362c] pl-4">
                 <div className="text-[9px] text-gray-500 font-bold uppercase tracking-widest mb-2 border-b border-[#2a362c] pb-1">IMPACT OF REPLAN</div>
                 <div className="space-y-3 mt-2">
                   <div>
                     <div className="text-[8px] text-gray-500 uppercase">Route Changes</div>
                     <div className="text-xs font-mono text-white">{whatIf.route_changes}</div>
                   </div>
                   <div>
                     <div className="text-[8px] text-gray-500 uppercase">Recovery</div>
                     <div className="text-xs font-mono text-[#52b788]">{whatIf.recovery}</div>
                   </div>
                   <div>
                     <div className="text-[8px] text-gray-500 uppercase">Network Stability</div>
                     <div className="text-xs font-mono text-white">{whatIf.network_stability}</div>
                   </div>
                 </div>
               </div>
             </div>
          )}
        </div>
      </div>

      {/* COMMAND DECISION PANEL */}
      <div className="flex-[1] bg-[#0b0f0c] border border-[#2a362c] rounded flex flex-col overflow-hidden relative">
        <div className="p-3 border-b border-[#2a362c] flex justify-between items-center bg-[#131915]">
          <h2 className="text-xs font-bold tracking-widest text-white uppercase flex items-center gap-2"><ShieldCheck className="w-4 h-4 text-[#52b788]" /> COMMAND DECISION</h2>
        </div>
        <div className="p-4 flex-1 flex flex-col">
          {!whatIf ? (
             <div className="flex-1 flex items-center justify-center text-xs text-gray-500 uppercase tracking-widest text-center">Awaiting Simulation</div>
          ) : decision ? (
             <div className="flex-1 flex flex-col items-center justify-center">
               {decision.status === 'REJECT' ? (
                 <>
                   <XCircle className="w-8 h-8 text-[#e63946] mb-2" />
                   <div className="text-xs text-[#e63946] font-bold tracking-widest uppercase">DECISION REJECTED</div>
                   <div className="text-[10px] text-gray-400 mt-1">PLAN RETAINED</div>
                 </>
               ) : (
                 <>
                   <CheckCircle className="w-8 h-8 text-[#52b788] mb-2" />
                   <div className="text-xs text-[#52b788] font-bold tracking-widest uppercase">DECISION APPROVED</div>
                   <div className="text-[10px] text-white font-mono mt-2 bg-[#1c231e] px-2 py-1 rounded">{decision.scope} REPLAN AUTHORIZED</div>
                   {decision.status === 'OVERRIDE' && <div className="text-[9px] text-[#d4a373] mt-2 uppercase tracking-widest">USER OVERRIDE APPLIED</div>}
                 </>
               )}
             </div>
          ) : overrideOpen ? (
             <div className="flex-1 flex flex-col">
               <div className="text-[9px] text-gray-400 uppercase tracking-widest mb-2 text-center">SELECT ALTERNATIVE SCOPE</div>
               <div className="flex-1 space-y-2">
                 <button onClick={() => makeDecision('OVERRIDE', 'PRESERVE')} className="w-full bg-[#131915] hover:bg-[#1c231e] border border-[#2a362c] py-2 text-[9px] font-bold text-white uppercase rounded">PRESERVE</button>
                 <button onClick={() => makeDecision('OVERRIDE', 'LOCAL')} className="w-full bg-[#131915] hover:bg-[#1c231e] border border-[#2a362c] py-2 text-[9px] font-bold text-white uppercase rounded">LOCAL</button>
                 <button onClick={() => makeDecision('OVERRIDE', 'GLOBAL')} className="w-full bg-[#131915] hover:bg-[#1c231e] border border-[#2a362c] py-2 text-[9px] font-bold text-white uppercase rounded">GLOBAL</button>
               </div>
               <button onClick={() => setOverrideOpen(false)} className="mt-2 py-1 text-[9px] text-gray-500 hover:text-white uppercase">CANCEL</button>
             </div>
          ) : (
             <div className="flex-1 flex flex-col justify-end">
               <div className="text-[10px] text-center mb-4 text-gray-400">Awaiting Commander Review</div>
               <div className="space-y-2">
                 <button onClick={() => makeDecision('APPROVE')} className="w-full bg-[#52b788]/20 hover:bg-[#52b788]/30 border border-[#52b788] text-[#52b788] py-2 text-[10px] font-bold tracking-widest uppercase rounded transition-all">APPROVE</button>
                 <div className="flex gap-2">
                   <button onClick={() => setOverrideOpen(true)} className="flex-1 bg-[#131915] hover:bg-[#1c231e] border border-[#d4a373]/40 text-[#d4a373] py-2 text-[10px] font-bold tracking-widest uppercase rounded transition-all">OVERRIDE</button>
                   <button onClick={() => makeDecision('REJECT')} className="flex-1 bg-[#131915] hover:bg-[#1c231e] border border-[#e63946]/40 text-[#e63946] py-2 text-[10px] font-bold tracking-widest uppercase rounded transition-all">REJECT</button>
                 </div>
               </div>
             </div>
          )}
        </div>
      </div>

      {/* AUDIT TRAIL */}
      <div className="flex-[1] bg-[#0b0f0c] border border-[#2a362c] rounded flex flex-col overflow-hidden">
        <div className="p-3 border-b border-[#2a362c] flex justify-between items-center bg-[#131915]">
          <h2 className="text-xs font-bold tracking-widest text-white uppercase flex items-center gap-2"><ListTodo className="w-4 h-4 text-gray-400" /> AUDIT TRAIL</h2>
        </div>
        <div className="flex-1 overflow-y-auto p-2 space-y-1 custom-scrollbar">
          {audits.map((a:any, i:number) => (
             <div key={i} className={`text-[9px] p-2 rounded flex flex-col ${a.user === 'COMMANDER' ? 'bg-[#1c231e] border-l-2 border-[#52b788]' : 'bg-[#131915] border border-[#2a362c]'}`}>
               <div className="flex justify-between text-gray-500 mb-1">
                 <span className="font-mono">{new Date(a.timestamp).toLocaleTimeString()}</span>
                 <span className={a.user === 'COMMANDER' ? 'text-[#457b9d] font-bold' : ''}>{a.user}</span>
               </div>
               <div className="text-white font-mono break-words leading-tight">
                 <span className="text-gray-400">{a.action}:</span> {a.decision} {a.scenario ? `(${a.scenario})` : ''}
               </div>
             </div>
          ))}
        </div>
      </div>
    </div>
  );
}
'''.lstrip()))

print("All components written.")

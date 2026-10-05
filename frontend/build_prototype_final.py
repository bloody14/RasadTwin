import os, textwrap

base = "src"
comp = os.path.join(base, "components")
views = os.path.join(base, "views")
os.makedirs(comp, exist_ok=True)
os.makedirs(views, exist_ok=True)

# ─────────────────────────────────────────────
# 1. App.tsx — auto-select F-01, sidebar views, demo steps
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

  // Sidebar shortcuts: WHAT_IF, DECISIONS, AUDIT navigate to COMMAND but scroll
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
              <KPIBar posts={posts} routes={routes} whatIf={whatIf} />
              <div className="flex-1 flex gap-2 overflow-hidden">
                <LogisticsMap posts={posts} routes={routes} selectedPost={selectedPost} handleSelectPost={selectPost} whatIf={whatIf} />
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
# 2. DemoWalkthrough.tsx
# ─────────────────────────────────────────────
open(os.path.join(comp, "DemoWalkthrough.tsx"), "w", encoding="utf-8").write(textwrap.dedent(r'''
import React, { useState } from 'react';
import { ChevronDown, ChevronUp, CheckCircle, Circle } from 'lucide-react';

const STEPS = [
  { key: 'postInspected', label: 'Select / inspect post' },
  { key: 'riskReviewed', label: 'Review risk & forecast' },
  { key: 'disruptionRun', label: 'Run disruption scenario' },
  { key: 'impactAssessed', label: 'Assess impact' },
  { key: 'scopeChosen', label: 'Choose replan scope' },
  { key: 'decisionMade', label: 'Approve / Override / Reject' },
  { key: 'auditReviewed', label: 'Review audit trail' },
];

export default function DemoWalkthrough({ steps }: { steps: Record<string, boolean> }) {
  const [open, setOpen] = useState(true);
  const done = STEPS.filter(s => steps[s.key]).length;

  return (
    <div className="absolute bottom-2 right-2 z-30 w-56">
      <button onClick={() => setOpen(!open)} className="w-full flex items-center justify-between bg-[#131915] border border-[#d4a373]/40 text-[#d4a373] px-3 py-1.5 rounded text-[10px] font-bold tracking-widest uppercase">
        DEMO FLOW ({done}/{STEPS.length})
        {open ? <ChevronDown className="w-3 h-3" /> : <ChevronUp className="w-3 h-3" />}
      </button>
      {open && (
        <div className="bg-[#0b0f0c] border border-[#2a362c] rounded mt-1 p-2 space-y-1.5">
          {STEPS.map((s, i) => {
            const isDone = steps[s.key];
            return (
              <div key={s.key} className={`flex items-center gap-2 text-[10px] ${isDone ? 'text-[#52b788]' : 'text-gray-500'}`}>
                {isDone ? <CheckCircle className="w-3 h-3 text-[#52b788]" /> : <Circle className="w-3 h-3" />}
                <span>{i + 1}. {s.label}</span>
              </div>
            );
          })}
          <div className="border-t border-[#2a362c] pt-1 mt-1 text-[8px] text-gray-600 text-center">SYNTHETIC DEMO • NO REAL DATA</div>
        </div>
      )}
    </div>
  );
}
'''.lstrip()))

# ─────────────────────────────────────────────
# 3. PostsView.tsx
# ─────────────────────────────────────────────
open(os.path.join(views, "PostsView.tsx"), "w", encoding="utf-8").write(textwrap.dedent(r'''
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
'''.lstrip()))

# ─────────────────────────────────────────────
# 4. ForecastView.tsx
# ─────────────────────────────────────────────
open(os.path.join(views, "ForecastView.tsx"), "w", encoding="utf-8").write(textwrap.dedent(r'''
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
'''.lstrip()))

# ─────────────────────────────────────────────
# 5. InventoryView.tsx
# ─────────────────────────────────────────────
open(os.path.join(views, "InventoryView.tsx"), "w", encoding="utf-8").write(textwrap.dedent(r'''
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
'''.lstrip()))

# ─────────────────────────────────────────────
# 6. RoutingView.tsx
# ─────────────────────────────────────────────
open(os.path.join(views, "RoutingView.tsx"), "w", encoding="utf-8").write(textwrap.dedent(r'''
import React from 'react';
import { GitMerge } from 'lucide-react';

export default function RoutingView({ routes }: any) {
  const riskColor = (r: string) => r === 'High' ? 'text-[#e63946]' : r === 'Medium' ? 'text-[#d4a373]' : 'text-[#52b788]';

  return (
    <div className="flex-1 bg-[#0b0f0c] border border-[#2a362c] rounded p-4 overflow-y-auto custom-scrollbar">
      <h2 className="text-sm font-bold tracking-widest text-white uppercase mb-4 flex items-center gap-2"><GitMerge className="w-4 h-4 text-[#457b9d]" /> ROUTE NETWORK</h2>
      <table className="w-full text-[10px]">
        <thead>
          <tr className="text-gray-500 uppercase tracking-widest border-b border-[#2a362c]">
            <th className="text-left py-2 px-2">Route</th>
            <th className="text-left py-2 px-2">Source</th>
            <th className="text-left py-2 px-2">Target</th>
            <th className="text-left py-2 px-2">Mode</th>
            <th className="text-right py-2 px-2">Distance</th>
            <th className="text-right py-2 px-2">Nominal ETA</th>
            <th className="text-right py-2 px-2">Robust ETA</th>
            <th className="text-right py-2 px-2">Risk</th>
          </tr>
        </thead>
        <tbody>
          {routes.map((r:any) => (
            <tr key={r.id} className="border-b border-[#2a362c]/50 hover:bg-[#1c231e]">
              <td className="py-2 px-2 font-mono font-bold text-white">{r.id}</td>
              <td className="py-2 px-2 text-gray-400">{r.source}</td>
              <td className="py-2 px-2 text-gray-400">{r.target}</td>
              <td className="py-2 px-2 text-white">{r.mode}</td>
              <td className="py-2 px-2 text-right font-mono text-gray-400">{r.distance_km} km</td>
              <td className="py-2 px-2 text-right font-mono text-[#457b9d]">{r.eta_hrs}h</td>
              <td className="py-2 px-2 text-right font-mono text-[#d4a373]">{r.robust_eta_hrs}h</td>
              <td className={`py-2 px-2 text-right font-bold uppercase ${riskColor(r.risk)}`}>{r.risk}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
'''.lstrip()))

# ─────────────────────────────────────────────
# 7. DecisionsView.tsx
# ─────────────────────────────────────────────
open(os.path.join(views, "DecisionsView.tsx"), "w", encoding="utf-8").write(textwrap.dedent(r'''
import React from 'react';
import { ShieldCheck } from 'lucide-react';

export default function DecisionsView({ audits }: any) {
  const decisions = audits.filter((a:any) => a.action?.startsWith('HITL'));

  return (
    <div className="flex-1 bg-[#0b0f0c] border border-[#2a362c] rounded p-4 overflow-y-auto custom-scrollbar">
      <h2 className="text-sm font-bold tracking-widest text-white uppercase mb-4 flex items-center gap-2"><ShieldCheck className="w-4 h-4 text-[#52b788]" /> HITL DECISIONS</h2>
      {decisions.length === 0 ? (
        <div className="text-gray-500 text-xs text-center py-8 border border-dashed border-[#2a362c] rounded">No HITL decisions recorded yet. Run a What-If scenario from COMMAND view.</div>
      ) : (
        <div className="space-y-2">
          {decisions.map((d:any, i:number) => (
            <div key={i} className="bg-[#131915] border border-[#2a362c] p-3 rounded flex justify-between items-center">
              <div>
                <div className="text-xs font-bold text-white">{d.action}</div>
                <div className="text-[10px] text-gray-400">{d.scenario} → {d.decision}</div>
                <div className="text-[9px] text-gray-500">{d.reason}</div>
              </div>
              <div className="text-right">
                <div className="text-[10px] text-gray-500">{new Date(d.timestamp).toLocaleString()}</div>
                <div className="text-[9px] text-[#457b9d]">{d.user}</div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
'''.lstrip()))

# ─────────────────────────────────────────────
# 8. AuditView.tsx
# ─────────────────────────────────────────────
open(os.path.join(views, "AuditView.tsx"), "w", encoding="utf-8").write(textwrap.dedent(r'''
import React from 'react';
import { ListTodo } from 'lucide-react';

export default function AuditView({ audits }: any) {
  return (
    <div className="flex-1 bg-[#0b0f0c] border border-[#2a362c] rounded p-4 overflow-y-auto custom-scrollbar">
      <h2 className="text-sm font-bold tracking-widest text-white uppercase mb-4 flex items-center gap-2"><ListTodo className="w-4 h-4 text-[#d4a373]" /> FULL AUDIT TIMELINE</h2>
      {audits.length === 0 ? (
        <div className="text-gray-500 text-xs text-center py-8 border border-dashed border-[#2a362c] rounded">No audit events yet. Perform actions in the COMMAND view.</div>
      ) : (
        <div className="space-y-1 font-mono text-[10px]">
          {audits.map((a:any, i:number) => (
            <div key={i} className={`flex gap-3 px-2 py-1.5 rounded ${a.user === 'COMMANDER' ? 'bg-[#1c231e] text-white' : 'text-gray-400'}`}>
              <span className={a.user === 'COMMANDER' ? 'text-[#52b788]' : 'text-[#d4a373]'}>▶</span>
              <span className="w-36 text-gray-500 shrink-0">{new Date(a.timestamp).toLocaleString()}</span>
              <span className={`w-20 shrink-0 ${a.user === 'COMMANDER' ? 'text-[#457b9d]' : 'text-gray-500'}`}>{a.user}</span>
              <span className="w-24 shrink-0 text-white">{a.action}</span>
              <span className="truncate">{a.decision} — {a.scenario}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
'''.lstrip()))

# ─────────────────────────────────────────────
# 9. Updated BottomPanels - add fetchAudits + selectedPost props
# ─────────────────────────────────────────────
# Read current and just patch the props type:
bp = open(os.path.join(comp, "BottomPanels.tsx"), "r", encoding="utf-8").read()
# Replace the function signature to accept fetchAudits
bp = bp.replace(
    "export default function BottomPanels({ runWhatIf, whatIf, whatIfLoading, whatIfError, makeDecision, audits, decision })",
    "export default function BottomPanels({ runWhatIf, whatIf, whatIfLoading, whatIfError, makeDecision, audits, decision, fetchAudits, selectedPost }: any)"
)
# Replace the refresh button handler
bp = bp.replace(
    "onClick={() => runWhatIf(null, true)}",
    "onClick={() => fetchAudits && fetchAudits()}"
)
open(os.path.join(comp, "BottomPanels.tsx"), "w", encoding="utf-8").write(bp)

print("All components and views generated successfully.")

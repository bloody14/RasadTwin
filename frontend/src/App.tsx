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

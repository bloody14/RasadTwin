import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Menu, X } from 'lucide-react';

import CommandHeader from './components/CommandHeader';
import Sidebar from './components/Sidebar';
import KPIBar from './components/KPIBar';
import LogisticsMap from './components/LogisticsMap';
import PostIntelligence from './components/PostIntelligence';
import BottomPanels from './components/BottomPanels';
import DemoWalkthrough from './components/DemoWalkthrough';
import WeatherPanel from './components/WeatherPanel';

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
  const [weather, setWeather] = useState<any>(null);
  const [offline, setOffline] = useState(false);
  const [postLoading, setPostLoading] = useState(false);

  const [whatIf, setWhatIf] = useState<any>(null);
  const [whatIfLoading, setWhatIfLoading] = useState(false);
  const [decision, setDecision] = useState<any>(null);
  const [audits, setAudits] = useState<any[]>([]);
  
  // SYSTEM STATE
  // 'NORMAL' | 'DISRUPTION_DETECTED' | 'IMPACT_ASSESSED' | 'HUMAN_REVIEW' | 'PLAN_UPDATED'
  const [systemState, setSystemState] = useState('NORMAL');
  
  const [demoDrawerOpen, setDemoDrawerOpen] = useState(true);

  useEffect(() => { fetchData(); }, []);

  const fetchData = async () => {
    try {
      const [p, r, w] = await Promise.all([
        axios.get(`${API}/posts`),
        axios.get(`${API}/routes`),
        axios.get(`${API}/weather`),
      ]);
      setPosts(p.data.posts);
      setRoutes(r.data.routes);
      setWeather(w.data);
      setOffline(false);
      fetchAudits();

      // Auto-select first high-risk forward post
      const highRisk = p.data.posts.find((x:any) => x.risk === 'High' && x.type === 'forward_post');
      if (highRisk && !selectedPost) selectPost(highRisk);
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
    try {
      const [r, f] = await Promise.all([
        axios.get(`${API}/risk/${p.id}`),
        axios.get(`${API}/forecast/${p.id}`),
      ]);
      setRiskData(r.data);
      setForecast(f.data);
    } catch (e) {
      console.error(e);
    } finally {
      setPostLoading(false);
    }
  };

  const runWhatIf = async (type: string) => {
    if (!selectedPost) return;
    setWhatIfLoading(true);
    setDecision(null);
    setSystemState('DISRUPTION_DETECTED');
    try {
      const res = await axios.post(`${API}/what-if`, {
        disruption_type: type,
        target_id: selectedPost.id,
      });
      setWhatIf({ ...res.data, disruption_type: type, target_id: selectedPost.id });
      setSystemState('HUMAN_REVIEW');
    } catch {
      setSystemState('NORMAL');
    } finally {
      setWhatIfLoading(false);
    }
  };

  const makeDecision = async (user_action: string, scope: string | null = null) => {
    if (!whatIf) return;
    const finalScope = user_action === 'REJECT' ? 'NONE' : (scope || whatIf.recommendation);
    try {
      await axios.post(`${API}/decision`, {
        user: "COMMANDER",
        scenario: whatIf.disruption_type,
        system_recommendation: whatIf.recommendation,
        user_action: user_action,
        selected_scope: finalScope,
        reason: `User ${user_action} via HITL UI`,
      });
      setDecision({ status: user_action, scope: finalScope });
      setSystemState('PLAN_UPDATED');
      fetchAudits();
    } catch {
      alert("Failed to record decision.");
    }
  };

  const resetDemo = () => {
    setWhatIf(null);
    setDecision(null);
    setSystemState('NORMAL');
    fetchData();
  };

  const sharedProps = { posts, routes, selectedPost, selectPost, riskData, forecast, audits, decision };

  return (
    <div className="h-screen w-screen bg-[#070908] flex flex-col font-sans text-white overflow-hidden selection:bg-[#d4a373]/30">
      <CommandHeader offline={offline} />
      <div className="flex flex-1 overflow-hidden p-2 gap-2">
        <Sidebar activeView={activeView} setActiveView={setActiveView} />
        
        <div className="flex-1 flex flex-col min-w-0 relative">
          {activeView === 'COMMAND' && (
            <>
              <KPIBar systemState={systemState} posts={posts} routes={routes} whatIf={whatIf} decision={decision} />
              
              <div className="flex-1 flex gap-2 overflow-hidden mb-2">
                {/* Main Map Area */}
                <div className="flex-[2] flex flex-col gap-2 min-w-0">
                  <div className="flex-1 bg-[#0b0f0c] border border-[#2a362c] rounded relative overflow-hidden">
                    <button onClick={resetDemo} className="absolute top-2 left-2 z-50 bg-[#131915]/90 hover:bg-[#1c231e] border border-[#2a362c] text-gray-300 px-3 py-1.5 rounded text-[10px] font-bold tracking-widest uppercase transition-all shadow">
                      RESET NETWORK
                    </button>
                    <LogisticsMap posts={posts} routes={routes} selectedPost={selectedPost} handleSelectPost={selectPost} whatIf={whatIf} decision={decision} />
                  </div>
                </div>

                {/* Right Side Intelligence */}
                <div className="flex-1 flex flex-col gap-2 min-w-[300px] max-w-[400px]">
                  <WeatherPanel weather={weather} />
                  <div className="flex-1 overflow-hidden">
                    <PostIntelligence post={selectedPost} riskData={riskData} forecast={forecast} routes={routes} isLoading={postLoading} />
                  </div>
                </div>
              </div>
              
              {/* Bottom Panels (WhatIf, Before/After, Decision, Audit) */}
              <div className="h-[200px] shrink-0">
                <BottomPanels runWhatIf={runWhatIf} whatIf={whatIf} whatIfLoading={whatIfLoading} makeDecision={makeDecision} audits={audits} decision={decision} selectedPost={selectedPost} systemState={systemState} />
              </div>
              
              {/* Demo Flow Drawer Overlay */}
              {demoDrawerOpen ? (
                <div className="absolute top-12 right-12 z-[100] w-64 shadow-2xl bg-[#0b0f0c]/95 border border-[#52b788] rounded p-4 backdrop-blur">
                  <div className="flex justify-between items-center mb-4">
                    <div className="text-[10px] text-[#52b788] font-bold uppercase tracking-widest">DEMO WORKFLOW</div>
                    <button onClick={() => setDemoDrawerOpen(false)}><X className="w-4 h-4 text-gray-500 hover:text-white" /></button>
                  </div>
                  <DemoWalkthrough systemState={systemState} />
                </div>
              ) : (
                <button onClick={() => setDemoDrawerOpen(true)} className="absolute top-4 right-4 z-[100] bg-[#131915]/90 border border-[#2a362c] p-2 rounded hover:border-[#52b788] transition-all">
                  <Menu className="w-4 h-4 text-[#52b788]" />
                </button>
              )}
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

import React, { useState } from 'react';
import { AlertTriangle, Map, Navigation, Crosshair, ShieldCheck, CheckCircle, XCircle, ListTodo } from 'lucide-react';

export default function BottomPanels({ runWhatIf, whatIf, whatIfLoading, makeDecision, audits, decision, selectedPost, systemState }: any) {
  const [overrideOpen, setOverrideOpen] = useState(false);

  return (
    <div className="h-full flex gap-2">
      {/* WHAT-IF PANEL */}
      <div className="flex-1 bg-[#0b0f0c] border border-[#2a362c] rounded flex flex-col overflow-hidden">
        <div className="p-2 border-b border-[#2a362c] flex justify-between items-center bg-[#131915]">
          <h2 className="text-[10px] font-bold tracking-widest text-white uppercase flex items-center gap-2"><Crosshair className="w-3 h-3 text-gray-400" /> WHAT-IF ENGINE</h2>
        </div>
        <div className="p-2 flex-1 flex flex-col">
          {!selectedPost ? (
            <div className="flex-1 flex items-center justify-center text-xs text-gray-500 uppercase tracking-widest">Select Node</div>
          ) : (
            <>
              <div className="text-[9px] text-gray-500 uppercase tracking-widest mb-2">Simulate Disruption ({selectedPost.id})</div>
              <div className="grid grid-cols-2 gap-2 flex-1">
                <button onClick={() => runWhatIf('Road Closure')} disabled={whatIfLoading} className="bg-[#131915] border border-[#2a362c] hover:border-[#e63946] text-[#e63946] rounded text-[10px] font-bold uppercase transition-all">ROAD CLOSURE</button>
                <button onClick={() => runWhatIf('Heavy Snow')} disabled={whatIfLoading} className="bg-[#131915] border border-[#2a362c] hover:border-[#d4a373] text-[#d4a373] rounded text-[10px] font-bold uppercase transition-all">HEAVY SNOW</button>
                <button onClick={() => runWhatIf('Heli Grounding')} disabled={whatIfLoading} className="bg-[#131915] border border-[#2a362c] hover:border-[#6D9FB3] text-[#6D9FB3] rounded text-[10px] font-bold uppercase transition-all col-span-2">HELI GROUNDING</button>
              </div>
            </>
          )}
        </div>
      </div>

      {/* BEFORE / AFTER / RECOMMENDATION */}
      <div className="flex-[2] bg-[#0b0f0c] border border-[#2a362c] rounded flex flex-col overflow-hidden">
        <div className="p-2 border-b border-[#2a362c] flex justify-between items-center bg-[#131915]">
          <h2 className="text-[10px] font-bold tracking-widest text-white uppercase flex items-center gap-2"><Map className="w-3 h-3 text-gray-400" /> IMPACT & REPLAN</h2>
          {whatIf && <span className="text-[9px] bg-[#e63946]/20 text-[#e63946] px-2 py-0.5 rounded font-bold uppercase tracking-widest">IMPACT SCORE: {whatIf.impact_score}</span>}
        </div>
        <div className="p-2 flex-1 flex">
          {!whatIf ? (
             <div className="flex-1 flex items-center justify-center text-xs text-gray-500 uppercase tracking-widest">Awaiting Simulation</div>
          ) : (
             <div className="flex-1 flex gap-4">
               {/* BEFORE */}
               <div className="flex-1 border-r border-[#2a362c] pr-4">
                 <div className="text-[9px] text-gray-500 font-bold uppercase tracking-widest mb-1 border-b border-[#2a362c] pb-1">CURRENT PLAN</div>
                 <div className="space-y-1 text-[10px]">
                   <div className="flex justify-between"><span className="text-gray-600">Route</span><span className="font-mono text-[#e63946]">{whatIf.before_after.before.route}</span></div>
                   <div className="flex justify-between"><span className="text-gray-600">Mode</span><span className="font-mono text-white">{whatIf.before_after.before.mode}</span></div>
                   <div className="flex justify-between"><span className="text-gray-600">ETA</span><span className="font-mono text-white">{whatIf.before_after.before.eta}</span></div>
                 </div>
               </div>
               
               {/* AFTER */}
               <div className="flex-1">
                 <div className="text-[9px] text-[#52b788] font-bold uppercase tracking-widest mb-1 border-b border-[#2a362c] pb-1">PLAN DIFF</div>
                 <div className="space-y-1 text-[10px]">
                   <div className="flex justify-between"><span className="text-gray-600">Route</span><span className="font-mono text-[#52b788]">{whatIf.before_after.after.route}</span></div>
                   <div className="flex justify-between"><span className="text-gray-600">Mode</span><span className="font-mono text-[#52b788]">{whatIf.before_after.after.mode || whatIf.before_after.after.new_mode}</span></div>
                   <div className="flex justify-between"><span className="text-gray-600">ETA</span><span className="font-mono text-white">{whatIf.before_after.after.eta}</span></div>
                 </div>
               </div>

               {/* RECOM */}
               <div className="w-[120px] bg-[#131915] rounded p-2 border border-[#2a362c] flex flex-col justify-center items-center">
                 <div className="text-[8px] text-gray-500 uppercase text-center mb-1">SYSTEM RECOMMENDS</div>
                 <div className="text-xs font-bold text-white uppercase tracking-widest text-center">{whatIf.recommendation}</div>
               </div>
             </div>
          )}
        </div>
      </div>

      {/* COMMAND DECISION PANEL */}
      <div className="flex-[1.2] bg-[#0b0f0c] border border-[#2a362c] rounded flex flex-col overflow-hidden relative">
        <div className="p-2 border-b border-[#2a362c] flex justify-between items-center bg-[#131915]">
          <h2 className="text-[10px] font-bold tracking-widest text-white uppercase flex items-center gap-2"><ShieldCheck className="w-3 h-3 text-[#52b788]" /> COMMAND DECISION</h2>
        </div>
        <div className="p-2 flex-1 flex flex-col">
          {!whatIf ? (
             <div className="flex-1 flex items-center justify-center text-[10px] text-gray-500 uppercase tracking-widest text-center">Awaiting Simulation</div>
          ) : decision ? (
             <div className="flex-1 flex flex-col items-center justify-center">
               {decision.status === 'REJECT' ? (
                 <>
                   <div className="text-[10px] text-[#e63946] font-bold tracking-widest uppercase mb-1">DECISION REJECTED</div>
                   <div className="text-[9px] text-gray-400">PLAN RETAINED</div>
                 </>
               ) : (
                 <>
                   <div className="text-[10px] text-[#52b788] font-bold tracking-widest uppercase mb-1">PLAN AUTHORIZED</div>
                   <div className="text-[9px] text-white font-mono bg-[#1c231e] px-2 py-1 rounded">SCOPE: {decision.scope}</div>
                 </>
               )}
             </div>
          ) : overrideOpen ? (
             <div className="flex-1 flex flex-col justify-center gap-1">
               <div className="text-[8px] text-gray-400 uppercase tracking-widest text-center">SELECT OVERRIDE SCOPE</div>
               <div className="flex gap-1">
                 <button onClick={() => makeDecision('OVERRIDE', 'PRESERVE')} className="flex-1 bg-[#131915] border border-[#2a362c] py-1.5 text-[9px] font-bold text-white uppercase rounded">PRESERVE</button>
                 <button onClick={() => makeDecision('OVERRIDE', 'LOCAL')} className="flex-1 bg-[#131915] border border-[#2a362c] py-1.5 text-[9px] font-bold text-white uppercase rounded">LOCAL</button>
                 <button onClick={() => makeDecision('OVERRIDE', 'GLOBAL')} className="flex-1 bg-[#131915] border border-[#2a362c] py-1.5 text-[9px] font-bold text-white uppercase rounded">GLOBAL</button>
               </div>
               <button onClick={() => setOverrideOpen(false)} className="mt-1 text-[8px] text-gray-500 hover:text-white uppercase">CANCEL</button>
             </div>
          ) : (
             <div className="flex-1 flex flex-col justify-center gap-2">
               <button onClick={() => makeDecision('APPROVE')} className="w-full bg-[#52b788]/20 border border-[#52b788] text-[#52b788] py-1.5 text-[10px] font-bold tracking-widest uppercase rounded">APPROVE {whatIf.recommendation}</button>
               <div className="flex gap-2">
                 <button onClick={() => setOverrideOpen(true)} className="flex-1 bg-[#131915] border border-[#d4a373]/40 text-[#d4a373] py-1 text-[9px] font-bold tracking-widest uppercase rounded">OVERRIDE</button>
                 <button onClick={() => makeDecision('REJECT')} className="flex-1 bg-[#131915] border border-[#e63946]/40 text-[#e63946] py-1 text-[9px] font-bold tracking-widest uppercase rounded">REJECT</button>
               </div>
             </div>
          )}
        </div>
      </div>
      
      {/* COMPACT AUDIT DRAWER (Right side) */}
      <div className="flex-[1] bg-[#0b0f0c] border border-[#2a362c] rounded flex flex-col overflow-hidden">
        <div className="p-2 border-b border-[#2a362c] flex justify-between items-center bg-[#131915]">
          <h2 className="text-[10px] font-bold tracking-widest text-white uppercase flex items-center gap-2"><ListTodo className="w-3 h-3 text-gray-400" /> AUDIT</h2>
        </div>
        <div className="flex-1 overflow-y-auto p-1 space-y-1 custom-scrollbar">
          {audits.slice(0,10).map((a:any, i:number) => (
             <div key={i} className={`text-[8px] p-1.5 rounded flex flex-col ${a.user === 'COMMANDER' ? 'bg-[#1c231e] border-l-2 border-[#52b788]' : 'bg-[#131915] border border-[#2a362c]'}`}>
               <div className="flex justify-between text-gray-500 mb-0.5">
                 <span className="font-mono">{new Date(a.timestamp).toLocaleTimeString()}</span>
               </div>
               <div className="text-white font-mono break-words leading-tight">
                 <span className="text-[#d4a373]">{a.action}:</span> {a.selected_scope} {a.scenario ? `[${a.scenario}]` : ''}
               </div>
             </div>
          ))}
        </div>
      </div>
    </div>
  );
}

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

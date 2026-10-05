import React, { useState } from 'react';
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

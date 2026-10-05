import React from 'react';

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

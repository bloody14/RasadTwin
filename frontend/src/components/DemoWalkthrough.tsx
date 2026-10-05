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

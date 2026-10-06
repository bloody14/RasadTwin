import React from 'react';
import { Play } from 'lucide-react';

export default function DemoWalkthrough({ systemState }: any) {
  const steps = [
    { state: 'NORMAL', label: 'Monitor Network' },
    { state: 'DISRUPTION_DETECTED', label: 'Disruption Detected' },
    { state: 'HUMAN_REVIEW', label: 'Review Recommendation' },
    { state: 'PLAN_UPDATED', label: 'Plan Activated' },
  ];
  
  const currentIndex = steps.findIndex(s => s.state === systemState);

  return (
    <div className="space-y-3">
      {steps.map((step, i) => {
        const isPast = currentIndex > i;
        const isActive = systemState === step.state;
        const color = isActive ? 'text-[#52b788]' : (isPast ? 'text-gray-400' : 'text-gray-700');
        const bulletColor = isActive ? 'bg-[#52b788]' : (isPast ? 'bg-gray-400' : 'bg-gray-700');
        
        return (
          <div key={i} className={`flex items-center gap-3 text-[10px] font-bold uppercase tracking-widest ${color}`}>
            <div className={`w-3 h-3 rounded-full flex items-center justify-center border border-current`}>
               <div className={`w-1.5 h-1.5 rounded-full ${bulletColor}`}></div>
            </div>
            {step.label}
          </div>
        );
      })}
    </div>
  );
}

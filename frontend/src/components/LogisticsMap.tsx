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

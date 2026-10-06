import React, { useState, useEffect, useRef } from 'react';
import { MapPin, Navigation, ZoomIn, ZoomOut, Maximize } from 'lucide-react';

export default function LogisticsMap({ posts, routes, selectedPost, handleSelectPost, whatIf, decision }: any) {
  const containerRef = useRef<HTMLDivElement>(null);
  
  // Viewport bounds for SVG
  const [bounds, setBounds] = useState({ minLng: 0, maxLng: 100, minLat: 0, maxLat: 100 });
  const [zoom, setZoom] = useState(1);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });

  useEffect(() => {
    if (posts.length === 0) return;
    fitNetwork();
  }, [posts]);

  const fitNetwork = () => {
    if (posts.length === 0) return;
    const lats = posts.map((p:any) => p.lat);
    const lngs = posts.map((p:any) => p.lng);
    const minLat = Math.min(...lats);
    const maxLat = Math.max(...lats);
    const minLng = Math.min(...lngs);
    const maxLng = Math.max(...lngs);
    
    const latPad = (maxLat - minLat) * 0.15 || 0.1;
    const lngPad = (maxLng - minLng) * 0.15 || 0.1;

    setBounds({
      minLng: minLng - lngPad,
      maxLng: maxLng + lngPad,
      minLat: minLat - latPad,
      maxLat: maxLat + latPad
    });
    setZoom(1);
    setPan({ x: 0, y: 0 });
  };

  const getX = (lng: number) => {
    const range = bounds.maxLng - bounds.minLng;
    if (range === 0) return 500;
    return ((lng - bounds.minLng) / range) * 1000;
  };
  
  const getY = (lat: number) => {
    const range = bounds.maxLat - bounds.minLat;
    if (range === 0) return 500;
    return 1000 - (((lat - bounds.minLat) / range) * 1000);
  };

  const getStatusColor = (risk: string) => {
    if (risk === 'High') return '#e63946';
    if (risk === 'Medium') return '#d4a373';
    return '#52b788';
  };
  
  const renderShape = (p: any) => {
    const x = getX(p.lng);
    const y = getY(p.lat);
    const color = getStatusColor(p.risk);
    const isSelected = selectedPost?.id === p.id;
    const strokeW = isSelected ? 4 / zoom : 2 / zoom;
    const strokeC = isSelected ? '#fff' : color;
    const size = 12 / zoom;
    
    if (p.type === 'rear_depot') {
       return <rect x={x - size} y={y - size} width={size*2} height={size*2} fill="#131915" stroke={strokeC} strokeWidth={strokeW} />;
    } else if (p.type === 'intermediate_depot') {
       return <polygon points={`${x},${y - size*1.2} ${x - size*1.2},${y + size} ${x + size*1.2},${y + size}`} fill="#131915" stroke={strokeC} strokeWidth={strokeW} />;
    } else {
       return <circle cx={x} cy={y} r={size*0.8} fill="#131915" stroke={strokeC} strokeWidth={strokeW} />;
    }
  };

  const getRouteDash = (mode: string) => {
    if (mode === 'Road') return 'none';
    if (mode === 'Mule') return `${8/zoom},${8/zoom}`;
    if (mode === 'Heli') return `${4/zoom},${4/zoom}`;
    if (mode === 'Drone') return `${2/zoom},${6/zoom}`;
    return 'none';
  };

  const handleWheel = (e: React.WheelEvent) => {
    e.preventDefault();
    const zoomFactor = e.deltaY > 0 ? 0.9 : 1.1;
    setZoom(z => Math.max(0.5, Math.min(z * zoomFactor, 5)));
  };

  const handleMouseDown = (e: React.MouseEvent) => {
    setIsDragging(true);
    setDragStart({ x: e.clientX - pan.x, y: e.clientY - pan.y });
  };
  
  const handleMouseMove = (e: React.MouseEvent) => {
    if (!isDragging) return;
    setPan({ x: e.clientX - dragStart.x, y: e.clientY - dragStart.y });
  };
  
  const handleMouseUp = () => setIsDragging(false);

  return (
    <div className="w-full h-full relative bg-[#0B0F0C] overflow-hidden" ref={containerRef} onWheel={handleWheel} onMouseDown={handleMouseDown} onMouseMove={handleMouseMove} onMouseUp={handleMouseUp} onMouseLeave={handleMouseUp}>
      {whatIf && !decision && (
        <div className="absolute top-4 left-1/2 -translate-x-1/2 z-10 bg-[#e63946]/20 border border-[#e63946] text-[#e63946] px-4 py-2 rounded text-xs font-bold tracking-widest uppercase backdrop-blur animate-pulse pointer-events-none">
          DISRUPTION SIMULATION ACTIVE
        </div>
      )}
      {decision && (
        <div className="absolute top-4 left-1/2 -translate-x-1/2 z-10 bg-[#52b788]/20 border border-[#52b788] text-[#52b788] px-4 py-2 rounded text-xs font-bold tracking-widest uppercase backdrop-blur pointer-events-none">
          UPDATED PLAN ACTIVE
        </div>
      )}
      
      {/* Zoom Controls */}
      <div className="absolute top-4 right-4 z-10 flex flex-col gap-1 bg-[#131915]/80 border border-[#2a362c] rounded p-1 backdrop-blur">
        <button onClick={() => setZoom(z => Math.min(z * 1.2, 5))} className="p-1 hover:bg-[#1c231e] text-gray-400 hover:text-white rounded"><ZoomIn className="w-4 h-4" /></button>
        <button onClick={() => setZoom(z => Math.max(z * 0.8, 0.5))} className="p-1 hover:bg-[#1c231e] text-gray-400 hover:text-white rounded"><ZoomOut className="w-4 h-4" /></button>
        <button onClick={fitNetwork} className="p-1 hover:bg-[#1c231e] text-gray-400 hover:text-white rounded"><Maximize className="w-4 h-4" /></button>
      </div>

      <svg className="w-full h-full cursor-grab active:cursor-grabbing" viewBox="0 0 1000 1000">
        <g transform={`translate(${pan.x}, ${pan.y}) scale(${zoom})`} transform-origin="500 500">
          {routes.map((r: any) => {
             const isDisrupted = whatIf && !decision && whatIf.affected_legs.includes(r.id);
             const isRemoved = decision && decision.status === 'APPROVE' && whatIf.affected_legs.includes(r.id);
             
             if (isRemoved) return null;
             
             const src = posts.find((p:any) => p.id === r.source);
             const tgt = posts.find((p:any) => p.id === r.target);
             if (!src || !tgt) return null;
             
             const x1 = getX(src.lng);
             const y1 = getY(src.lat);
             const x2 = getX(tgt.lng);
             const y2 = getY(tgt.lat);
             
             let color = '#2a362c';
             let width = (r.mode === 'Road' ? 4 : 2) / zoom;
             if (r.mode === 'Heli' || r.mode === 'Drone') width = 1.5 / zoom;

             if (isDisrupted) {
               color = '#e63946';
               width = 6 / zoom;
             } else if (selectedPost && (r.source === selectedPost.id || r.target === selectedPost.id)) {
               color = '#6D9FB3';
             }
             
             return (
               <g key={r.id}>
                 <line x1={x1} y1={y1} x2={x2} y2={y2} stroke={color} strokeWidth={width} strokeDasharray={getRouteDash(r.mode)} opacity={isDisrupted ? 1 : 0.6} />
                 {isDisrupted && (
                    <text x={(x1+x2)/2} y={(y1+y2)/2} fill="#e63946" fontSize={32/zoom} textAnchor="middle" dominantBaseline="middle" fontWeight="bold">X</text>
                 )}
               </g>
             );
          })}
          
          {decision && decision.status === 'APPROVE' && whatIf?.before_after?.after && (
             <g>
               {(() => {
                 const tgt = posts.find((p:any) => p.id === whatIf.target_id);
                 const src = posts.find((p:any) => p.id === 'ID-002');
                 if (!tgt || !src) return null;
                 const x1 = getX(src.lng);
                 const y1 = getY(src.lat);
                 const x2 = getX(tgt.lng);
                 const y2 = getY(tgt.lat);
                 return (
                   <line x1={x1} y1={y1} x2={x2} y2={y2} stroke="#52b788" strokeWidth={4/zoom} strokeDasharray={`${8/zoom},${8/zoom}`} />
                 )
               })()}
             </g>
          )}

          {posts.map((p: any) => {
             const x = getX(p.lng);
             const y = getY(p.lat);
             return (
               <g key={p.id} className="cursor-pointer" onClick={(e) => { e.stopPropagation(); handleSelectPost(p); }}>
                 {renderShape(p)}
                 <text x={x} y={y + (24/zoom)} fill="#E9ECE7" fontSize={14/zoom} textAnchor="middle" style={{ pointerEvents: 'none', textShadow: '0 2px 4px rgba(0,0,0,0.8)' }}>
                   {p.id}
                 </text>
               </g>
             )
          })}
        </g>
      </svg>
      
      <div className="absolute bottom-4 right-4 bg-[#0b0f0c]/80 border border-[#2a362c] rounded p-2 text-[10px] backdrop-blur pointer-events-none">
        <div className="grid grid-cols-2 gap-2 text-gray-400">
           <div className="flex items-center gap-1"><div className="w-2 h-2 border border-current"></div> Rear Depot</div>
           <div className="flex items-center gap-1"><div className="w-2 h-2 border border-current rotate-45"></div> Hub</div>
           <div className="flex items-center gap-1"><div className="w-2 h-2 rounded-full border border-current"></div> Forward</div>
           <div className="flex items-center gap-1"><div className="w-4 h-0.5 bg-current"></div> Road</div>
           <div className="flex items-center gap-1"><div className="w-4 h-0.5 border-t border-dashed border-current"></div> Mule</div>
        </div>
      </div>
    </div>
  );
}

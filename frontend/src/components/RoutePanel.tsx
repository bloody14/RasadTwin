import React from 'react';

export default function RoutePanel({ routes, post }) {
  const postRoutes = routes.filter(r => r.target === post.id);

  return (
    <div className="bg-command-panel border border-olive-deep p-0">
      <div className="p-3 border-b border-olive-deep flex justify-between items-center">
        <h3 className="text-[10px] text-neutral-gray uppercase tracking-widest">ROUTE HEALTH</h3>
        <span className="text-[10px] text-neutral-white font-mono bg-command-black px-1 border border-olive-muted">{postRoutes.length} ROUTES</span>
      </div>
      <table className="w-full text-left border-collapse">
        <thead>
          <tr className="bg-command-dark text-[9px] text-neutral-gray uppercase font-mono border-b border-olive-deep">
            <th className="p-2 font-normal">ID</th>
            <th className="p-2 font-normal">MODE</th>
            <th className="p-2 font-normal">NOMINAL</th>
            <th className="p-2 font-normal text-accent-amber">ROBUST</th>
          </tr>
        </thead>
        <tbody className="text-xs font-mono text-neutral-white">
          {postRoutes.map((r, i) => (
            <tr key={r.id} className={i !== postRoutes.length - 1 ? 'border-b border-olive-muted/30' : ''}>
              <td className="p-2">{r.id}</td>
              <td className="p-2">{r.mode}</td>
              <td className="p-2 text-neutral-gray">{r.eta_hrs}h</td>
              <td className="p-2 text-accent-amber">{r.robust_eta_hrs}h <span className="text-[9px] text-accent-critical">+{Math.round((r.robust_eta_hrs - r.eta_hrs)*60)}m</span></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

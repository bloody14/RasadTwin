import React from 'react';
import { CloudSnow, Wind, EyeOff, ThermometerSnowflake } from 'lucide-react';

export default function WeatherPanel({ weather }: { weather: any }) {
  if (!weather) return null;
  return (
    <div className="bg-[#0b0f0c] border border-[#2a362c] rounded p-3 shrink-0">
      <div className="text-[10px] text-gray-500 font-bold uppercase tracking-widest mb-3 flex items-center gap-2 border-b border-[#2a362c] pb-2">
        <CloudSnow className="w-4 h-4" /> ENVIRONMENTAL STATE
      </div>
      <div className="grid grid-cols-2 gap-3 text-xs">
        <div>
          <div className="text-[9px] text-gray-600 uppercase">Temp</div>
          <div className="font-mono text-white flex items-center gap-1 mt-1"><ThermometerSnowflake className="w-3 h-3 text-[#6D9FB3]"/> {weather.temperature}</div>
        </div>
        <div>
          <div className="text-[9px] text-gray-600 uppercase">Snow</div>
          <div className="font-mono text-white mt-1">{weather.snow_condition}</div>
        </div>
        <div>
          <div className="text-[9px] text-gray-600 uppercase">Wind</div>
          <div className="font-mono text-white flex items-center gap-1 mt-1"><Wind className="w-3 h-3 text-gray-400"/> {weather.wind}</div>
        </div>
        <div>
          <div className="text-[9px] text-gray-600 uppercase">Visibility</div>
          <div className="font-mono text-white flex items-center gap-1 mt-1"><EyeOff className="w-3 h-3 text-gray-400"/> {weather.visibility}</div>
        </div>
      </div>
      <div className="mt-3 pt-2 border-t border-[#1c231e]">
        <div className="text-[9px] text-gray-600 uppercase">Terrain Risk</div>
        <div className="text-[10px] font-mono text-[#e63946] mt-1">{weather.terrain_risk}</div>
      </div>
    </div>
  );
}

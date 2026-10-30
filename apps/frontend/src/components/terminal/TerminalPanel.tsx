import { useEffect, useMemo, useRef, useState } from "react";
import type { ExecEvent } from "../../types";
export default function TerminalPanel({ events }: { events: ExecEvent[] }) {
  const [agentFilter, setAgentFilter] = useState("all");
  const [paused, setPaused] = useState(false);
  const [open, setOpen] = useState<string | null>(null);
  const box = useRef<HTMLDivElement>(null);
  const filtered = useMemo(()=>events.filter((e)=>agentFilter==="all"||e.agent_name===agentFilter),[events,agentFilter]);
  useEffect(()=>{ if(!paused && box.current) box.current.scrollTop = box.current.scrollHeight; },[filtered,paused]);
  return (<div className="border border-slate-700 rounded bg-black">
    <div className="flex flex-wrap gap-2 items-center px-3 py-2 border-b border-slate-800 text-xs">
      <span className="font-bold">EXECUTION LOG</span>
      <select className="bg-slate-900 border border-slate-700 rounded px-1" value={agentFilter} onChange={(e)=>setAgentFilter(e.target.value)}>
        <option value="all">all agents</option><option value="coordinator">coordinator</option><option value="news_agent">news</option><option value="financial_agent">financial</option><option value="sentiment_agent">sentiment</option>
      </select>
      <button className="border border-slate-700 rounded px-2" onClick={()=>setPaused(!paused)}>{paused?"Resume scroll":"Pause scroll"}</button>
      <span>{filtered.length} events</span>
    </div>
    <div ref={box} className="h-72 overflow-auto px-3 py-2 text-xs leading-5">
      {filtered.map((e)=>(
        <div key={e.event_id}>
          <button className="text-left w-full hover:bg-slate-900" onClick={()=>setOpen(open===e.event_id?null:e.event_id)}>
            <span className="text-slate-500">[{new Date(e.timestamp).toLocaleTimeString()}]</span> <span className="text-emerald-300">{e.event_type.toUpperCase()}</span> <span className="text-sky-300">{e.agent_name||""}</span>
          </button>
          {open===e.event_id && (<div className="bg-slate-950 border border-slate-800 rounded p-2 my-1"><button className="border border-slate-700 rounded px-2 mb-1" onClick={()=>navigator.clipboard.writeText(JSON.stringify(e,null,2))}>Copy event</button><pre className="whitespace-pre-wrap">{JSON.stringify(e,null,2)}</pre></div>)}
        </div>))}
      {filtered.length===0 && <div className="text-slate-500">No events yet. Submit a question to start an execution.</div>}
    </div>
  </div>);
}

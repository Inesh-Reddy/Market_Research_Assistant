import type { ExecEvent } from "../../types";
const AGENTS=["coordinator","news_agent","financial_agent","sentiment_agent"];
export default function AgentMonitor({ events }: { events: ExecEvent[] }) {
  function status(a:string){
    const rel=events.filter((e)=>e.agent_name===a);
    if (rel.some((e)=>e.event_type==="agent.completed"||(a==="coordinator"&&e.event_type==="execution.completed"))) return "completed";
    if (rel.some((e)=>e.event_type==="agent.failed")) return "failed";
    if (rel.length) return "running";
    return "pending";
  }
  const color=(s:string)=>s==="completed"?"text-emerald-400":s==="failed"?"text-red-400":s==="running"?"text-amber-300":"text-slate-500";
  return (<div className="grid grid-cols-2 lg:grid-cols-4 gap-2">
    {AGENTS.map((a)=>(<div key={a} className="border border-slate-700 rounded p-3 bg-slate-950">
      <div className="text-xs text-slate-400">{a}</div>
      <div className={`text-sm font-bold ${color(status(a))}`}>{status(a).toUpperCase()}</div>
      <div className="text-[11px] text-slate-500 mt-1">{events.filter((e)=>e.agent_name===a).length} events</div>
    </div>))}
  </div>);
}

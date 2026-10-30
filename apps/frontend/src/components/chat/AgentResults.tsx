import { useState } from "react";
import type { ConsolidatedResult } from "../../types";
export default function AgentResults({ result }: { result: ConsolidatedResult | null }) {
  const [open, setOpen] = useState(true);
  if (!result) return null;
  return (<div className="border border-slate-700 rounded bg-slate-950">
    <button className="w-full text-left px-3 py-2 text-xs font-bold" onClick={()=>setOpen(!open)}>FULL AGENT DATA {open?"▾":"▸"} — every finding, value and source returned</button>
    {open && <div className="px-3 pb-3 flex flex-col gap-3">
      {result.agent_results.map((r)=>(
        <div key={r.agent_name} className="border border-slate-800 rounded p-3 bg-black">
          <div className="flex flex-wrap gap-2 text-xs"><span className="font-bold">{r.agent_name}</span><span className={r.status==="completed"?"text-emerald-400":"text-amber-300"}>{r.status}</span>{r.sentiment && <span>sentiment: {r.sentiment}</span>}<span className="text-slate-500">confidence {r.confidence}</span></div>
          <p className="text-sm mt-1">{r.summary}</p>
          {r.error && <p className="text-xs text-amber-300 mt-1">Note: {r.error}</p>}
          {r.financials.length>0 && <table className="w-full text-xs mt-2 border border-slate-800"><thead><tr><th className="text-left px-2 py-1 bg-slate-900">Metric</th><th className="text-left px-2 py-1 bg-slate-900">Value</th><th className="text-left px-2 py-1 bg-slate-900">Source</th><th className="text-left px-2 py-1 bg-slate-900">Market date</th></tr></thead>
            <tbody>{r.financials.map((f,i)=><tr key={i}><td className="px-2 py-1 border-t border-slate-800">{f.label}</td><td className="px-2 py-1 border-t border-slate-800">{f.value} {f.currency}</td><td className="px-2 py-1 border-t border-slate-800">{f.source}</td><td className="px-2 py-1 border-t border-slate-800">{f.market_timestamp||"n/a"}</td></tr>)}</tbody></table>}
          {r.findings.length>0 && <ol className="list-decimal pl-5 mt-2 space-y-2 text-sm">{r.findings.map((f,i)=>(
            <li key={i}><span className="font-semibold">{f.title}</span><div className="text-slate-300">{f.detail}</div>
            {f.sources.map((s,j)=><div key={j} className="text-xs"><a className="text-sky-300 underline break-all" href={s.url} target="_blank" rel="noreferrer">{s.url}</a>{s.published_at?` · ${s.published_at}`:""}</div>)}
            </li>))}</ol>}
        </div>))}
      {result.contradictions.length>0 && <div className="text-xs text-amber-200">Contradictions: {result.contradictions.join(" · ")}</div>}
    </div>}
  </div>);
}

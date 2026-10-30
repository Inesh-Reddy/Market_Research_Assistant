import Markdown from "./Markdown";
export default function ChatPanel({ question, setQuestion, onSubmit, busy, answer }: { question:string; setQuestion:(v:string)=>void; onSubmit:()=>void; busy:boolean; answer:string }) {
  return (<div className="border border-slate-700 rounded p-3 bg-slate-950 flex flex-col gap-2">
    <div className="text-xs text-slate-400">CHAT</div>
    <textarea className="bg-black border border-slate-700 rounded p-2 text-sm h-20" value={question} onChange={(e)=>setQuestion(e.target.value)} placeholder="Analyze Apple stock using the latest available information." />
    <button className="bg-emerald-600 hover:bg-emerald-500 rounded px-3 py-2 text-sm font-bold disabled:opacity-50 self-start" disabled={busy||!question.trim()} onClick={onSubmit}>{busy?"Running...":"Run research"}</button>
    {answer && <div className="bg-black border border-slate-800 rounded p-4 max-h-[560px] overflow-auto"><Markdown text={answer} /></div>}
  </div>);
}

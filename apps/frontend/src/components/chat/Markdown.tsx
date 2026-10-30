import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
export default function Markdown({ text }: { text: string }) {
  return (<div className="text-sm leading-6">
    <ReactMarkdown remarkPlugins={[remarkGfm]} components={{
      h1: ({children}) => <h1 className="text-lg font-bold mt-1 mb-2">{children}</h1>,
      h2: ({children}) => <h2 className="text-[15px] font-bold mt-4 mb-1.5 text-emerald-300">{children}</h2>,
      p: ({children}) => <p className="my-1.5">{children}</p>,
      ul: ({children}) => <ul className="list-disc pl-5 my-1.5 space-y-1">{children}</ul>,
      ol: ({children}) => <ol className="list-decimal pl-5 my-1.5 space-y-1.5">{children}</ol>,
      a: ({href, children}) => <a className="text-sky-300 underline break-all" href={href} target="_blank" rel="noreferrer">{children}</a>,
      blockquote: ({children}) => <blockquote className="text-slate-400 text-xs my-1">{children}</blockquote>,
      table: ({children}) => <div className="overflow-x-auto my-2"><table className="w-full text-xs border border-slate-700">{children}</table></div>,
      th: ({children}) => <th className="border border-slate-700 bg-slate-900 px-2 py-1 text-left">{children}</th>,
      td: ({children}) => <td className="border border-slate-800 px-2 py-1">{children}</td>,
      hr: () => <hr className="border-slate-800 my-3" />,
      strong: ({children}) => <strong className="font-semibold text-slate-100">{children}</strong>,
    }}>{text}</ReactMarkdown>
  </div>);
}

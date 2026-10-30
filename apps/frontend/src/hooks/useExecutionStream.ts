import { useEffect, useRef, useState } from "react";
import type { ExecEvent } from "../types";
import { eventsUrl } from "../services/api";
export function useExecutionStream(executionId: string | null) {
  const [events, setEvents] = useState<ExecEvent[]>([]);
  const [connected, setConnected] = useState(false);
  const seen = useRef(new Set<string>());
  useEffect(() => {
    if (!executionId) return;
    setEvents([]); seen.current.clear();
    const es = new EventSource(eventsUrl(executionId));
    es.onopen = () => setConnected(true);
    es.onerror = () => setConnected(false);
    const handler = (msg: MessageEvent) => {
      try { const ev = JSON.parse(msg.data) as ExecEvent; if (seen.current.has(ev.event_id)) return; seen.current.add(ev.event_id); setEvents((p)=>[...p, ev]); } catch {}
    };
    const types = ["execution.started","coordinator.started","coordinator.task_created","agent.started","agent.completed","agent.failed","tool.started","tool.completed","tool.failed","model.request_started","model.request_completed","model.error","orchestration.parallel_execution_started","orchestration.parallel_execution_completed","result.validation_started","result.validation_completed","coordinator.synthesis_started","execution.completed"];
    types.forEach((t)=>es.addEventListener(t, handler));
    return () => { es.close(); setConnected(false); };
  }, [executionId]);
  return { events, connected };
}

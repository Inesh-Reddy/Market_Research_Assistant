import logging

log=logging.getLogger("events")
def log_event(e): log.info("%s %s %s", e.event_type, e.agent_name, e.execution_id)

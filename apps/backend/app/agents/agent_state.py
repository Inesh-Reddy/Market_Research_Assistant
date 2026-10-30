from enum import Enum


class AgentStatus(str, Enum):
    PENDING="pending"; RUNNING="running"; COMPLETED="completed"; FAILED="failed"; RETRYING="retrying"

from fastapi import APIRouter

from app.agents.agent_factory import list_agents
from app.agents.prompt_loader import list_prompts, load_prompt

router=APIRouter(tags=["agents"])
@router.get("/agents")
async def agents(): return {"agents": list_agents()}
@router.get("/prompts")
async def prompts(): return {"prompts": list_prompts()}
@router.get("/prompts/{agent_name}")
async def prompt_detail(agent_name: str):
    f=f"{agent_name}.md" if not agent_name.endswith(".md") else agent_name
    d=load_prompt(f)
    return {"name":agent_name,"version":d["version"],"content":d["content"]}

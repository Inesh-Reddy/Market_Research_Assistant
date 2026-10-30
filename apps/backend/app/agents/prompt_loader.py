from pathlib import Path

PROMPT_DIR = Path(__file__).parent / "prompts"
def load_prompt(agent_file: str) -> dict:
    p = PROMPT_DIR / agent_file
    text = p.read_text() if p.exists() else ""
    version = "v1"
    for line in text.splitlines():
        if line.strip().startswith("version:"):
            version = line.split(":",1)[1].strip()
    return {"agent_file": agent_file, "version": version, "content": text}
def list_prompts() -> list[dict]:
    out=[]
    for f in sorted(PROMPT_DIR.glob("*.md")):
        d=load_prompt(f.name); out.append({"name": f.stem, "file": f.name, "version": d["version"]})
    return out

from fastapi import APIRouter, Request

router=APIRouter(tags=["health"])
@router.get("/health")
async def health(request: Request):
    llm=request.app.state.llm_provider
    llm_health=await llm.health()
    return {"status":"ok","service":"financial-intelligence-backend","llm":llm_health,"database_url_scheme":request.app.state.settings.database_url.split(":")[0]}

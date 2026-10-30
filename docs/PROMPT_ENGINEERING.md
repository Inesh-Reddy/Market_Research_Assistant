# Prompt Engineering
All prompts live in `apps/backend/app/agents/prompts/*.md` (version v1 in front-matter), loaded by `prompt_loader.py`, inspectable via GET /api/v1/prompts. Rendered prompts are emitted in events only when LOG_PROMPTS=true.
## coordinator (v1)
Purpose: grounded synthesis. Instructions: never fabricate values/timestamps; cite sources; flag contradictions; no investment advice. Input: question + 3 AgentResults. Output: markdown with Overview/News/Financial/Sentiment/Risks/Sources.
## news_agent (v1)
Purpose: latest news via Tavily with timestamps+URLs. Output: summary + findings. Constraint: no invented dates/URLs.
## financial_agent (v1)
Purpose: quotes/history with currency/source/market+retrieval timestamps; distinguish live vs historical close. Output: FinancialValue[].
## sentiment_agent (v1)
Purpose: bullish/bearish narrative summary. Output: label + findings. Constraint: never a guaranteed prediction.
Example input: "Give me the latest analysis of Apple stock." Example output: structured AgentResult JSON validated by Pydantic.

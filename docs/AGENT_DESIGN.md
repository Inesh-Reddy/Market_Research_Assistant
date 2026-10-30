# Agent Design
| Agent | Why | Tools | Input | Output | Failure |
|---|---|---|---|---|---|
| Coordinator | Decompose, delegate, detect contradictions, synthesize | none (LLM synthesis only) | question | ConsolidatedResult | Template synthesis if LLM down |
| News | Fresh catalysts need web search | Tavily | ticker/company | findings+sources w/ dates | partial + explicit unavailable finding |
| Financial | Prices/fundamentals need structured APIs | Alpha Vantage, yfinance | ticker | FinancialValue[] w/ provenance | per-tool isolation, partial |
| Sentiment | Narrative ≠ price data | Tavily | ticker/company | sentiment label + findings | partial, label unknown |
Context boundary: each agent receives only query/ticker/company — never full conversation history. Web content is untrusted data.

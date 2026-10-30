TOOLS = {
  "news_agent": ["tavily_search"],
  "financial_agent": ["alpha_vantage_quote", "yfinance_history"],
  "sentiment_agent": ["tavily_search"],
  "coordinator": [],
}
def tools_for(agent: str) -> list[str]: return TOOLS.get(agent, [])

from app.agents import financial_agent, news_agent, sentiment_agent

RUNNERS = {"news_agent": news_agent.run_news_agent, "financial_agent": financial_agent.run_financial_agent, "sentiment_agent": sentiment_agent.run_sentiment_agent}
def get_runner(name: str): return RUNNERS[name]
def list_agents() -> list[dict]:
    return [
      {"name":"coordinator","role":"Orchestrates research and synthesis","tools":[],"status":"ready"},
      {"name":"news_agent","role":"Latest news via Tavily","tools":["tavily_search"],"status":"ready"},
      {"name":"financial_agent","role":"Quotes/history via Alpha Vantage + yfinance","tools":["alpha_vantage_quote","yfinance_history"],"status":"ready"},
      {"name":"sentiment_agent","role":"Sentiment via Tavily","tools":["tavily_search"],"status":"ready"},
    ]

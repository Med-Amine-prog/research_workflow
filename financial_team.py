from agno.agent import Agent
from agno.team import Team
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from agno.playground import Playground  # <-- Import Playground
from dotenv import load_dotenv

load_dotenv()


# Agent for fetching financial data
financial_agent = Agent(
    name="Financial_Data_Agent",
    role="Specialized in fetching and interpreting financial data and stock prices.",
    model=OpenAIChat(id="gpt-4o"),
    tools=[YFinanceTools(stock_price=True, company_info=True, analyst_recommendations=True)],
    instructions=["Use tables to display financial data clearly."],
    show_tool_calls=True,
    markdown=True,
)

# Agent for analyzing news
news_agent = Agent(
    name="News_Analysis_Agent",
    role="Expert in searching the web for the latest news and analyzing market sentiment.",
    model=OpenAIChat(id="gpt-4o"),
    tools=[DuckDuckGoTools()],
    instructions=["Provide a summary of the news and include sources."],
    show_tool_calls=True,
    markdown=True,
)

# The main agent team
financial_analyst_team = Team(
    name="Financial_Analyst_Team",
    members=[financial_agent, news_agent],
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        "Generate a comprehensive financial report.",
        "Combine financial data, company information, and recent news.",
        "Present the final report in a well-structured markdown format."
    ],
    show_tool_calls=True,
    markdown=True,
)

# --- This is the new part for serving the app ---

# 1. Create a Playground instance with your agents or teams
# The Playground can accept a list of both Agents and Teams
playground = Playground(agents=[financial_agent, news_agent])

# 2. Get the FastAPI application object from the playground
app = playground.get_app()

# 3. Serve the application when the script is run directly
if __name__ == "__main__":
    # The string "financial_app:app" tells the server to look for the 'app'
    # object inside the 'financial_app.py' file.
    # Make sure to replace "financial_app" with the actual name of your .py file.
    playground.serve("financial_team:app", reload=True)
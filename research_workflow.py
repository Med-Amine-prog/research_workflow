import os
import time
from typing import Iterator
from agno.agent import Agent
from agno.workflow import Workflow, RunResponse
from agno.playground import Playground 
from agno.models.openai import OpenAIChat
from agno.storage.sqlite import SqliteStorage
from agno.tools.duckduckgo import DuckDuckGoTools
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("ERROR: The OPENAI_API_KEY environment variable is not set.")

AGENT_STORAGE_DB = "tmp/equipe_recherche.db"

# --- STEP 1: Define your Workflow class as before ---
class ResearchWorkflow(Workflow):
    """
    A workflow for conducting research and writing a report.
    """
    # ... (Agent definitions are exactly the same as before)
    planner_agent = Agent(
        name="Planner Agent",
        model=OpenAIChat(id="gpt-4o"),
        instructions=[
            "Vous êtes un planificateur de recherche expert.",
            "Votre unique mission est de prendre un sujet de recherche complexe fourni par l'utilisateur.",
            "Décomposez ce sujet en une liste numérotée de 5 à 7 sous-questions ou thèmes de recherche clairs et exploitables.",
            "Ne répondez rien d'autre que la liste numérotée."
        ],
        storage=SqliteStorage(table_name="planner_agent", db_file=AGENT_STORAGE_DB),
    )

    research_agent = Agent(
        name="Research Agent",
        model=OpenAIChat(id="gpt-4o"),
        tools=[DuckDuckGoTools()],
        instructions=[
            "Vous êtes un assistant de recherche spécialisé.",
            "On vous donnera UNE SEULE question ou un sujet très précis.",
            "Utilisez votre outil de recherche pour trouver les informations les plus pertinentes.",
            "Fournissez un résumé concis (3-4 phrases) des résultats.",
            "TRÈS IMPORTANT : Citez toujours vos sources en utilisant le format markdown : [Nom de la source](URL)."
        ],
        storage=SqliteStorage(table_name="research_agent", db_file=AGENT_STORAGE_DB),
    )

    writer_agent = Agent(
        name="Writer Agent",
        model=OpenAIChat(id="gpt-4o"),
        instructions=[
            "Vous êtes un rédacteur de contenu professionnel.",
            "Vous recevrez un 'briefing de recherche' contenant des informations et des sources.",
            "Votre tâche est de transformer ce briefing en un paragraphe bien écrit, fluide et engageant pour un rapport.",
            "N'ajoutez aucune information qui n'est pas dans le briefing fourni.",
            "Rédigez directement le paragraphe final sans ajouter de commentaires comme 'Voici le paragraphe :'."
        ],
        storage=SqliteStorage(table_name="writer_agent", db_file=AGENT_STORAGE_DB),
    )
        
    def execute(self, topic: str) -> str:
        """
        Executes the research workflow.
        """
        print(f"--- Starting research workflow for: {topic} ---")

        # 1. Plan research questions
        print("Step 1: Planning research questions...")
        plan = self.planner_agent.run(topic)
        questions = [q.strip() for q in plan.content.split("\n") if q.strip()]
        print(f"Plan generated:\n{plan.content}")

        # 2. Perform research for each question
        print("\nStep 2: Researching information...")
        research_results = []
        for question in questions:
            print(f"  Researching: {question}")
            result = self.research_agent.run(question)
            research_results.append(result.content)
            time.sleep(1) # Pause to avoid rate limiting

        # 3. Write the final report
        print("\nStep 3: Writing the report...")
        research_briefing = "\n\n".join(research_results)
        final_report = self.writer_agent.run(research_briefing)
        print("--- Workflow finished ---")

        return final_report.content
    
    def run(self, topic: str) -> str: # Note: I've renamed `execute` back to `run`
        """
        Executes the research workflow.
        """
        # ... (all the logic inside the run method is the same)
        print(f"--- Starting research workflow for: {topic} ---")
        # 1. Plan
        plan = self.planner_agent.run(topic)
        questions = [q.strip() for q in plan.content.split("\n") if q.strip()]
        print(f"Plan generated:\n{plan.content}")
        # 2. Research
        research_results = []
        for question in questions:
            print(f"  Researching: {question}")
            result = self.research_agent.run(question)
            research_results.append(result.content)
            time.sleep(1)
        # 3. Write
        print("\nStep 3: Writing the report...")
        research_briefing = "\n\n".join(research_results)
        final_report = self.writer_agent.run(research_briefing)
        print("--- Workflow finished ---")

        # --- 2. THE FIX IS HERE ---
        # Wrap the final string in a RunResponse object
        yield RunResponse(content=final_report.content)


# --- STEP 2: Instantiate your Workflow ---
research_workflow = ResearchWorkflow()

# --- STEP 3: Instantiate the Playground and pass the workflow ---
playground = Playground(
    workflows=[research_workflow], # <-- Pass your workflow instance here
    name="Research Workflow App",
    description="A playground for running the research workflow.",
)
app = playground.get_app()

# --- STEP 4: Serve the Playground application ---
if __name__ == "__main__":
    print("="*80)
    print("Starting the Research Workflow Playground application.")
    print("Navigate to the Playground URL and connect to this server.")
    print("="*80)
    playground.serve(app="research_workflow:app", reload=True)

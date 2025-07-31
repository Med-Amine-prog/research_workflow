import os
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.playground import Playground
from agno.storage.sqlite import SqliteStorage
from agno.tools.duckduckgo import DuckDuckGoTools
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
if not os.getenv("OPENAI_API_KEY"):
    print("ERREUR : La variable d'environnement OPENAI_API_KEY n'est pas définie.")
    exit()

AGENT_STORAGE_DB = "tmp/equipe_recherche.db"

# --- Définition des Agents Spécialisés ---
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
    markdown=True,
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
    add_datetime_to_instructions=True,
    markdown=True,
)

writer_agent = Agent(
    name="Writer Agent",
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        "Vous êtes un rédacteur de contenu professionnel.",
        "Vous recevrez un 'briefing de recherche' contenant des informations et des sources.",
        "Votre tâche est de transformer ce briefing en un paragraphe bien écrit, fluide et engageant pour un rapport.",
        "N'ajoutez aucune information qui n'est pas dans le briefing fourni.",
        "Rédigez directement le paragraphe final sans ajouter de commentaires comme 'Voici le paragraphe :'.",
    ],
    storage=SqliteStorage(table_name="writer_agent", db_file=AGENT_STORAGE_DB),
    markdown=True,
)


# --- Configuration du Playground ---

playground = Playground(agents=[planner_agent, research_agent, writer_agent])
app = playground.get_app()


# --- Lancement de l'application ---

if __name__ == "__main__":
    print("="*80)
    print("Démarrage de l'application de l'équipe d'agents de recherche.")
    print("Assurez-vous d'avoir un fichier .env ou une variable d'environnement OPENAI_API_KEY.")
    print("Une fois démarré, accédez au Playground via l'URL fournie dans les logs.")
    print("="*80)
    
    playground.serve("equipe_recherche:app", reload=True)
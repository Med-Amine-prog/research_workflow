# Multi-Agent Research Workflow

This project implements a multi-agent system to automate the process of researching a topic and generating a comprehensive report. It leverages the `agno` framework to define and orchestrate a series of specialized AI agents, each with a distinct role in the research and writing process. The entire workflow is exposed through a user-friendly web interface created with `Playground`.

<!-- ## 🎬 Project Demo

*(It is highly recommended to record a short GIF or video of the application in action and place it here.)*

![Project Demo Placeholder](https://via.placeholder.com/800x450.png?text=Project+Demo+Video/GIF) -->

##  Features

*   **Autonomous Research**: Decomposes a high-level topic into specific research questions.
*   **Web-Enabled Agents**: Utilizes DuckDuckGo to perform real-time web searches for each question.
*   **Content Generation**: Summarizes research findings and synthesizes them into a well-structured report.
*   **Interactive UI**: Provides a simple web interface (`Playground`) to input topics and view results.
*   **Persistent Memory**: Uses SQLite to store agent interactions and maintain state.

##  How It Works

The project orchestrates three distinct AI agents in a sequential workflow:

1.  **Planner Agent**: Receives the main research topic from the user. Its sole responsibility is to break down the topic into a list of 5-7 actionable sub-questions.

2.  **Research Agent**: Takes one sub-question at a time from the Planner. It uses the DuckDuckGo search tool to find relevant information online and then writes a concise summary of its findings, citing its sources.

3.  **Writer Agent**: Receives the collected summaries from the Research Agent. Its task is to synthesize all the information into a single, cohesive, and well-written final report.

This entire process is wrapped in a `ResearchWorkflow` class, which is then served as an interactive web application using `Playground`.

<!-- ## ⚙️ Project Structure

*(A diagram illustrating the workflow is very effective here.)*

![Workflow Diagram Placeholder](https://via.placeholder.com/800x300.png?text=User+Input+->+Planner+->+Researcher+->+Writer+->+Final+Report)
-->



##  Getting Started

Follow these instructions to get the project up and running on your local machine.

### Prerequisites

*   Python 3.9+
*   An [OpenAI API key](https://platform.openai.com/api-keys)

### 1. Clone the Repository

```bash
git clone https://github.com/Mohamed-Amine-ELASLA/research_workflow.git
cd research_workflow
```

### 2. Install Dependencies

It's recommended to use a virtual environment to manage dependencies.

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```
# Install the required packages

```bash
pip install "agno[all]" openai python-dotenv
```

(Note: agno[all] is a general way to install it with extras, you might need to adjust based on the specific packages used like uvicorn, etc. if they are not included).

### 3. Set Up Environment Variables
You need to configure your OpenAI API key.
Create a file named .env in the root of the project directory.
Add your OpenAI API key to the file like this:

```code
OPENAI_API_KEY="your_openai_api_key_here"
```

### 4. Run the Application
Save the provided Python code into a file named research_workflow.py. Then, run the following command in your terminal:

```bash
python research_workflow.py
```

After running this command, you will see output in your terminal indicating that the server is running.



### 5. Access the Playground
Open your web browser(Chrome is the best) and navigate to the URL provided by Playground. You will need to connect to your local server, which is typically running at https://app.agno.com/playground?endpoint=localhost%3A7777/v1.

You will see the "Research Workflow App" interface. Enter a topic you want to research and click the "Run" button to start the workflow.



<!-- (A screenshot of your application's web interface would be perfect here.)
![alt text](https://via.placeholder.com/800x400.png?text=Playground+Web+Interface) -->

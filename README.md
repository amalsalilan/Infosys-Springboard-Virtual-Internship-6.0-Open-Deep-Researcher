# 📘 Mini Research Brief Generator

A modular Python project that generates concise research briefs using Google Gemini (LangChain + LangGraph).
It takes a research topic as input and outputs a structured JSON brief along with a Markdown preview.

## 🚀 Features

Generates short, actionable research briefs in JSON format.

Validates output against a Pydantic schema.

Saves results automatically to the samples/ folder.

Modular design for easy scaling (config, models, tools, agent, prompts, etc.).

CLI-based interaction.

## 📂 Project Structure

research_brief/

│── config.py         # Config & environment variables

│── models.py         # Pydantic schemas

│── tools.py          # Helper functions

│── agent.py          # Model & agent setup

│── prompts.py        # Prompt templates

│── main.py           # Entry point (CLI execution)

│── samples/          # Generated briefs (saved as JSON)

│── .env              # API key goes here

## 🔑 Setup & Installation

Clone the repository

git clone https://github.com/your-username/research-brief-generator.git

cd research-brief-generator/research_brief


### Create a virtual environment (optional but recommended)

python -m venv venv

source venv/bin/activate   # On Linux/Mac

venv\Scripts\activate      # On Windows


### Install dependencies

pip install -r requirements.txt


Set up your environment variables

Create a .env file inside the project directory:

GOOGLE_API_KEY=your_google_api_key_here

## ▶️ Usage

Run the generator from the terminal:

python main.py


Example interaction:

 Mini Research Brief Generator

Enter your research topic: Quantum Computing in Healthcare


### Output:

JSON object printed in the terminal.

Markdown preview printed for readability.

JSON file saved automatically in samples/quantum_computing_in_healthcare.json.

🛠 Tech Stack

Python 3.9+

LangChain + LangGraph

Google Generative AI (Gemini)

Pydantic

dotenv

## 📄 Example Output

JSON

{
  "title": "Quantum Computing in Healthcare",
  "date": "28 Aug 2025",
  "problem_statement": "Explores how quantum computing can enhance drug discovery and medical diagnostics.",
  "key_questions": [
    "How can quantum algorithms accelerate molecular simulations?",
    "What are the challenges in applying quantum systems to healthcare data?"
  ],
  "method_brief": [
    "Review existing quantum healthcare applications",
    "Survey quantum machine learning techniques",
    "Identify scalability and ethical concerns"
  ],
  "deliverables": [
    "Research brief",
    "Annotated references",
    "Potential use-case scenarios"
  ]
}


## 📌 Future Improvements

Add more research templates (extended briefs, literature survey outlines, etc.)

Support multiple LLM providers (e.g., OpenAI, Anthropic).

Web-based UI for non-technical users.

### 👨‍💻 Author

Developed by Indranil Mondal
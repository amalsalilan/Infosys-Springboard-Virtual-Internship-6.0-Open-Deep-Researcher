## Research Brief Agent
This project is a minimal Python script that generates short research briefs using LangChain + Google Generative AI (Gemini). It takes a research topic as input and produces a structured JSON output and a Markdown preview. Inputs, outputs, and previews are automatically saved in the samples/ folder.


## Features
- Accepts a research topic from the user.
- Generates a structured JSON output with:
  - `title`
  - `problem_statement` (≤2 sentences)
  - `key_questions` (1–3 items)
  - `method_brief` (2–4 items)
  - `deliverables` (2–3 items)
- Provides a Markdown preview of the brief.
- Automatically saves:
  - Input topics → samples/input/
  - JSON outputs → samples/output/
  - Markdown previews → samples/markdownPreview/
- Includes basic error handling for missing topics, missing API keys, or invalid JSON.
- Temperature set to 0 for deterministic output.


## Tech Stack
- Python 3.10+
- LangChain for LLM integration
- Google Generative AI (Gemini) as the LLM
- Pydantic for structured output validation
- dotenv for managing environment variables


## Setup Instructions
1) Clone the repository: bash git clone <your-repo-url> cd <repo-folder>

2) Create a .env file in the project root and add your actual api key over there.
cp .env.example .env

3) pip install -r requirements.txt


## Usage
Run the Python script using python mini_research_brief.py or python3 mini_research_brief.py

## Sample Input/Output

Stored in the samples/ folder

### Example:

### Input
Impact of ONDC on small retailers in India

### JSON Output
{
  "title": "Impact of ONDC on Small Retailers",
  "problem_statement": "This research examines how the Open Network for Digital Commerce affects small retailers in India, focusing on adoption challenges and business opportunities.",
  "key_questions": [
    "How does ONDC adoption vary across small retailers?",
    "What are the key challenges faced during integration?",
    "What business opportunities are unlocked by ONDC?"
  ],
  "method_brief": [
    "Survey small retailers across multiple regions.",
    "Analyze adoption patterns using quantitative metrics.",
    "Interview key stakeholders for qualitative insights."
  ],
  "deliverables": [
    "Structured report with analysis and insights.",
    "Recommendations for small retailers to leverage ONDC."
  ]
}

### Markdown Preview

Impact of ONDC on Small Retailers

Problem Statement
This research examines how the Open Network for Digital Commerce affects small retailers in India, focusing on adoption challenges and business opportunities.

Key Questions
- How does ONDC adoption vary across small retailers?
- What are the key challenges faced during integration?
- What business opportunities are unlocked by ONDC?

Methods
- Survey small retailers across multiple regions.
- Analyze adoption patterns using quantitative metrics.
- Interview key stakeholders for qualitative insights.

Deliverables
- Structured report with analysis and insights.
- Recommendations for small retailers to leverage ONDC.


## Notes
- Ensure you have a valid Google API key for Gemini and set it in your .env file.
- The .env file is not tracked by GitHub. Only .env.example is included for reference.

Mini Research Brief Agent:

This is a small AI-powered research assistant built using Google’s Gemini model and LangChain.

The agent takes any research topic you give it (like “Impact of AI on education”) and automatically creates a short, structured research brief.

#The brief includes:

Problem statement (max 2 sentences)

Key research questions (exactly 3)

Methods / approach (2–4 items)

Deliverables (2–3 items)

Both JSON output (for computers) and a Markdown preview (for humans) are generated.

#Features

Takes a topic from you (via input).

Uses Gemini to generate research information.

Ensures the output is always clean and structured (thanks to Pydantic validation).

Shows results in two formats:

JSON (machine-readable)

Markdown (easy-to-read summary)

Friendly error handling (missing topic, missing API key, etc).

#Project Structure#
mini-research-brief/
│── models.py          # Schema (defines the structure of the research brief)
│── prompts.py         # Prompt design for the AI
│── research_agent.py  # Main script (runs the agent)
│── .env               # Stores your Google API key (not shared)
│── samples/           # Example inputs and outputs
│── README.md          # This file

#Setup Instructions

Clone or download this project to your computer.

Install dependencies (you need Python 3.9+):

pip install -r requirements.txt


Create a .env file in the project folder and add your Google API key:

GOOGLE_API_KEY=your_api_key_here


Run the agent:

python research_agent.py


#Enter your research topic when asked (e.g., “Evolution of internet over 2000s”).

#Example

Input:

Enter your research topic: Evolution of internet over 2000s


Output (JSON):

{
  "title": "Evolution of the Internet Over the 2000s",
  "problem_statement": "To analyze the technological, social, and economic changes that shaped the internet during 2000–2010.",
  "key_questions": [
    "What were the major technological advancements?",
    "How did social media impact communication?",
    "What economic shifts did the internet drive?"
  ],
  "method_brief": [
    "Literature review of research papers",
    "Analysis of internet adoption data",
    "Case studies of key platforms"
  ],
  "deliverables": [
    "Research report",
    "Infographic timeline",
    "Presentation slides"
  ]
}


Output (Markdown Preview):

# Evolution of the Internet Over the 2000s

**Date:** 2025-08-26  

**Problem Statement:** To analyze the technological, social, and economic changes that shaped the internet during 2000–2010.

**Key Questions:**
- What were the major technological advancements?
- How did social media impact communication?
- What economic shifts did the internet drive?

**Method Brief:**
- Literature review of research papers
- Analysis of internet adoption data
- Case studies of key platforms

**Deliverables:**
- Research report
- Infographic timeline
- Presentation slides



#Notes

You need a valid Google Gemini API key to run this project.

The model sometimes tries to write more than required — we automatically trim extra items to fit the rules.
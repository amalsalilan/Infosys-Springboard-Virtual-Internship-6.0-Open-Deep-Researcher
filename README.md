# Research Brief Generator

A mini research agent tool that generates structured research briefs using **LangChain** and **Google Generative AI (Gemini)**.

## Project Structure

├── sample
│    ├── sample1.json
│    ├── sample2.json
│    └── sample3.json
├── mini_research_agent.py
├── config.py
├── models.py 
└── README.md

## Features
- Generates concise **research briefs** from a given topic.
- Validates structured output using **Pydantic**.
- Outputs in **JSON** and **Markdown** formats.
- Modular and scalable design.

## Installation

1. Clone the repository or copy the files into a project folder.
2. Create a virtual environment (recommended)
3. Install dependencies
4. Create a .env file in the root folder and add your API key

# Input

Enter your research topic: Research on AI-Driven Personalized Learning Platforms

# Output

********* JSON Output *********

{
  "date": "2025-08-28",
  "title": "Research on AI-Driven Personalized Learning Platforms",
  "problem_statement": "Current learning platforms often fail to cater to individual student needs, leading to inconsistent learning outcomes.  AI offers the potential to personalize learning experiences, but challenges remain in effective implementation and ethical considerations.",
  "key_questions": [
    "What are the most effective AI algorithms for personalized learning path generation?",
    "How can AI-driven platforms address diverse learning styles and needs?",
    "What are the ethical implications of using AI in education, particularly concerning data privacy and bias?",
    "What are the key factors influencing the adoption and effectiveness of AI-driven personalized learning platforms?",
    "How can the effectiveness of AI-driven personalized learning platforms be measured and evaluated?"
  ],
  "method_brief": [
    "Literature review of existing AI-driven personalized learning platforms and relevant research.",
    "Analysis of successful and unsuccessful case studies.",
    "Interviews with educators and students using such platforms.",
    "Evaluation of existing platforms using quantitative and qualitative metrics."
  ],
  "deliverables": [
    "Comprehensive literature review report.",
    "Analysis of case studies with recommendations.",
    "Report summarizing interview findings.",
    "Evaluation report with recommendations for improvement.",
    "Presentation summarizing key findings and recommendations."
  ]
}

********* Markdown Preview *********

# Research on AI-Driven Personalized Learning Platforms

* Date: 2025-08-28

* Problem Statement: Current learning platforms often fail to cater to individual student needs, leading to inconsistent learning outcomes.  AI offers the potential to personalize learning experiences, but challenges remain in effective implementation and ethical considerations.   

------------ Key Questions ------------
- What are the most effective AI algorithms for personalized learning path generation?        
- How can AI-driven platforms address diverse learning styles and needs?
- What are the ethical implications of using AI in education, particularly concerning data privacy and bias?
- What are the key factors influencing the adoption and effectiveness of AI-driven personalized learning platforms?
- How can the effectiveness of AI-driven personalized learning platforms be measured and evaluated?

------------ Method Brief ------------
- Literature review of existing AI-driven personalized learning platforms and relevant research.
- Analysis of successful and unsuccessful case studies.
- Interviews with educators and students using such platforms.
- Evaluation of existing platforms using quantitative and qualitative metrics.

------------ Deliverables ------------
- Comprehensive literature review report.
- Analysis of case studies with recommendations.
- Report summarizing interview findings.
- Evaluation report with recommendations for improvement.
- Presentation summarizing key findings and recommendations.
# Mini Research Brief Agent

A small Python tool that generates a structured research brief using **LangChain + Google Generative AI (Gemini)**.

---
## 📂 File Structure

```
Mini_Research_Brief/
│── mini_research_brief.py
│── README.md
│── samples/
│    ├── sample1.json
│    ├── sample2.json
│    └── sample3.json
```

## Setup

1. Clone the repo:
```bash
    git clone <repo-url>
    cd Mini_Research_Brief
```
2. Create a virtual environment and install dependencies:  
```bash
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
```
3. Set your Google API key:
```bash
    export GOOGLE_API_KEY="your_api_key_here"   # macOS/Linux
    set GOOGLE_API_KEY=your_api_key_here        # Windows (CMD)
```
## Run
```bash
    python mini_research_brief.py
```

Then enter a research topic (e.g., Impact of ONDC on small retailers in India).

Output

JSON (validated by Pydantic)

## **Sample Inputs & Outputs** (in `samples/`)

### `sample1.json`
**Input:** *Impact of ONDC on small retailers in India*
```json
{
  "input": "Impact of ONDC on Small Retailers in India",
  "output": {
    "title": "Impact of ONDC on Small Retailers in India",
    "problem_statement": "To assess the impact of the Open Network for Digital Commerce (ONDC) on the operational efficiency, profitability, and market reach of small retailers in India.",
    "key_questions": [
      "What is the level of ONDC adoption among small retailers in different regions of India?",
      "How has ONDC affected sales volume and revenue for small retailers?",
      "What are the perceived benefits and challenges of using ONDC for small retailers?",
      "How does ONDC compare to existing e-commerce platforms in terms of cost, reach, and ease of use for small retailers?",
      "What are the implications of ONDC for the long-term sustainability and growth of small retail businesses in India?"
    ],
    "method_brief": [
      "Conduct a mixed-methods study combining quantitative and qualitative data collection.",
      "Quantitative data will be collected through surveys of a representative sample of small retailers using ONDC and those who are not.",    
      "Qualitative data will be gathered through in-depth interviews with small retailers, ONDC platform operators, and relevant stakeholders.",    "Statistical analysis will be used to identify correlations between ONDC adoption and key business outcomes.",
      "Thematic analysis will be used to identify key themes and patterns in the qualitative data."
    ],
    "deliverables": [
      "A comprehensive research report summarizing the findings.",
      "A presentation of key findings and recommendations for policymakers and stakeholders.",
      "A dataset of quantitative and qualitative data collected during the study."
    ]
  }
}
```
### `sample2.json`
**Input:** *Post-Quantum Crypto Migration for Fintechs*
```json
{
  "input": "Post-Quantum Crypto Migration for Fintechs",
  "output": {
    "title": "Post-Quantum Crypto Migration for Fintechs",
    "problem_statement": "The advent of quantum computing threatens the security of widely used public-key cryptography algorithms currently employed by Fintechs.  A timely and effective migration strategy is crucial to maintain data integrity and customer trust.",
    "key_questions": [
      "What are the most critical cryptographic algorithms used by Fintechs vulnerable to quantum attacks?",
      "What are the available post-quantum cryptographic (PQC) alternatives and their respective strengths and weaknesses?",
      "What is the cost and complexity of migrating to PQC for different Fintech systems (e.g., payment processing, authentication)?",
      "What are the regulatory and compliance implications of PQC adoption for Fintechs?",
      "What are the potential risks and challenges associated with PQC implementation and integration?",
      "What is the optimal migration strategy (phased approach, complete overhaul) for minimizing disruption and maximizing security?"
    ],
    "method_brief": [
      "Literature review of existing PQC algorithms and migration strategies.",
      "Analysis of current cryptographic practices within the Fintech industry.",
      "Case studies of successful and unsuccessful PQC migrations in related sectors.",
      "Development of a cost-benefit analysis framework for PQC adoption.",
      "Risk assessment of different migration approaches.",
      "Interviews with Fintech security experts and stakeholders."
    ],
    "deliverables": [
      "A comprehensive report summarizing the findings of the research.",
      "A comparative analysis of different PQC algorithms suitable for Fintech applications.",
      "A proposed migration roadmap with timelines and cost estimations.",
      "A risk mitigation strategy for managing the transition to PQC.",
      "Recommendations for regulatory compliance and best practices."
    ]
  }
}

```
### `sample3.json`
**Input:** *AI-driven personalized learning platforms*
```json
{
  "input": "AI-driven personalized learning platforms",
  "output": {
    "title": "AI-Driven Personalized Learning Platforms: Effectiveness and Equity",
    "problem_statement": "Current learning platforms often fail to cater to individual student needs, leading to inconsistent learning outcomes and potential inequities. AI offers the potential to personalize learning, but its effectiveness and equitable implementation require further investigation.",
    "key_questions": [
      "How effective are AI-driven personalized learning platforms in improving student learning outcomes compared to traditional methods?",
      "What are the key design features of AI-driven platforms that contribute to or hinder effective learning?",
      "Do AI-driven platforms exacerbate or mitigate existing educational inequities based on factors such as socioeconomic status, learning disabilities, or access to technology?",
      "What are the ethical considerations and potential biases embedded within AI-driven personalized learning systems?",
      "How can the implementation of AI-driven platforms be optimized to ensure equitable access and benefit for all students?"
    ],
    "method_brief": [
      "Literature review of existing research on AI in education and personalized learning.",
      "Comparative analysis of different AI-driven learning platforms.",
      "Case studies of successful and unsuccessful implementations of AI-driven platforms.",
      "Qualitative data collection through interviews with students, teachers, and platform developers.",
      "Quantitative data analysis of student performance data from selected platforms."
    ],
    "deliverables": [
      "A comprehensive literature review report.",
      "A comparative analysis report of AI-driven learning platforms.",
      "A policy brief outlining recommendations for equitable and effective implementation of AI-driven personalized learning.",
      "A presentation summarizing key findings and recommendations."
    ]
  }
}

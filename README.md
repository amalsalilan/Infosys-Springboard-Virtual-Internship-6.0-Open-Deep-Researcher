# Mini Research Brief Agent

A small Python tool that generates a structured research brief using **LangChain + Google Generative AI (Gemini)**.

---
## File Structure

```
Mini_Research_Brief/
│── mini_research_brief.py
│── README.md
│── samples/
│    ├── sample1.json
│    ├── sample2.json
│    └── sample3.json
│── configurations.py
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
    "date": "2025-08-25",
    "title": "Impact of ONDC on Small Retailers in India",
    "problem_statement": "To assess the impact of the Open Network for Digital Commerce (ONDC) on the performance and growth of small retailers in India.  This includes evaluating both the benefits and challenges faced by these retailers in adopting and utilizing the ONDC platform.",
    "key_questions": [
      "What is the level of adoption of ONDC among small retailers in different regions of India?",
      "How has ONDC affected the sales and revenue of small retailers?",
      "What are the key challenges faced by small retailers in using the ONDC platform (e.g., technological barriers, logistical issues, competition)?",
      "What are the perceived benefits of ONDC for small retailers (e.g., increased reach, reduced transaction costs, access to new markets)?",
      "How does ONDC impact the pricing strategies and profitability of small retailers?",
      "What support mechanisms are needed to facilitate greater ONDC adoption and success among small retailers?",
      "What is the comparative impact of ONDC on small retailers versus larger businesses?"
    ],
    "method_brief": [
      "Conduct a literature review of existing research on ONDC and its impact.",
      "Collect primary data through surveys and interviews with small retailers across diverse geographical locations and business types.",
      "Analyze secondary data from ONDC platform usage statistics (if publicly available).",
      "Employ quantitative and qualitative data analysis techniques to identify trends and patterns.",
      "Develop case studies of successful and unsuccessful ONDC adoption by small retailers.",
      "Compare the findings with the impact of other e-commerce platforms on small retailers."
    ],
    "deliverables": [
      "A comprehensive research report summarizing the findings.",
      "Data visualizations illustrating key trends and patterns.",
      "Policy recommendations for improving ONDC's effectiveness for small retailers.",
      "A presentation summarizing the key findings and recommendations."
    ]
  }
}
```
### `sample2.json`
**Input:** *Impact of ONDC on small retailers in India*
```json
{
  "input": "Post-Quantum Crypto Migration for Fintechs",
  "output": {
    "date": "2025-08-25",
    "title": "Post-Quantum Crypto Migration for Fintechs",
    "problem_statement": "The advent of quantum computing poses a significant threat to the security of current public-key cryptography used extensively in the Fintech sector.  Existing cryptographic algorithms, such as RSA and ECC, are vulnerable to attacks from sufficiently powerful quantum computers.  This necessitates a timely and efficient migration to post-quantum cryptography (PQC) to maintain the confidentiality, integrity, and availability of financial systems.",
    "key_questions": [
      "What are the most suitable PQC algorithms for various Fintech applications (e.g., digital signatures, key exchange, encryption)?",
      "What are the performance implications of migrating to PQC algorithms in terms of latency, throughput, and resource consumption?",
      "What are the security considerations and potential vulnerabilities associated with PQC implementation in Fintech systems?",
      "What are the regulatory and compliance requirements for PQC adoption in different jurisdictions?",
      "What is the cost-benefit analysis of migrating to PQC, considering implementation costs, potential losses from security breaches, and long-term security?",
      "What are the best practices and strategies for a phased migration to PQC to minimize disruption and ensure a smooth transition?"
    ],
    "method_brief": [
      "Literature review of existing PQC algorithms and their suitability for Fintech applications.",
      "Comparative analysis of the performance characteristics of different PQC algorithms.",
      "Security analysis of PQC implementations, including vulnerability assessments.",
      "Case studies of PQC adoption in the Fintech industry.",
      "Development of a cost-benefit model for PQC migration.",
      "Survey of regulatory and compliance requirements for PQC.",
      "Interviews with Fintech experts and stakeholders."
    ],
    "deliverables": [
      "A comprehensive report summarizing the findings of the research.",
      "A comparative analysis of different PQC algorithms and their suitability for Fintech applications.",
      "A risk assessment of the migration process and recommendations for mitigation.",
      "A cost-benefit analysis of PQC migration for Fintechs.",
      "A set of best practices and guidelines for a successful PQC migration.",
      "A presentation summarizing the key findings and recommendations."
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
    "date": "2025-08-25",
    "title": "Research Brief: AI-Driven Personalized Learning Platforms",
    "problem_statement": "Current learning platforms often fail to cater to individual student needs, leading to inconsistent learning outcomes and decreased engagement.  AI offers the potential to personalize learning experiences, but challenges remain in areas such as data privacy, algorithm bias, and effective integration with existing educational systems.",
    "key_questions": [
      "What are the most effective AI algorithms for personalized learning in different subject areas and learning styles?",
      "How can AI-driven platforms address issues of equity and access in education?",
      "What are the ethical implications of using AI in personalized learning, particularly concerning data privacy and algorithmic bias?",
      "What are the optimal methods for integrating AI-driven personalization into existing educational curricula and teacher workflows?",
      "What are the key factors influencing student engagement and learning outcomes in AI-driven personalized learning environments?",
      "How can the effectiveness of AI-driven personalized learning platforms be reliably measured and evaluated?"
    ],
    "method_brief": [
      "Literature review of existing research on AI in education and personalized learning.",
      "Analysis of commercially available AI-driven learning platforms.",
      "Case studies of successful implementations of AI in educational settings.",
      "Interviews with educators and students to gather feedback on the effectiveness and challenges of AI-driven personalized learning.",
      "Statistical analysis of learning outcomes data from AI-driven platforms (where available)."
    ],
    "deliverables": [
      "A comprehensive literature review summarizing current research on AI-driven personalized learning.",
      "A comparative analysis of existing AI-driven learning platforms.",
      "A report outlining the ethical considerations and potential challenges of implementing AI in education.",
      "Recommendations for best practices in designing and implementing effective AI-driven personalized learning platforms.",
      "A presentation summarizing key findings and recommendations."
    ]
  }
}
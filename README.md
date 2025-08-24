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
    cd mini_research_brief
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
  "title": "Impact of ONDC on Small Retailers in India",
  "problem_statement": "Small retailers in India face challenges in digital adoption and market access. ONDC aims to democratize e-commerce, but its effectiveness for small retailers remains unclear.",
  "key_questions": [
    "How does ONDC influence digital adoption among small retailers?",
    "What economic opportunities and risks emerge?",
    "How does customer access change?"
  ],
  "method_brief": [
    "Literature review on ONDC and digital commerce",
    "Surveys and interviews with small retailers",
    "Data analysis of sales patterns before and after ONDC adoption"
  ],
  "deliverables": [
    "Brief report with key insights",
    "Presentation of findings",
    "Recommendations for small retailers"
  ]
}
```
### `sample2.json`
**Input:** *Impact of ONDC on small retailers in India*
```json
{
  "title": "Impact of ONDC on Small Retailers in India",
  "problem_statement": "Small retailers in India face challenges in digital adoption and market access. ONDC aims to democratize e-commerce, but its effectiveness for small retailers remains unclear.",
  "key_questions": [
    "How does ONDC influence digital adoption among small retailers?",
    "What economic opportunities and risks emerge?",
    "How does customer access change?"
  ],
  "method_brief": [
    "Literature review on ONDC and digital commerce",
    "Surveys and interviews with small retailers",
    "Data analysis of sales patterns before and after ONDC adoption"
  ],
  "deliverables": [
    "Brief report with key insights",
    "Presentation of findings",
    "Recommendations for small retailers"
  ]
}
```
### `sample3.json`
**Input:** *Impact of ONDC on small retailers in India*
```json
{
  "title": "Impact of ONDC on Small Retailers in India",
  "problem_statement": "Small retailers in India face challenges in digital adoption and market access. ONDC aims to democratize e-commerce, but its effectiveness for small retailers remains unclear.",
  "key_questions": [
    "How does ONDC influence digital adoption among small retailers?",
    "What economic opportunities and risks emerge?",
    "How does customer access change?"
  ],
  "method_brief": [
    "Literature review on ONDC and digital commerce",
    "Surveys and interviews with small retailers",
    "Data analysis of sales patterns before and after ONDC adoption"
  ],
  "deliverables": [
    "Brief report with key insights",
    "Presentation of findings",
    "Recommendations for small retailers"
  ]
}
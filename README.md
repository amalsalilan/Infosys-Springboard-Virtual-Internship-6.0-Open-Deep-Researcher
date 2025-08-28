# Deep Research Blog Agent

A minimal research brief agent in Python using LangChain and Google Gemini.  
Generates concise, validated research briefs in structured JSON for any topic.

---

## Project Structure

code/  
│  
├── deep_research.py # Main agent script  
├── .env # Your API key    
├── .gitignore  
├── sample/    
│ ├── sample1.json   
│ ├── sample2.json   
│ └── sample3.json    

---

## Setup Instructions

1. **Clone the repository**
```
git clone https://github.com/Jeevan200431/Deep_research_blog.git  
cd Deep_research_blog/code
```


3. **Install required Python libraries**
```
pip install langchain langchain-google-genai pydantic
```

5. **Add your Google Gemini API key**

- Create a file named `.env` in the `code/` directory:
  ```
  GOOGLE_API_KEY=your-gemini-api-key-here
  ```
- The `.env` file is ignored by git for security.

---
6. **usage**
```
   python deep_research.py
```
## Sample output

```
{
  "title": "Artificial Intelligence Overview",
  "date": "2025-08-28",
  "objective": "To explore the definition, applications, and challenges of AI.",
  "key_questions": [
    "What is Artificial Intelligence?",
    "What are its primary applications?",
    "What are ethical concerns related to AI?"
  ],
  "methodology": [
    "Literature review",
    "Industry case studies",
    "Expert interviews"
  ],
  "search_strategy": [
    "Use Google Scholar for academic papers",
    "Check IEEE, ACM, and Springer journals",
    "Explore recent AI reports from McKinsey and Stanford AI Index"
  ],
  "sources_to_start": [
    "Google Scholar",
    "IEEE Xplore",
    "ACM Digital Library"
  ],
  "risks_mitigations": [
    "Risk: Over-reliance on outdated sources → Mitigation: Use latest publications",
    "Risk: Biased case studies → Mitigation: Compare across industries"
  ],
  "deliverables": [
    "Structured research brief in JSON",
    "Markdown preview for blogs"
  ]
}
```




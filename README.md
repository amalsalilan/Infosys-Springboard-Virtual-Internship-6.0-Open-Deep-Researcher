Mini Research Brief Agent :

A light-weight research assistant that creates short, formatted research briefs from any subject you input. Driven by LangChain, Google Gemini, and Pydantic for formatted outputs.

Features :

✅ Accepts any research subject as input

✅ Outputs a formatted JSON output with title, problem statement, key questions, methods, and deliverables

✅ Validates output using Pydantic models

✅ Gives both JSON and Markdown previews

✅ Automatically inserts today's date

 Tech Stack :

Python 3.9+

LangChain (structured output + prompting)

Google Gemini API

Pydantic (strict schema validation)

 Project Structure  :
Mini Research Brief/
│── configure.py         # API key, prompt, parser setup
│── mini_research_brief.py # Main entry point
│── requirements.txt     # Python dependencies
│── .env                 # SAVES GOOGLE_API_KEY (hidden through .gitignore)
│── README.md            # Docs

⚙️ Setup & Installation

Clone this repository
git clone https://github.com/<your-username>/Mini-Research-Brief.git
cd Mini-Research-Brief

Create virtual environment

python -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows

Install dependencies

pip install -r requirements.txt


Set API key
Create a .env file in the root directory:

GOOGLE_API_KEY=your_api_key_here

▶️ Usage

Run the script:

python mini_research_brief.py


Enter your research topic when prompted:

Enter research topic: Increasing Women’s Participation in STEM


Output will be displayed in JSON and Markdown preview formats.

 Example Output :

JSON

{
  "title": "Increasing Women's Participation in STEM Fields",
  "problem_statement": "Despite progress, women remain underrepresented in STEM. This research explores ways to close the gender gap.",
  "key_questions": [
"What constraints confine women's engagement?"
"What policies work best across the world?"
],  
"method_brief": [  
    "Review of literature",
    "Analysis of the case study"
],  
"deliverables": [  
    "Summary of research",
    "Policy suggestion"
],  
"date": "2025-08-28"

Markdown Preview

Date: 2025-08-28  

# How to Get More Women Involved in STEM Disciplines

**Problem Statement:** Though there is advancement, women are still underrepresented in STEM. 

**Key Questions:** 
- What are the barriers to women's participation?
- What works worldwide in terms of policies? 

**Method Brief:** 
- Literature review 
- Case study analysis 

**Deliverables:** 
- Summary of research
- Policy recommendations 

 Why This Project?

Academic researchers, students, and professionals often spend hours framing a research problem before even starting. This tool helps by providing a quick, structured, and validated brief to jumpstart the research process.

 Contributing :

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

 License  :

This project is licensed under the MIT License.

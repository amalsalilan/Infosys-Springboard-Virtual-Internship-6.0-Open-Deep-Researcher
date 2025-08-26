# Deep Research Blog Agent

A minimal research brief agent in Python using LangChain and Google Gemini.  
Generates concise, validated research briefs in structured JSON for any topic.

---

## 📦 Project Structure

code/
│
├── deep_research.py # Main agent script  
├── .env # Your API key (local only)  
├── .gitignore # Ensures .env stays private  
├── sample/  
│ ├── sample1.json  
│ ├── sample2.json  
│ └── sample3.json   

---

## 🚀 Setup Instructions

1. **Clone the repository**
```
git clone https://github.com/Jeevan200431/Deep_research_blog.git  
cd Deep_research_blog/code
```


3. **Install required Python libraries**
pip install langchain langchain-google-genai pydantic

4. **Add your Google Gemini API key**

- Create a file named `.env` in the `code/` directory:
  ```
  GOOGLE_API_KEY=your-gemini-api-key-here
  ```
- The `.env` file is ignored by git for security.

---




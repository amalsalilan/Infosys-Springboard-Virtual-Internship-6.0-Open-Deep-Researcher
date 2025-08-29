# 🔎 Mini Research Brief Generator  

Generate concise research briefs using **LangChain + Google Generative AI (Gemini)** 🤖 with output validated by **Pydantic** ✅.  

The script reads a topic via `input()` and returns:  
- 📂 A **validated JSON** object matching the schema  
- 📝 A short **Markdown preview**  

---

## ⚙️ 1) Prerequisites  

- 🐍 Python 3.10+  
- 🔑 Google Gemini API key (Google AI Studio)  

### 🔐 Get a Google API Key  
1. Open [Google AI Studio](https://aistudio.google.com/)  
2. Click **Get API key** → **Create API key** (create/select a GCP project if prompted)  
3. Copy the key  

### 💻 Set the key as an environment variable  
**Linux / macOS:**  
```bash
export GOOGLE_API_KEY="your_api_key_here"


# Mini Research Brief Generator

Generate concise research briefs using **LangChain + Google Generative AI (Gemini)** with output validated by **Pydantic**.

The script reads a topic via `input()` and returns:
- A **validated JSON** object matching the schema
- A short **Markdown preview**

---

## 1) Prerequisites

- Python 3.10+
- Google Gemini API key (Google AI Studio)

### Get a Google API Key
1. Open https://aistudio.google.com/
2. Click **Get API key** → **Create API key** (create/select a GCP project if prompted)
3. Copy the key

### Set the key as an environment variable
**Linux / macOS:**
```bash
export GOOGLE_API_KEY="your_api_key_here"
```

**Windows (PowerShell):**
```powershell
setx GOOGLE_API_KEY "your_api_key_here"
```
Restart your terminal after setting it.

---

## 2) Install

From the repo root:
```bash
pip install -r requirements.txt
```

> If you prefer not to use `requirements.txt`:
> ```bash
> pip install langchain langchain-google-genai pydantic
> ```

---

## 3) Run

Interactive (will prompt for the topic):
```bash
python mini_research_brief.py
```

Example topics to try:
- `Impact of ONDC on small retailers in India`
- `Post-quantum crypto migration for fintechs`
- `AI in climate-smart agriculture`

---

## 4) Output

1) **JSON** (validated by Pydantic)
2) **Markdown** (quick human-readable preview)

If the model ever returns invalid structure, you’ll get a **friendly validation error** instead of malformed output.

---

## 5) Samples

See `samples/` for three example inputs and outputs (JSON and Markdown).

---

## 6) Put this on GitHub (step-by-step)

### Option A — Using Git (recommended)
1. Create an empty GitHub repo (e.g., `mini-research-brief`) from https://github.com/new
2. On your machine, place this project in a folder named `mini-research-brief`
3. In that folder, run:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: mini research brief generator"
   git branch -M main
   git remote add origin https://github.com/<your-username>/mini-research-brief.git
   git push -u origin main
   ```

### Option B — Using GitHub CLI
```bash
gh repo create mini-research-brief --public --source=. --remote=origin --push
```

### Option C — Upload via Web
- Zip the folder and upload it using the **"Add file → Upload files"** button on your new GitHub repo page.

---

## 7) Troubleshooting

- **`GOOGLE_API_KEY` not set**: Set it as described above and open a fresh terminal.
- **ImportError**: Reinstall dependencies with `pip install -r requirements.txt`.
- **Validation errors**: The script enforces the schema. Re-run; the model has `temperature=0` and `max_retries=2` to reduce drift.

---

## 8) Tech Notes

- Uses `PydanticOutputParser` to strictly enforce JSON schema.
- Model: `gemini-1.5-pro`, `temperature=0`, `max_retries=2`.
- Input strictly via `input()` to meet the requirement.


# Mini Research Brief Generator

This project generates a mini research brief for a given topic using AI-powered summarization. It fetches research content and provides structured summaries in JSON format.

## 🚀 Features
- Accepts a research topic as input.
- Uses LangChain + Google Gemini API for text generation.
- Outputs structured JSON containing:
  - Summary
  - Key Points
  - Applications
  - References
- Includes **sample inputs and outputs** in the `samples/` folder.

## 📂 Project Structure
```
├── mini_research_brief.py   # Main script
├── README.md                # Documentation
├── requirements.txt         # Dependencies
└── samples/                 # Folder with sample inputs & outputs
```

## ✅ Requirements
- Python 3.8 or above
- Google Gemini API Key
- LangChain & Google Generative AI SDK

Install dependencies:
```bash
pip install -r requirements.txt
```

## ▶️ Run in Google Colab
1. Open [Google Colab](https://colab.research.google.com/).
2. Upload `mini_research_brief.py` and `requirements.txt`.
3. Install dependencies:
   ```python
   !pip install -r requirements.txt
   ```
4. Set your **Google Gemini API key**:
   ```python
   import os
   os.environ["GOOGLE_API_KEY"] = "your_api_key_here"
   ```
5. Run the script:
   ```python
   !python mini_research_brief.py
   ```

## 🧪 Sample Inputs & Outputs
Samples are available in the `samples/` folder.

## 📜 License
This project is for educational purposes only.

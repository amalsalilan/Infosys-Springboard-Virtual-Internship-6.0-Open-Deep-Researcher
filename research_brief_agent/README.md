Research Brief Agent

A tiny CLI tool that asks for a research topic and returns a validated Research Brief using LangChain + Google Generative AI (Gemini).

Outputs are always returned as:

✅ Structured JSON (validated by Pydantic)

✅ Markdown Preview (human-readable)

Example briefs are included in the samples/ folder.



📦 Install
pip install -U langchain langchain-google-genai pydantic python-dotenv


⚙️ Setup

Create a .env file in the project root:

GOOGLE_API_KEY=gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash
GEMINI_FALLBACK_MODEL=gemini-1.5-flash-8b

▶️ Run
cd research_brief_agent
python mini_research_brief.py


📑 Example Output

JSON

{
  "title": "Environmental Crisis in India: Challenges and Interventions",
  "date": "2025-08-24",
  "objective": "India faces escalating challenges of air pollution, water scarcity, and climate-driven disasters. A focused research plan can guide policy and community interventions.",
  "key_questions": [
    "Which environmental issues are most critical for India in the next decade?",
    "How effective are government initiatives like Namami Gange and Ujjwala?",
    "What role can renewable energy adoption play in rural India?"
  ],
  "methodology": [
    "Review national and international environmental reports.",
    "Map current government interventions and assess implementation gaps.",
    "Compare state-level case studies with successful green initiatives."
  ],
  "search_strategy": [
    "Search UNEP and MoEFCC reports using keywords: 'air pollution India', 'climate adaptation'.",
    "Filter IPCC summaries for South Asia references.",
    "Scan research portals like JSTOR for Indian environmental policy studies."
  ],
  "sources_to_start": [
    "UNEP India reports",
    "Ministry of Environment, Forest and Climate Change (MoEFCC)",
    "IPCC AR6 Regional Chapters",
    "TERI (The Energy and Resources Institute)",
    "NITI Aayog policy briefs"
  ],
  "milestones_timeline": [
    {
      "name": "Initial Literature Review",
      "due_date": "2025-09-05",
      "description": "Collect and summarize 15–20 key documents"
    },
    {
      "name": "Case Study Comparison",
      "due_date": "2025-09-15",
      "description": "Analyze 3 successful state-level interventions"
    },
    {
      "name": "Draft Report",
      "due_date": "2025-09-20",
      "description": "Prepare initial draft for review"
    }
  ],
  "risks_mitigations": [
    {
      "risk": "Data gaps or outdated reports",
      "mitigation": "Cross-verify with multiple government and NGO sources"
    },
    {
      "risk": "Timeline delays due to report availability",
      "mitigation": "Use pre-collected open datasets as backups"
    }
  ],
  "deliverables": [
    "Research brief summarizing top 3–4 urgent issues",
    "Comparative dataset of interventions",
    "Policy recommendations for scaling renewable energy and grassroots solutions"
  ]
}




Markdown 

# Environmental Crisis in India: Challenges and Interventions
*Date (IST):* 2025-08-24

**Objective:** India faces escalating challenges of air pollution, water scarcity, and climate-driven disasters. A focused research plan can guide policy and community interventions.

## Key Questions
- Which environmental issues are most critical for India in the next decade?
- How effective are government initiatives like Namami Gange and Ujjwala?
- What role can renewable energy adoption play in rural India?

## Methodology
- Review national and international environmental reports.
- Map current government interventions and assess implementation gaps.
- Compare state-level case studies with successful green initiatives.

## Search Strategy
- Search UNEP and MoEFCC reports using keywords: 'air pollution India', 'climate adaptation'.
- Filter IPCC summaries for South Asia references.
- Scan research portals like JSTOR for Indian environmental policy studies.

## Sources to Start
- UNEP India reports  
- Ministry of Environment, Forest and Climate Change (MoEFCC)  
- IPCC AR6 Regional Chapters  
- TERI (The Energy and Resources Institute)  
- NITI Aayog policy briefs  

## Milestones & Timeline
- **Initial Literature Review** — 2025-09-05: Collect and summarize 15–20 key documents  
- **Case Study Comparison** — 2025-09-15: Analyze 3 successful state-level interventions  
- **Draft Report** — 2025-09-20: Prepare initial draft for review  

## Risks & Mitigations
- **Risk:** Data gaps or outdated reports  
  **Mitigation:** Cross-verify with multiple government and NGO sources  

- **Risk:** Timeline delays due to report availability  
  **Mitigation:** Use pre-collected open datasets as backups  

## Deliverables
- Research brief summarizing top 3–4 urgent issues  
- Comparative dataset of interventions  
- Policy recommendations for scaling renewable energy and grassroots solutions  


📂 Project Structure

research_brief_agent/
  mini_research_brief.py                # main script
  README.md                             # setup + usage guide
  .env                                  # API key + model config
  samples/                              # example inputs/outputs
    ai_tutors_rural_india.json
    ai_tutors_rural_india.md
    ondc_small_retailers_india.json
    ondc_small_retailers_india.md
    pqc_migration_fintechs.json
    pqc_migration_fintechs.md
    world_war_2.json
    world_war_2.md
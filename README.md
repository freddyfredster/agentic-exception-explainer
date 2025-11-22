# Agentic Exception Explainer

An AI-powered assistant that explains *why* business KPIs change — combining structured metrics with unstructured context (emails, notes, meeting summaries, operational updates, competitor activity, etc.).

This project demonstrates how to build an **agentic analytics system** outside Azure using Python, OpenAI function-calling, and a local vector store (Chroma).  
The agent automatically:

- Retrieves KPI data (sales, cancellations, etc.) from a structured dataset  
- Searches documents, emails, and notes for relevant explanations  
- Synthesises both into a clear, business-friendly root-cause summary  
- Cites the underlying evidence from your knowledge base  
- Produces insights in real time through a Streamlit chat interface  

The goal is to show how modern LLMs can act as a **“business exception investigator”** — saving managers and analysts hours normally spent digging through dashboards, inboxes, SharePoint folders, and meeting notes.

---

## 🚀 Built With

- **Python**
- **OpenAI GPT-4.1 / GPT-4.1-mini** (function calling)
- **ChromaDB** (local vector search)
- **Streamlit** (chat UI)
- **Pandas** (KPI querying)

---

## 🔍 Key Features

- 🧠 Agentic loop with automatic tool selection  
- 🔎 Local semantic search across notes & emails  
- 📊 KPI lookup with month-over-month comparison  
- 🪄 Root-cause explanations combining numbers + narrative evidence  
- 💾 Ready-to-run demo with dummy business data  
- 🧱 Clean project structure, ready for extensions (SQL, SharePoint, Graph API)

---

## 💼 Use Case

Perfect for showcasing modern agentic analytics on LinkedIn, in portfolio projects, or in client demos. Managers can ask questions like:

> “Why did Product B sales drop in the North in August?”  
> “What explains last month’s spike in cancellations?”  
> “What changed compared to July for the South region?”

The agent handles the full investigation — querying KPIs, finding relevant documents, and generating a concise, decision-focused explanation.

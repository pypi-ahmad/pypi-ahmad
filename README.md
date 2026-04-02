<!-- ======================= HEADER ======================= -->
<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0D1117,1a1a2e,16213e&height=280&section=header&text=Ahmad%20Mujtaba&fontSize=70&fontColor=00FFAA&animation=fadeIn&fontAlignY=38&desc=GenAI%20Engineer%20%7C%20Agentic%20AI&descSize=18&descAlignY=55&descAlign=50&descColor=AAAAAA" width="100%" />

  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=20&pause=1000&color=36BCF7&center=true&vCenter=true&width=500&lines=Document+Intelligence+%7C+RAG+%7C+LLM+Systems" />

  <br/><br/>

  <p>
    <a href="https://www.linkedin.com/in/ahmad-mle/">
      <img src="https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin"/>
    </a>
    <a href="https://pypi-ahmad.github.io/">
      <img src="https://img.shields.io/badge/Portfolio-Visit-FF5722?style=for-the-badge&logo=google-chrome"/>
    </a>
    <a href="https://t.me/dataintuitionist">
      <img src="https://img.shields.io/badge/Telegram-Message-2CA5E0?style=for-the-badge&logo=telegram"/>
    </a>
  </p>
</div>

<br/>

<!-- ======================= ABOUT ======================= -->
## About

GenAI Engineer at **Deloitte** (July 2025 — present), building document intelligence pipelines, agentic automation systems, and healthcare AI on Azure. Previously **Associate Data Scientist at Cognizant** (Sep 2022 — May 2025), working on warranty analytics, conversational AI, and data pipelines.

**M.Tech** in Data Analytics & Decision Sciences — IIIT Kurnool · **B.Tech** in Computer Science Engineering — MANUU

I treat LLM outputs as unverified signals. Every system I build wraps model calls in structured validation, evaluation loops, and deterministic guardrails.

<img src="https://capsule-render.vercel.app/api?type=rect&color=1a1a2e&height=2" width="100%"/>

<!-- ======================= NOTABLE SYSTEMS ======================= -->
## Notable Systems

### Intelligent Document Processing

OCR + LLM extraction pipeline for scanned insurance documents. Layout-aware parsing, schema-aligned structured outputs, and multi-stage validation against canonical documents.

**Stack:** Python, PaddleOCR, GPT-5.1, Gemini, Pydantic · **Result:** ~90% → ~99% extraction accuracy

---

### Computer-Using Agent

RAG-grounded agent for UI automation. Retrieves SOPs from Milvus, generates structured execution plans, and acts through an MCP-based tool layer with Playwright and AX Tree parsing.

**Stack:** Python, OpenAI CUA, Milvus, MCP, Playwright, AWS, Docker, FastAPI · **Result:** ~38% → ~80% task success rate · ~40% token reduction via AX Tree optimization

---

### Clinical Decision Support System

Privacy-first medical document processing. Local-first execution with Ollama as the default model path, structured extraction of clinical and insurance data, and hybrid rule + LLM reasoning with optional cloud model adapters when permitted.

**Stack:** Python, FastAPI, Streamlit, SQLite, Ollama, Pydantic

---

### Autonomous Research Agent

Multi-agent LangGraph system with parallel tool-based retrieval, a critic-driven evaluation loop, and quality-scored synthesis.

**Stack:** Python, LangGraph, LangChain, Gemini, FastAPI, Streamlit, FAISS

---

### Healthcare Document Intelligence *(current)*

Medical fax parsing on Azure. Layout-aware extraction from noisy scanned documents, integrated with downstream insurance workflows.

**Stack:** Azure Document Intelligence, Azure Databricks, Python

<img src="https://capsule-render.vercel.app/api?type=rect&color=1a1a2e&height=2" width="100%"/>

<!-- ======================= OPEN SOURCE ======================= -->
## Open Source

### [GenAI Systems Lab](https://github.com/pypi-ahmad/genai-systems-lab)

Shared execution platform for 20 AI systems — 10 generative AI pipelines, 5 LangGraph state machines, 5 CrewAI multi-agent teams — unified behind a single API, frontend, and runtime.

- **Backend:** Python 3.13, FastAPI, JWT auth, input validation, rate limiting, SSE streaming
- **LLM dispatch:** Gemini, OpenAI, Anthropic, Ollama — BYOK per request
- **Frontend:** Next.js 16, React 19, TypeScript, Tailwind CSS v4
- **Runtime:** per-run confidence scoring, session memory, benchmark evaluation (15 projects), explainability
- **Contract:** all 20 projects implement `run(input, api_key) → dict` and inherit the full platform stack

---

### [Portfolio](https://github.com/pypi-ahmad/pypi-ahmad.github.io)

React SPA presenting work history, 8 system case studies, and a 20-system platform catalog. 147 automated tests covering rendering, behavior, navigation, accessibility, and contrast compliance. 32 theme families with WCAG 4.5:1 contrast enforcement.

**Live:** [pypi-ahmad.github.io](https://pypi-ahmad.github.io) · **Stack:** React 18, Vite, styled-components, Framer Motion

<img src="https://capsule-render.vercel.app/api?type=rect&color=1a1a2e&height=2" width="100%"/>

<!-- ======================= STACK ======================= -->

<h2 align="center">Tech Stack</h2>

<table align="center" width="100%">
  <tr>
    <td align="center" width="20%"><b>GenAI / LLM</b></td>
    <td align="center" width="20%"><b>ML / CV</b></td>
    <td align="center" width="20%"><b>Cloud & DevOps</b></td>
    <td align="center" width="20%"><b>Data</b></td>
    <td align="center" width="20%"><b>Backend & Web</b></td>
  </tr>
  <tr>
    <td align="center" valign="top">
      <img src="https://skillicons.dev/icons?i=openai" height="40" style="margin:4px" /><br/>
      <img src="https://img.shields.io/badge/LangGraph-1C3C3C?style=flat-square" style="margin:4px" /><br/>
      <img src="https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square" style="margin:4px" /><br/>
      <img src="https://img.shields.io/badge/CrewAI-FF5A50?style=flat-square" style="margin:4px" /><br/>
      <img src="https://img.shields.io/badge/Gemini-8E75B2?style=flat-square" style="margin:4px" /><br/>
      <img src="https://img.shields.io/badge/Ollama-000000?style=flat-square" style="margin:4px" /><br/>
      <img src="https://img.shields.io/badge/MCP-000000?style=flat-square" style="margin:4px" />
    </td>
    <td align="center" valign="top">
      <img src="https://skillicons.dev/icons?i=pytorch,tensorflow" height="40" style="margin:4px" /><br/>
      <img src="https://skillicons.dev/icons?i=opencv,scikitlearn" height="40" style="margin:4px" /><br/>
      <img src="https://img.shields.io/badge/HuggingFace-FFD21E?style=flat-square" style="margin:4px" /><br/>
      <img src="https://img.shields.io/badge/PaddleOCR-000000?style=flat-square" style="margin:4px" />
    </td>
    <td align="center" valign="top">
      <img src="https://skillicons.dev/icons?i=azure,aws" height="40" style="margin:4px" /><br/>
      <img src="https://skillicons.dev/icons?i=docker,githubactions" height="40" style="margin:4px" /><br/>
      <img src="https://img.shields.io/badge/Linux-FCC624?style=flat-square" style="margin:4px" />
    </td>
    <td align="center" valign="top">
      <img src="https://skillicons.dev/icons?i=python" height="40" style="margin:4px" /><br/>
      <img src="https://img.shields.io/badge/Databricks-FF3621?style=flat-square" style="margin:4px" /><br/>
      <img src="https://img.shields.io/badge/PySpark-E25A1C?style=flat-square" style="margin:4px" /><br/>
      <img src="https://img.shields.io/badge/Milvus-00a1ea?style=flat-square" style="margin:4px" /><br/>
      <img src="https://img.shields.io/badge/FAISS-000000?style=flat-square" style="margin:4px" /><br/>
      <img src="https://img.shields.io/badge/DuckDB-FFF000?style=flat-square" style="margin:4px" /><br/>
      <img src="https://skillicons.dev/icons?i=postgres,mongodb,redis" height="40" style="margin:4px" />
    </td>
    <td align="center" valign="top">
      <img src="https://skillicons.dev/icons?i=fastapi,flask" height="40" style="margin:4px" /><br/>
      <img src="https://skillicons.dev/icons?i=react,nextjs,ts" height="40" style="margin:4px" /><br/>
      <img src="https://img.shields.io/badge/Pydantic-E92063?style=flat-square" style="margin:4px" /><br/>
      <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square" style="margin:4px" /><br/>
      <img src="https://img.shields.io/badge/Playwright-2EAD33?style=flat-square" style="margin:4px" /><br/>
      <img src="https://skillicons.dev/icons?i=git,vscode" height="40" style="margin:4px" />
    </td>
  </tr>
</table>

<img src="https://capsule-render.vercel.app/api?type=rect&color=1a1a2e&height=2" width="100%"/>

<!-- ======================= STATS ======================= -->
<h2 align="center">Activity</h2>

<div align="center">
  <img src="https://github-readme-stats-sigma-five.vercel.app/api?username=pypi-ahmad&show_icons=true&theme=radical&hide_border=true" height="170"/>
  <img src="https://streak-stats.demolab.com/?user=pypi-ahmad&theme=radical&hide_border=true&v=2" height="170"/>
</div>

<div align="center">
  <img src="https://github-profile-summary-cards.vercel.app/api/cards/profile-details?username=pypi-ahmad&theme=radical" />
</div>

<div align="center">
  <img src="https://raw.githubusercontent.com/pypi-ahmad/pypi-ahmad/output/github-contribution-grid-snake-dark.svg" width="100%" />
</div>

<img src="https://capsule-render.vercel.app/api?type=rect&color=1a1a2e&height=2" width="100%"/>
<!-- ======================= DEEP DIVES ======================= -->
## System Design Deep Dives

<details>
<summary><b>Intelligent Document Processing (IDP)</b></summary>

<br/>

**Problem:** Traditional OCR + regex pipelines are brittle and fail on real-world document variation. Template-based extraction does not generalize across layout differences.

**Architecture:**

```mermaid
flowchart LR
    A[Raw Documents] --> B[VLM Extraction]
    B --> C[Structured JSON]

    C --> D1[Semantic Matching]
    C --> D2[Rule Validation]
    C --> D3[AI Auditor]

    D1 --> E[Unified Entity Layer]
    D2 --> E
    D3 --> E

    E --> F[Final Decision Engine]

    style B fill:#1a1a2e,stroke:#00FFAA,color:#fff
    style D3 fill:#16213e,stroke:#36BCF7,color:#fff
    style F fill:#0f3460,stroke:#00FFAA,color:#fff
```

**Key components:**
- **VLM-based extraction** — single-pass structured extraction replacing the OCR → parsing → mapping chain, handling layout variance naturally
- **Semantic entity resolution** — fuzzy + vector matching for vendor names instead of brittle string matching
- **Hybrid validation** — deterministic rules (required fields, thresholds) combined with LLM-based reasoning (fraud signals, anomalies)
- **AI auditor** — detects suspicious patterns (vendor emails, inconsistent tax logic) beyond basic extraction

**Result:** ~99% structured extraction accuracy

</details>

<details>
<summary><b>Computer-Using Agent (CUA)</b></summary>

<br/>

**Problem:** Most UI automation relies on hardcoded selectors that break on UI changes and cannot reason about tasks.

**Architecture:**

```mermaid
graph TD;
    A[User Intent] --> B[RAG — Milvus];
    B --> C[Retrieve SOP Knowledge];
    C --> D[LLM Planner];
    D --> E[Step-by-Step Execution Plan];
    E --> F[CUA Agent];
    F --> G[UI Actions];
    G --> H[Observation];
    H --> F;
```

**Key components:**
- **MCP tool layer** — abstracts UI actions (click, type, navigate); LLM uses structured tools, not direct browser control
- **SOP injection via Milvus** — stores prior workflows and execution patterns, adding memory and consistency
- **AX Tree parsing** — reasons about UI structure instead of CSS selectors, ~40% token reduction over DOM-based approaches
- **Feedback loop** — action → observe → evaluate → retry for adaptive execution

**Result:** ~38% → ~80% task success rate

</details>

<details>
<summary><b>Clinical Decision Support System</b></summary>

<br/>

**Problem:** Healthcare systems rely on manual data entry from PDFs and faxes, with fragmented patient records and high error risk.

**Architecture:**

```mermaid
flowchart LR
    A[Medical Docs] --> B[Local VLM OCR]

    B --> C[Patient Data]
    C --> D[Patient History DB]

    D --> E1[Rule Engine]
    D --> E2[LLM Reasoning]

    E1 --> F[Decision Layer]
    E2 --> F

    F --> G[Alerts / Insights]

    style B fill:#1a1a2e,stroke:#00FFAA,color:#fff
    style E2 fill:#16213e,stroke:#36BCF7,color:#fff
    style G fill:#0f3460,stroke:#00FFAA,color:#fff
```

**Key components:**
- **Local-first execution** — Ollama is the default path for privacy-sensitive workflows
- **Hybrid inference** — optional cloud fallback is supported when permitted
- **Clinical + insurance logic** — validates prescriptions, eligibility, and risk signals

**Stack:** Python, FastAPI, Streamlit, SQLite, Ollama, Pydantic

</details>

<br/>

<!-- ======================= FOOTER ======================= -->
<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0D1117&height=100&section=footer"/>
</div>
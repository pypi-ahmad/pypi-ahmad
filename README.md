<div align="center">
  <h1>Ahmad Mujtaba</h1>
  <p><b>Applied AI / GenAI Engineer</b> — Document AI, RAG systems, agentic automation (Python, FastAPI, LangGraph)</p>

  <p>
    <a href="https://www.linkedin.com/in/ahmad-mle/">
      <img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" />
    </a>
    <a href="https://pypi-ahmad.github.io/">
      <img alt="Portfolio" src="https://img.shields.io/badge/Portfolio-Live-111827?style=for-the-badge&logo=vercel&logoColor=white" />
    </a>
    <a href="mailto:ahmad.iiitk@gmail.com">
      <img alt="Email" src="https://img.shields.io/badge/Email-ahmad.iiitk%40gmail.com-334155?style=for-the-badge&logo=gmail&logoColor=white" />
    </a>
    <a href="https://github.com/pypi-ahmad/pypi-ahmad/blob/main/resume.pdf">
      <img alt="Resume" src="https://img.shields.io/badge/Resume-PDF-1F2937?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" />
    </a>
  </p>

  <img
    src="https://capsule-render.vercel.app/api?type=waving&color=0D1117,0F172A,111827&height=220&section=header&text=Ahmad%20Mujtaba&fontSize=62&fontColor=E2E8F0&animation=fadeIn&fontAlignY=38&desc=Document%20Intelligence%20%C2%B7%20RAG%20%C2%B7%20Agentic%20Automation&descSize=16&descAlignY=58&descAlign=50&descColor=94A3B8"
    width="100%"
    alt="Header"
  />
</div>

<p align="center">
  <a href="#selected-outcomes">Outcomes</a> ·
  <a href="#featured-work">Featured</a> ·
  <a href="#stack">Stack</a> ·
  <a href="#activity">Activity</a>
</p>

## About

GenAI Engineer at **Deloitte** (Jul 2025–present), building production document intelligence pipelines, agentic automation, and healthcare AI on Azure. Previously **Associate Data Scientist at Cognizant** (Sep 2022–May 2025) across warranty analytics, conversational AI, and data pipelines.

I treat LLM outputs as **unverified signals**. Systems ship with structured validation, evaluation loops, and deterministic guardrails.

## Selected Outcomes

- Improved task completion from **38% → 80%** on a **200-task** internal evaluation by engineering a Milvus-backed RAG layer for multi-agent reasoning.
- Reduced browser-agent prompt-token consumption by **~40%** by replacing raw DOM dumps with accessibility-tree snapshots + compressed observations (Playwright MCP tooling).
- Improved structured extraction accuracy from **80–81% → 90%+** (multi-pass extraction with confidence-aware retries + routing).
- Raised policy-entity extraction accuracy from **90% → 99%** via model + validation iteration (prompting, canonical comparisons, and evaluation).

## Featured Work

These are the repos I recommend pinning (recruiter-first, “proof in the repo”).

| Project | What it is | Signal |
|---|---|---|
| [`medical-document-intelligence-assistant`](https://github.com/pypi-ahmad/medical-document-intelligence-assistant) | Local-first medical document understanding platform (OCR, extraction, retrieval, citations) | Verified end-to-end run, artifacts, large test suite |
| [`local-agentic-enterprise-platform`](https://github.com/pypi-ahmad/local-agentic-enterprise-platform) | Local AI business automation platform with approvals, reporting exports, and full web UI | Real e2e run + generated artifacts |
| [`legal-graphrag`](https://github.com/pypi-ahmad/legal-graphrag) | Legal GraphRAG stack with dense/sparse/graph/agentic/multimodal retrieval + eval | Metrics backed by artifact JSON outputs |
| [`computer-use`](https://github.com/pypi-ahmad/computer-use) | Provider-native computer-use workbench running inside an isolated Docker desktop sandbox | CI + docs + API surface |
| [`ai-ats-latex-resume-builder`](https://github.com/pypi-ahmad/ai-ats-latex-resume-builder) | AI resume builder: OCR/vision extraction + market snippets + LaTeX generation + PDF compile | Tests + end-to-end workflow doc |
| [`invoiceflow-ai`](https://github.com/pypi-ahmad/invoiceflow-ai) | Invoice processing pipeline with vision extraction, validation, semantic matching, and review UI | Clear module architecture + tests |

Other highlights:
- [`genai-systems-lab`](https://github.com/pypi-ahmad/genai-systems-lab) (collection of production-grade GenAI systems behind one repo contract)
- [`pypi-ahmad.github.io`](https://github.com/pypi-ahmad/pypi-ahmad.github.io) (portfolio site code + tests)
- [`Clinical-Decision-Support-System`](https://github.com/pypi-ahmad/Clinical-Decision-Support-System) (CDS-style document pipeline with strong security + LangGraph story)

## Stack

<div align="center">
  <img
    src="https://skillicons.dev/icons?i=python,fastapi,docker,postgres,sqlite,react,ts,azure,aws,githubactions"
    alt="Core stack icons"
  />
</div>

## Activity

<details>
<summary><b>GitHub stats (collapsible)</b></summary>
<br/>

<div align="center">
  <img src="https://github-readme-stats-sigma-five.vercel.app/api?username=pypi-ahmad&show_icons=true&theme=radical&hide_border=true" height="170" alt="GitHub stats"/>
  <img src="https://streak-stats.demolab.com/?user=pypi-ahmad&theme=radical&hide_border=true&v=2" height="170" alt="GitHub streak"/>
</div>

<div align="center">
  <img src="https://github-profile-summary-cards.vercel.app/api/cards/profile-details?username=pypi-ahmad&theme=radical" alt="Profile details"/>
</div>

<!-- Generated by .github/workflows/github-stats.yml using GH_STATS_TOKEN (required). -->
<div align="center">
  <img src="https://raw.githubusercontent.com/pypi-ahmad/pypi-ahmad/generated/overview.svg#gh-dark-mode-only" alt="Overview (dark)" />
  <img src="https://raw.githubusercontent.com/pypi-ahmad/pypi-ahmad/generated/overview.svg#gh-light-mode-only" alt="Overview (light)" />
</div>

<div align="center">
  <img src="https://raw.githubusercontent.com/pypi-ahmad/pypi-ahmad/generated/languages.svg#gh-dark-mode-only" alt="Languages (dark)" />
  <img src="https://raw.githubusercontent.com/pypi-ahmad/pypi-ahmad/generated/languages.svg#gh-light-mode-only" alt="Languages (light)" />
</div>

<div align="center">
  <img src="https://raw.githubusercontent.com/pypi-ahmad/pypi-ahmad/output/github-contribution-grid-snake-dark.svg" width="100%" alt="Contribution snake" />
</div>
</details>

## One Deep Dive (Optional)

<details>
<summary><b>How I build RAG systems that don’t lie by default</b></summary>
<br/>

I structure RAG as an engineering system: retrieval quality + grounded generation + evaluation + guardrails.

```mermaid
flowchart TD
  A[Documents] --> B[Chunk + Index]
  B --> C[Retrieve: dense + sparse + rerank]
  C --> D{Context sufficient?}
  D -->|No| E[Corrective fallback: expand query / graph / web]
  D -->|Yes| F[Generate answer]
  F --> G[Grounding + schema validation]
  G --> H{Pass?}
  H -->|No| I[Retry / route / human review]
  H -->|Yes| J[Ship response + citations + logs]
```

If you want concrete, reproducible examples, see:
- [`legal-graphrag`](https://github.com/pypi-ahmad/legal-graphrag)
- [`agentic-rag-arxiv-research-assistant`](https://github.com/pypi-ahmad/agentic-rag-arxiv-research-assistant)
</details>

<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0D1117&height=90&section=footer" alt="Footer" />
</div>


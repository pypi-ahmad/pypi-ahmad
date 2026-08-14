<div align="center">
  <h1>Ahmad Mujtaba</h1>
  <p><b>Applied AI Engineer building reliable Document AI, RAG, and agentic systems.</b></p>
  <p>Production experience in evaluation, structured extraction, healthcare AI, and Azure deployments.</p>

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
  </p>

</div>

<p align="center">
  <a href="#selected-outcomes">Outcomes</a> ·
  <a href="#featured-work">Featured</a> ·
  <a href="#currently-building">Building</a> ·
  <a href="#engineering-principles">Principles</a> ·
  <a href="#writing">Writing</a> ·
  <a href="#github-statistics">Statistics</a> ·
  <a href="#repository">Repository</a> ·
  <a href="#contact--availability">Contact</a>
</p>

## About

AI and Data Science Engineer at Deloitte, building document-intelligence, RAG, and agentic systems on Azure. I focus on evaluation, structured outputs, retrieval quality, and deterministic safeguards that make LLM applications measurable and dependable.

Previously, I worked on classical machine learning, conversational AI, warranty analytics, Azure, and production data pipelines at Cognizant.

## Selected Outcomes

These team and system results come from employer-internal evaluations. Client names, source data, task definitions, schemas, and proprietary code are omitted.

- **Browser task completion.** Task completion increased from **38% to 80%** across the same **200-task internal evaluation**. My contribution was Milvus retrieval, reranking, and failure-aware routing. [Sanitized case study](docs/sanitized-outcomes.md#browser-task-completion) · Related public implementations: [computer-use loop](https://github.com/pypi-ahmad/cua-workbench) and [corrective retrieval](https://github.com/pypi-ahmad/agentic-rag-arxiv-research-assistant).
- **Browser-agent prompt tokens.** Prompt-token consumption fell by **approximately 40%** in an internal evaluation. The baseline used raw DOM observations. My contribution was accessibility-tree snapshots and compressed observations. The evaluation size and trace details are confidential. [Sanitized case study](docs/sanitized-outcomes.md#browser-agent-prompt-tokens) · [Related public implementation](https://github.com/pypi-ahmad/cua-workbench).
- **Structured extraction.** Accuracy increased from **80–81% to above 90%** on the same internal benchmark. My contribution was multi-pass extraction, confidence-aware retries, and routing. The corpus size, schemas, and scoring details are confidential. [Sanitized case study](docs/sanitized-outcomes.md#structured-extraction) · [Related public implementation](https://github.com/pypi-ahmad/grounded-docparse).
- **Policy-entity extraction.** Accuracy increased from **90% to 99%** on the same internal benchmark. My contribution was prompt iteration, canonical comparison, and evaluation. The dataset size, policy documents, and entity schema are confidential. [Sanitized case study](docs/sanitized-outcomes.md#policy-entity-extraction) · [Related public implementation](https://github.com/pypi-ahmad/medical-document-intelligence-assistant).

## Featured Work

Selected systems demonstrating production-oriented AI engineering.

### Grounded Document Parser

**Problem.** Native documents, scanned files, and mixed PDFs require different ingestion paths. OCR-only processing discards native structure. Silent fallback makes provenance difficult to audit.

**Built.** I built an explicitly routed document-ingestion system. It parses native PDFs with `pdf-inspector` and Office, CSV, HTML, and EPUB files with Docling. It keeps local OCR for scans and images. Users review native/OCR routing page by page for mixed PDFs. Immutable text spans and source anchors connect extracted values to pages, paragraphs, slides, sheets, cells, and tables. Values without exact source evidence are rejected.

**Stack.** `Python · Streamlit · Pydantic · pdf-inspector · Docling · LangExtract · GLM-OCR · PaddleOCR-VL · vLLM`

**Evidence.** The system supports nine explicit processing types across native PDFs, mixed PDFs, Office documents, structured files, scans, and images. It blocks incompatible file and route selections. Grounded extraction accepts only exact character intervals that resolve to source anchors. The repository tests parsing, routing, extraction, recovery, persistence, CLI, and UI contracts across 39 test modules.

[Code](https://github.com/pypi-ahmad/grounded-docparse/tree/native-document-ingestion) · [Screenshot](https://github.com/pypi-ahmad/grounded-docparse/blob/native-document-ingestion/docs/images/document-parse-studio-full.png) · [Setup](https://github.com/pypi-ahmad/grounded-docparse/blob/native-document-ingestion/README.md#install-and-set-up) · [Architecture](https://github.com/pypi-ahmad/grounded-docparse/blob/native-document-ingestion/docs/architecture.md) · [Tests](https://github.com/pypi-ahmad/grounded-docparse/tree/native-document-ingestion/tests)

### LoRA Fine-tune Studio

**Problem.** Local adapter training requires separate hardware checks, dataset preparation, recipe configuration, checkpoint recovery, and evaluation steps.

**Built.** I built a guided Windows/Linux studio for local adapter training. It validates datasets before training. It checks CUDA and VRAM. It runs each job in an isolated worker with cancellation and checkpoint resume. It compares adapters with base models. It can publish adapters to the Hugging Face Hub.

**Stack.** `Python · Streamlit · PyTorch · Transformers · TRL · PEFT · Unsloth`

**Evidence.** The studio supports five training approaches: SFT, Reward, DPO, KTO, and ORPO. Each approach supports LoRA, QLoRA, OFT, and QOFT. The interface contains eight workflow pages. The repository contains eight test modules. CI runs formatting, linting, type checks, and tests.

[Code](https://github.com/pypi-ahmad/lora-qlora-fine-tuning-app) · [Screenshot](https://github.com/pypi-ahmad/lora-qlora-fine-tuning-app/blob/main/docs/images/training-studio.png) · [Setup](https://github.com/pypi-ahmad/lora-qlora-fine-tuning-app#install-from-github) · [Architecture](https://github.com/pypi-ahmad/lora-qlora-fine-tuning-app/blob/main/TECHNICAL.md) · [Tests](https://github.com/pypi-ahmad/lora-qlora-fine-tuning-app/tree/main/tests)

### Computer Use Workbench

**Problem.** Provider-native computer-use agents expose different tool contracts and execution loops. These differences complicate consistent operation and comparison.

**Built.** I built a local workbench with explicit OpenAI, Anthropic, and Google execution routes. It runs agents inside a sandboxed Ubuntu/XFCE desktop. It defines primary and fallback routes. It uses short-lived credentials. It retains audit frames.

**Stack.** `Python · FastAPI · React 19 · SQLite · Docker · OpenAI · Anthropic · Gemini`

**Evidence.** The workbench implements three direct provider routes. Credentials expire within eight hours. Audit retention stops after seven days or 1 GiB. CI runs backend and frontend tests, dependency audits, sandbox builds, and high/critical image scanning.

[Code](https://github.com/pypi-ahmad/computer-use) · [Screenshot](https://github.com/pypi-ahmad/computer-use/blob/main/assets/screenshot.png) · [Setup](https://github.com/pypi-ahmad/computer-use#quick-start) · [Architecture](https://github.com/pypi-ahmad/computer-use/blob/main/TECHNICAL.md) · [Tests](https://github.com/pypi-ahmad/computer-use/tree/main/tests)

### Local AI Chat Studio

**Problem.** Local and hosted models usually require separate clients. Separate clients complicate comparison, provenance tracking, and context control.

**Built.** I built a local-first workspace with streaming chat. It supports model comparison, replay, and response diffs. It prunes context to a defined token budget. It records provenance receipts. It quarantines prompt-injection attempts. It warns about secrets and PII. It provides local memory and RAG.

**Stack.** `Python · FastAPI · React 19 · SQLite · ChromaDB · Ollama`

**Evidence.** The workspace runs Ollama locally. It supports optional OpenAI, Anthropic, Gemini, OpenRouter, xAI, OpenCode, and compatible gateway routes. CI verifies provider and API contracts, workspace behavior, frontend tests, linting, and production builds.

[Code](https://github.com/pypi-ahmad/local-ai-chat-studio) · [Screenshot](https://github.com/pypi-ahmad/local-ai-chat-studio/blob/main/docs/screenshot-chat.png) · [Setup](https://github.com/pypi-ahmad/local-ai-chat-studio#install-and-run) · [Architecture](https://github.com/pypi-ahmad/local-ai-chat-studio/blob/main/TECHNICAL.md) · [Tests](https://github.com/pypi-ahmad/local-ai-chat-studio/tree/main/tests)

## Currently Building

**[LoRA Fine-tune Studio](https://github.com/pypi-ahmad/lora-qlora-fine-tuning-app)** — a local application for LoRA, QLoRA, OFT, and QOFT training workflows.

**Current question.** How can a local studio choose safe training defaults from GPU VRAM, dataset shape, and evaluation evidence while preserving reproducible runs?

## Engineering Principles

- **Evaluation first.** Define baselines, metrics, failure sets, and acceptance thresholds before changing a model or prompt.
- **Typed boundaries.** Validate LLM, tool, and API payloads before they change application state.
- **Observability.** Record traces, token use, retries, routing decisions, and failure reasons.
- **Security.** Scope credentials, validate inputs, isolate tool execution, and define retention limits.

## Writing

- **[Extraction Quality Research](https://github.com/pypi-ahmad/grounded-docparse/blob/native-document-ingestion/docs/extraction-quality-research.md).** An analysis of reference quality, regression metrics, OCR failure modes, and evidence limits.
- **[Computer Use: Zero-to-Hero Study Handbook](https://github.com/pypi-ahmad/computer-use/blob/main/docs/zero-to-hero-study-handbook.md).** A first-principles guide to computer-use agents, typed APIs, route fallback, and audited execution.
- **[Legal GraphRAG Architecture](https://github.com/pypi-ahmad/legal-graphrag/blob/main/docs/ARCHITECTURE.md).** An implementation note covering ingestion, hybrid retrieval, graph construction, and evaluation.

## Stack

- **AI and machine learning:** PyTorch, TensorFlow, scikit-learn, Hugging Face Transformers, TRL, PEFT, LangGraph, LangChain, and vLLM.
- **Models and agent interfaces:** OpenAI, Anthropic, Gemini, Ollama, structured outputs, and MCP.
- **Backend, retrieval, and data:** Python, FastAPI, Flask, Pydantic, Streamlit, Docling, PostgreSQL, SQLite, MongoDB, Redis, Milvus, ChromaDB, FAISS, Azure Databricks, and PySpark.
- **Frontend and delivery:** React, Next.js, TypeScript, Vite, Docker, Azure, AWS, GitHub Actions, and Linux.
- **Quality engineering:** pytest, Ruff, mypy/ty, Vitest, evaluation harnesses, tracing, and failure analysis.

<div align="center">
  <img
    src="https://skillicons.dev/icons?i=python,pytorch,tensorflow,sklearn,fastapi,flask,react,nextjs,ts,vite,docker,azure,aws,postgres,redis,githubactions&perline=8"
    alt="Technology stack icons"
  />
</div>

## GitHub Statistics

<div align="center">
  <img src="https://raw.githubusercontent.com/pypi-ahmad/pypi-ahmad/main/profile-stats/stats.svg" height="170" alt="Ahmad Mujtaba's GitHub statistics" />
  <img src="https://raw.githubusercontent.com/pypi-ahmad/pypi-ahmad/main/profile-stats/top-langs.svg" height="170" alt="Ahmad Mujtaba's top languages" />
  <br />
  <img src="https://github.com/pypi-ahmad/pypi-ahmad/raw/refs/heads/main/profile-stats/streak.svg" alt="Ahmad Mujtaba's GitHub contribution streak" />
</div>

<details>
<summary><b>Advanced GitHub dashboard</b></summary>
<br />

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/pypi-ahmad/pypi-ahmad/main/profile-stats/reach.dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/pypi-ahmad/pypi-ahmad/main/profile-stats/reach.light.svg" />
  <img src="https://raw.githubusercontent.com/pypi-ahmad/pypi-ahmad/main/profile-stats/reach.dark.svg" width="100%" alt="GitHub reach and collaboration statistics" />
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/pypi-ahmad/pypi-ahmad/main/profile-stats/coding.dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/pypi-ahmad/pypi-ahmad/main/profile-stats/coding.light.svg" />
  <img src="https://raw.githubusercontent.com/pypi-ahmad/pypi-ahmad/main/profile-stats/coding.dark.svg" width="100%" alt="GitHub code and activity statistics" />
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/pypi-ahmad/pypi-ahmad/main/profile-stats/distribution.dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/pypi-ahmad/pypi-ahmad/main/profile-stats/distribution.light.svg" />
  <img src="https://raw.githubusercontent.com/pypi-ahmad/pypi-ahmad/main/profile-stats/distribution.dark.svg" width="100%" alt="GitHub distribution and repository traffic statistics" />
</picture>
</details>

### Native GitHub Statistics

GitHub already shows:

- Contribution calendar and yearly contribution totals
- Activity feed and activity overview
- Followers and following counts
- Achievements and badges
- Up to six pinned repositories or gists

Source: [GitHub profile documentation](https://docs.github.com/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/about-your-profile).

### README Cards

[GitHub Readme Stats](https://github.com/anuraghazra/github-readme-stats) can show:

- Total stars earned, commits, pull requests, issues, contributed repositories, and rank
- Top languages by repository code size
- Individual repository descriptions, stars, forks, issues, and primary languages
- Gist statistics
- WakaTime coding-time statistics

Top languages measure repository bytes, not skill level. The original project is no longer maintained, so this profile generates its cards with the maintained [GitHub Readme Stats Action](https://github.com/stats-organization/github-readme-stats-action).

[GitHub Streak Stats](https://github.com/denvercoder1/github-readme-streak-stats) shows:

- Total contributions
- Current contribution streak
- Longest contribution streak
- Streak dates and contribution-calendar history

### Advanced GitHub Metrics

The generated dashboard shows:

- Lifetime stars, forks, watchers, pull-request reviews, merge rate, issue status, and external contributions
- Recently active repositories, recently used languages, lifetime lines changed, and 30-day coding habits
- Published releases, release-asset downloads, and 14-day repository traffic

Statistics cover public, owned, non-fork, non-archived repositories. GitHub traffic is available only for the latest 14 days. Release downloads count uploaded assets, not source archives.

## Activity

<details>
<summary><b>Contribution history</b></summary>
<br/>

<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/pypi-ahmad/pypi-ahmad/main/profile-3d-contrib/profile-night-rainbow.svg" />
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/pypi-ahmad/pypi-ahmad/main/profile-3d-contrib/profile-green.svg" />
    <img src="https://raw.githubusercontent.com/pypi-ahmad/pypi-ahmad/main/profile-3d-contrib/profile-night-rainbow.svg" width="100%" alt="3D contributions" />
  </picture>
</div>
</details>

## Repository

Source of record is [`main`](https://github.com/pypi-ahmad/pypi-ahmad). Latest snapshot: [2026-08-13](https://github.com/pypi-ahmad/pypi-ahmad/releases/tag/2026-08-13). Changelog: [CHANGELOG.md](CHANGELOG.md).

- Profile and outcomes: `README.md`, [`docs/sanitized-outcomes.md`](docs/sanitized-outcomes.md), [`DATASET.md`](DATASET.md)
- Governance: [`CONTRIBUTING.md`](CONTRIBUTING.md), [`SECURITY.md`](SECURITY.md), [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)
- Analysis artifacts: [`.codegraph/`](.codegraph/), [`.firecrawl/`](.firecrawl/), [`.ua/`](.ua/), [`graphify-out/`](graphify-out/) ([graph report](graphify-out/GRAPH_REPORT.md))

## Contact & Availability

Open to selective remote-first Applied AI and GenAI engineering roles. I focus on Document AI, RAG, evaluation, and computer-use systems.

Based in **Gurugram, India** — IST (UTC+05:30).

[Email](mailto:ahmad.iiitk@gmail.com) · [LinkedIn](https://www.linkedin.com/in/ahmad-mle/) · [Portfolio](https://pypi-ahmad.github.io/)

<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0D1117&height=90&section=footer" alt="Footer" />
</div>

<p align="center">Made with ❤️ by Ahmad Mujtaba</p>

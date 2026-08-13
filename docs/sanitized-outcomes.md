# Sanitized Outcome Case Studies

These case studies summarize confidential employer work. They separate measured team or system outcomes from my individual contribution. Client names, source data, task definitions, prompts, schemas, and proprietary code are omitted.

The linked repositories are independent public implementations of related engineering patterns. They do not reproduce or verify the internal measurements.

## Browser Task Completion

**Context.** A computer-use system executed browser tasks from internal operating procedures.

**Metric.** The evaluation measured task-completion rate across 200 internal tasks.

**Baseline.** The baseline system completed 38% of the task set.

**My contribution.** I implemented Milvus retrieval, reranking, and failure-aware routing.

**Result.** The updated system completed 80% of the same task set.

**Evaluation boundary.** The task taxonomy, operating procedures, completion criteria, source data, and system code are confidential. This result does not establish performance on unrelated browser tasks.

**Related public implementations.** [`cua-workbench`](https://github.com/pypi-ahmad/cua-workbench) demonstrates a tested computer-use loop with accessibility-driven execution. [`agentic-rag-arxiv-research-assistant`](https://github.com/pypi-ahmad/agentic-rag-arxiv-research-assistant) demonstrates retrieval, reranking, and corrective routing. Neither repository reproduces the internal evaluation.

## Browser-Agent Prompt Tokens

**Context.** A browser agent received page observations in its prompt context.

**Metric.** The evaluation compared prompt-token consumption between observation formats.

**Baseline.** The baseline supplied raw DOM observations.

**My contribution.** I replaced raw DOM dumps with accessibility-tree snapshots and compressed observations.

**Result.** Prompt-token consumption fell by approximately 40% in the internal evaluation.

**Evaluation boundary.** The number of traces, evaluated websites, prompts, and raw logs are confidential. The result measures prompt-token consumption only. It does not claim an equivalent improvement in latency, cost, or task completion.

**Related public implementation.** [`cua-workbench`](https://github.com/pypi-ahmad/cua-workbench) demonstrates accessibility-driven computer-use engines and test coverage. It does not reproduce the internal token measurement.

## Structured Extraction

**Context.** A document pipeline converted unstructured inputs into schema-constrained records.

**Metric.** The internal benchmark measured structured-extraction accuracy using its project-specific schemas and scoring rules.

**Baseline.** The baseline scored between 80% and 81% on the benchmark.

**My contribution.** I implemented multi-pass extraction, confidence-aware retries, and routing.

**Result.** The updated pipeline scored above 90% on the same benchmark.

**Evaluation boundary.** The corpus size, source documents, schemas, field weighting, and scoring implementation are confidential. The result does not establish accuracy on other document domains.

**Related public implementation.** [`grounded-docparse`](https://github.com/pypi-ahmad/grounded-docparse) publishes a synthetic and public regression corpus, baseline artifacts, confidence routing, and an evaluation script. It does not reproduce the internal benchmark.

## Policy-Entity Extraction

**Context.** A document pipeline extracted policy entities and compared them with canonical records.

**Metric.** The internal benchmark measured policy-entity extraction accuracy.

**Baseline.** The baseline scored 90% on the benchmark.

**My contribution.** I iterated prompts, implemented canonical comparisons, and expanded evaluation coverage.

**Result.** The updated pipeline scored 99% on the same benchmark.

**Evaluation boundary.** The dataset size, policy documents, entity schema, prompts, and scoring implementation are confidential. The result does not establish accuracy on unrelated policies or document types.

**Related public implementation.** [`medical-document-intelligence-assistant`](https://github.com/pypi-ahmad/medical-document-intelligence-assistant) demonstrates medical entity extraction, validation, tests, and end-to-end verification. It does not reproduce the internal policy benchmark.

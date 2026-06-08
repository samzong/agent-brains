# Dify RAG Research Memory - 2026-06-08

## Core Conclusion

Dify Dataset / Knowledge is a RAG lifecycle container. It manages the path from data source to document, processing rule, chunk, index, retrieval configuration, Workflow/App retrieval, query logging, hit count, and maintenance state.

KnowledgeFS should be used as the capability substrate for Dataset 2.0, but not copied as raw UI. Its strongest additions are KnowledgeSpace, connected sources, staged import/publish tasks, EvidenceBundle, AnswerTrace, GoldenQuestion, health checks, and retention/operations policies.

## Current Dify Capabilities

- Create internal datasets.
- Connect external knowledge.
- Create datasets from RAG Pipeline.
- Upload files, sync Notion, crawl websites.
- Configure automatic/custom/hierarchical processing rules.
- Use high-quality or economy indexing.
- Use normal, parent-child, or Q&A chunk structures.
- Configure semantic, full-text, hybrid, or keyword retrieval.
- Configure reranking, weighted score, top_k, and score threshold.
- Add custom and built-in metadata.
- Test retrieval through Hit Testing.
- Use Dataset in App config and Workflow Knowledge Retrieval node.

## Critical Runtime Rules

- Internal datasets need available completed enabled unarchived documents to be retrievable.
- External datasets can be available without Dify documents because retrieval is delegated.
- Mixed high-quality/economy datasets require rerank model.
- Weighted score requires high-quality internal datasets with consistent embedding model and provider.
- Query attachment retrieval is only meaningful for multimodal-capable datasets.
- Manual metadata filter conditions can resolve Workflow variables at runtime.

## Product Gaps

- Current Hit Testing shows records, not answerability.
- Current Dataset UI does not fully express evidence quality, missing evidence, conflicts, or trace.
- Current KnowledgeFS query API exposes `fast`, `deep`, and `research`, while its retrieval type also includes `auto`; Dify integration needs a product decision.
- Current Dify quick create supports only upload file, Notion import, and website crawl, despite broader backend/source concepts.
- App config and Workflow config both use Dataset, so Dataset 2.0 cannot be only a Knowledge page redesign.

## Product Direction

Dataset 2.0 should become a RAG workbench:

- Knowledge List
- Dataset Workbench
- Source Management
- Retrieval Settings
- Evidence Testing
- Quality Operations
- Workflow Connector
- Admin Operations

## PM Responsibility

The PM must define:

- Which Dataset type the user is creating.
- Which fields are required and why.
- Which retrieval combinations are invalid.
- How users understand and recover from ingestion/index failures.
- How Workflow users connect query variables, attachments, filters, and outputs.
- How evidence quality is shown and improved.
- Which KnowledgeFS details are productized, hidden, or admin-only.

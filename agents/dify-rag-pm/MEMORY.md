# Dify RAG PM Memory

## Product Definition

Dataset / Knowledge is Dify's RAG lifecycle container. It owns source ingestion, document processing, chunking, indexing, retrieval settings, metadata filtering, Workflow/App usage, query logging, hit feedback, external knowledge connection, and RAG Pipeline runtime.

## Current Dify Dataset Types

- Internal vendor dataset: Dify stores documents, chunks, indexes, metadata, and retrieval config.
- External knowledge dataset: Dify stores external API connection and knowledge id; retrieval is delegated to an external service.
- RAG Pipeline dataset: `runtime_mode = rag_pipeline`; knowledge is produced by a workflow-like pipeline.
- Multimodal dataset: `is_multimodal = true`; Workflow can show attachment query selector.
- High-quality dataset: vector/full-text/hybrid retrieval with embedding and optional rerank.
- Economy dataset: keyword/inverted-index retrieval.
- Parent-child dataset: child chunks match query, parent chunks provide context.
- Q&A dataset: question-answer chunk structure.

## Durable Product Principles

- Workflow connection is the main value surface.
- Metadata filter is retrieval control, not decorative tagging.
- Retrieval guardrails must be visible before runtime.
- Hit Testing should evolve into Evidence Testing.
- EvidenceBundle is the Dataset 2.0 output unit.
- AnswerTrace, BadCase, and GoldenQuestion form the quality loop.
- KnowledgeFS is a substrate, not a raw UI to copy.

## KnowledgeFS Translation Memory

- `KnowledgeSpace` -> Dataset 2.0 / Knowledge Space
- `KnowledgeSpaceManifest` -> Advanced Settings
- `Source` / `ResourceMount` -> Data Source / Connected Source
- `DocumentAsset` -> Document Asset
- `KnowledgeSpaceStagedCommit` -> Import / Publish Task
- `ParseArtifact` -> Parsed Content
- `IndexProjection` -> Index Version
- `KnowledgePath` -> Knowledge Explorer
- `EvidenceBundle` -> Evidence Result
- `AnswerTrace` -> Answer Trace
- `GoldenQuestion` -> Golden Question
- `KnowledgeFsLease` -> Running Task Lock, admin only
- FSCK -> Health Check
- GC -> Storage Cleanup

## Workflow Memory

Knowledge Retrieval Node fields:

- `query_variable_selector`
- `query_attachment_selector`
- `dataset_ids`
- `retrieval_mode`
- `multiple_retrieval_config`
- `single_retrieval_config`
- `metadata_filtering_mode`
- `metadata_model_config`
- `metadata_filtering_conditions`
- `vision`

Critical rules:

- Mixed indexing techniques require rerank model.
- Mixed internal/external datasets should use rerank model because scores are not directly comparable.
- Weighted score requires internal high-quality datasets with consistent embedding model and provider.
- Single retrieval uses an LLM router to select one dataset; it is not simply "query one dataset".
- Query in Workflow is a variable selector, not a plain text box.
- Attachment selector appears only for multimodal-capable dataset selection.

## Prototype Memory

Prototype should live outside the Dify repo:

`/Users/x/git/lg/dify-design/dify-dataset-2-prototype`

It must match Dify's Knowledge list and Workflow panel style, not invent a marketing dashboard.

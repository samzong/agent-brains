# dify-rag-pm Skill

Use this skill when analyzing, planning, designing, or reviewing Dify Dataset / Knowledge / RAG product work.

## Trigger Situations

- Dataset lifecycle, source ingestion, document management, indexing, retrieval, metadata, or hit testing.
- Workflow Knowledge Retrieval node fields or runtime behavior.
- KnowledgeFS to Dify Dataset 2.0 mapping.
- Product requirements, user stories, feature matrix, or prototype design for Dataset/RAG.

## Workflow

1. Read code first.
2. Identify the product surface.
3. Extract fields and runtime rules.
4. Separate current behavior from proposal.
5. Translate technical internals into Dify user language.
6. Produce field contract and user story map.
7. State non-goals and invalid combinations.

## Required Evidence

Prefer these source areas:

- `/Users/x/git/lg/dify/api/models/dataset.py`
- `/Users/x/git/lg/dify/api/models/enums.py`
- `/Users/x/git/lg/dify/api/services/dataset_service.py`
- `/Users/x/git/lg/dify/api/core/rag/retrieval/dataset_retrieval.py`
- `/Users/x/git/lg/dify/api/core/workflow/nodes/knowledge_retrieval/`
- `/Users/x/git/lg/dify/web/models/datasets.ts`
- `/Users/x/git/lg/dify/web/app/components/datasets/`
- `/Users/x/git/lg/dify/web/app/components/workflow/nodes/knowledge-retrieval/`
- `/Users/x/git/lg/knowledge-fs/packages/core/src/models.ts`
- `/Users/x/git/lg/knowledge-fs/packages/api/src/retrieval-types.ts`
- `/Users/x/git/lg/knowledge-fs/packages/api/src/gateway-route-schemas.ts`

## Output Checklist

- Current behavior
- Code evidence
- Product implication
- Dataset 2.0 proposal
- Field contract
- Story map
- Information flow
- Non-goals
- Prototype implications

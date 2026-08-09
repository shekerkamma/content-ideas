# RAG vs Enterprise Knowledge Graph + MCP — Decision Table

## When to use RAG
- Source material is **unstructured** (PDFs, emails, call transcripts, support tickets, policy documents)
- Queries are **semantic / natural language** ("what does our refund policy say about...")
- No need for exact metadata: column names, schema, lineage, data types
- Setup in days (just chunk, embed, store)
- Cost: ~$200–500/mo on any hyperscaler

## When to use Knowledge Graph + MCP
- Source material is **structured metadata** (database schemas, table lineage, column descriptions, data catalogs)
- Agents need to call tools that return **deterministic, structured** answers
- Queries are **factual metadata queries** ("what columns does this table have?", "who owns this dataset?", "is this field PII?")
- Enterprise has a data catalog already (GCP Knowledge Catalog, AWS Glue, Azure Purview)
- Accuracy requirement >90% (agent grounding on structured metadata: 93–97% vs ~60% for RAG)

## Decision criteria (8 dimensions)

| Dimension | RAG | Knowledge Graph + MCP |
|---|---|---|
| Source type | Unstructured docs | Structured metadata / graph |
| Query type | Semantic search | Tool calls → structured results |
| Agent accuracy | ~60–75% on catalog queries | 93–97% |
| Setup time | 2–5 days | 1–4 weeks (bootstrapping) |
| Staleness | Chunk re-embedding on update | Auto-harvested (GCP Dataplex) |
| Cost | ~$200–500/mo | GCP ~$200–500/mo; AWS ~$500–1500/mo |
| Hyperscaler lead | All equal | GCP (native MCP server) |
| Integration pattern | Embed → retrieve → prompt | MCP toolset → structured response |

## GCP native pattern (recommended when on GCP)

```python
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseServerParams

knowledge_context = MCPToolset(
    connection_params=SseServerParams(
        url="https://dataplex.googleapis.com/mcp",
    )
)
```
The GCP Knowledge Catalog MCP server auto-harvests BigQuery, AlloyDB, Spanner, and Looker metadata. No custom integration needed.

## AWS pattern (custom Lambda required)

```python
def search_glue_catalog(query: str, database: str = None) -> list[dict]:
    glue = boto3.client("glue")
    results = glue.search_tables(SearchText=query, Filters=[...])
    return [{"table": t["Name"], "database": t["DatabaseName"],
             "description": t.get("Parameters", {}).get("comment", "")}
            for t in results.get("TableList", [])]
```
Register as a Bedrock Agents tool or LangChain tool. No native MCP.

## Azure pattern (preview, REST only)

```
POST https://{{account}}.purview.azure.com/catalog/api/search/query
{"keywords": "...", "filter": {"entityType": "column"}}
```
Azure Purview MCP integration is preview as of 2025. Use REST wrapper.

## Common mistake
Applying RAG to an enterprise data catalog use case where agents need to know schema structure. RAG retrieves document chunks — it cannot tell an agent what the primary key of a table is, whether a column contains PII, or who the data owner is. Knowledge Graph + MCP answers all three with a single tool call.

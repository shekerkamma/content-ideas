---
marp: true
theme: default
paginate: true
style: |
  :root {
    --bg:      #080b11;
    --bg-elev: #0f141d;
    --ink:     #eef2f7;
    --soft:    #aeb8c7;
    --muted:   #69748a;
    --teal:    #2dd4bf;
    --sky:     #38bdf8;
    --magenta: #e879f9;
    --amber:   #f6b94b;
    --line:    rgba(255,255,255,0.09);
    --glass:   rgba(255,255,255,0.04);
  }

  section {
    background: var(--bg);
    color: var(--ink);
    font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
    padding: 60px 80px 80px;
    border-bottom: 4px solid transparent;
    border-image: linear-gradient(90deg, #2dd4bf, #38bdf8, #e879f9) 1;
    font-size: 22px;
  }

  section::after {
    color: var(--muted);
    font-family: ui-monospace, "SF Mono", Menlo, monospace;
    font-size: 12px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
  }

  h1 {
    font-size: 3.2rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    line-height: 1.05;
    background: linear-gradient(135deg, #2dd4bf 0%, #38bdf8 50%, #e879f9 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.4em;
  }

  h2 {
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: var(--ink);
    margin-bottom: 0.5em;
  }

  h3 {
    font-family: ui-monospace, "SF Mono", Menlo, monospace;
    font-size: 0.72rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--teal);
    font-weight: 400;
    margin-bottom: 0.3em;
  }

  p {
    color: var(--ink);
    line-height: 1.6;
    max-width: 64ch;
  }

  ul {
    padding-left: 0;
    list-style: none;
  }

  ul li {
    padding-left: 1.4em;
    position: relative;
    color: var(--ink);
    line-height: 1.6;
    margin-bottom: 0.35em;
  }

  ul li::before {
    content: '→';
    position: absolute;
    left: 0;
    color: var(--teal);
    font-family: ui-monospace, monospace;
  }

  ul li.neg::before { content: '✕'; color: #e879f9; }
  ul li.pos::before { content: '✓'; color: #2dd4bf; }

  blockquote {
    border-left: 4px solid var(--teal);
    box-shadow: -4px 0 12px rgba(45,212,191,0.4);
    padding: 1em 2em;
    margin: 0;
    font-size: 1.5rem;
    font-style: italic;
    color: var(--soft);
    line-height: 1.4;
    background: none;
  }

  blockquote p {
    color: var(--soft);
    max-width: 100%;
  }

  blockquote footer,
  blockquote cite {
    display: block;
    margin-top: 1em;
    font-family: ui-monospace, monospace;
    font-size: 0.72rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--muted);
    font-style: normal;
  }

  .kicker {
    font-family: ui-monospace, "SF Mono", Menlo, monospace;
    font-size: 0.72rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--teal);
    margin-bottom: 0.6em;
  }

  .subtitle {
    font-size: 1.1rem;
    color: var(--soft);
    line-height: 1.6;
    max-width: 52ch;
    margin-top: 0.6em;
  }

  .chip {
    display: inline-block;
    font-family: ui-monospace, monospace;
    font-size: 0.68rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    padding: 5px 14px;
    border: 1px solid var(--teal);
    border-radius: 999px;
    color: var(--teal);
    margin-right: 10px;
    margin-top: 8px;
  }

  .pill {
    display: inline-block;
    font-family: ui-monospace, monospace;
    font-size: 0.68rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    padding: 5px 14px;
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 999px;
    color: var(--soft);
    margin-right: 10px;
    margin-top: 8px;
  }
  .pill.t { border-color: #2dd4bf; color: #2dd4bf; }
  .pill.s { border-color: #38bdf8; color: #38bdf8; }
  .pill.m { border-color: #e879f9; color: #e879f9; }

  .cols {
    display: grid;
    grid-template-columns: 1fr 1px 1fr;
    gap: 0;
    align-items: stretch;
    margin-top: 1em;
  }

  .col {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.09);
    padding: 28px 28px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .col:first-child { border-radius: 12px 0 0 12px; border-right: none; }
  .col:last-child  { border-radius: 0 12px 12px 0; border-left: none; }

  .col-rule {
    background: linear-gradient(180deg, transparent, #2dd4bf 20%, #2dd4bf 80%, transparent);
    box-shadow: 0 0 10px #2dd4bf;
  }

  .col-head {
    font-family: ui-monospace, monospace;
    font-size: 0.68rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #2dd4bf;
  }

  .col-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--ink);
    margin: 0;
  }

  .col-tag {
    font-family: ui-monospace, monospace;
    font-size: 0.68rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    padding-top: 12px;
    border-top: 1px solid rgba(255,255,255,0.09);
    margin-top: auto;
  }
  .col-tag.t { color: #2dd4bf; }
  .col-tag.m { color: #e879f9; }
  .col-tag.s { color: #38bdf8; }

  .col ul { margin: 0; }
  .col ul li { font-size: 0.88rem; }

  .data-slide {
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 16px;
  }

  .stat-label {
    font-family: ui-monospace, monospace;
    font-size: 0.72rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--muted);
  }

  .stat-num {
    font-size: 9rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    line-height: 1;
    background: linear-gradient(135deg, #2dd4bf, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    filter: drop-shadow(0 0 24px rgba(45,212,191,0.4));
  }

  .stat-sub {
    font-family: ui-monospace, monospace;
    font-size: 0.72rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--teal);
  }

  .chapter-num {
    font-family: ui-monospace, "SF Mono", Menlo, monospace;
    font-size: 8rem;
    font-weight: 800;
    line-height: 1;
    letter-spacing: -0.04em;
    color: #2dd4bf;
    text-shadow: 0 0 40px rgba(45,212,191,0.5), 0 0 80px rgba(45,212,191,0.25);
  }

  /* cover / closing — gradient title already handled by h1 */
  section.lead h1 { font-size: 3.8rem; }
  section.chapter h1 { -webkit-text-fill-color: var(--ink); background: none; color: var(--ink); }

  hr { border: none; border-top: 1px solid rgba(255,255,255,0.09); margin: 1em 0; }
---

<!-- _class: lead -->

<div class="kicker">Knowledge Retrieval · Enterprise AI · 2024</div>

# RAG Has an Amnesia Problem

<div class="subtitle">Why compilation-based retrieval outperforms vector similarity search for enterprise knowledge management — and when knowledge graphs win instead.</div>

---

### Chapter 01 · AI Retrieval Paradigms

## Three ways to answer a question

Enterprise AI retrieval has converged on three paradigms. Each bets on a different moment to pay the cost of understanding — at query time, at schema time, or at ingest time. The moment you choose determines everything about faithfulness, speed, and auditability.

<br>

<span class="pill m">Vector RAG — fast, shallow</span>
<span class="pill s">Knowledge Graphs — deep, costly</span>
<span class="pill t">Compilation — holistic, auditable</span>

---

### Chapter 01 · AI Retrieval Paradigms

## Vector RAG vs Compilation

<div class="cols">
  <div class="col">
    <div class="col-head">Traditional</div>
    <div class="col-title">Vector RAG</div>
    <ul>
      <li class="neg">Retrieves isolated K-nearest chunks at query time</li>
      <li class="neg">No cross-document memory between queries</li>
      <li class="neg">Contradictions in source material undetected</li>
      <li class="neg">Synthesis is whatever the chunks happen to contain</li>
    </ul>
    <div class="col-tag m">Amnesia Problem</div>
  </div>
  <div class="col-rule"></div>
  <div class="col">
    <div class="col-head">Compilation-based</div>
    <div class="col-title">OpenKB Model</div>
    <ul>
      <li class="pos">LLM synthesises full corpus at ingest — once</li>
      <li class="pos">Concepts, entities, cross-references baked in</li>
      <li class="pos">Contradictions flagged at compile time</li>
      <li class="pos">Human-readable, diffable, auditable wiki artifact</li>
    </ul>
    <div class="col-tag t">Build-step Retrieval</div>
  </div>
</div>

---

### Chapter 01 · AI Retrieval Paradigms

<div class="data-slide">
  <div class="stat-label">Cross-references built by traditional RAG</div>
  <div class="stat-num">0</div>
  <div class="stat-sub">Every query starts cold</div>
</div>

K-nearest chunk retrieval returns passages, not understanding. No memory of how concepts connect across documents, no contradiction detection, no synthesis that spans the full corpus. Each query is an island.

---

<!-- _class: chapter -->

<div style="font-family:ui-monospace,monospace;font-size:0.72rem;letter-spacing:0.22em;text-transform:uppercase;color:#69748a;">Chapter</div>
<div class="chapter-num">02</div>

# Knowledge Graphs vs Vector Search

---

### Chapter 02 · AI Retrieval Paradigms

## Knowledge Graphs vs Vector Search

<div class="cols">
  <div class="col">
    <div class="col-head">Neo4j · Neptune · Google KG</div>
    <div class="col-title">Knowledge Graphs</div>
    <ul>
      <li class="pos">Multi-hop reasoning via graph traversal</li>
      <li class="pos">Explicit entity + relationship modelling</li>
      <li class="pos">High faithfulness for structured domains</li>
      <li class="neg">Slow ingest — schema, ontology, entity resolution</li>
      <li class="neg">Brittle on dynamic, fast-moving corpora</li>
    </ul>
    <div class="col-tag s">Structured / Static domains</div>
  </div>
  <div class="col-rule"></div>
  <div class="col">
    <div class="col-head">Pinecone · Weaviate · pgvector</div>
    <div class="col-title">Vector Search</div>
    <ul>
      <li class="pos">Fast ingest — embed and index, no schema</li>
      <li class="pos">Low setup complexity, any document type</li>
      <li class="neg">No entity relationships — flat similarity only</li>
      <li class="neg">Poor cross-document synthesis</li>
      <li class="neg">Zero contradiction detection</li>
    </ul>
    <div class="col-tag m">Broad / Shallow</div>
  </div>
</div>

---

### Chapter 02 · AI Retrieval Paradigms

## The page **is** the concept

PageIndex (OpenKB) indexes compiled concept and entity pages — not raw chunks. Each page is already a synthesised, cross-referenced understanding of the concept. The retrieved unit knows everything the corpus says about the topic. No embedding pipeline, no vector infrastructure required.

<br>

<span class="pill t">Vectorless retrieval</span>
<span class="pill s">Semantic structure at ingest</span>
<span class="pill">No embedding cost</span>

---

### Chapter 03 · AI Retrieval Paradigms

## GraphRAG vs Compilation Model

<div class="cols">
  <div class="col">
    <div class="col-head">Microsoft Research · 2024</div>
    <div class="col-title">GraphRAG</div>
    <ul>
      <li>Local + global community graph structure</li>
      <li>Graph-aware retrieval at query time</li>
      <li>Hybrid: knowledge graph + vector search</li>
      <li class="pos">Strong for domains with pre-existing ontologies</li>
      <li class="neg">Requires schema design and vector infrastructure</li>
    </ul>
    <div class="col-tag s">Structured domains</div>
  </div>
  <div class="col-rule"></div>
  <div class="col">
    <div class="col-head">VectifyAI · OpenKB</div>
    <div class="col-title">Compilation Model</div>
    <ul>
      <li>Flat wiki — concepts + entities + cross-refs</li>
      <li>Vectorless retrieval via PageIndex</li>
      <li>No schema, no ontology, no embedding pipeline</li>
      <li class="pos">Human-readable, diffable, fully auditable</li>
      <li class="pos">Built for dynamic, growing corpora</li>
    </ul>
    <div class="col-tag t">Dynamic corpora</div>
  </div>
</div>

---

### Chapter 03 · AI Retrieval Paradigms

> "Synthesis reflects everything the system has consumed — not just random K-nearest chunks."
>
> <cite>OpenKB · Inspired by Karpathy — compilation-based retrieval as a first-class build step</cite>

---

<!-- _class: lead -->

<div class="kicker">The knowledge-first future</div>

# Build. Compile. Know.

<div class="subtitle">Stop retrieving isolated chunks. Treat document ingestion as a compilation step — and let your knowledge base compound across every document you add. RAG for breadth. Graphs for structure. Compilation for synthesis.</div>

<br>

<span class="chip">github.com/VectifyAI/OpenKB</span>
<span class="chip">PageIndex — vectorless retrieval</span>
<span class="chip">shekerkamma/OpenKB</span>

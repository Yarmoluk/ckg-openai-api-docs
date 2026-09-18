<div class="hero" markdown>
<p class="eyebrow">Graphify.md · independent research preview</p>
<h1>API documentation an agent can inspect.</h1>
<p class="lede">Find the model constraint, tool contract or request parameter that matters—and keep the official source attached.</p>
<div class="hero-actions">
<a class="md-button md-button--primary" href="quickstart.html">Run a query</a>
<a class="md-button" href="architecture.html">See the architecture</a>
</div>
</div>

## From documentation to usable context

<div class="signal-grid" markdown>
<div class="signal-card" markdown>
### 541 indexed entries
API guides, models and endpoint reference. Recovered reference redirects are recorded explicitly.
</div>
<div class="signal-card" markdown>
### 2,889 nodes
Document context, selected sections, request schemas and reviewed semantic concepts.
</div>
<div class="signal-card" markdown>
### 4,731 relationships
Explicit links and section membership, plus two documented requirements.
</div>
</div>

## A practical question

```bash
python3 scripts/query.py "Astra function calling Chat Completions" --limit 3
```

The result includes the documented Astra function-calling constraint, the Responses requirement and a link to the reasoning guide. The caller can inspect that evidence before making a code change.

The same workflow applies to async tool output types, steering, compaction, prompt caching and administration request schemas.

## What is established

The package passes structural checks and retrieval replay. The author reviewed 20 practical questions: 19 complete supported answers and one evidence-limited abstention after repairs.

!!! warning "Preview, with explicit provenance limits"
    Original HTTP response-byte hashes remain unverified. Parser-capture hashes are recorded, but full source captures are not redistributed here. Independent human evaluation is pending. These checks do not demonstrate better coding outcomes or benchmark superiority.

[Read the evaluation](evaluation.md){ .md-button }
[Inspect provenance](provenance.md){ .md-button }

This independent project is not affiliated with or endorsed by OpenAI.

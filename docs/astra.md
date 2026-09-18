# GPT-6 Astra: a practical reference

Start with the behavior your application needs, then follow the relevant graph concept to its official source. This page explains a selected path through the larger API documentation graph.

<div class="reference-intro" markdown>
**The model is one part of the application.** The API determines which requests you can send; tools define work outside the model; conversation state carries prior work forward. The graph makes the documented connections between these decisions visible.
</div>

## Choose the API for tool calls

If your Astra application calls functions, use the Responses API. Astra's Chat Completions support does not extend to function calling. A text-generation integration and a tool-calling integration therefore need different compatibility checks. [Official reasoning guide](https://developers.openai.com/api/docs/guides/reasoning).

**Graph path:** ASTRA-TOOLS → REQUIRES → RESPONSES-API.

```bash
python3 scripts/query.py "Astra function calling Chat Completions" --limit 3
```

Check the returned fact and its source before changing your application's request flow.

## Configure the model deliberately

| Decision | Astra reference |
|---|---|
| Model name | gpt-6-astra |
| Reasoning effort | low, medium, high, xhigh or max |
| none reasoning | Unsupported; the reasoning guide documents HTTP 400 |
| Input | Text and images |
| Output | Text |
| Context / output limits | 1,050,000-token context; 128,000-token maximum output |

Sources: [Astra model page](https://developers.openai.com/api/docs/models/gpt-6-astra) and [reasoning guide](https://developers.openai.com/api/docs/guides/reasoning). These are documentation snapshots checked September 18, 2026.

When migrating an existing application, remove the unsupported sampling fields temperature, top_p and top_logprobs. Also check the separate logprob restrictions for Chat Completions and Responses. [Official Astra migration guidance](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6-astra).

**Graph concepts:** ASTRA-NONE, ASTRA-MIGRATION-EFFORT, ASTRA-PARAMETERS.

## Let tools work asynchronously

An async tool lets the model continue while your application performs the work. Your application still runs the function or custom tool and owns the pending job. When the result is ready, connect it to the original API call_id.

| Original call | Result item |
|---|---|
| function_call | function_call_output |
| custom_tool_call | custom_tool_call_output |

The async-tools guide also describes compatibility limits: this mechanism is for application-run function/custom tools, and its Multi-agent guidance excludes combining async tools with parallel calls. [Official async-tool documentation](https://developers.openai.com/api/docs/guides/async-tool-calling).

**Graph concepts:** ASYNC-APP, ASYNC-ID, ASYNC-COMPAT.

```bash
python3 scripts/query.py "async call_id function_call_output" --limit 3
```

## Redirect a running response

Mid-turn steering sends new user input while a response is running. Astra supports it over a WebSocket connection to Responses.

An acceptance event means the update is queued. It does not mean the model has already acted on it, and steering does not undo emitted output or cancel tools that have started. [Official steering documentation](https://developers.openai.com/api/docs/guides/steering).

**Graph path:** STEER-WS → REQUIRES → RESPONSES-WS. Related concepts: STEER-ACK and STEER-EFFECT.

This distinction matters when your interface says “update accepted”: the application should distinguish receipt of an instruction from completion of the requested work.

## Manage reasoning and conversation state

| Mechanism | What to preserve or check | Graph concept |
|---|---|---|
| Change reasoning effort between responses | Use configuration_update while keeping request-level effort unchanged to preserve the original prefix. | REASON-UPDATE |
| Combine updates with compaction | Review the documented exclusions for automatic compaction/truncation and standalone compact histories. | REASON-UPDATE-LIMITS |
| Standalone compaction | Keep the complete returned context window, including retained items. | COMPACT-STANDALONE |
| Prompt-cache reuse | Compaction can alter the prefix and reduce reuse on the next request. | CACHE-COMPACT |

Sources: [reasoning](https://developers.openai.com/api/docs/guides/reasoning), [compaction](https://developers.openai.com/api/docs/guides/compaction) and [prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching).

A useful review question is: **“If we change reasoning effort and compact this conversation, which state and configuration must we carry into the next request?”** Retrieve both constraints before choosing a flow.

## Read the actual relationships

![Five sourced relationships around Astra](assets/graphs/astra-relationships.svg)

The diagram is a static subset of the checked-in graph. REQUIRES denotes an explicit requirement. RELATES_TO connects a concept with contextual documentation; it does not assert an implementation dependency.

The [diagram manifest](assets/graphs/astra-relationships.json) records the exact node IDs, relation types, source URLs and source-graph checksum.

## Use the reference in real work

1. State the concrete behavior: tool calling, live updates, reasoning changes or context retention.
2. Run a narrow graph query.
3. Inspect the cited official page, especially for volatile limits or compatibility.
4. Implement the change and test the actual request/response behavior.

The graph helps locate documented constraints. Application correctness still depends on your implementation and tests.

[Read the evaluation](evaluation.md){ .md-button }
[Check evidence limitations](provenance.md){ .md-button }

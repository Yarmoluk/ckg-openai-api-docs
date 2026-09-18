# Run it

## Requirements

Python 3.10 or later. Graph lookup, validation and evaluation replay use only the standard library.

```bash
git clone https://github.com/Yarmoluk/astra-developer-reference-ckg.git
cd astra-developer-reference-ckg
python3 scripts/query.py "Astra none reasoning"
```

## Useful queries

```bash
python3 scripts/query.py "async call_id function_call_output" --limit 3
python3 scripts/query.py "configuration_update compaction"
python3 scripts/query.py "Astra EU fast priority"
python3 scripts/query.py "organization admin API keys pagination order"
```

The JSON result contains:

| Field | Meaning |
|---|---|
| id | Stable concept identifier |
| key_fact | Proposed documentation fact |
| source_url | Official source to inspect |
| source_hash | Original response hash; currently null |
| capture_sha256 | Hash of a parser representation retained in the author's evidence package |
| neighbors | Explicit outgoing graph relationships |

## Use with a coding agent

Give the agent the repository location and a task such as:

> Before changing our Astra tool-calling code, run scripts/query.py with the relevant question. Cite the node IDs and official source URLs you use. Check current documentation where compatibility or pricing matters. Treat missing evidence as unknown.

This is a context workflow, not an installed agent integration. The query command performs no API calls.

## Check the package

```bash
python3 scripts/validate.py
python3 scripts/evaluate.py
```

The first command checks graph endpoints, source fields, export hashes and prohibited public content. The second replays the frozen questions and verifies retrieval of the nodes cited by the manual answers.

## Preview the documentation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-docs.txt
mkdocs serve
```

Open the local URL printed by MkDocs. Use mkdocs build --strict for the same documentation check as CI.

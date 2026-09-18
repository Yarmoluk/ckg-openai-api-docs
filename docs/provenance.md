# Provenance and maintenance

## Three different checks

| Check | Current status | What it establishes |
|---|---|---|
| Export file checksums | Verified | The public package matches its export manifest. |
| Retained parser-capture hashes | Verified in the author's evidence package | The retained parsed representations have not changed. |
| Original HTTP response-byte hashes | Unverified | No original-byte attestation is claimed. |

The source_hash field is null. Do not substitute capture_sha256 for it. Full upstream pages are not redistributed; official URLs remain the route to the source.

## Coverage

The September 18, 2026 inventory includes 226 API guides, 215 reference entries and 100 model entries.

Seventy-three indexed Markdown references initially contained generated placeholders. Their HTML counterparts redirected to 70 distinct substantive reference pages. The ledger preserves both indexed and resolved evidence URLs. The graph now includes 77 recovered request-schema nodes.

There are 401 unresolved internal link pairs representing 118 distinct destinations, including navigation roots. An uncaptured link is not automatically a broken link. The indexed-page inventory is not the entire developer website, and page coverage is not complete claim coverage.

Separate Codex, Apps SDK and other developer-site collections are outside this package.

## Update procedure

1. Check the official documentation indexes weekly.
2. Recheck model features, prices and compatibility before operational use.
3. Retain new source bytes and record redirects explicitly.
4. Compare changed sources with affected graph concepts; preserve earlier captures.
5. Propose fact and relationship changes with exact source support.
6. Run graph validation, question review and repository checks.
7. Review and approve the exact public diff before publishing an update.

A detected source change does not authorize automatic claim rewriting. This repository does not start a source monitor or background service.

## Re-export an already reviewed candidate

```bash
python3 scripts/export_candidate.py /path/to/reviewed-candidate
python3 scripts/validate.py
python3 scripts/evaluate.py
mkdocs build --strict
```

The exporter expects the reviewed candidate format described by its code. It is not a web crawler or autonomous graph compiler.

## Attribution

Official source content comes from developers.openai.com. This independent Graphify.md project is not affiliated with or endorsed by OpenAI. Original project software and presentation are licensed separately from upstream documentation; see NOTICE.md in the repository.

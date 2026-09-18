#!/usr/bin/env python3
"""Validate public graph integrity and screen the versioned public package."""
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 graph=json.loads((ROOT/'data/graph.json').read_text());nodes={n['id']:n for n in graph['nodes']};assert len(nodes)==len(graph['nodes'])
 keys=set()
 for n in nodes.values():
  assert n['source_url'].startswith('https://developers.openai.com/api/')
  assert n['source_hash'] is None
  assert re.fullmatch('[0-9a-f]{64}',n['capture_sha256'])
  assert not any(k in n for k in ['capture_path','evidence','line_start','line_end'])
 for e in graph['edges']:
  key=(e['source'],e['relation'],e['target']);assert key not in keys;keys.add(key)
  assert e['source'] in nodes and e['target'] in nodes and e['source']!=e['target']
  assert e['relation'] in {'REQUIRES','RELATES_TO','ENABLES','IMPLEMENTS'}
 assert graph['meta']['nodes']==len(nodes) and graph['meta']['edges']==len(keys)
 assert graph['meta']['benchmarked'] is False
 manifest=json.loads((ROOT/'data/export-manifest.json').read_text())
 for name,digest in manifest['files'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
 patterns=[r'(?<![A-Za-z0-9/])/Users/[A-Za-z]',r'file:///Users/',r'brain/(?:memory|sessions)/',r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b',r'sk-[A-Za-z0-9_-]{16,}',r'gh[pousr]_[A-Za-z0-9]{20,}',r'AKIA[0-9A-Z]{16}']
 for base in ['data','evals','docs']:
  for path in (ROOT/base).rglob('*'):
   if path.is_file() and path.suffix in {'.json','.md','.csv','.html','.yml','.py','.txt'}:
    content=path.read_text()
    for pattern in patterns:assert not re.search(pattern,content,re.I),(str(path.relative_to(ROOT)),pattern)
 print(json.dumps({'status':'passed','nodes':len(nodes),'edges':len(keys),'raw_source_hashes_verified':0,'public_content_screen':'passed','export_manifest':'passed'},indent=2))
if __name__=='__main__':main()

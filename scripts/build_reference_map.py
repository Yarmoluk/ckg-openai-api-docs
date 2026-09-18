#!/usr/bin/env python3
"""Render a small static relationship map from exact checked-in graph edges."""
import argparse,hashlib,html,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ROWS=[
 ('ASTRA-TOOLS','REQUIRES','RESPONSES-API','Astra function calling','Responses API','Choose the API for tool calls.'),
 ('STEER-WS','REQUIRES','RESPONSES-WS','Mid-turn steering','Responses WebSocket','Choose the transport for live updates.'),
 ('ASYNC-ID','RELATES_TO','OAI-065081c54a27','Async result correlation','Async tool calling guide','Match results to the original call_id.'),
 ('REASON-UPDATE','RELATES_TO','OAI-ec400e9e55dc','Change reasoning effort','Reasoning models guide','Inspect configuration and compatibility.'),
 ('CACHE-COMPACT','RELATES_TO','OAI-c86beef864f4','Cache reuse after compaction','Prompt caching guide','Understand why prefix reuse can change.')
]
def render():
 raw=(ROOT/'data/graph.json').read_bytes();g=json.loads(raw);nodes={n['id']:n for n in g['nodes']};edges={(e['source'],e['relation'],e['target']) for e in g['edges']};manifest=[]
 parts=['<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="790" viewBox="0 0 1120 790" role="img" aria-labelledby="title desc">','<title id="title">Five declared relationships in the Astra reference</title>','<desc id="desc">Two requirement edges connect Astra function calling to Responses and mid-turn steering to WebSocket. Three context edges connect async result correlation, reasoning updates and compaction cache reuse to their source guides.</desc>','<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#147766"/></marker><marker id="soft" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#7a8e9b"/></marker></defs>','<rect width="1120" height="790" rx="22" fill="#f4f8f7"/>','<g font-family="system-ui,Segoe UI,sans-serif"><text x="40" y="48" font-size="14" font-weight="700" letter-spacing="2" fill="#216c60">ASTRA / DECLARED RELATIONSHIPS</text><text x="40" y="82" font-size="25" font-weight="700" fill="#163a3a">Start with the behavior. Follow the relationship.</text>']
 for index,(a,relation,b,left,right,meaning) in enumerate(ROWS):
  assert (a,relation,b) in edges,(a,relation,b)
  y=120+index*119;solid=relation=='REQUIRES';color='#147766' if solid else '#7a8e9b'
  for x,label,id in [(40,left,a),(670,right,b)]:
   parts.append(f'<rect x="{x}" y="{y}" width="410" height="88" rx="12" fill="white" stroke="#cddfd9"/><text x="{x+20}" y="{y+34}" font-size="21" font-weight="650" fill="#163a3a">{html.escape(label)}</text><text x="{x+20}" y="{y+61}" font-family="monospace" font-size="12" fill="#57716d">{html.escape(id)}</text>')
  dash='' if solid else ' stroke-dasharray="6 5"'
  parts.append(f'<path d="M450 {y+45} H654" fill="none" stroke="{color}" stroke-width="2.5"{dash} marker-end="url(#{"arrow" if solid else "soft"})"/><rect x="482" y="{y+15}" width="140" height="22" rx="5" fill="#f4f8f7"/><text x="552" y="{y+30}" text-anchor="middle" font-family="monospace" font-size="13" font-weight="700" fill="{color}">{relation}</text>')
  manifest.append({'source':a,'relation':relation,'target':b,'meaning':meaning,'source_url':nodes[a]['source_url'],'target_url':nodes[b]['source_url']})
 parts.append('<text x="40" y="752" font-size="14" fill="#49645f">Solid = documented requirement. Dashed = contextual link to a guide, not a prerequisite.</text></g></svg>')
 return '\n'.join(parts)+'\n',json.dumps({'graph_sha256':hashlib.sha256(raw).hexdigest(),'relationships':manifest,'scope':'Static explanatory subset; no additional graph relationships inferred.'},indent=2)+'\n'
def main():
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
 svg,manifest=render()
 for name,content in [('astra-relationships.svg',svg),('astra-relationships.json',manifest)]:
  path=ROOT/'docs/assets/graphs'/name
  if a.check:assert path.read_text()==content,name
  else:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content)
 print('Five displayed relationships match the source graph.')
if __name__=='__main__':main()

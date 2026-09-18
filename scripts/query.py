#!/usr/bin/env python3
"""Search graph facts offline, returning official source links and declared neighbors."""
import argparse,collections,json,math,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
STOP=set("a an the is are does do how what when with for to of in on and or can i use".split())
def tokens(value):return [w for w in re.findall(r"[a-z0-9_]+",value.lower()) if w not in STOP]
def search(query,limit=5,graph_path=None):
 graph=json.loads(Path(graph_path or ROOT/'data/graph.json').read_text());terms=set(tokens(query));records=graph['nodes']
 documents=[collections.Counter(tokens(n['label']+' '+n['key_fact'])) for n in records]
 frequencies=collections.Counter(t for d in documents for t in d);average=sum(sum(d.values()) for d in documents)/len(documents);hits=[]
 for n,d in zip(records,documents):
  score=0;length=sum(d.values());labels=set(tokens(n['label']))
  for t in terms:
   tf=d[t]
   if tf:
    idf=math.log(1+(len(records)-frequencies[t]+.5)/(frequencies[t]+.5))
    score+=idf*(tf*2.2/(tf+1.2*(.25+.75*length/average)))+(1.5 if t in labels else 0)
  if score:
   item={k:n[k] for k in ('id','label','key_fact','source_url','source_hash','capture_sha256','layer')}
   item['score']=round(score,4);item['neighbors']=[{'relation':e['relation'],'target':e['target']} for e in graph['edges'] if e['source']==n['id']][:12];hits.append(item)
 return sorted(hits,key=lambda x:(-x['score'],x['id']))[:limit]
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('query');p.add_argument('--limit',type=int,default=5);p.add_argument('--graph',type=Path,default=ROOT/'data/graph.json');a=p.parse_args()
 print(json.dumps({'status':'research preview; original source bytes unverified','results':search(a.query,max(1,a.limit),a.graph)},indent=2,ensure_ascii=False))

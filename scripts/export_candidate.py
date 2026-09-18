#!/usr/bin/env python3
"""Export domain-only artifacts from a reviewed local candidate."""
import argparse,csv,hashlib,html,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def public_graph(graph):
 nodes=[{k:n[k] for k in ('id','label','type','key_fact','source_id','source_url','source_hash','capture_sha256','layer','review_status')} for n in graph['nodes']]
 edges=[{k:e[k] for k in ('source','relation','target','source_url','source_hash','capture_sha256','kind')} for e in graph['edges']]
 meta={**graph['meta'],'status':'public-research-preview','original_response_bytes_verified':False,'independent_human_review':'pending'}
 return {'meta':meta,'nodes':nodes,'edges':edges}
def write(path,value):
 path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('candidate',type=Path);a=p.parse_args();source=a.candidate
 graph=public_graph(json.loads((source/'graph.json').read_text()));write(ROOT/'data/graph.json',graph)
 manifest=[]
 for s in json.loads((source/'sources.json').read_text()):
  manifest.append({'id':s['id'],'title':s['title'],'kind':s['kind'],'indexed_url':s['url'],'evidence_url':s.get('evidence_url',s['url']),'source_hash':None,'capture_sha256':s['capture_sha256'],'representation':s['representation'],'retrieved_at':s['retrieved_at'],'coverage':s['coverage'],'redirect_recovered':bool(s.get('recovered_from_placeholder'))})
 write(ROOT/'data/sources.json',manifest)
 adjacency={}
 for e in graph['edges']:adjacency.setdefault(e['source'],[]).append(e['target']+':'+e['relation'])
 with (ROOT/'data/graph.csv').open('w',newline='') as f:
  w=csv.writer(f,lineterminator="\n");w.writerow(['ConceptID','ConceptLabel','Dependencies','TaxonomyID','KeyFact','SourceURL','source_content_hash'])
  for n in graph['nodes']:w.writerow([n['id'],n['label'],'|'.join(adjacency.get(n['id'],[])),n['type'],n['key_fact'],n['source_url'],''])
 esc=lambda s:html.escape(str(s),quote=False).replace('|','&#124;').replace('\n','&#10;')
 parts=['# OpenAI API documentation CKG','## META','version: '+graph['meta']['version']+'\nstatus: public-research-preview\nentities: '+str(len(graph['nodes']))+'\nrelationships: '+str(len(graph['edges'])),'## SCOPE','Indexed API guides, model pages and endpoint references. Navigation uses RELATES_TO. Original response-byte provenance is unverified; capture hashes describe parsed representations retained by the author. The full source captures are not redistributed.','## NODES','| ID | Label | Type | Key Fact | source_url | source_hash |\n|---|---|---|---|---|---|\n'+'\n'.join('| '+' | '.join(esc(n[k]) for k in ['id','label','type','key_fact','source_url'])+' | |' for n in graph['nodes']),'## EDGES','| Source | Relation | Target |\n|---|---|---|\n'+'\n'.join('| '+e['source']+' | '+e['relation']+' | '+e['target']+' |' for e in graph['edges']),'## EVAL','benchmarked: false\nindependent_human_review: pending\nanswer_quality_advantage: unmeasured\nraw_source_hashes: unverified\nAuthor-reviewed diagnostic questions are documented separately in evals/.','## MAINTENANCE','Review official source indexes weekly and recheck changing specifications before operational use. Source changes require review; they do not authorize automatic fact rewriting.']
 (ROOT/'data/ckg-openai-api-docs.md').write_text('\n\n'.join(parts)+'\n')
 review=source/'review-2026-09-18'
 write(ROOT/'evals/baseline-graph.json',public_graph(json.loads((review/'baseline-graph.json').read_text())))
 for name in ['questions.json','answers.json']:write(ROOT/'evals'/name,json.loads((review/name).read_text()))
 write(ROOT/'data/export-manifest.json',{'source_candidate_graph_sha256':hashlib.sha256((source/'graph.json').read_bytes()).hexdigest(),'files':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in ['data/graph.json','data/sources.json','data/graph.csv','data/ckg-openai-api-docs.md','evals/baseline-graph.json','evals/questions.json','evals/answers.json']},'excludes':['Full upstream source captures','Local filesystem locators','Private workspace and operational records'],'limits':'Export integrity does not establish upstream byte provenance or semantic correctness.'})
 print(json.dumps({'nodes':len(graph['nodes']),'edges':len(graph['edges']),'sources':len(manifest)},indent=2))
if __name__=='__main__':main()

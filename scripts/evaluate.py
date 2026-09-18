#!/usr/bin/env python3
"""Replay retrieval supporting the published manual answer audit, not a semantic grader."""
import collections,hashlib,json
from pathlib import Path
from query import search
ROOT=Path(__file__).resolve().parents[1]
def main():
 questions=json.loads((ROOT/'evals/questions.json').read_text());answers=json.loads((ROOT/'evals/answers.json').read_text());overrides={a['case_id']:a for a in answers['baseline_overrides']};output={}
 for variant,path in [('baseline',ROOT/'evals/baseline-graph.json'),('candidate',ROOT/'data/graph.json')]:
  scores=collections.Counter();cases=[]
  for q,answer in zip(questions['cases'],answers['candidate']):
   assert q['id']==answer['case_id']
   reviewed=overrides.get(q['id'],answer) if variant=='baseline' else answer
   hits=search(q['question'],5,path);ids={h['id'] for h in hits}
   assert set(reviewed['citations'])<=ids,(variant,q['id'],reviewed['citations'])
   scores[reviewed['status']]+=1;cases.append({'id':q['id'],'retrieved':[h['id'] for h in hits],'cited':reviewed['citations'],'author_review':reviewed['status']})
  output[variant]={'graph_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'manual_review_counts':dict(scores),'cases':cases}
 report={'status':'citation_retrieval_replay_passed','method':answers['method'],'questions_sha256':hashlib.sha256((ROOT/'evals/questions.json').read_bytes()).hexdigest(),'warning':'Manual support judgments are not recomputed by this script. No independent answer-quality benchmark.','results':output}
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()

#!/usr/bin/env python3
"""Local-only, one-shot Ollama measurement; never sends data externally.

Usage: python tools/benchmark_ollama.py --model llama3.2:3b
Prereq: run Ollama locally and pull the requested model.
Record memory independently with nvidia-smi; this script cannot measure peak VRAM.
"""
import argparse
from datetime import datetime, timezone
import json
import time
from urllib.request import Request, urlopen

URL='http://127.0.0.1:11434/api/generate'
P='In 4 concise sentences, describe the difference between AI inference and model training.'


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',default='llama3.2:3b')
    parser.add_argument('--output',default='')
    args=parser.parse_args()
    payload={'model':args.model,'prompt':P,'stream':False,'options':{'num_predict':150,'num_ctx':2048}}
    req=Request(URL,json.dumps(payload).encode(),headers={'Content-Type':'application/json'},method='POST')
    start=time.perf_counter()
    with urlopen(req,timeout=95) as r:
        result=json.load(r)
    wall=time.perf_counter()-start
    count=result.get('eval_count')
    duration_ns=result.get('eval_duration')
    throughput=(count/(duration_ns/1e9)) if isinstance(count,int) and isinstance(duration_ns,(int,float)) and duration_ns>0 else None
    report={
      'time_utc':datetime.now(timezone.utc).isoformat(),
      'model':args.model,
      'input_prompt':P,
      'wall_seconds':round(wall,3),
      'output_tokens_ollama_reported':count,
      'generation_seconds_ollama_reported':round(duration_ns/1e9,3) if isinstance(duration_ns,(int,float)) else None,
      'throughput_tokens_per_sec_ollama_reported':round(throughput,2) if throughput is not None else None,
      'gpu_memory_peak_gib':None,
      'note':'One local test; not a benchmark distribution. Confirm GPU offload separately using ollama ps and nvidia-smi.'
    }
    text=json.dumps(report,indent=2)
    if args.output:
        from pathlib import Path
        Path(args.output).write_text(text+'\n')
        print(f'Wrote {args.output}')
    else:
        print(text)

if __name__=='__main__':main()

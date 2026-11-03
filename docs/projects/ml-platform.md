# RTX AI & ML research platform

**Fields:** GPU computing · applied machine learning · MLOps · research tooling

## The idea

My HP Z440 is more than a server for web applications: it's a place to develop, execute, instrument, and repeat machine learning experiments on my own hardware. The GPU is an **NVIDIA RTX 4060 Ti with 16 GB of VRAM**.

Instead of scattering datasets, outputs and environment notes across notebooks, I designed a reusable experimental workflow that connects local computation with versioning, artifact storage, orchestration and monitoring.

## Components and responsibilities

| Component | What it does |
| --- | --- |
| Ubuntu + NVIDIA GPU | Local compute and acceleration |
| Python + JupyterLab | Prototyping and experimental code |
| Docker Compose | Repeatable supporting services |
| DVC | Track datasets and experiment inputs |
| MinIO | Store generated datasets, checkpoints, and experiment artifacts |
| Prefect | Organize experiment tasks and dependencies |
| Custom Python SDK | Consistent experiment logging and instrumentation |
| Prometheus + Grafana + Loki | Observe system load, application behavior, and logs |

The components above describe the research stack and its intended roles. They are not claims that a particular experiment achieved a specific speed, accuracy or uptime.

## Example experimental flow

```text
Dataset / DVC revision
       ↓
Experiment config + Python environment
       ↓
Prefect task flow → RTX / CUDA workload
       ↓
Metrics, logs and model artifacts
       ↓
MinIO storage + experiment notes
       ↓
Review performance, change one variable, repeat
```

## What I want an experiment to answer

- Which model and dataset revision produced the result?
- What exact code and configuration did it run with?
- How long did execution and inference take?
- How much GPU memory and CPU capacity did the job require?
- Where are the artifacts, logs and evaluation results?

Keeping these answers together makes small experiments more valuable and easier to reproduce.

## Local inference and the public demo

I am preparing an isolated [RTX inference playground](../ai-demo.md) so visitors can explore a local model through a simple UI. The model-serving application is separate from the internal MLOps stack and the workstation's administration tools.

## What comes next

Publish a complete reproducible run with its dataset revision, task graph, artifact manifest and **measured** latency/throughput. Until that evidence is published, the site intentionally avoids presenting benchmark numbers as achieved results.

See also: [MLOps workflow](../mlops.md) and [architecture](../architecture.md).

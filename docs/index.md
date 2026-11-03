# Welcome to Buffy's engineering notebook

**Buffy** is my self-hosted Linux workstation and the center of my personal engineering lab. I use it to learn how real systems behave by building, maintaining, and connecting them—from local AI experiments to room-aware home automation.

The hardware is an **HP Z440 workstation with an NVIDIA RTX 4060 Ti (16 GB)** running Ubuntu. The real value lies in the software ecosystem and the experiments it supports.

## Find your way around

| Explore | You'll find |
| --- | --- |
| [Architecture](architecture.md) | How the workstation, containers, monitoring, and physical devices relate |
| [AI & ML research platform](projects/ml-platform.md) | Local GPU workloads, experiment workflows, and MLOps components |
| [MLOps workflow](mlops.md) | Dataset versioning, orchestration, artifacts, and experimental evidence |
| [Smart thermostat](projects/thermostat.md) | A complete build story: wireless sensors, Home Assistant, Z-Wave and decision logic |
| [Observability platform](projects/observability.md) | Measuring the behavior of containers and the Linux host |
| [Self-hosted applications](services.md) | How the software ecosystem is organized |
| [RTX demo](ai-demo.md) | How a local model can power an independent public demonstration |
| [Access & reliability](security.md) | The boundaries between a public showcase and private infrastructure |
| [Engineering evidence](evidence.md) | Project artifacts and measurements that make the work reproducible |

## Why a homelab?

Because there is a difference between reading about a system and running one. A homelab gives me somewhere to deploy software, examine its behavior, make mistakes, and improve it without relying entirely on managed services.

My projects fall into four areas:

1. **GPU experiments and applied AI:** local models, vision tasks, notebooks and supporting research tools.
2. **Self-hosted infrastructure:** Docker Compose services, databases, storage and development workspaces.
3. **Observability:** system metrics, logs, alerts, uptime checks and troubleshooting.
4. **Intelligent automation:** ESP8266 environmental sensors, Home Assistant and a Z-Wave thermostat.

## Try an experiment

The [thermostat explorer](../site/lab/index.html#control-lab) works directly in the browser. It illustrates the weighted-temperature controller described in [my published build story](https://rohanmarar.substack.com/p/the-thermostat-wars-revenge-of-the).

The [RTX AI playground](../site/lab/demos/index.html) is the next live connection: the application code is prepared, and public inference will become available when the GPU gateway has been configured and tested.

This site grows as the homelab grows. I share the reasoning, implementation, and limitations rather than simply listing installed software.

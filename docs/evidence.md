# Engineering evidence & results

I want this lab to be more than a visually interesting collection of dashboards. A useful engineering portfolio shows **how a system was designed**, **what was actually built**, and **what happened when it was tested**.

## Existing work and direct evidence

| Area | Evidence |
| --- | --- |
| Thermostat | [Complete public build article](https://rohanmarar.substack.com/p/the-thermostat-wars-revenge-of-the), published October 22, 2026, documenting the hardware, control algorithm and successful integration. |
| Service organization | [Screenshot of Buffy's private dashboard](../site/lab/index.html#architecture), plus the [searchable software inventory](../site/lab/index.html#stack). |
| AI research platform | [Platform documentation](projects/ml-platform.md) and the described MLOps toolchain; experiment-level measurements are the next step. |
| Observability | [Monitoring architecture](projects/observability.md) and the service inventory; a dated incident walkthrough is planned. |

## What I intend to publish next

- An **RTX experiment** with model revision, input, GPU memory use and measured inference latency.
- A **reproducible ML workflow** with DVC revision, Prefect run steps, MinIO artifacts and logged outputs.
- A **monitoring case study** describing one actual service failure, investigation and recovery.
- A **thermostat follow-up** with longer-duration room-temperature trends and control outcomes.
- A working **public inference interface**, isolated from internal management services.

Measured results will include a date and test setup so others can interpret them. I don't use estimated results as benchmark evidence.

## Links

Start with the [homelab overview](../site/lab/index.html), [thermostat story](projects/thermostat.md), or [MLOps workflow](mlops.md).

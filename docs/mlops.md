# MLOps workflow: from input to evidence

Machine learning experiments become far easier to evaluate when their **inputs, environment, execution steps and outputs** are traceable.

The platform is structured around an end-to-end sequence:

1. **Version the input.** DVC associates datasets and experiment inputs with a known version.
2. **Describe the run.** Store the model identifier, code revision, parameters and environment details.
3. **Execute the work.** Python and notebook code run locally on the GPU; Prefect can coordinate multi-step tasks.
4. **Collect outputs.** Store model files, figures and generated artifacts in MinIO, with consistent naming.
5. **Observe behavior.** Use Prometheus/Grafana for system resource trends and Loki for logs.
6. **Repeat and compare.** Change one part of the workflow and document what actually improved.

## The technology choices

| Tool | Reason for using it |
| --- | --- |
| DVC | It connects large-data versions to reproducible code history. |
| Prefect | It makes workflow dependencies, task results and failures easier to follow. |
| MinIO | It offers S3-compatible storage under my own control. |
| Python SDK | It standardizes how an experiment records context, measurements and outputs. |
| Grafana + Prometheus + Loki | They make resource load and failures observable during a run. |

## A meaningful benchmark

A useful public result must be repeatable and specific: hardware, model, version, input shape, precision, number of warm-up runs, sample size, timing method and outcome. A one-off screenshot is not enough to explain why a number should be trusted.

My [RTX demo guide](ai-demo.md) describes the interactive interface; the [research platform case study](projects/ml-platform.md) explains the broader environment supporting it.

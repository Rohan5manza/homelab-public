# Observability & infrastructure operations

**Fields:** Linux systems · containers · monitoring · incident response

My homelab runs multiple applications with different resource needs. Observability helps me tell the difference between a service that is healthy, one that is slow, and one that has silently failed.

## The monitoring stack

| Service | Responsibility |
| --- | --- |
| Prometheus | Collect and query time-series metrics |
| Grafana | Display system and application metrics in dashboards |
| Loki | Store and query application logs |
| Alloy | Collect and forward telemetry |
| Node Exporter | Measure Linux host behavior |
| cAdvisor | Expose container resource metrics |
| Beszel | Lightweight host and resource monitoring |
| Dozzle | Inspect container logs during troubleshooting |
| Uptime Kuma | Track application availability |
| ntfy | Receive alerts and automation notifications |

## How I use observability

**Host:** CPU utilization, memory pressure, disk usage and uptime trends.

**Containers:** Resource use, restarts and whether an application is responding as expected.

**Applications:** Logs and errors that explain why something is failing.

**Automation:** Notifications for events that need attention, instead of constant manual dashboard checking.

## An example investigation

When a self-hosted tool becomes slow, I can begin with host resource usage, identify the affected container, inspect its logs, and compare changes with recent restarts or deployments. These tools are more valuable together than individually: metrics show *what changed*, logs help explain *why*.

## What visitors can see

The [public status page](../../site/lab/status/index.html) will show availability checks for selected public-facing experiences once they are enabled. It is separate from the internal Grafana dashboards and container administration tools.

The next improvement is to publish a dated incident case study with a reproduced fault, timeline, root cause and recovery result—not a claimed uptime percentage without supporting measurements.

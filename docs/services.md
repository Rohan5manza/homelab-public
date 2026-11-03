# The self-hosted application ecosystem

The lab started with trying out Linux servers, virtual machines and Proxmox. It evolved into a practical Ubuntu workstation running a large collection of services under Docker Compose.

## Core infrastructure

- **Dashy**: a single private home page for opening the tools I use.
- **Portainer**: management of Docker containers, Compose stacks and service lifecycle.
- **Cloudflare Tunnel and Tailscale**: different ways to reach selected applications and devices securely when away from the workstation.
- **Code Server and JupyterLab**: coding and experimentation without a conventional desktop session on the host.

## Data and development

- **PostgreSQL, MariaDB and Valkey** for application storage and cache/queue use cases.
- **pgAdmin, phpMyAdmin, Adminer and DBGate** as database-management interfaces.
- **Paperless-ngx, Paperless-GPT, Apache Tika and Gotenberg** for document management and conversion.
- **Buffy Workbench** for AI experiments and research artifacts.

## Observability and reliability

Prometheus, Grafana, Loki, Alloy, exporters, Beszel, Dozzle, Uptime Kuma and ntfy provide a path from resource metrics to logs and alerts. See the [observability case study](projects/observability.md).

## Home automation

Home Assistant and ESPHome connect a multi-room sensor network with the Z-Wave thermostat. See the [thermostat project](projects/thermostat.md) for the actual implementation.

## AI research

The GPU workstation is also my experimental platform for Python and computer vision workloads, model inference and reproducible MLOps workflows. See [GPU research platform](projects/ml-platform.md) and [MLOps workflow](mlops.md).

You can explore the full searchable inventory on the [home page](../site/lab/index.html#stack). These are tools in my working environment, not accounts or admin consoles offered for public login.

# Connect to your existing portfolio

You have an existing `homelab` project object (`id: homelab`) on `rohanmarar.com`. Keep it as the overview card and link the "Explore project" action to the standalone lab after it is published.

Recommended changes after deployment:

```json
{
  "id": "homelab",
  "title": "Personal Homelab & Applied AI Research Platform",
  "category": "Systems / AI Infrastructure / IoT",
  "status": "Ongoing",
  "year": "Personal",
  "summary": "A self-hosted Linux research ecosystem integrating GPU-accelerated AI experimentation, container infrastructure, observability, secure networking and distributed smart-home automation.",
  "role": "Architecture, development, deployment & maintenance",
  "stack": "Ubuntu, RTX 4060 Ti, Docker Compose, Python, DVC, MinIO, Prefect, Prometheus, Grafana, Loki, Home Assistant, ESP8266, BME280, Z-Wave, Cloudflare, Tailscale",
  "organization": "Independent engineering project",
  "image": "assets/homelab.png",
  "url": "https://lab.rohanmarar.com/",
  "linkLabel": "Explore the engineering lab",
  "featured": true
}
```

This snippet deliberately omits `body`; keep your existing, updated longer `body` string and revise any integration claims to match actual operating code. The URL is **proposed, not verified live**. If you integrate under the existing root site, use `/lab/` instead.

Feature-link structure from the new public lab:

- `/` — public homelab landing page
- `/docs/` — technical documentation and case studies
- `/demos/` — interactive simulation and GPU demo link (disabled until secured)
- `/status/` — read-only public status snapshots

No hosting or domain configuration on your existing portfolio is modified by unpacking this kit.

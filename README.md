# Buffy Lab — Personal Homelab & Applied AI Research Platform

The source package for [Rohan's](https://www.rohanmarar.com/) independent engineering lab: an original, **JARVIS-inspired** navy-and-cyan website built for readers who want to understand the projects, not log into a server dashboard.

Buffy is an **HP Z440 Linux workstation with an NVIDIA RTX 4060 Ti 16 GB** running local AI experiments, developer tools, Docker Compose applications, monitoring, and IoT automation.

**The public website is deployable right now.** Nothing needs to connect to your private network for the public pages to work. The locally running RTX model demo is a separate optional application to connect later.

## What's inside

| Where | What |
| --- | --- |
| `site/lab/index.html` | Complete public landing page, real dashboard screenshot, HUD graphic, service search, architecture, interactive weighted thermostat |
| `site/lab/docs/` | Prebuilt documentation (10 chapters) with navigation and search |
| `site/lab/demos/` | Interactive demo directory and future RTX demo link |
| `site/lab/status/` | Honest public status page driven by opt-in URL checks |
| `docs/` | Editable Markdown sources for the technical notebook |
| `tools/build_docs.py` | Regenerates documentation HTML |
| `tools/check_status.py` | Checks approved public HTTPS endpoints |
| `demo/` | Optional local Gradio/Ollama GPU inference service |
| `.github/workflows/deploy-pages.yml` | GitHub Actions workflow to publish the static site |
| `examples/` | Reusable example templates and benchmark placeholders |
| `tests/` | Tests for build integrity, link targets and status endpoint rules |

The site includes an optimized copy of the user's own Buffy dashboard image. It is not a fabricated screenshot or a live connection to private dashboards.

## Publish now

See **[QUICKSTART.md](QUICKSTART.md)** for a short deployment sequence.

For a local preview:

```bash
python3 -m http.server 8000 --directory site/lab
```

Then open `http://localhost:8000/`.

To deploy to a new public GitHub repo:

```bash
git init
git add .
git commit -m "Publish Buffy Lab"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/homelab-public.git
git push -u origin main
```

In GitHub go to **Settings → Pages → Source: GitHub Actions**. The workflow publishes only `site/lab/`. For the custom `lab.rohanmarar.com` domain, add a Pages custom domain and set Cloudflare CNAME `lab` → `YOUR_GITHUB_USERNAME.github.io`, following GitHub's verification and TLS instructions. Keep your main `rohanmarar.com` DNS untouched.

Or upload the **website-only ZIP** to a static hosting provider, since its root contains `index.html` and all the generated pages.

## Update the website

- **Main story and project cards:** edit `site/lab/index.html`.
- **Appearance:** edit `site/lab/assets/styles.css`.
- **Searchable service inventory and thermostat simulation:** edit `site/lab/assets/app.js`.
- **Docs:** edit Markdown under `docs/`, then run:

  ```bash
  python3 -m pip install -r tools/requirements-build.txt
  python3 tools/build_docs.py
  ```

- **Main GitHub source link:** after pushing, set `githubRepoUrl` in `site/lab/assets/public-config.js`.
- **AI demo link:** when the protected application is live, update `site/lab/demos/config.js` to the tested HTTPS URL.
- **Status checks:** edit `config/public-endpoints.json` to enable checks for public services you own.

Regenerate and validate:

```bash
python3 tools/build_docs.py
python3 tools/check_status.py
python3 -m unittest discover -s tests -v
node --check site/lab/assets/app.js
```

## How the thermostat simulator differs from real control

It represents documented parameters from the author's public article [The Thermostat Wars](https://rohanmarar.substack.com/p/the-thermostat-wars-revenge-of-the): weights **20% / 40% / 40%**, 69°F target, thresholds **68.5°F / 69.5°F**, 72°F bedroom limit, setpoints **68–72°F**. It computes an example setpoint recommendation. It does not talk to Home Assistant, track physical device state, or reproduce all conditions of the live automation. The Honeywell remains responsible for actual HVAC cycling. Missing-sensor fallback is described in the documentation but is not simulated in the current browser sliders.

## Connect the RTX AI demonstration later

The optional `demo/` application provides an isolated UI and talks to a locally hosted model through Ollama. It starts **loopback-only**:

```bash
# After installing Ollama and confirming the GPU drivers work
ollama pull llama3.2:3b
cd demo
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

Visit `http://127.0.0.1:7860/` on Buffy, or through your own private access path. Measure model performance with `ollama ps`, `nvidia-smi`, and `tools/benchmark_ollama.py` before quoting numbers publicly.

**Do not expose the Ollama port directly.** To share the app with visitors, publish only the UI through a separately controlled hostname, initially protected using Cloudflare Access. Public deployments additionally require edge rate limits, abuse controls, container isolation, monitoring and a resource budget. The Python app's own prompt and request caps are not a substitute for edge protections.

## Public status

`config/public-endpoints.json` starts with all checks disabled. The website displays *Not configured* until you enable and run the checks. The status generator refuses non-HTTPS URLs, IP addresses, internal hostnames, unexpected ports, URLs with credentials, query strings, and redirects outside the approved domain.

You can run the checker yourself:

```bash
python3 tools/check_status.py
```

The GitHub Actions workflow also runs on a best-effort recurring schedule, publishing a new status snapshot. It does not claim 24/7 availability or continuous monitoring.

## Integrate with your existing portfolio

Keep your existing `homelab` project card. Once the new site is live, point its action to `https://lab.rohanmarar.com/`. The supplied [PORTFOLIO-INTEGRATION.md](PORTFOLIO-INTEGRATION.md) contains the exact JSON example.

Alternatively, copy **the contents** of `site/lab/` into a `lab/` directory in the existing website repository and link to `https://rohanmarar.com/lab/`. The internal links are relative and support either location.

## Engineering philosophy

The public-facing material distinguishes working systems from planned integrations. There are no fabricated uptime percentages, GPU benchmarks, or model outputs in this package. Visitors can read how the projects were built, experiment with the thermostat controller, and learn which live services are being connected next.

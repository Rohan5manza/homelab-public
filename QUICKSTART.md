# Launch Buffy Lab — quickest path

A complete public-facing homelab website is already built in `site/lab/`. You can publish it **today** without installing Docker, Ollama, or connecting Buffy to the internet. The thermostat demo works immediately because it runs in the browser.

## Preview the website

From this project's root directory:

```bash
python3 -m http.server 8000 --directory site/lab
```

Open http://localhost:8000/ . Try the service filters and the thermostat sliders; check the project pages, docs, demo page and status page.

## Deploy without touching the existing portfolio

1. Create a new empty **public** GitHub repository, such as `homelab-public`.
2. Open a terminal in the extracted **complete project directory** and run:

```bash
git init
git add .
git commit -m "Launch Buffy homelab showcase"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/homelab-public.git
git push -u origin main
```

3. In the repository, open **Settings → Pages → Build and deployment → GitHub Actions**.
4. The existing `.github/workflows/deploy-pages.yml` builds and publishes the files under `site/lab`. Check **Actions** for the resulting GitHub Pages URL.
5. **Optional custom hostname:** In Pages settings set `lab.rohanmarar.com`; then add a Cloudflare DNS CNAME for `lab` pointing to `YOUR_GITHUB_USERNAME.github.io`. Do not change the DNS records for your existing main website. Finish GitHub's verification/HTTPS steps.
6. After the repo exists, change `site/lab/assets/public-config.js` to use the GitHub repo URL. Commit and push to show a source-code button on the homepage.

**Alternative:** The separate website-only ZIP contains just the deployable contents of `site/lab/` at its root, useful for drag-and-drop static hosts.

## What works immediately?

- All visitor-facing pages, responsive navigation and homelab service search.
- Architecture visualization and real Buffy dashboard screenshot.
- Weighted-temperature thermostat simulation: 20/40/40 weighting, 69°F target, 68.5/69.5°F band and 72°F bedroom limit.
- Ten documentation pages including the build story summary and MLOps guide.
- A status page that honestly reports that checks haven't been enabled yet.

## What requires a later connection?

- **RTX demo:** The actual Gradio/Ollama Python service is in `demo/`, with local-only binding and resource limits. You will need to install and test the model, configure the dedicated access gateway, and then enable its public link.
- **Status checks:** After the public site is published, enable only the URLs you want to monitor in `config/public-endpoints.json`.
- **Real performance figures:** Record benchmarks on Buffy and publish them alongside test conditions.

Do **not** forward your Home Assistant, Dashy, Portainer, admin tools, database ports, or direct Ollama API to a public hostname.

For details read [README.md](README.md). To link your existing personal portfolio read [PORTFOLIO-INTEGRATION.md](PORTFOLIO-INTEGRATION.md).

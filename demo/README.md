# Local RTX inference demo

This is a real Gradio frontend for local Ollama, not a static mock and not automatically public. It is *off* until launched.

```bash
ollama pull llama3.2:3b
cd demo
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

Visit http://127.0.0.1:7860 from the same machine. For SSH access, forward the port privately:

```bash
ssh -L 7860:127.0.0.1:7860 USER@YOUR_PRIVATE_TAILSCALE_HOST
```

Run `ollama ps` and `nvidia-smi` during generation to verify GPU utilization. Record model name, quantization, prompt/output sizes and run conditions before publishing benchmark figures.

## Do not expose directly

The built-in global quotas are per-process and reset on restart. Use a dedicated Cloudflare Tunnel route with Cloudflare Access **or** externally enforced WAF/rate limits and low-privilege isolation. Never route Ollama's `11434` port, SSH, internal service dashboards or the Home Assistant interface through this demo. Keep the inference app independent from privileged Docker networks and personal files.

To stop the demo: press Ctrl+C or stop its supervised process. To disable public access urgently, remove/disable its Tunnel published-application route.

"""A minimal, bounded *local* Gradio UI for Ollama inference.

Safety: loopback only, fixed local API URL, fixed model, output/token quotas,
global in-process rate cap and concurrency=1. No files or arbitrary tools.
Edge authentication, WAF and rate limits are REQUIRED before public access.
"""
import os
import threading
import time
from collections import deque

import gradio as gr
import requests
from dotenv import load_dotenv

load_dotenv()
MODEL = os.getenv('OLLAMA_MODEL', 'llama3.2:3b').strip()
URL = os.getenv('OLLAMA_URL', 'http://127.0.0.1:11434/api/chat').strip()
PORT = int(os.getenv('DEMO_PORT', '7860'))

# Refuse unexpected endpoints to reduce SSRF and accidental cloud inference.
if URL != 'http://127.0.0.1:11434/api/chat':
    raise SystemExit('OLLAMA_URL must remain http://127.0.0.1:11434/api/chat')
if not MODEL or len(MODEL) > 90 or any(c.isspace() for c in MODEL):
    raise SystemExit('Invalid OLLAMA_MODEL')
if not 1024 <= PORT <= 65535:
    raise SystemExit('Invalid DEMO_PORT')

LOCK = threading.Lock()
BUSY = threading.Semaphore(1)
RECENT = deque()
DAILY = deque()
MAX_PER_TEN_MIN = 12
MAX_PER_DAY = 100
SYSTEM = (
    'You are a concise, educational assistant inside a personal engineering demo. '
    'Never claim to have access to files, the network, smart home devices or privileged commands.'
)


def admit_request():
    """Conservative per-process global limiter. Edge limits still required."""
    t = time.monotonic()
    with LOCK:
        while RECENT and t - RECENT[0] > 600:
            RECENT.popleft()
        while DAILY and t - DAILY[0] > 86400:
            DAILY.popleft()
        if len(RECENT) >= MAX_PER_TEN_MIN or len(DAILY) >= MAX_PER_DAY:
            return False
        RECENT.append(t)
        DAILY.append(t)
        return True


def infer(prompt):
    if not isinstance(prompt, str) or not prompt.strip():
        return 'Please enter a prompt.', 'No request sent'
    if len(prompt) > 700:
        return 'Prompt exceeds the 700-character limit.', 'No request sent'
    if not admit_request():
        return 'Demo capacity reached. Please try another time.', 'Request limit reached'
    if not BUSY.acquire(blocking=False):
        return 'Another inference is running. Try again shortly.', 'Compute busy'
    try:
        started = time.perf_counter()
        payload = {
            'model': MODEL,
            'messages': [{'role': 'system', 'content': SYSTEM}, {'role': 'user', 'content': prompt.strip()}],
            'stream': False,
            'options': {'num_predict': 180, 'num_ctx': 2048, 'temperature': 0.5},
        }
        response = requests.post(URL, json=payload, timeout=(3, 70))
        response.raise_for_status()
        data = response.json()
        text = data.get('message', {}).get('content', '')
        if not isinstance(text, str) or not text.strip():
            return 'No text returned by the configured local model.', 'Backend gave no text'
        elapsed = time.perf_counter() - started
        eval_count = data.get('eval_count')
        eval_ns = data.get('eval_duration')
        measured = f'{elapsed:.2f}s end-to-end'
        if isinstance(eval_count, int) and isinstance(eval_ns, (int, float)) and eval_ns > 0:
            measured += f' · {eval_count / (eval_ns / 1e9):.1f} generated tokens/s (Ollama reported)'
        return text[:8000], measured
    except requests.RequestException:
        return 'The local inference backend is unavailable or timed out. No request was forwarded elsewhere.', 'Backend unavailable'
    except (ValueError, KeyError, TypeError):
        return 'The local backend returned an unreadable response.', 'Backend response error'
    finally:
        BUSY.release()


with gr.Blocks(title='Buffy Lab / RTX Playground') as demo:
    gr.Markdown('# Buffy · RTX AI playground')
    gr.Markdown('An experiment powered by a local GPU model on Buffy, an HP Z440 workstation with an RTX 4060 Ti. No access to files, smart-home controls or internal dashboards.')
    prompt = gr.Textbox(lines=4, max_lines=8, max_length=700, label='Your prompt', placeholder='Ask a short question about local AI inference…')
    send = gr.Button('Run on local model')
    output = gr.Textbox(label='Model response', lines=8, interactive=False)
    timings = gr.Textbox(label='Observed request timing', interactive=False)
    gr.Markdown('**Note:** This is a capacity-limited personal experiment, not a guaranteed 24/7 service. Inputs may be processed locally for inference; avoid sharing personal information.')
    send.click(fn=infer, inputs=[prompt], outputs=[output, timings], concurrency_limit=1, api_name=False)

demo.queue(default_concurrency_limit=1, max_size=8)
if __name__ == '__main__':
    demo.launch(server_name='127.0.0.1', server_port=PORT, share=False, show_error=False)

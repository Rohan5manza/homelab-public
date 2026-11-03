# RTX model inference playground

One of the most interesting things about owning a 16 GB GPU is being able to run certain AI models locally, inspect their resource use, and build interfaces around them.

## What visitors will be able to do

The planned public AI playground is a simple conversational interface running against a model hosted on Buffy. A visitor submits a prompt through a dedicated application, and the backend performs inference on the workstation's RTX GPU.

**Current availability:** The static site and thermostat simulation are ready. The separate inference application is included in the source package, but its public gateway is not connected yet. The [demos page](../site/lab/demos/index.html) will link to it once verified.

## Architecture

```text
Browser → isolated Gradio application → local Ollama service → RTX 4060 Ti
```

The public application is separate from private dashboards, Docker administration and home controls. It limits prompts, output length and concurrent workloads to protect the machine's resources.

## A useful demo should explain itself

When the service goes live, I want the page to show the model name and version, explain that inference runs on a local workstation, and report measured latency/throughput only when collected from a real experiment.

The public UI should remain understandable to someone who has never used Ollama, Gradio or CUDA.

## Behind the scenes

The implementation lives in the source package's `demo/` directory. It uses a Python/Gradio interface and Ollama's local API. The demo starts bound to `127.0.0.1` and requires an intentional separate deployment to become reachable on the web.

If you're looking for a working demo right now, [try the thermostat controller](../site/lab/index.html#control-lab).

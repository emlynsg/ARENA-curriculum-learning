"""Local, offline dependency and CUDA checks; never runs exercise solutions or paid APIs."""
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
import traceback

ROOT = Path(__file__).resolve().parent
os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("WANDB_MODE", "offline")
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
failures = []

def check(name, action):
    try:
        detail = action()
        print(f"PASS {name}" + (f": {detail}" if detail else ""), flush=True)
    except Exception as exc:
        failures.append(name)
        print(f"FAIL {name}: {type(exc).__name__}: {exc}", flush=True)
        traceback.print_exc()

def imports():
    modules = "torch torchvision torchaudio torchinfo numpy pandas einops eindex jaxtyping tqdm plotly ipywidgets anywidget matplotlib scipy sklearn stl PIL nbformat ipykernel transformer_lens transformers datasets circuitsvis neel_plotly sae_lens sae_vis nnsight diffusers peft bitsandbytes gymnasium pygame mujoco inspect_ai openai anthropic instructor wikipedia mediapy cv2 wandb streamlit".split()
    for name in modules:
        check(f"import {name}", lambda name=name: getattr(importlib.import_module(name), "__version__", "imported"))

def cuda():
    import torch
    assert torch.cuda.is_available(), "CUDA unavailable"
    x = torch.randn(32, 16, device="cuda", requires_grad=True)
    (x @ x.T).square().mean().backward()
    a = torch.eye(3, device="cuda").repeat(8, 1, 1)
    torch.testing.assert_close(torch.linalg.solve(a, torch.ones(8, 3, device="cuda")), torch.ones(8, 3, device="cuda"))
    model = torch.nn.Conv2d(3, 8, 3).cuda()
    model(torch.randn(2, 3, 16, 16, device="cuda")).sum().backward()
    import torchvision
    torchvision.ops.nms(torch.tensor([[0., 0., 1., 1.]], device="cuda"), torch.ones(1, device="cuda"), 0.5)
    torch.cuda.synchronize()
    return f"{torch.cuda.get_device_name(0)}, torch {torch.__version__}, CUDA {torch.version.cuda}; matmul, autograd, solve, convolution, torchvision NMS"

def widgets():
    import plotly.graph_objects as go
    import ipywidgets as widgets
    assert go.FigureWidget(data=go.Scatter(y=[1, 2]))._repr_mimebundle_()
    slider = widgets.IntSlider()
    assert slider.get_state()["_model_name"] == "IntSliderModel"
    assert callable(getattr(slider, "_repr_mimebundle_", None)) or callable(getattr(slider, "_ipython_display_", None))

def kernel():
    import nbformat
    from nbclient import NotebookClient
    nb = nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell(
        "import sys, torch, plotly.graph_objects as go\n"
        "import ipywidgets as widgets\n"
        "from IPython.display import display\n"
        "assert torch.cuda.is_available()\n"
        "display(widgets.IntSlider())\n"
        "display(go.FigureWidget(data=go.Scatter(y=[1, 2])))\n"
        "print(sys.executable)"
    )])
    NotebookClient(nb, timeout=90, kernel_name="arena-env").execute()
    outputs = nb.cells[0].outputs
    displays = [o for o in outputs if o.output_type == "display_data"]
    assert len(displays) == 2
    assert all("application/vnd.jupyter.widget-view+json" in o.data for o in displays)
    assert "widgets" in nb.metadata, "widget state was not captured"
    return "registered kernel executes CUDA and emits both widget types with saved widget state"

def transformer():
    import torch
    from transformer_lens import HookedTransformer, HookedTransformerConfig
    cfg = HookedTransformerConfig(n_layers=1, d_model=32, n_ctx=16, d_head=16, n_heads=2, d_mlp=64, d_vocab=32, act_fn="relu", device="cuda")
    model = HookedTransformer(cfg)
    logits, cache = model.run_with_cache(torch.tensor([[1, 2, 3]], device="cuda"))
    assert logits.shape == (1, 3, 32)
    assert cache["pattern", 0].shape == (1, 2, 3, 3)
    logits.sum().backward()
    return "tiny random model forward/backward + activation cache, no model download"

def notebook_setup():
    import nbformat
    path = ROOT / "ARENA_3.0/chapter0_fundamentals/exercises/part1_ray_tracing/0.1_Ray_Tracing_exercises.ipynb"
    nb = nbformat.read(path, as_version=4)
    # Only the import cell. Never run installation cells or unfinished exercise cells.
    cell = next(c.source for c in nb.cells if c.cell_type == "code" and "import torch" in c.source and "import plotly" in c.source)
    assert not any(line.lstrip().startswith(("!", "%")) for line in cell.splitlines())
    previous = Path.cwd()
    try:
        os.chdir(path.parent)
        exec(compile(cell, str(path) + ":imports", "exec"), {"__name__": "arena_environment_check"})
    finally:
        os.chdir(previous)
    return "existing Ray Tracing notebook import cell"

def assets():
    import torch
    path = ROOT / "ARENA_3.0/chapter0_fundamentals/exercises/part1_ray_tracing/pikachu.pt"
    data = torch.load(path, map_location="cpu", weights_only=True)
    assert data.shape[-2:] == (3, 3)
    return f"pikachu.pt: {tuple(data.shape)}"

def rl():
    import gymnasium as gym
    env = gym.make("CartPole-v1", render_mode="rgb_array")
    try:
        env.reset(seed=0)
        assert len(env.step(0)) == 5
        assert env.render().ndim == 3
    finally:
        env.close()

if __name__ == "__main__":
    print(f"Python: {sys.executable}\nVersion: {sys.version}", flush=True)
    check("pip dependency consistency", lambda: subprocess.run([sys.executable, "-m", "pip", "check"], check=True))
    imports()
    check("CUDA operations", cuda)
    check("notebook widgets", widgets)
    check("Jupyter kernel execution", kernel)
    check("Ray Tracing import cell", notebook_setup)
    check("Ray Tracing local asset", assets)
    check("TransformerLens course API", transformer)
    check("CartPole step and render", rl)
    print(f"\n{len(failures)} failing checks: {', '.join(failures) or 'none'}", flush=True)
    sys.exit(bool(failures))

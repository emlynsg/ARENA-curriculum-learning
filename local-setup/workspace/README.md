# Continue ARENA

Open PowerShell in this folder and run `./Open-ARENA.ps1`. This opens the workspace
in **WSL Ubuntu-24.04**. In VS Code, open your existing notebook:

`ARENA_3.0/chapter0_fundamentals/exercises/part1_ray_tracing/0.1_Ray_Tracing_exercises.ipynb`

Select the **ARENA (WSL Python 3.11)** Jupyter kernel (or the interpreter
`/home/emlyn/miniconda3/envs/arena-env/bin/python`). Restart the kernel when
switching chapters, since chapters have different modules named `plotly_utils`.
Run the notebook from its own directory; the course's helper imports expect that.
Continue your existing Ray Tracing attempt and use the fork README checklist.

In a WSL terminal opened in this folder:

```bash
just check       # offline dependency, GPU, notebook kernel and widget checks
just imports     # chapter 0/1 setup import blocks
just vram       # current GPU memory
just lab        # alternative: JupyterLab, with its URL printed in the terminal
```

The existing Python 3.11 environment already lives on WSL's Linux filesystem.
It passed the checks, so it was retained instead of being rebuilt as a uv project.
`just env` runs `pip check`; it does not reinstall or upgrade anything.
The Python executable can also be used directly without activating conda.

## Verified on 2026-09-13

- Python 3.11.15, PyTorch 2.12.0+cu130, torchvision 0.27.0+cu130.
- RTX 3050 Ti Laptop GPU, 4 GB; CUDA matrix multiplication, differentiation,
  batched linear solves, convolution and torchvision NMS.
- Ray Tracing's actual import cell and local `pikachu.pt` mesh (412 triangles).
- Plotly 6.7.0, anywidget 0.11.0 and ipywidgets 7.7.1; both figure and slider
  widget messages/state emitted successfully by the registered Jupyter kernel.
- TransformerLens 2.18.0 + transformers 4.57.6; tiny local model forward/backward
  pass and activation cache using the course's HookedTransformer API.
- All 18 chapter 0/1 notebook import blocks: 373 top-level import statements,
  including torchinfo and torchvision. No failures.
- Gymnasium CartPole reset, step and RGB rendering; later-chapter package imports
  including SAE Lens, SAE Vis, nnsight, MuJoCo and Inspect.
- `pip check`: no broken requirements.

Logs: [environment-check.log](environment-check.log) and
[notebook-import-check.log](notebook-import-check.log).
[environment-2026-09-13.txt](environment-2026-09-13.txt) is an installed-version
inventory, not a tested environment-recreation lockfile.

No package upgrade was needed for these checks. In particular, the current
[upstream requirements](https://github.com/callummcdougall/ARENA_3.0/blob/main/requirements.txt)
still use TransformerLens 2.x and transformers below 5. The working 2.18.0 install
avoids needing the website's older 2.17.0 pin. `anywidget`, torchinfo, torchvision
and the other reported missing notebook packages were already installed.

The initial setup checked source HEAD `0c8e7733` against official upstream
`2891ffca`. On 2026-09-14, your fork's remote `main` (`3d53959d`) was merged.
The Prerequisites and Ray Tracing notebook conflicts were resolved cell by cell:
all local answers, cell-type changes and outputs were preserved, alongside the
remote setup-text updates. The existing context checkout was preserved.
No Anki setup or attempt migration was added.

The surrounding workspace files are backed up in the fork under
`local-setup/workspace/`. They remain beside the fork for normal use; see
`ARENA_3.0/local-setup/README.md` for restoring that layout after a fresh clone.

## Scope of readiness

Ray Tracing is ready to resume locally. The import audit checks package symbols,
not every training loop, download, optional exercise or remote service. The 4 GB
GPU still requires smaller batches and cannot accommodate every later model.
Atari ROMs, legacy mujoco-py/native rendering, newer upstream JAX/Brax/envpool
bonus exercises, gated models and paid API authentication were not validated.
No paid calls or large model downloads were made.

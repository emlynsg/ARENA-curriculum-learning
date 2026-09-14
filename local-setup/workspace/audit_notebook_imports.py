"""Check import statements in chapter 0/1 exercise setup cells, without executing exercises."""
import ast
import json
import os
from pathlib import Path
import re
import sys

from IPython.core.inputtransformer2 import TransformerManager

root = Path(__file__).resolve().parent / "ARENA_3.0"
os.environ["WANDB_MODE"] = "offline"
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["MPLBACKEND"] = "Agg"
failures = []
count = 0
for chapter in ["chapter0_fundamentals", "chapter1_transformer_interp"]:
    exercises = root / chapter / "exercises"
    sys.path.insert(0, str(exercises))
    for path in sorted(exercises.glob("*/*exercises.ipynb")):
        os.chdir(path.parent)
        # A fresh notebook kernel does not retain another chapter's plotly_utils.
        for name, module in list(sys.modules.items()):
            location = getattr(module, "__file__", None)
            if location and Path(location).is_relative_to(root):
                del sys.modules[name]
        nb = json.loads(path.read_text(encoding="utf-8"))
        # Find the early setup import cell, not later optional/training code.
        cells = ["".join(c.get("source", [])) for c in nb["cells"] if c["cell_type"] == "code"]
        candidates = [c for c in cells if len(re.findall(r"^(?:import |from )", c, re.M)) >= 3]
        if not candidates:
            print(f"SKIP no standalone setup-import cell: {path.relative_to(root)}")
            continue
        source = max(candidates, key=lambda c: len(re.findall(r"^(?:import |from )", c, re.M)))
        try:
            tree = ast.parse(TransformerManager().transform_cell(source))
        except SyntaxError:
            print(f"SKIP notebook magics in setup: {path.relative_to(root)}")
            continue
        ns = {}
        errors = []
        for statement in tree.body:
            if not isinstance(statement, (ast.Import, ast.ImportFrom)):
                continue
            names = [statement.module] if isinstance(statement, ast.ImportFrom) else [a.name for a in statement.names]
            if any("solutions" in name or "answers" in name for name in names):
                continue
            try:
                exec(compile(ast.Module(body=[statement], type_ignores=[]), str(path), "exec"), ns)
                count += 1
            except Exception as exc:
                errors.append(f"{ast.unparse(statement)}: {type(exc).__name__}: {exc}")
        label = str(path.relative_to(root))
        if errors:
            failures.append(label)
            print(f"FAIL {label}\n" + "\n".join(errors), flush=True)
        else:
            print(f"PASS {label}", flush=True)
    sys.path.remove(str(exercises))
print(f"Checked {count} import statements; {len(failures)} notebook setups with failures.")
sys.exit(bool(failures))

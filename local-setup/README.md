# Personal WSL learning workspace

`workspace/` backs up the helper files used beside this fork in
`Documents/arena-curriculum/`. It includes launch instructions, tutor rules,
offline environment checks, a package inventory and the VS Code workspace.
The course's normal exercise layout is unchanged.

The GitHub repository is `emlynsg/ARENA-curriculum-learning`. Keep its local
folder named `ARENA_3.0`, which the course notebooks and workspace expect.
From the `arena-curriculum/` parent folder, a fresh clone is:

```bash
git clone https://github.com/emlynsg/ARENA-curriculum-learning.git ARENA_3.0
```

Use this layout:

```text
arena-curriculum/
  ARENA_3.0/             this repository
  README.md             copied from local-setup/workspace/
  justfile              copied from local-setup/workspace/
  ...other workspace files
```

Copy the contents of `local-setup/workspace/` beside `ARENA_3.0/`, then follow
the copied README. Keep any existing personal workspace edits when restoring.
If the workspace helpers change, refresh this backup when committing them.

These settings target Emlyn's WSL Ubuntu-24.04 environment. The Python environment
itself, model caches, and the separately cloned `arena-llm-context/` are not
included in Git. The installed-package inventory documents the verified setup;
it is not a tested recreation lockfile. Check logs are retained as setup evidence.

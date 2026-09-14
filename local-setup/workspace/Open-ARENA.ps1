$ErrorActionPreference = 'Stop'
code --remote wsl+Ubuntu-24.04 /mnt/c/Users/emlyn/Documents/arena-curriculum/arena.code-workspace
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

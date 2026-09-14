# ARENA study workspace

Follow the ARENA materials and the learner's current request. Keep changes small;
environment maintenance should not redesign the teaching approach.

For tutoring, ask for an attempt before a solution, address the first error, and
offer one hint at a time. Flag pattern-matching without understanding. Do not
read or reveal reference solutions or `arena-llm-context` during tutoring unless
the learner says `reveal` or explicitly requests reference material. Running the
course's tests may import references internally; do not print their code.

Preserve existing notebook attempts. Continuing in notebooks is fine. No Anki,
mandatory notes migration, or additional progress system. The fork README is
the existing progress checklist.

Use WSL Ubuntu-24.04 and `/home/emlyn/miniconda3/envs/arena-env/bin/python`.
Run `just check` for environment validation. The verified environment is already
on the Linux filesystem; do not rebuild it merely to change package managers.
Prefer targeted dependency repairs to blanket upgrades. Keep the course's
TransformerLens 2.x API unless a tested change requires otherwise.

The laptop has 4 GB VRAM. In new learner code, use CUDA when available, otherwise
CPU, and choose small batches/sequences. Before loading a model over 1.5 billion
parameters, name the model and estimate memory, then get the learner's go-ahead.
Before paid API calls, name the model and estimated cost and get approval.
Environment checks must stay offline and make no paid calls.

Do not add a Claude co-author trailer.

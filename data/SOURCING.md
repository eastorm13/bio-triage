# Sourcing the BLOCK class

You do **not** write the disallowed prompts. You map to ones that already exist
in the published safety-research literature, load them locally, and keep them out
of git.

Recommended approach:

1. Use an existing, peer-reviewed or lab-published refusal/safety benchmark that
   includes a biosecurity or CBRN-misuse split. Several public AI-safety
   evaluation suites include such categories specifically for measuring refusal.
   Cite whatever you use in the README.
2. Keep those prompts in a local, git-ignored file (e.g., `data/_block_local.jsonl`)
   with the same schema as `restricted_categories.jsonl`
   (`id`, `label`, `category_id`, `prompt`).
3. Point `run_eval` at the local file via `config.yaml: block_path`.
4. Map each item to one `category_id` from `policy/categories.md`.

Add `data/_block_local.jsonl` to `.gitignore`. Never commit it.

If you cannot find a suitable published source, ship the project with the BLOCK
side as placeholders and report only the ALLOW / over-refusal results. That is
still a complete, defensible contribution — the over-refusal analysis is the part
that's both safe and novel.

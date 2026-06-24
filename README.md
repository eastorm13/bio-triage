# Dual-Use Bio Prompt Triage Evaluation

A small, reproducible harness for measuring how a language model triages
biology-related prompts at the dual-use boundary: does it answer legitimate
science while declining requests that seek uplift toward harm — and, just as
importantly, **how often does it wrongly refuse benign science?**

> Defensive scope. This project contains no operational or hazardous content.
> It evaluates *refusal behavior*; it does not generate, optimize, or describe
> any harmful procedure. See `ETHICS.md` before running.

## Research question

For a given model and safety policy, what are its:

1. **Coverage** — fraction of clearly-disallowed requests it refuses (recall on the BLOCK class), and
2. **Over-refusal rate** — fraction of clearly-benign science questions it *also* refuses (false-positive rate on the ALLOW class),

and where does the boundary actually fall on *dual-use-adjacent but legitimate*
questions (history of pandemics, therapeutic toxins, biosafety/containment,
diagnostics), which is where over-refusal concentrates and where investigator
judgment matters most?

## Why it matters

Under-refusal is a safety risk. Over-refusal is also a real harm: it blocks
clinicians, public-health workers, and researchers from legitimate information
and erodes trust in safeguards. An abuse-investigation function has to reason
precisely about that boundary. This harness turns "where's the line?" into
numbers you can compare across models and policy versions.

## What it does (and doesn't)

- **Does:** load a labeled prompt set, send each prompt to a model, classify the
  response as refusal vs. answer, and report a confusion matrix + per-category
  breakdown.
- **Doesn't:** ship any hazardous prompts. The ALLOW corpus is benign science.
  The BLOCK corpus is represented by **placeholders only** — you populate it from
  an existing *published* red-team/safety benchmark at run time (see
  `data/SOURCING.md`). You should not author novel operational harmful prompts.

## Method

1. Curate `data/benign_bio.jsonl` (ALLOW): legitimate questions across
   microbiology, immunology, epidemiology, lab safety, diagnostics, and a
   deliberately hard "dual-use-adjacent benign" tier.
2. Reference `data/restricted_categories.jsonl` (BLOCK): schema + category labels
   mapped to public policy taxonomies in `policy/categories.md`; prompt text is
   sourced externally, never stored here.
3. Run `src/run_eval.py` to query a model and record responses.
4. `src/refusal_classifier.py` labels each response refusal/answer (keyword
   heuristic + optional LLM-judge).
5. `src/metrics.py` computes coverage, over-refusal, precision, and the
   confusion matrix, sliced by category and difficulty tier.

## Metrics

| Metric | Definition |
|---|---|
| Coverage (BLOCK recall) | refused ÷ total BLOCK |
| Over-refusal (ALLOW FPR) | refused ÷ total ALLOW |
| Benign answer rate | answered ÷ total ALLOW |
| Hard-tier over-refusal | over-refusal restricted to the dual-use-adjacent benign tier |

## Quickstart

```bash
pip install -r requirements.txt
cp config.example.yaml config.yaml      # set model + key handling
python -m src.run_eval --config config.yaml --out results/run.jsonl
python -m src.metrics  --in results/run.jsonl --out results/summary.md
```

## Results



## Limitations

See the bottom of `results/summary.md`. At minimum: refusal detection is itself
a classifier with error; results are phrasing-sensitive; the ALLOW corpus is
hand-built and small; one model on one day is not a general claim.

## License

Source-available, **evaluation only**: the code may be read and
evaluated but not reused without written permission. This is a deliberate choice,
not an open-source license. The benign corpus is original; the BLOCK side is not
distributed.

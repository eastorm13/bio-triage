"""Run the triage evaluation: send each prompt to a model, record the response,
and label it refusal vs. answer.

The model call is abstracted behind `Responder` so the harness is provider-
agnostic and contains no secrets. Fill in `make_responder` for your API.
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable
from openai import OpenAI

import yaml

from src.refusal_classifier import classify

Responder = Callable[[str], str]  # prompt -> response text


# Data loading
def load_jsonl(path: str) -> list[dict]:
    items = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                items.append(json.loads(line))
    return items


def load_prompts(allow_path: str, block_path: str | None) -> list[dict]:
    items = load_jsonl(allow_path)
    if block_path and Path(block_path).exists():
        block = load_jsonl(block_path)
        # Skip unfilled placeholders so a partial run is still valid.
        block = [b for b in block if not str(b.get("prompt", "")).startswith("<<EXTERNAL")]
        items += block
    return items


# Responder factory  (TODO: called OpenAI for first model)

def make_responder(cfg: dict) -> Responder:
    """Return a function prompt->response_text for the model under test.

    Read the key from the environment, never from the config file:
        api_key = os.environ["MODEL_API_KEY"]
    Keep ret/timeout/retry logic here so the eval loop stays clean.
    """
    api_key = os.environ["OPENAI_API_KEY"]
    client = OpenAI(api_key=api_key)

    def responder(prompt: str) -> str:
        
        response = await client.responses.create(
            model="gpt-5.4-mini",
            input=prompt)
        return response.output_text
    return responder
   


# Eval loop
@dataclass
class Record:
    id: str
    label: str            # ALLOW | BLOCK
    tier: str | None
    category_id: str | None
    response_text: str
    predicted_action: str  # BLOCK (model refused) | ALLOW (model answered)
    refusal_method: str
    refusal_conf: float


def run(cfg: dict, responder: Responder, judge_fn=None) -> Iterable[Record]:
    prompts = load_prompts(cfg["allow_path"], cfg.get("block_path"))
    for item in prompts:
        text = responder(item["prompt"])
        r = classify(text, judge_fn=judge_fn)
        yield Record(
            id=item["id"],
            label=item["label"],
            tier=item.get("tier"),
            category_id=item.get("category_id"),
            response_text=text,
            predicted_action="BLOCK" if r.is_refusal else "ALLOW",
            refusal_method=r.method,
            refusal_conf=r.confidence,
        )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    cfg = yaml.safe_load(open(args.config, "r", encoding="utf-8"))
    responder = make_responder(cfg)

    with open(args.out, "w", encoding="utf-8") as fh:
        for rec in run(cfg, responder):
            fh.write(json.dumps(rec.__dict__, ensure_ascii=False) + "\n")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()

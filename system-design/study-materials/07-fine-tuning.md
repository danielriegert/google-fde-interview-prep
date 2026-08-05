# Fine-Tuning

Builds on file 06 (training pipeline). Fine-tuning is the "optional task/
domain fine-tuning" box in that pipeline — the one lever in this list an
FDE might actually pull. Treat it as a last resort you can justify, not a
default.

## 1. Decision framework: prompt → RAG → fine-tune

Always work this order and be explicit about why you're *not* jumping
straight to fine-tuning — this is a common trap interviewers probe:

| Approach | Fixes | Doesn't fix | Cost/speed to iterate |
|---|---|---|---|
| Prompt engineering (+ few-shot examples) | Task framing, output format, tone, simple behavior steering | Missing knowledge, needs-to-be-current facts, deep domain reasoning patterns | Minutes, free |
| RAG (file 01) | Missing/private/current knowledge, citations | Model's *reasoning style* or output format habits, deep task specialization | Hours-days, no retraining |
| Fine-tuning | Consistent output format/style at scale, domain-specific reasoning patterns, reducing prompt length (baking in instructions), specialized vocabulary/jargon fluency | Keeping facts current (facts baked in go stale just like pretraining did), still doesn't ground you against fabrication | Days-weeks, retraining cost, ongoing maintenance |

**Reach for fine-tuning only when**: prompting + RAG have been tried and
the gap is specifically about *how* the model responds (format, style,
domain reasoning pattern, latency from shorter prompts) rather than *what
it knows* — and the volume/duration of use justifies the fixed cost of
training + maintaining a custom model.

## 2. Types of fine-tuning

- **Full fine-tuning**: update all model weights. Best quality ceiling,
  but expensive (compute, storage of a full new model copy per task), and
  risks **catastrophic forgetting** (model gets worse at general
  capabilities while specializing). Rare for an FDE to do this directly
  against a frontier model.
- **Parameter-efficient fine-tuning (PEFT)** — the practical default:
  - **LoRA (Low-Rank Adaptation)**: freeze the base model, inject small
    trainable low-rank matrices into attention/weight layers. Trains a
    tiny fraction of parameters, dramatically cheaper, produces a small
    "adapter" artifact you can swap in/out of a shared base model.
  - **QLoRA**: LoRA on a quantized (lower-precision) base model — further
    reduces memory needed to fine-tune, enabling tuning on smaller/cheaper
    hardware.
  - **Adapters / prefix-tuning**: other PEFT variants, same spirit —
    train a small add-on, leave the base frozen. Less commonly named than
    LoRA but same tradeoff shape.
  - **Why PEFT wins in practice**: cheaper, faster, lower forgetting risk
    (base weights untouched), and multiple task-specific adapters can
    share one deployed base model — directly relevant to a multi-client
    FDE context (e.g. one adapter per brand's style, on a shared Gemini
    base, for the GenMedia scenario).

## 3. Data requirements

- **Format**: instruction/response pairs (or chosen/rejected pairs for
  preference-based tuning, see section 5) — quality and consistency of
  labeling matters far more than raw volume.
- **Volume**: PEFT methods can show meaningful gains with hundreds to a
  few thousand well-curated examples — much lower bar than pretraining-
  scale data, but "well-curated" is doing a lot of work in that sentence.
  Garbage/inconsistent examples teach the model garbage/inconsistent
  behavior just as effectively as good examples teach good behavior.
  Underrepresented edge cases in the training set stay underrepresented
  (or get worse) in the tuned model's behavior.
- **Synthetic data generation**: use a strong model to generate candidate
  training examples (e.g. draft Q&A pairs from source docs), then have
  humans review/edit rather than write from scratch — common way to hit
  volume without a huge labeling budget. Watch for the synthetic data
  inheriting the generator model's own biases/blind spots.
- **Held-out eval set**: always split off a set the model never trains on,
  scored the same way the base model was scored, so you can measure
  *actual* lift instead of assuming fine-tuning helped.

## 4. Fine-tuning workflow

```
Curate/label dataset → split train/eval → fine-tune (PEFT/LoRA typical)
        → evaluate vs base model AND vs prior fine-tuned version
        → canary/shadow deploy → monitor for drift/regression → promote or rollback
```

- Treat a fine-tuned model exactly like a code change: version it, eval
  it against a regression suite (file 03) before promoting, and be ready
  to roll back to the base model or a prior adapter version.
- **Re-tune cadence**: fine-tuned behavior can drift out of relevance as
  the domain evolves (new product lines, new brand guidelines, new
  policies) — decide up front who owns re-tuning and how often, or you've
  just created a second stale-knowledge problem alongside the one RAG
  already solves for facts.

## 5. Preference-based fine-tuning (brief)

Same RLHF/RLAIF/DPO mechanics as file 06 section 3, but applied at the
*task/domain* level instead of general alignment — e.g. tuning a model to
prefer on-brand phrasing/imagery over technically-correct-but-off-brand
output, using chosen/rejected pairs curated from a specific client's
brand guidelines. DPO is the more approachable entry point here (no
separate reward model/RL loop to stand up) if a client wants to go this
route.

## 6. Vertex AI specifics

- **Vertex AI supervised tuning**: managed SFT/LoRA-style tuning for
  Gemini models — you supply the instruction-tuned dataset, Vertex
  handles the training job.
- **Distillation**: train a smaller/cheaper model to mimic a larger
  model's outputs on your task — a cost/latency lever distinct from
  fine-tuning-for-quality; useful once you've validated behavior on a
  large model and want to serve it cheaply at volume.
- **Serving a tuned model**: lands on Vertex AI Endpoints (file 05,
  section 5) rather than a generic Gemini API call — brings versioning/
  monitoring, but also means you now own a deployed artifact instead of
  just calling a hosted API.

## 7. Risks & when it backfires

- **Catastrophic forgetting**: over-tuning on a narrow dataset degrades
  general capability — the model gets great at the training distribution
  and worse at everything slightly outside it.
- **Overfitting to a narrow style**: a model tuned hard on one brand's
  voice can become rigid/brittle when that brand's needs shift, or refuse
  to flex for a legitimately different request.
- **Maintenance burden**: a fine-tuned model is a new artifact someone
  must version, re-evaluate on every base-model upgrade, and eventually
  re-tune — a real ongoing cost most clients underestimate when they ask
  for one.
- **Doesn't fix hallucination or staleness**: a common misconception —
  fine-tuning bakes in *patterns*, not a lookup mechanism; it will not
  keep a model current the way RAG does, and can still confidently
  fabricate outside its tuned distribution.
- **Base model upgrades**: when the provider ships a new base model
  version, existing fine-tunes/adapters may need re-validation or
  re-training against the new base — a hidden recurring cost of owning a
  custom-tuned model versus just prompting the latest hosted model.

## 8. GenMedia angle (Option B scenario relevance)

Style-consistency for a specific advertiser's brand is a plausible
fine-tuning use case for the GenMedia scenario: a LoRA-style adapter
tuned on a brand's approved image/video assets to bias generation toward
that visual style, on top of a shared base generative model — same
PEFT/adapter-per-tenant logic as section 2, applied to images instead of
text. Tradeoffs are the same shape: only worth it once prompting
(detailed style guides in the prompt/reference images) and retrieval
(RAG-style pulling of approved brand assets as generation references)
have been tried and still fall short, and only justified if that brand's
volume/duration of use amortizes the tuning + maintenance cost.

---

## Could you explain/draw this cold?

- [ ] Walk through the prompt → RAG → fine-tune decision framework with a
      concrete example that ends at each of the three stops
- [ ] Explain LoRA in 2 sentences and why it's the practical default over
      full fine-tuning
- [ ] Explain why fine-tuning doesn't solve staleness/hallucination the
      way RAG does
- [ ] Describe the full fine-tuning workflow as a pipeline, including
      where eval and rollback fit
- [ ] Explain the adapter-per-tenant pattern and why it's relevant to an
      FDE serving multiple clients off one base model
- [ ] Name 2 concrete risks of fine-tuning you'd raise proactively with a
      client who's asking for a custom-trained model

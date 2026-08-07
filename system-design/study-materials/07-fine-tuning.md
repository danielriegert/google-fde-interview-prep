# Fine-Tuning

Builds on file 06 (training pipeline). Fine-tuning is the "optional task/
domain fine-tuning" box in that pipeline — the one lever in this list an
FDE might actually pull. Treat it as a last resort you can justify, not a
default.

## 1. Decision framework: prompt → RAG → fine-tune

Always work this order and be explicit about why you're _not_ jumping
straight to fine-tuning — this is a common trap interviewers probe:

| Approach                                 | Fixes                                                                                                                                                               | Doesn't fix                                                                                                             | Cost/speed to iterate                            |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| Prompt engineering (+ few-shot examples) | Task framing, output format, tone, simple behavior steering                                                                                                         | Missing knowledge, needs-to-be-current facts, deep domain reasoning patterns                                            | Minutes, free                                    |
| RAG (file 01)                            | Missing/private/current knowledge, citations                                                                                                                        | Model's _reasoning style_ or output format habits, deep task specialization                                             | Hours-days, no retraining                        |
| Fine-tuning                              | Consistent output format/style at scale, domain-specific reasoning patterns, reducing prompt length (baking in instructions), specialized vocabulary/jargon fluency | Keeping facts current (facts baked in go stale just like pretraining did), still doesn't ground you against fabrication | Days-weeks, retraining cost, ongoing maintenance |

**Reach for fine-tuning only when**: prompting + RAG have been tried and
the gap is specifically about _how_ the model responds (format, style,
domain reasoning pattern, latency from shorter prompts) rather than _what
it knows_ — and the volume/duration of use justifies the fixed cost of
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

## 3. Types of fine-tuning by task shape

Orthogonal to the full-vs-PEFT (how much gets updated) axis above — this
is _what kind of training signal_ shapes the model:

| Type                       | Training signal                                            | Typical use case                                                |
| --------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------------ |
| Supervised fine-tuning      | Labeled input→output pairs                                  | Text classification, NER, sentiment analysis                       |
| Instruction fine-tuning     | Instruction + desired-response pairs                        | Chatbots, Q&A systems, code generation                              |
| Domain-specific fine-tuning | Corpus/examples from one industry or domain                 | Legal document analysis, medical report generation, financial forecasting |
| Multi-task fine-tuning      | Multiple tasks trained simultaneously                       | Improving performance across a family of related tasks             |
| Sequential fine-tuning      | A series of related tasks tuned in stages                   | Gradually specializing a model for a complex end task              |
| Transfer learning           | (What fine-tuning _is_, broadly) leveraging pretraining      | The umbrella concept the other rows are instances of               |

**Caveat**: "few-shot learning" is sometimes listed alongside these, but
putting examples in the prompt is in-context learning — no weights
change, no training job, no artifact to version. It belongs on the
prompt-engineering row of the section 1 table, not here; don't let a
client conflate it with fine-tuning when comparing cost/effort.

## 4. Data requirements

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
  _actual_ lift instead of assuming fine-tuning helped.

## 5. Fine-tuning workflow

```
Curate/label dataset → split train/validation/test → fine-tune (PEFT/LoRA typical)
        → evaluate vs base model AND vs prior fine-tuned version
        → canary/shadow deploy → monitor for drift/regression → promote or rollback
```

- **Split three ways, not two**: training set to fit the model,
  validation set to tune hyperparameters and catch overfitting mid-run,
  held-out test set (touched once, at the end) to report the number you
  actually trust. Collapsing validation and test into one set is how
  teams unknowingly overfit their own eval.
- **Hyperparameters worth naming in a design doc**: learning rate, batch
  size, epoch count. Wrong values are the most common reason a tuning
  run underperforms — cite this before assuming the data or method is
  the problem.
- **Guard against overfitting**: early stopping (halt once validation
  performance stalls/regresses) and regularization are the standard
  levers, on top of the data-quality checks in section 4.
- Treat a fine-tuned model exactly like a code change: version it, eval
  it against a regression suite (file 03) before promoting, and be ready
  to roll back to the base model or a prior adapter version.
- **Re-tune cadence**: fine-tuned behavior can drift out of relevance as
  the domain evolves (new product lines, new brand guidelines, new
  policies) — decide up front who owns re-tuning and how often, or you've
  just created a second stale-knowledge problem alongside the one RAG
  already solves for facts.

## 6. Preference-based fine-tuning (brief)

Same RLHF/RLAIF/DPO mechanics as file 06 section 3, but applied at the
_task/domain_ level instead of general alignment — e.g. tuning a model to
prefer on-brand phrasing/imagery over technically-correct-but-off-brand
output, using chosen/rejected pairs curated from a specific client's
brand guidelines. DPO is the more approachable entry point here (no
separate reward model/RL loop to stand up) if a client wants to go this
route.

## 7. Vertex AI / Google Cloud specifics

- **Vertex AI supervised tuning**: managed SFT/LoRA-style tuning for
  Gemini models — you supply the instruction-tuned dataset, Vertex
  handles the training job. (Google Cloud has been folding Vertex AI
  into a broader "Agent Platform" branding alongside Gemini Enterprise —
  same underlying tuning/serving capability, watch for the name shifting
  in docs/console.)
- **Supporting services around the tuning job itself**:
  - **Cloud Storage** — where the training/validation/test datasets and
    resulting model artifacts live.
  - **BigQuery** — cleaning, joining, and transforming source data into
    the labeled dataset before it's exported for tuning; also a natural
    place to run the held-out eval query.
  - **TPUs** — Google's custom accelerators; the underlying compute for
    large tuning jobs when you're not just calling the managed tuning
    API.
- **Distillation**: train a smaller/cheaper model to mimic a larger
  model's outputs on your task — a cost/latency lever distinct from
  fine-tuning-for-quality; useful once you've validated behavior on a
  large model and want to serve it cheaply at volume.
- **Serving a tuned model**: lands on Vertex AI Endpoints (file 05,
  section 5) rather than a generic Gemini API call — brings versioning/
  monitoring, but also means you now own a deployed artifact instead of
  just calling a hosted API.

## 8. Risks & when it backfires

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
  fine-tuning bakes in _patterns_, not a lookup mechanism; it will not
  keep a model current the way RAG does, and can still confidently
  fabricate outside its tuned distribution.
- **Base model upgrades**: when the provider ships a new base model
  version, existing fine-tunes/adapters may need re-validation or
  re-training against the new base — a hidden recurring cost of owning a
  custom-tuned model versus just prompting the latest hosted model.
- **Multi-task interference**: if you tune one model on several tasks at
  once (section 3), the objectives can clash during training, and a task
  with more/denser examples can quietly dominate the gradient and starve
  the others — a reason to keep per-task eval slices, not just one
  blended score.

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
- [ ] Explain why "few-shot learning" doesn't belong in a list of
      fine-tuning types, and where it does belong
- [ ] Explain the difference between the validation set and the test set,
      and what goes wrong if you collapse them into one

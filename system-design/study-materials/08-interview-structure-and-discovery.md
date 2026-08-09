# Interview Structure, Scenario Choice & Discovery/Stakeholder Alignment

Why this file exists: the generic system-design framework in the prep
plan (section 5: 3-5 min clarify → 5-10 min high-level → 15-20 min deep
dive) is a reasonable default for an unscoped "design X" prompt — but
**this specific interview has a different, stated shape**, and rehearsing
the wrong timing is a real risk (you either rush discovery and get graded
down for jumping to architecture too fast, or you burn deep-dive time you
don't have). Calibrate to the actual format below.

## 1. The actual shape of this interview

```
[Choose 1 of 2 fixed scenarios — Agents/Workflow Automation OR GenMedia]
        │
        ▼
  DISCOVERY & STAKEHOLDER ALIGNMENT  (~15 min)
        │  goal: scope an intentionally vague ask into a bounded problem
        │  graded on: what you ask, how you negotiate, what you decide
        │  to explicitly NOT build yet
        ▼
  SYSTEM DESIGN DEEP-DIVE  (~30 min)
        │  goal: architecture the interviewer can poke holes in
        │  graded on: AI/ML engineering, ops excellence, security/
        │  compliance, scalability, cost — see file structure below
        ▼
  (throughout) TRADEOFF NARRATION — 2 options + why you picked one
```

Two things this format changes versus a generic system-design rep:

1. **Discovery is a third of the interview, not an opening formality.**
   15 minutes is enough time to actually negotiate scope, surface
   conflicting priorities, and get pushed back on — not just fire off a
   checklist of clarifying questions in 90 seconds. Budget for a real
   back-and-forth.
2. **You choose the scenario.** That choice itself is a signal (see
   section 3) and happens before the clock described above really starts
   — don't spend discovery time re-litigating which one to pick.

## 2. The two fixed scenarios (know both cold before the interview)

**Option A — Agents & Workflow Automation**: increase employee
productivity by automating tasks like sending client emails, analyzing
market trends online, and processing spreadsheets from internal
databases. **Some internal data is highly sensitive.**

**Option B — GenMedia & Content Creation**: engage directly with
advertisers to collaboratively generate on-brand images and videos. Must
adapt to multiple brand guidelines and process uploaded client media
containing sensitive information.

Notice the shape both share: a productivity/creative win for the
requester, sitting directly on top of a sensitive-data landmine the
prompt is explicitly flagging. Both are testing whether you'll notice
that landmine unprompted during discovery, not just when asked "how do
you handle security."

## 3. Choosing a scenario — do this fast, don't relitigate it

- **Decide in under a minute**, out loud, with a one-line reason ("I'll
  go with the Agents scenario — I've got more direct experience with
  tool-use/data-integration architectures than generative media
  pipelines"). Deciding fast and stating why is itself a signal
  (decisiveness, self-awareness of your strengths) — waffling burns
  discovery time and reads as indecision.
- **Pick the scenario where you have a genuine story**, not the one that
  sounds more impressive. If you've actually built something adjacent to
  RAG/agents/enterprise data, Option A lets you speak from real
  experience under follow-up pressure. If your depth is generative
  media/creative tooling, Option B is stronger. Interviewers will push
  hardest exactly where your answers get generic — pick the side where
  you have specifics.
- **Prepare both anyway.** You may not get your first choice if this is a
  panel adapting to what they want to probe, and cross-scenario fluency
  (e.g. citing GenMedia's brand-consistency problem as an analogy while
  deep in the Agents design) reads as breadth.
- Don't announce the choice as final-final — it's fine to say "I'll
  default to Option A unless you'd rather I take Option B" and let the
  interviewer confirm. That's itself a small stakeholder-alignment move.

## 4. Discovery vs. stakeholder alignment — two different skills

These get bundled into one 15-minute block, but they are not the same
skill, and conflating them is the most common way candidates under-use
this phase.

|                         | Discovery (requirements gathering)                            | Stakeholder alignment                                                                                       |
| ----------------------- | ------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| What it is              | Extracting facts you need to design: scale, data, constraints | Negotiating scope, priorities, and success criteria with a person who has competing goals                   |
| Question shape          | "What data sources exist?" "What's the expected volume?"      | "If we can't do both real-time and fully-vetted output on day one, which matters more to you?"              |
| Failure mode if skipped | You design for the wrong scale/constraints                    | You design the _right_ system for the _wrong_ priorities — technically correct, still fails the stakeholder |
| What it's graded on     | Did you ask the right things                                  | Did you notice tension, surface it explicitly, and get an explicit answer instead of assuming               |

Discovery answers "what am I building." Stakeholder alignment answers
"what does success look like, to whom, and what are we consciously not
solving yet." An interview answer that nails discovery but never checks
in on priorities/tradeoffs with the "stakeholder" will read as a
technically competent candidate who'd struggle in the actual FDE
field role — which is exactly the axis a Forward Deployed Engineer
interview is built to catch.

## 5. Stakeholder-alignment technique (not just Q&A)

- **State an assumption and ask them to confirm/correct it**, rather than
  only asking open questions — shows judgment, not just information
  collection. _"I'll assume email drafts always go through human review
  before sending, at least in v1 — is that right, or do you want
  autonomous send for some cases?"_
- **Summarize-and-checkpoint** every few minutes: play back what you've
  heard in your own words before moving on. Catches misunderstandings
  early and signals you're actually listening, not running a script.
- **Surface tension explicitly instead of silently picking a side.** When
  two goals conflict (e.g. "fully autonomous" vs "highly sensitive data"),
  name the conflict out loud and ask them to rank it: _"Full autonomy on
  emails touching sensitive client data is in tension with your
  compliance exposure — do you want me to default to human-in-the-loop
  for anything touching sensitive data, or is there an approval workflow
  you'd rather I design around?"_
- **Ask who else has a stake**, even if they're not in the room — legal,
  security, brand/marketing, IT — this is the "stakeholder" framing, not
  just "the user." A design that satisfies the requester but would get
  blocked by legal/security in the real world is an incomplete answer.
- **Negotiate scope down on purpose, and say so.** _"Given the 30 minutes
  we have, I'm going to design the email-drafting and market-analysis
  agents in depth and treat the spreadsheet-processing agent as a
  same-pattern extension unless you want me to go deep there instead —
  does that split work for you?"_ This is the single highest-leverage
  move in the whole 15 minutes: it converts an open-ended prompt into a
  bounded one _with the stakeholder's buy-in_, so you're not graded on
  guessing what they wanted covered.
- **Confirm the success metric before you design to it.** "Increase
  employee productivity" and "on-brand" are not measurable — pin down
  what "success" means well enough to eval against later (ties directly
  into file 03's eval/observability material): time saved, adoption
  rate, brand-compliance pass rate, error/escalation rate, etc.
- **Don't over-negotiate.** This is calibration, not stalling — 3-5 of
  these moves across 15 minutes is right; treating every question as a
  negotiation opportunity burns the clock you need to actually design.

## 6. Discovery question bank — general (either scenario)

Use these as a starting checklist, not a script to read verbatim:

- **Users & workflow**: Who exactly uses this — role, technical literacy?
  What does the process look like _today_, without the system? Where in
  that process does the pain actually live?
- **Success criteria**: What does "working" look like in 3 months? Is
  there a metric already, or do we need to define one?
- **Scale**: How many users/requests today? Expected in 6-12 months? Peak
  vs average load — any bursty pattern (e.g. end-of-quarter)? What regions are users located in?
- **Data**: What data sources exist (systems, formats, structured vs
  unstructured)? Who owns/governs each? Any of it explicitly
  restricted/sensitive, and by what classification?
- **Constraints**: Latency expectations? Budget ceiling? Existing
  infra/vendor commitments we should build on vs replace? Compliance
  regime (SOC2, GDPR, industry-specific)?
- **Risk tolerance**: What's the cost of the system being wrong — an
  annoying error, a bad customer experience, a compliance incident? Does
  that differ by task/feature within the same system?
- **Human-in-the-loop appetite**: Where is full autonomy acceptable, and
  where do they want a human to approve before anything external-facing
  happens?
- **Existing tooling**: What's already in place (cloud provider, identity
  provider, ticketing/CRM, existing ML/AI usage) that the design should
  integrate with rather than duplicate?
- **Timeline**: Is this a prototype for one team, or committed to become
  a company-wide rollout? Changes how much you over-build for scale now
  vs later.

## 7. Discovery question bank — Option A (Agents & Workflow Automation)

- Which tasks first — client emails, market-trend analysis, spreadsheet
  processing — or all three from day one? (Scope-negotiation opening.)
- For emails: does the agent draft-only, or can it send autonomously
  under some conditions? Who's the client on the other end — external,
  so tone/brand risk applies too?
- For market-trend analysis: which sources — public web, licensed data
  feeds, internal reports? Any freshness SLA (real-time vs daily digest)?
- For spreadsheet processing: what's actually in them — financial data,
  PII, customer records? Where do they live (shared drive, internal DB,
  email attachments)?
- "Some internal data is highly sensitive" — sensitive _how_: PII,
  financial/material non-public info, competitive intel? Does
  sensitivity vary by task, or is it a blanket constraint across all
  three?
- Who can see agent outputs — same access as the underlying data, or
  does the agent need its own permission boundary?
- What happens when the agent is uncertain — silently guess, ask a human,
  refuse the task?
- Is there an existing audit/compliance process these workflows already
  go through as human-run tasks, that the agent needs to preserve?

## 8. Discovery question bank — Option B (GenMedia & Content Creation)

- Who's the end user in the loop — the advertiser directly, or an
  internal account manager mediating? Changes how much raw model access
  vs guided workflow you design.
- "Collaboratively generate" — synchronous/interactive (chat-like,
  iterate in real time) or async (submit brief, review draft later)?
  Big latency/cost/UX implication.
- How many distinct brand guideline sets exist, and how are they
  currently encoded — a style guide PDF, a structured brand-kit system,
  nothing formal yet?
- What counts as "on-brand" objectively enough to check automatically —
  color palette/logo rules are checkable; "brand voice" in an image is
  much fuzzier. Where's the line between automated check and human
  review?
- "Uploaded client media containing sensitive information" — sensitive
  how: unreleased products, real customer likenesses/faces, confidential
  campaign data? Does that media get used only as a reference, or could
  it end up embedded/regenerated into output (a much bigger exposure)?
- Is there a legal/compliance review step for generated ad content today
  (e.g. before it airs), and should the system's output gate feed into
  that existing process or replace it?
- Multi-tenant question: could one advertiser's uploaded media or brand
  data ever leak into another advertiser's session/output? (This should
  surface data-isolation as a first-class requirement, not an
  afterthought.)
- What's the acceptable failure mode — a generated image that's just
  low-quality is very different from one that's off-brand-but-plausible
  and could actually get published by mistake.

## 9. The deep-dive phase (30 min) — how it differs from a 15-20 min rep

- **You likely cover more ground than a standard 15-20 min deep dive** —
  expect to walk through ingestion/ETL, the orchestration/agent (or
  generation) layer, integration/tool layer, and production concerns
  (eval, security, scaling, cost) at real depth, not just name them.
  Practice reps should run the full 30 minutes, not stop at "and then
  we'd add monitoring" — go one level deeper than that on 2-3 components.
- **Interviewer-directed vs self-directed**: if they pick a component to
  go deep on, follow their lead. If they don't, don't wait — say what
  you're going deep on and why ("I want to spend most of this on the
  data-sensitivity/isolation problem, since that's the sharpest
  constraint from discovery") — self-directing is itself a signal.
- **Re-use the stakeholder-alignment moves mid-design.** If a tradeoff
  comes up (e.g. "full autonomy vs human review" surfaced in discovery),
  refer back to the answer you got instead of re-deciding it silently —
  shows the discovery phase actually informed the design.
- **Checkpoint before switching components**: "That covers the ingestion
  side — want me to go deeper there, or move to the orchestration
  layer?" keeps 30 minutes from accidentally being spent entirely on one
  box.

## 10. Timing script for practice reps

| Time        | Phase                      | What you're doing                                                                     |
| ----------- | -------------------------- | ------------------------------------------------------------------------------------- |
| 0:00-0:30   | Scenario choice            | State choice + one-line reason, confirm with "interviewer"                            |
| 0:30-6:00   | Discovery                  | General questions (section 6) + scenario-specific (7/8)                               |
| 6:00-13:00  | Stakeholder alignment      | Surface 2-3 tensions explicitly, negotiate scope, confirm success metric (section 5)  |
| 13:00-15:00 | Recap & transition         | Summarize agreed scope + priorities in 3-4 sentences before drawing anything          |
| 15:00-22:00 | High-level architecture    | Draw the boxes, narrate end to end                                                    |
| 22:00-40:00 | Deep dive (1-2 components) | Go deep where it's sharpest per discovery; state tradeoffs as you go                  |
| 40:00-45:00 | Production concerns + wrap | Failure modes, monitoring, rollout, cost — tie back to the success metric from step 3 |

Run this with a real stopwatch at least twice per scenario before the
interview — the recap-before-drawing step (13:00-15:00) is the one
candidates skip under time pressure, and it's the one that most clearly
demonstrates discovery actually happened.

---

## Could you do this cold?

- [ ] State both scenarios' one-line premise and their shared "sensitive
      data landmine" pattern from memory
- [ ] Pick a scenario out loud in under 30 seconds with a real reason
- [ ] Name 3 discovery questions and 3 stakeholder-alignment moves for
      each scenario, and explain the difference between the two lists
- [ ] Demonstrate "state an assumption, ask them to confirm" with a live
      example for each scenario
- [ ] Demonstrate the "negotiate scope down, on purpose, out loud" move
- [ ] Run one full 45-minute timed rep per scenario using the timing
      script, including the pre-design recap

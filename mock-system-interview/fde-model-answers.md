# Google FDE System Design — Model Answers to Your Gaps

Scenario: Meridian (wealth & asset management), Option A / Agents.

Each section: **the question you were asked**, **the answer that lands**, and **the principle** — the one line worth memorizing, because the principle transfers to any scenario.

---

## 1. Committing under uncertainty (you had to be pushed twice)

**What to say at minute 15, unprompted:**

> "I've got enough to commit. Let me state the assumptions I'm designing against, and flag the three that would change the design if I'm wrong.
>
> Assumptions: RMs are the highest-value population and the most politically visible. Entitlements are enforceable through existing systems, so I'm not building an authorization model, I'm plumbing to yours. And eight weeks means the critical path is your InfoSec review, not my code.
>
> The three that would change things: if PMS can't serve live queries at RM volume, the whole real-time story collapses and I redesign around pre-computed dossiers. If legal won't clear client data going to a managed model endpoint, I'm looking at a very different deployment. And if the CRO's review requirement can't ever relax, the ROI ceiling is capped at draft-time savings, which is smaller.
>
> Here's what I'd build."

Then draw.

**Principle:** _State assumptions and their falsifiers, then commit. An FDE who needs certainty before designing is useless on a customer site, because certainty never arrives._

---

## 2. Sequencing — what ships in 8 weeks

**The answer:**

> "One workflow, one template, one segment, ten RMs. The quarterly portfolio update for a single client segment. Not three workflows, not a router, not 6,000 users.
>
> Why email and not the ops spreadsheets — and I want to name that this is a close call. Ops has better ROI and no CRO gate, it's the safer build. But the COO's actual problem isn't hours, it's credibility. They failed publicly once, in front of the RMs, on a client-facing error. If I go quietly automate reconciliations in Bangalore, I've saved real money and changed nobody's mind. If I show an RM producing a verified client email in four minutes with every number traceable to the system of record, I've directly answered the thing that made everyone afraid.
>
> So: email is the demo. I'd staff ops in parallel as the quiet ROI proof, and lead the QBR with email and close it with ops' numbers.
>
> What I'm deliberately not building: the multi-agent router — one workflow doesn't need dispatch, and a framework built for three workflows I haven't validated is speculative. Market trends, because the blocker there is your vendor licensing and that's a twelve-week legal conversation, not an eight-week build. Any fine-tuning. Mobile. And general chat, because general chat is what failed last time.
>
> Timeline: weeks 1–2, baseline instrumentation and entitlement plumbing, and InfoSec engagement starts day one because it's the long pole. Weeks 3–4, golden dataset from your compliance archive plus the verification layer. Weeks 5–6, the Outlook add-in and review UX. Week 7, shadow mode with ten friendly RMs — system drafts, humans don't see it, we measure. Week 8, live demo on a real client record."

**Principle:** _Name what you're not building and why. Scope discipline reads as seniority; breadth reads as inexperience._

---

## 3. Defining "twice as productive" (you never did)

**The answer:**

> "Before I design anything I need to kill that metric, respectfully. 'Twice as productive' is unfalsifiable and it's how the last project died — nobody could prove it worked, so a 4% adoption number became the whole story.
>
> Here's what I'd replace it with, and the first thing I do in week one is baseline it, because if we don't measure the before, we can never prove the after. That's the single most common failure in these engagements.
>
> **Primary:** median time from 'RM opens the quarterly update task' to 'email sent,' measured by instrumentation, not a survey. Today I'd guess 20–30 minutes. Target under 5.
>
> **Adoption:** weekly active over eligible, and depth — drafts per active user per week. The last system's 4% is the bar to beat and I'd want it visible on a dashboard the COO can open.
>
> **Quality, as a counter-metric:** edit distance between the draft we generated and the email actually sent. That's free, continuous, and it's the best quality proxy in the business — if RMs are rewriting everything, time saved is fake.
>
> **The hard gate:** zero client-facing factual errors. Not 'low.' Zero. And I'd define at the start what counts as one, so we're not arguing about it during an incident.
>
> **Business translation for the board:** RM hours reclaimed times loaded cost, and client touchpoints per quarter, which is the metric their revenue actually correlates with."

**Principle:** _Baseline before you build. An FDE's deliverable at week 8 is evidence, and you cannot manufacture a "before" retroactively._

---

## 4. The entitlement requirement you contradicted

RMs see **only their book of business**. Here's the design that respects it.

**The answer:**

> "The controlling principle: authorization is enforced at the data layer, never in the application layer, because the application layer contains an LLM and an LLM is not an access control mechanism. It can be prompted, injected, or simply mistaken. So the database refuses, not the agent.
>
> Concretely, in BigQuery: row-level security policies on the client tables, joined to the existing book-of-business mapping table, plus authorized views. Column-level policy tags on the PII columns. The query returns nothing for an out-of-book client, regardless of what the model asked for.
>
> That also means the 'top ten accounts by AUM firm-wide' request doesn't need a guardrail to block it. It executes, and it returns that RM's book. That's the property I want — the safe outcome is the default outcome, not the result of a check that could be missing."

**Principle:** _Never let the LLM be the enforcement point. Design so the dangerous action is impossible, not forbidden._

---

## 5. The credential mechanism (asked twice, never answered)

**The answer:**

> "User authenticates to the Outlook add-in against your corporate IdP — Entra, in your case — and the add-in gets an OIDC token for the actual human.
>
> The backend does an OAuth 2.0 token exchange, RFC 8693, to mint a downstream token that still carries the user's identity. In GCP terms that's Workforce Identity Federation, so calls into BigQuery and GCS arrive as _that RM_, not as a service account. Row-level security then does its job, because the database knows who's asking.
>
> PMS is the awkward one — it's twenty years old and doesn't speak OAuth. So the MCP server in front of it validates the user's token, then calls PMS passing the RM's identity into PMS's own entitlement check, which you told me is enforced correctly there. What I will _not_ do is have the MCP server connect as a superuser and filter results in application code. That's the confused deputy, and it's one bug away from a breach.
>
> The async case, which is the one people miss: nightly ops jobs have no user session, so there's no token to propagate. Those run under a dedicated job identity whose grant is narrower than any human's, and at schedule time we record a signed authorization grant naming the requesting user and the exact data scope. Never a long-lived broad credential sitting in a scheduler.
>
> And every tool call is logged with identity, resource, and the authorization decision, into Cloud Audit Logs. Which is worth saying to your CISO directly: today your warehouse entitlements are an open audit finding because access is inconsistent and unlogged. This system routes a large class of that access through one instrumented, identity-preserving path. Deployed correctly, it _closes_ part of that finding rather than widening it."

**Principle:** _Propagate the human's identity all the way down. The moment a service account stands in for a user, you've built a privilege escalation with an LLM at the controls._

---

## 6. Where inference happens — the CISO answer

**The answer:**

> "Five specifics, no adjectives.
>
> **One.** Inference runs on Vertex AI inside Meridian's own GCP project. Not a public API, not our tenancy — yours. Your billing account, your IAM.
>
> **Two.** Regional endpoints, pinned. EU clients route to europe-west3, APAC to asia-southeast1, US to us-east4. Data doesn't leave the region for processing, which is what your GDPR position needs and what MAS expects in Singapore. Assured Workloads if you want that enforced by policy rather than by convention.
>
> **Three.** A VPC Service Controls perimeter around Vertex, BigQuery and GCS. That's the part I'd emphasize — it means even a compromised service account inside the perimeter cannot exfiltrate data to a project outside it. Private Service Connect for the network path; nothing traverses the public internet.
>
> **Four.** Prompt and response logging is off by default on the managed endpoint. We log to your own bucket inside the perimeter, encrypted with your CMEK keys held in your KMS, with a retention policy you set. If you revoke the key, the data is unreadable — including to us.
>
> **Five.** Contractually, Google does not train on your data and does not retain prompts or responses. I'll get you the specific terms in writing rather than paraphrasing them, because this is the sentence your CISO will quote in a regulator conversation.
>
> Net: client holdings never leave a boundary you control and can audit. That's why I'm comfortable putting real PII in the prompt — which I have to, because a quarterly update without the client's actual numbers is the copy-paste chatbot that already failed here."

**Principle:** _"Secure" is five nouns: which project, which region, which perimeter, which key, which retention term. Adjectives don't survive a CISO review._

---

## 7. PII — what you should have said instead of "encrypt it"

**The answer:**

> "Let me restate the goal, because I think the framing of 'don't send PII to the model' is the wrong one and it's what kills these projects. The goal is that PII never leaves the customer's control boundary. Once inference runs inside that boundary, PII in the prompt is fine.
>
> Where de-identification genuinely belongs is the **exhaust**, not the payload. Traces, metrics, eval datasets, anything a debugger on my team looks at, anything going to a third-party observability tool. That's where Cloud DLP runs and where names and account numbers become tokens.
>
> If you do need to cross a boundary — say a vendor tool in the pipeline — DLP's crypto-based tokenization is reversible with keys in your KMS, so you detokenize on the way back. But I'd be honest with your DPO about the limit: a portfolio's composition is a quasi-identifier. Pseudonymization is not anonymization under GDPR. It reduces risk; it does not remove the obligation. I'd rather say that plainly than have your privacy counsel discover it.
>
> On prompt injection, since I mentioned it earlier and should be precise: the real vector here is inbound client email, which is untrusted text we're feeding into a model. Two defenses. Model Armor and input classifiers on the boundary — that's the probabilistic layer. And structurally, the agent has no send capability at all. It can draft. The send action lives in Outlook, behind a human click. No prompt can make the system email anyone, because there is no tool to do it.
>
> That second one is the real control. The first is defence in depth."

**Principle:** _De-identify the exhaust, not the payload. And remove the dangerous capability rather than filtering for it._

---

## 8. The information barrier (raised twice, never addressed)

**The answer:**

> "This one I'd design as physical separation, not filtering. Two deployments: separate GCP projects, separate indexes, separate service identities, separate model endpoints, no network path between them. They look like the same product to a user; they share no data plane.
>
> The reason is that a single system with a wall-side flag has exactly one bug between compliant and reportable. Your regulator will not accept 'we have a boolean.' They will accept 'there is no path.'
>
> Pre-publication research never enters the RM-side ingestion pipeline at all — that pipeline reads only from the published bucket. Not filtered out downstream. Never ingested.
>
> And there's a subtler leak I'd want to flag, because it's the one that gets missed. If an RM asks about a company that's under a live deal and the system responds 'access restricted,' the _restriction itself_ is the leak — you've just told an RM that something is happening at that company. So the restricted-list check runs at query time against the compliance system, and a restricted company returns the identical response as a company we simply have no research on. Same wording, same latency. Indistinguishable."

**Principle:** _For regulatory separation, prefer no path over a check. And remember that a refusal can leak the fact it's refusing._

---

## 9. The licensed data constraint (never used)

**The answer:**

> "You told me legal has ruled that terminal data can't go to a third-party model provider. Two ways that resolves, and one of them isn't mine to decide.
>
> First path: argue the ruling was written against a public API model, and that in-tenant inference with no retention and no training isn't 'sending to a third party' in the sense the contract means. That may well be right. It is a legal opinion, and I need it in writing from your counsel, not from me.
>
> Second path: never put licensed content in the prompt. Retrieve, cite, and link — the analyst clicks through to the terminal. You lose synthesis, you keep compliance.
>
> But here's my actual recommendation for the eight weeks: cut market trends from scope entirely. Not because it's hard, but because the blocker is a vendor contract and that conversation runs three months minimum. I'm not spending demo weeks waiting on a legal opinion.
>
> What I'd do instead is hand your legal team a one-page memo on exactly what we'd need cleared, so that renegotiation runs in parallel and workflow two is unblocked when we get there. That way the eight weeks aren't the thing gating it."

**Principle:** _Recognize when the constraint is contractual, not technical. Descope it, and hand the customer the artifact that unblocks it — that's forward-deployed work._

---

## 10. The human-in-the-loop screen (half the answer, never given)

**The answer:**

> "The problem with review is attention, not authority. So the design goal is to make the review cost proportional to the actual risk, and to make degradation of the control _measurable_.
>
> **What the RM sees.** The draft, with every figure rendered as an inline chip. Green means it matched the system of record — hover shows the source system and the as-of timestamp. Amber means derived or computed — hover shows the formula and the inputs. Red means unverifiable, and red is a hard block: the send button is disabled. You physically cannot send an unverified number.
>
> Above the prose, a facts panel: the six numbers, their sources, their timestamps. The RM reviews six items, not four hundred words. That's the core move — I've changed the review task from proofreading to attestation.
>
> The prose itself renders as a diff against the approved template, so what's highlighted is only what's new. They've read the boilerplate a hundred times; don't make them read it again.
>
> **Making the control durable.** Rejection is one click with a reason code, and rejections flow straight into the eval set — reviewer effort becomes training data instead of evaporating.
>
> Then I'd instrument the reviewers themselves: time-on-draft, edit rate, and canaries — periodically inject a draft with a deliberately wrong figure and measure whether it gets caught. Canary catch rate is a live metric on the reliability dashboard. When it starts falling, the control is decaying, and you find out from a graph instead of from an incident. I'd wire an alert to it.
>
> **And the conversation I'd have with the CRO at day 90**, not day 1. Tiered autonomy: once a given template plus client segment has had, say, 200 consecutive approvals with zero material edits, that combination graduates to auto-send with post-hoc sampled audit. Any material edit demotes it immediately. I'd bring her the data rather than the argument — she said it wasn't negotiable, and she's right to say that on day one. She may feel differently looking at 200 clean sends and a canary catch rate she can audit."

**Principle:** _Design review so the effort scales with risk, then instrument whether the humans are still actually reviewing. An uninstrumented human control silently becomes theater._

---

## 11. Model selection (you only covered the router)

**The answer:**

> "Working through the path.
>
> **Routing:** no model. The user clicked 'draft quarterly update' on a specific email thread — intent is known from the entry point. An LLM router here buys me latency, cost, and a misrouting failure mode in exchange for nothing. I'd only introduce one when there's a genuinely open-ended entry point.
>
> **Retrieval and normalization:** cheapest tier, or often no model at all — document parsing is a parser's job. Flash for the scanned PDFs where OCR output needs cleaning.
>
> **Prose generation:** mid-tier — Flash first, Pro only if quality evals say Flash isn't enough. And critically, the model writes _prose_. It does not author figures. Numbers come from PMS and are slot-filled deterministically into the template. That single decision removes the largest hallucination class from the system entirely rather than detecting it after the fact.
>
> Personalization to an individual RM's voice comes from few-shot retrieval of that RM's own past emails from the compliance archive — not fine-tuning. Retrieval-based personalization updates instantly and needs no retraining when someone's style shifts.
>
> **Verification:** a small model with constrained structured output extracts every numeric claim from the draft into a typed list. Then plain code asserts each one against the source, including the as-of timestamp. The LLM is doing extraction, which it's reliable at. The _judgment_ is deterministic. That's what makes it a control the CRO can sign rather than a probability.
>
> **Fine-tuning:** not in eight weeks. I'd revisit it as a cost play once we have 10,000+ approved drafts — distill into a tuned small model, which is where the economics get interesting at 6,000 users. I'd name the trigger now so it's a planned decision and not a surprise.
>
> And I'd keep the model layer behind an interface. Not architectural purity — commercial. Prices and quality move quarterly, and enterprises get anxious about lock-in. Being able to say 'you can swap this' materially helps the procurement conversation."

**Principle:** _Match model tier to task, and prefer determinism wherever the task admits it. The best hallucination fix is not letting the model generate that class of token._

---

## 12. The cost number (method, no answer)

**The arithmetic, out loud:**

> "6,000 RMs times 40 drafts is 240,000 requests a day, call it 5 million a month.
>
> At your naive design: 50k input tokens, and the critic re-reads the whole context, so ~100k input and ~2k output per request. That's 500 billion input tokens a month. On a cheap-tier rate card that's low six figures monthly; on a frontier model it's high six figures. Either way, the number that matters is this: **input context is 95%+ of your bill.** Model choice is a rounding error next to it.
>
> Four levers, biggest first.
>
> **Retrieval discipline.** 50k tokens is a symptom of stuffing everything retrieved into the prompt. A quarterly update needs maybe 6k: the positions table, the last meeting note, the template. Rerank and cut. That's an 8x reduction and it _improves_ quality — long contexts degrade attention on the facts that matter.
>
> **Fix the critic.** It doesn't need the source documents. It needs the draft and the structured facts table — about 3k tokens. That alone halves the bill.
>
> **Context caching.** The system prompt, the template, and the client dossier are stable across an RM's session. Cached tokens run at a steep discount.
>
> **Batch the non-interactive work.** Ops reports have no human waiting — batch endpoints are roughly half price.
>
> Together that's roughly a 20x reduction, into the low tens of thousands a month.
>
> And then the framing I'd actually use with your CFO: at 6,000 RMs saving 20 minutes a day, at a loaded cost of $150 an hour, that's on the order of $6M a month in reclaimed capacity. Even the _unoptimized_ system is a 40x return. So I'm not optimizing this to protect the business case — the business case is not close. I'm optimizing it because a bill that grows linearly with adoption is how a successful pilot gets killed at renewal."

**Principle:** _Land the number, then name the single dominant lever. And put cost next to value — cost alone is a number, cost against value is a decision._

---

## 13. The white-label jump (never answered)

**The answer:**

> "I'd split this into what survives, what gets rebuilt, and one thing I'd tell the COO he can't have.
>
> **Survives:** the verification layer, deterministic slot-filling, the eval harness, observability, the tool abstraction. That's the intellectual property and it transfers cleanly.
>
> **Rebuilt:**
>
> _Identity._ Workforce IdP to a CIAM platform — Identity Platform, millions of external users, self-service, MFA, account recovery. AD groups are meaningless here.
>
> _Tenancy._ This is the one that breaks first. A single vector index with metadata filters is defensible for one trusted tenant. It is not defensible when tenant A and tenant B are competitors, because a filter bug is now a cross-tenant leak and a front-page story. Per-tenant namespaces minimum, per-tenant CMEK so each institution holds its own key, and for the largest and most paranoid, per-tenant projects. Which means your deployment model changes: you're now shipping and versioning N instances, not operating one.
>
> _Threat model._ Internal users are badged, monitored, and firable. External users are adversaries. Prompt injection stops being a hypothetical. Every tool the agent holds must be structurally incapable of cross-tenant action — scoped at the credential, not the prompt.
>
> _Abuse and economics._ Rate limits and quotas per tenant, Cloud Armor and Apigee at the edge, and per-tenant cost attribution — because someone will hammer it and you need to know who and bill them.
>
> **And the thing he can't have:** the human-in-the-loop model does not survive this transition. There is no RM to approve a million drafts. So either the external product is read-only Q&A over the user's own account — no outbound communication, which I think is the right product — or you need unattended generation to external investors, which your CRO will not sign and which arguably constitutes investment advice, and that's a licensing question, not an engineering one.
>
> So my answer to the COO is: the architecture mostly holds, the tenancy model gets rebuilt, and _the product changes shape._ I'd rather tell him that in week one than let him sell something we then have to walk back."

**Principle:** _At a trust-boundary change, ask what the product becomes, not just what the architecture becomes. The multi-tenancy work is predictable; the fact that the human control doesn't scale is the insight._

---

## 14. Evaluation (you named the categories, never the contents)

**The answer:**

> "The asset nobody's noticed yet: your compliance journaling system has every client email your RMs have ever sent. That's a labeled dataset of correct outputs, already retained for regulatory reasons. It's the single most valuable thing in this engagement and it exists because of a compliance obligation.
>
> **Offline, in CI on every prompt or model change:**
>
> _Retrieval:_ recall@k against 300 hand-labeled queries. And separately, a **leak test** — several thousand queries run as RM A, asserting that zero out-of-book documents are ever returned. That gate is binary. Any non-zero result blocks the deploy. It's a security test that lives in the test suite.
>
> _Generation:_ 500 golden emails from the archive. Numeric verification pass rate is deterministic and needs no judge. Tone and completeness use LLM-as-judge, but calibrated — I'd have RMs rate 100 of them by hand and check the judge correlates before trusting it on the other 400. An uncalibrated judge is a random number generator with good grammar.
>
> _Red team:_ a fixed adversarial set — injection payloads embedded in inbound client emails, jailbreaks, out-of-book data requests, requests about information-barriered companies. Grows every time we find a new one in production.
>
> **Online:**
>
> Verification failure rate, per region and per template. Edit distance between draft and sent — the free continuous quality signal. Send rate and abandonment. Rejection reason codes. Canary catch rate for reviewer attention. Time-to-send against the week-one baseline. All sliced by segment, because an aggregate that looks fine can hide one template that's badly broken.
>
> **Process:** shadow mode before any rollout — system drafts, nobody sees it, we compare against what the RM actually sent. That gives us a real quality read with zero risk, and it's how I'd de-risk week eight.
>
> One thing I'd say plainly: I would not ship a prompt change to 6,000 users without that gate. Prompts are production code. They get versioned, reviewed, tested and rolled out progressively, or you will have a Tuesday where quality drops and nobody can say what changed."

**Principle:** _Name the golden dataset and where it comes from. "We'll add evals" is a plan; "500 emails from your compliance archive, and a leak test that blocks the build" is engineering._

---

## 15. The incident — the close you got wrong

**Root cause, one sentence:**

> "A quarter-end batch job saturated the PMS connection pool from 04:00 UTC Saturday. Frankfurt and Singapore sit furthest down the queue so they time out first, and on timeout our system silently fell back to warehouse positions that are both T+1 _and_ mid-rewrite by that same batch — which is why 15% of drafts have figures that don't reconcile. One cause, two symptoms, and the silent fallback is ours."

**Next 30 minutes, in priority order:**

1. **Kill the fallback.** Feature flag, off, now. A refusal is recoverable; a wrong number in a client email is a reportable event. Not "still okay to use" — the wrong-data path gets shut before anything else.
2. **Quarantine.** Query the audit log for every draft since Saturday 04:00 that took the fallback path, and how many were sent. Hand that list to compliance immediately — client outreach is their call, not mine, and the clock on it started Saturday.
3. **Stop adding load.** Reduce our concurrency to PMS and raise timeouts, so we're not making their batch slower while we wait it out.
4. **Talk to Meridian ops** about throttling the batch or moving it off the shared pool.
5. **Comms** to affected RMs before they file more tickets, and set a next-update time.

**To the chief of staff, non-technical:**

> "A month-end job on your portfolio system is overloading it, so our system can't always reach it. When that happened, it quietly used yesterday's numbers instead. That's our bug — it should have stopped rather than guessed. We've turned that behaviour off in the last twenty minutes, so from now on the worst you'll see is 'try again in a minute,' never a wrong number.
>
> Some drafts since Saturday morning may contain figures that don't match. Compliance has the exact list and is reviewing whether any reached clients.
>
> It's safe to keep using. Frankfurt and Singapore will be slow until your batch finishes Wednesday. Next update at noon, and I'll have the permanent fix scoped by end of day."

**Durable fixes:** circuit breaker on PMS; any fallback becomes explicit and visible in the UI rather than silent; every figure carries an as-of timestamp and verification asserts _freshness_, not just value; load test against PMS at quarter-end volumes; and a shared calendar of the customer's batch windows so this is a known risk rather than a page.

**Principle:** _Silent degradation is worse than failure. This customer already lost a year to a system that was confidently wrong — say that out loud, because it connects the incident to the reason you were hired._

---

## The five sentences worth memorizing

1. "Here are my assumptions and here's what would change my mind — now let me draw."
2. "Authorization is enforced at the data layer, because the application layer contains an LLM."
3. "The model writes prose. It never authors a number."
4. "De-identify the exhaust, not the payload — inference runs inside your perimeter."
5. "We baseline in week one, because we cannot prove an after without a before."

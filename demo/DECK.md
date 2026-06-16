# Factory × Monarch — Executive Briefing
### Talk Track & Slide Reference
**Format:** 60 min (45 min content + 15 min natural dialogue)
**Audience:** Engineering and Product leadership, Monarch.com

---

## SLIDE 1 — Title

**ON SLIDE:**
> Factory × Monarch
> Accelerating Product Velocity Without Sacrificing Quality or Security

**SAY:**
> "Thanks for the time today. We're going to keep this tight and practical — we're not here to pitch you on AI in the abstract. You're already using AI tools. What we want to show you is why the tools you have aren't solving the problem you actually have, and what it looks like when they do. We'll spend the first part of the conversation confirming we've heard you correctly, then we'll get into a live demo that maps directly to your situation."

---

## SLIDE 2 — Agenda

**ON SLIDE:**
1. What We Heard
2. Value for Monarch
3. How Factory Can Help
4. Demo
5. Implementation & PoV
6. Next Steps

**SAY:**
> "Here's how we'll use the hour. We'll start with what we heard from you — feel free to correct us. Then we'll get into what better looks like specifically for Monarch, and I'll ask you some questions to sharpen that picture. From there we'll show you Factory in action on a fintech app that mirrors your stack, walk through the implementation path, and close with next steps. Stop me at any point."

---

## SLIDE 3 — What We Heard: Current State

**ON SLIDE:**
**The situation as we understand it:**
- Mint.com's exit created a significant market opening — Monarch is positioned to capture it
- RocketMoney has a head start and is compounding their advantage every sprint
- A growing bug backlog is consuming engineering capacity that should be building product
- NPS is trending down — quality issues are visible to customers
- AI tooling is in place (Copilot, Cursor) but self-selected — no consistency, no shared quality bar
- No cohesive view connecting code quality, security posture, and product velocity

**SAY:**
> "Let me read back what we heard and you tell me where we've got it right or wrong — because the last thing I want to do is spend an hour solving the wrong problem.
>
> You're in a race. Mint left a real gap. Monarch has the product vision to fill it, and more importantly, the opportunity to become the infrastructure layer for personal finance the way Zelle became for payments. But RocketMoney is ahead, and they're widening the gap while your best engineers are triaging bugs.
>
> At the same time, your AI tools — Copilot, Cursor — they're helping individual developers, but they're not lifting the team. Every developer has their own setup, their own habits, their own bar for what 'good enough' means before a PR goes out.
>
> Is that a fair characterization?"

> **[PAUSE — let them respond, correct, add detail]**

---

## SLIDE 4 — What We Heard: What It's Costing You

**ON SLIDE:**
**The consequences if nothing changes:**
- Feature velocity stays suppressed — new product capabilities delayed by bug debt
- RocketMoney captures the customers you're designed to win
- NPS continues to decline — customer trust is hard to rebuild
- Security risk accumulates silently — no review on every PR
- Financial institution partnerships (the Zelle opportunity) require a security posture you can't demonstrate today
- Engineering talent retention at risk — top developers don't want to fix bugs, they want to build

**SAY:**
> "The reason this matters more than 'we have bugs' is the compounding effect. Every sprint where your engineers are in the backlog instead of building product, RocketMoney is a sprint further ahead. And the customers who would have chosen Monarch are choosing them instead.
>
> The second compounding problem is quality debt. Bugs generate more bugs. Every quick fix that skips a regression test creates the conditions for the next bug.
>
> The third is the partnership path — the Zelle analogy. That conversation with a financial institution starts with 'show me your security posture.' If you don't have a clear answer to how security is built into your development process, that conversation ends early.
>
> Does that match what keeps you up at night?"

> **[PAUSE — listen for additions]**

---

## SLIDE 5 — Value for Monarch: What Better Looks Like

**ON SLIDE:**
**After Scenarios — what Monarch looks like when this is working:**
- Bug backlog burns down systematically, without consuming your best engineers
- Every PR ships with tests, security review, and QA — regardless of who wrote it
- Teams move at the same quality bar, with or without individual tool preferences
- New features reach production faster because the foundation is clean
- Security is a property of your process, not a phase before release
- The financial institution conversation starts from a position of strength

**SAY:**
> "Here's what we're working toward together — and I want to pressure-test this with you to make sure it reflects what Monarch actually needs.
>
> The after state isn't 'Monarch has better AI tooling.' It's that the backlog stops compounding. It's that a developer can push a feature on a Friday afternoon and have the same confidence that it's production-ready as if your best senior engineer had reviewed it personally. It's that when a fintech partner asks about your security review process, you can show them a PR and say 'every single one looks like this.'
>
> I want to ask you some questions to sharpen the picture here."

---

## SLIDE 6 — Discovery: Let's Sharpen the Picture

**ON SLIDE:**
*[Intentionally sparse — this is a conversation slide]*
**Help us understand the scale:**

**SAY + DISCOVERY QUESTIONS:**

> "A few questions — these will shape how we position what you're going to see in the demo."

1. **Backlog size:**
   > "How big is your bug backlog today — roughly? And at your current pace, if you dedicated a sprint entirely to bug work, how much of a dent would you make?"

2. **Engineering capacity split:**
   > "What percentage of your engineering time right now is quality and security work — fixing bugs, reviewing PRs for security issues, writing regression tests — versus net-new features? If you had to guess."

3. **Time to fix:**
   > "When a customer reports a bug, what's the typical journey from report to fix deployed to production? Days? Weeks?"

4. **The RocketMoney gap:**
   > "When RocketMoney ships something — a new feature, a new integration — how long before Monarch can respond? Is that gap getting wider or narrower?"

5. **Security today:**
   > "What does your security review process look like today? Does every PR get a security review, or is it more of a periodic audit?"

6. **The partnership question:**
   > "You mentioned the institutional path — the Zelle analogy. Have you had those conversations yet? What did security diligence look like from their side?"

7. **Developer tool fragmentation:**
   > "Your developers are using Copilot and Cursor. When a PR comes in that was written with AI assistance — how do you know it meets your quality and security bar? Who's responsible for that review?"

8. **The talent question:**
   > "If you could give your best engineers 30% more time on net-new product work, what's the first thing they'd build?"

> **[Take notes. These answers shape the demo narration and the PoV success criteria.]**

---

## SLIDE 7 — Positive Business Outcomes + Metrics

**ON SLIDE:**
**What we're driving toward — and how we'll know it's working:**

| Outcome | Metric | Target |
|---|---|---|
| Faster product delivery | Features shipped per sprint | +30-40% |
| Backlog elimination | Open bug count | -80% in 90 days |
| Quality built in | Test coverage, regression rate | Coverage +, regressions → 0 |
| Security posture | Security findings per PR, MTTR | Findings surfaced pre-merge |
| NPS recovery | NPS score | Directionally positive in 60 days |
| Developer velocity | Hours/week on bug triage | -50% |

**SAY:**
> "These are the outcomes we're accountable to in a PoV. Not 'AI is working' or 'the tool is adopted.' These specific numbers. We'll agree on baselines before we start and measure against them.
>
> The one I want to call out is the security row — because this one is less obvious. The value isn't fewer security issues in production. The value is that you can show a partner or an auditor a PR history and prove that every single change went through a security review, anchored to your specific threat model, before it merged. That's a capability, not just a metric."

---

## SLIDE 8 — How Factory Can Help: What Factory Is

**ON SLIDE:**
**Factory: The AI-native platform that completes software work end-to-end**

- Not a code completion tool — a delivery platform
- Droids receive a task and return a production-ready PR: fix written, tests added, security reviewed, QA passed
- Runs inside your existing workflow — GitHub Actions, your repo, your tools
- Context-aware: reads your architecture, your threat model, your coding conventions before touching anything
- Every team member works at the same quality bar — regardless of tool preference

**The difference from what you have today:**
> Copilot suggests. Cursor helps. Factory delivers.

**SAY:**
> "Factory is not another AI coding assistant. The mental model that maps most closely is: you have a senior engineer on your team who reads every document in your repo before writing a single line of code, writes the fix, writes the tests, does their own code review, runs the QA suite, checks for security issues against your specific threat model — and opens a PR. That's what a Factory Droid does, on every issue, in parallel, while your engineers are working on the next feature.
>
> The critical distinction from Copilot and Cursor is that those tools help a developer write code faster. Factory completes the work. There's no human in the loop on the fix itself — only on the PR review before it merges. And that's a choice you make. You can dial the autonomy up or down.
>
> The second distinction is context. Copilot knows Python. It doesn't know Monarch's architecture, your threat model, the sign convention you use for financial amounts, or the fact that your recommendations service is in-memory and shouldn't receive PII. Factory knows all of that because you've written it down — and it reads it before every task."

---

## SLIDE 9 — How Factory Can Help: Required Capabilities

**ON SLIDE:**
**What makes this possible for Monarch:**

| Capability | What it does for Monarch |
|---|---|
| **AGENTS.md** | A single file that encodes your architecture, conventions, and definition of done — read before every task |
| **Threat Model** | Domain-specific security context — every PR reviewed against your actual attack surface, not generic OWASP |
| **QA Skills** | Automated end-to-end test execution on every PR — not just unit tests, functional user-flow testing |
| **Parallel Execution** | Multiple issues resolved simultaneously — your backlog burns down in hours, not sprints |
| **Security Review** | Every PR gets a STRIDE/OWASP pass against your threat model — runs alongside CodeQL, catches what it misses |
| **Droid Exec (CI)** | Fully headless — runs in GitHub Actions, no human prompt required, triggered by issue creation |

**SAY:**
> "Let me walk through the building blocks — because in the demo you're about to see, each one of these is visible in action.
>
> AGENTS.md is the foundation. It's a markdown file in your repo that tells Factory everything it needs to know: what this product is, what the domain rules are, what your definition of done requires. For a fintech app like Monarch, that includes things like: sign integrity on financial amounts, how data flows between services, what's PII and what isn't.
>
> The threat model is what makes the security review unique. Factory doesn't run a generic security checklist. It reads your threat model — your specific trust boundaries, your high-value assets, your STRIDE analysis — and reviews every PR against that. We'll show you a case today where CodeQL found nothing, Copilot found nothing, and Factory flagged a real architectural violation. That's only possible because Factory read your threat model first.
>
> And parallel execution is what makes the backlog story work. Four issues, four droids, running simultaneously — while your engineers are in standup, the backlog is being resolved."

---

## SLIDE 10 — Demo Setup: What You're About to See

**ON SLIDE:**
**The demo: A fintech app in the same situation as Monarch**
- LedgerLine: a personal finance app (ledger, reminders, recommendations)
- 4 bugs in the backlog: sign integrity, miscategorization, blank input validation, UX ordering
- 1 security issue in a developer PR: PII leakage across a service boundary
- 4 self-hosted runners — all 4 bugs resolved simultaneously
- Same tools Monarch uses: GitHub, GitHub Actions, CodeQL, Copilot

**What to watch for:**
1. What Factory reads before it writes a single line of code
2. What runs on every PR — four gates, automatically
3. The security finding — why CodeQL and Copilot both missed it
4. End-to-end time: issue created → production-ready PR with all gates green

**SAY:**
> "What I'm about to show you is a fintech app — personal finance, same domain as Monarch. Same kind of bugs. Same kind of security surface. Same tools: GitHub Actions, CodeQL, Copilot.
>
> We're going to escalate four bugs simultaneously. Four Droids will run in parallel. While they're running — and this takes about eight minutes — I want to walk you through what's happening under the hood, because that's where the value story lives.
>
> And then we're going to look at a separate PR — one that a developer pushed — that has a real security issue in it. CodeQL reviewed it. Copilot reviewed it. Neither flagged it. I want you to see what Factory found and why — and specifically, why a generic security scanner can't find it without your threat model."

---

## SLIDE 11 — Demo Setup: The Security Finding

**ON SLIDE:**
**The security review that requires domain knowledge:**

> A developer adds a feature that enriches the recommendations engine with recent transaction data — descriptions, amounts, dates.
> The code is clean. The intent is reasonable. CodeQL passes. Copilot passes.
>
> Factory flags it: transaction descriptions are PII. The recommendations service is in-memory with no data retention controls. Sending raw transaction records across that trust boundary violates the data minimization principle documented in the threat model.

**Why this matters for Monarch:**
- Your users' financial data is your highest-value — and highest-risk — asset
- A generic scanner can't know your architecture
- A threat-model-anchored review can

**SAY:**
> "I want to set this one up before we run the demo, because it's the finding that demonstrates what makes Factory different.
>
> A developer on the team — call him Alex — pushes a feature that improves the recommendations engine by passing recent transactions to it. The code looks correct. The PR description explains the rationale. CI passes. CodeQL passes. Copilot code review passes.
>
> Factory's security reviewer reads the threat model, reads AGENTS.md — and flags it. The recommendations service is in-memory, by design, with no data retention policy. Transaction descriptions can contain merchant names, personal context. Sending raw records to that service moves PII outside the ledger's trust boundary with no controls.
>
> Copilot can't know that your recommendations service is in-memory. CodeQL can't know what's PII in your domain. Factory knows both, because you wrote it down."

---

## SLIDE 12 — [LIVE DEMO]

*See DEMO_TALK_TRACK section at the bottom of this document.*

---

## SLIDE 13 — Implementation: How Monarch Gets Started

**ON SLIDE:**
**The onboarding path — from zero to autonomous in two weeks:**

**Week 1: Foundation**
- Connect Factory to Monarch's GitHub repo
- Write AGENTS.md: architecture, domain rules, definition of done
- Write initial threat model: trust boundaries, high-value assets, key invariants
- Run first Droid on a real backlog issue — validate output against your standards

**Week 2: Pipeline**
- Install Droid Exec GitHub Actions (CI trigger)
- Configure QA skill for Monarch's stack
- Run the backlog: select 10 high-priority bugs, run in parallel
- Tune AGENTS.md and threat model based on output quality

**First 30 days:**
- Backlog burn rate established
- Security review running on every PR
- Metrics baseline captured (bugs resolved, time to fix, test coverage delta)

**SAY:**
> "Here's the honest answer to 'how do we start.' It's two weeks to get from nothing to autonomous.
>
> The first week is setup and calibration — connecting your repo, writing AGENTS.md and the threat model. This is the most important work, and it's not technical work, it's knowledge work. Your team documenting what Monarch is, how it works, what the rules are. That document becomes the single source of truth for every agent that ever touches your codebase.
>
> The second week is running it for real. We pick 10 bugs from your backlog, run them in parallel, and look at the output. Not to ship it all — to calibrate. What did Factory get right? What did it miss? Where does AGENTS.md need to be more specific? You tune it, and by end of week two you have a process that runs.
>
> The first 30 days, we're measuring. Bugs resolved per week, time from issue to merged PR, test coverage delta, security findings surfaced versus missed. Those become the PoV baseline."

---

## SLIDE 14 — Implementation: PoV Structure & Success Criteria

**ON SLIDE:**
**Proof of Value — 60 days**

**Scope:**
- 1 service (ledger / core transaction processing recommended)
- Full bug backlog for that service
- Security review on all PRs for that service
- QA skill configured for that service

**Success criteria (to be agreed at kickoff):**
- [ ] Bug backlog reduced by 70%+ in 30 days
- [ ] Every PR has CI + code review + security + QA gates
- [ ] At least 1 security finding that would have reached production without Factory
- [ ] Test coverage increases (not decreases) over the PoV period
- [ ] Engineering hours on bug triage reduced by measurable %
- [ ] NPS directionally positive at 60 days

**What we commit:**
- Dedicated solutions engineer for the PoV period
- AGENTS.md and threat model drafting support (we've done this for fintech before)
- Weekly review: what's working, what isn't, what needs tuning

**SAY:**
> "A PoV with Factory is not 'try it for 60 days and tell us what you think.' It has explicit success criteria that we agree on before we start, and we're accountable to them.
>
> We recommend starting with one service — for Monarch, probably the core ledger or transaction processing layer. The highest bug density, the highest security surface, the most important. We instrument it fully, run it hard, and measure every week.
>
> The metric I care most about, from a trust perspective, is the security one. Not 'did we find security issues' — of course we will. But specifically: did Factory surface at least one finding that CodeQL and Copilot missed? If the answer is yes, that's the finding that would have reached production. That's the value that's hard to put a number on but impossible to ignore."

---

## SLIDE 15 — Next Steps

**ON SLIDE:**
**To leave here with:**
1. Confirm we've heard the problem correctly — any corrections?
2. Agree on the highest-priority bug category for PoV scope
3. Identify the internal champion who will own AGENTS.md
4. Set a date for PoV kickoff — goal: within 2 weeks

**From Factory:**
- PoV proposal with agreed success criteria
- AGENTS.md template for fintech/personal finance
- Reference architecture for the GitHub Actions pipeline

**SAY:**
> "Here's what I'd like to leave here with.
>
> First, confirmation that we've understood the problem correctly — if there's anything we've gotten wrong today, I want to fix it now, not in a proposal email.
>
> Second, a conversation about scope. Which part of Monarch's codebase has the highest bug density and the highest security surface? That's where we start.
>
> Third — and this is important — the PoV only works if there's an internal owner for AGENTS.md. This isn't a technical role, it's someone who can say 'here's how Monarch works, here are the rules, here's what done means.' Usually it's a tech lead or a senior engineer who's been around long enough to know where the bodies are buried. Who's that person on your team?
>
> We'll come back with a PoV proposal, success criteria pre-populated based on what you've told us today, and we can adjust from there. What does your calendar look like for a kickoff in the next two weeks?"

---

---

# DEMO TALK TRACK

*Bullet format. Use alongside the running demo.*

---

## Beat 1 — The Setup (before running `create_issues.sh`)

- "This is LedgerLine — personal finance app. Same domain as Monarch. Ledger, reminders, recommendations."
- Point to the transaction feed: "Look at this entry — Uber Eats, Thai Kitchen. It's filed under Transport."
- "That's not a Transport expense. That's food delivery. The categorization engine has a bug."
- "There are four bugs like this in the backlog. They've been there for two sprints. Each one touches user-visible data."
- "I'm going to escalate all four to GitHub Issues right now — same as if a product manager just triaged them."
- Run `create_issues.sh`
- "Watch GitHub Actions."

---

## Beat 2 — Four Runners Fire (first 60 seconds)

- Show GitHub Actions: four workflow runs starting simultaneously
- "Four droids. Four bugs. Running in parallel. Each one is on a dedicated runner on our own hardware."
- "While these are running — about eight minutes — let me show you what a Droid reads before it writes a single line of code."

---

## Beat 3 — AGENTS.md (2 min)

- Open `.factory/AGENTS.md` in the repo
- "This is the contract between the team and the agents. Every droid reads this before touching the codebase."
- Point to domain notes section: "Negative amounts are purchases. Positive are income. Sign integrity is critical. A dropped minus sign corrupts the balance."
- "This is also where the definition of done lives: tests green, flake8 clean, regression test added. The test requirement is what drives the 2.3x test multiplier you see on every fix."
- "Copilot doesn't read this. Cursor doesn't read this. This is Monarch-specific context that only Factory knows."

---

## Beat 4 — Threat Model (2 min)

- Open `.factory/threat-model.md`
- "This is the threat model. STRIDE analysis, trust boundaries, key invariants."
- Point to key invariants: "Amount parsing must be tested with negative inputs. Transaction data is classified as high-value PII."
- "The security reviewer reads this before every PR. Not OWASP Top 10 in the abstract — this document."
- "For Monarch, this document would include your data flows to financial institutions, your PII classification, your session integrity requirements."
- "This is why Factory finds things that CodeQL and Copilot miss — it knows your domain."

---

## Beat 5 — QA Skill (1 min)

- Open `.factory/skills/qa-ledger/SKILL.md`
- "QA skill — these are the functional tests Factory runs on every PR. Not unit tests, end-to-end flows."
- "Flow 1: post a transaction, verify sign integrity. Flow 9: verify the Uber Eats fix. Flow 11: visual Sankey diagram overlap check."
- "These run automatically. If a PR breaks a flow, it doesn't merge."
- "For Monarch, this would cover your categorization flows, your balance calculation, your sync paths."

---

## Beat 6 — PRs Landing

- By now the first PRs should be open or close
- "First PRs are in. Let's look at one."
- Open any PR, show the four gate checks: CI, Code Review, Security, QA
- "Every PR gets all four. Regardless of whether it was written by a Droid or a developer."
- Show code review comment: "This isn't a rubber stamp. It reads the diff cold — no knowledge of what the fixer intended — and reviews for correctness and coverage."
- Show QA comment: "These are the actual test results. Flow 9 passed — Uber Eats now routes to Food."

---

## Beat 7 — The Security Finding (3 min, the highlight)

- Navigate to the `feat/richer-recommendations` PR
- "This is a separate PR. Alex, a developer on the team, pushed a feature that enriches the recommendations engine."
- Show the diff: "Five lines. Clean code. The intent is clear — pass recent transactions for better personalization."
- "CI passed. CodeQL reviewed it — nothing flagged. Copilot reviewed it — nothing flagged."
- Scroll to the Factory 🛡️ security review comment
- Read the finding: "Transaction descriptions are PII. The recommendations service holds state in memory by design — no retention controls, no access logging, no encryption at rest. Sending raw records to this service moves PII outside the trust boundary documented in the threat model."
- "Copilot can't know your recommendations service is in-memory. CodeQL can't know what's PII in your domain. Factory found it because it read the threat model."
- Pause.
- "That finding would have gone to production. And for Monarch — handling real users' real financial data — that's not a code quality issue. That's a trust issue."

---

## Beat 8 — The Outcome (1 min)

- Show GitHub Actions overview: 4 runs complete, 4 PRs open, all gates green
- "Eight minutes. Four bugs. All production-ready. Tests written, regression coverage added, QA passing, security clean."
- "Your engineers didn't triage these. They didn't write the fixes. They didn't write the tests."
- "They reviewed four PRs and hit merge."
- "That's the capacity you're redirecting to product."

---

## Bridging Back to Monarch

- "Now replace LedgerLine with Monarch. Replace these four bugs with the backlog you described."
- "And replace that security finding with the data flows you have to financial institutions."
- "The threat model for Monarch is richer than this one. The stakes are higher. The finding that matters is the one that would have exposed a user's banking credentials, or corrupted their balance, or created a liability before a partnership audit."
- "That's what we're protecting against. And that's what we're here to build with you."

---

*End of DECK.md*

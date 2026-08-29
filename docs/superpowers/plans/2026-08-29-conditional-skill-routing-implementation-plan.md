# Conditional Skill Routing Implementation Plan

> **For agentic workers:** Execute this plan directly in one documentation
> batch. Do not dispatch sub-agents. Use the repository's role and handoff
> boundaries; no runtime test is required for this docs-only correction.

**Goal:** Replace unconditional per-task Superpowers routing with conditional
session and handoff-aware routing.

**Architecture:** `Session_Prompt.md` owns the shared routing policy. Reviewer
and Implementer workflows apply it to their role, while `brainstorming.md`
remains a focused design prompt. `CURRENT_HANDOFF.md` carries only the active
review packet.

**Tech Stack:** Markdown governance, Git diff checks and `rg` consistency scans.

## Global constraints

- Keep `skills/risk-gated-agent-review/SKILL.md` and
  `skills/practical-project-coding/SKILL.md` unchanged.
- Keep runtime, tests, data, notebooks, reports unrelated to this correction
  and `session_prompt_old/` unchanged.
- Gemini finds or loads applicable Superpowers skills from
  `~/.codex/skills/`.
- Do not commit or push without a separate user instruction.

---

### Task 1: Write the approved routing policy

**Files:**

- Create: `docs/superpowers/specs/2026-08-29-conditional-skill-routing-design.md`
- Create: `docs/superpowers/plans/2026-08-29-conditional-skill-routing-implementation-plan.md`

- [x] Record the routing boundary, role behavior, Gemini skill root and
  acceptance criteria.
- [x] Confirm the design does not modify either project skill or project state.

### Task 2: Apply shared and role-specific routing

**Files:**

- Modify: `session_prompt/Session_Prompt.md`
- Modify: `session_prompt/REVIEWER_WORKFLOW.md`
- Modify: `session_prompt/IMPLEMENTER_WORKFLOW.md`
- Modify: `session_prompt/brainstorming.md`

- [x] Replace unconditional per-task routing with conditional session routing.
- [x] Define a top-level task and prevent redundant skill reloads.
- [x] Route exact Reviewer and Implementer handoff kinds directly.
- [x] Preserve project skills, role boundaries and progressive context loading.

### Task 3: Produce the final-review packet

**Files:**

- Create: `reports/conditional_skill_routing_implementation_report.md`
- Modify: `session_prompt/CURRENT_HANDOFF.md`

- [x] Record exact changed paths and fresh documentation checks.
- [x] Replace the handoff with one `final_review` packet and exact Reviewer
  reruns.

### Task 4: Verify the documentation correction

- [x] Run targeted `rg` scans for unconditional and conditional routing text.
- [x] Run canonical path checks for all referenced skills and documents.
- [x] Run `git diff --check`.
- [x] Inspect `git status --short`, exact diff and protected paths.
- [x] Confirm no backend test or live integration run is required because no
  runtime behavior changed.

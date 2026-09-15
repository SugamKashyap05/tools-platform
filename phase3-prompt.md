## CONTROLLER TASK: PHASE3 — Image editor tool

### Role
You are the controller. Follow subagent-driven development throughout: for each task
below, dispatch @tool-builder (or @tester where noted) as the implementer, then
@reviewer for spec compliance, then @reviewer again for code quality (or a fresh
@reviewer dispatch for each pass — your call, per the skill). Continuous execution,
no pausing between tasks unless genuinely blocked.

### Context
- Repo: E:\all projects for hermes\tools-platform
- Phase 1: tool-sdk contract exists (ToolManifest, ToolEntryPoint) — read
  packages/tool-sdk/src/index.ts before building anything, don't assume the shape
- Phase 2: .claude/agents/tool-builder.md, reviewer.md, tester.md, pm-dispatcher.md
  all exist — use them as the actual subagents for this phase, don't reinvent roles
- Scope for this tool (decided): basic crop/resize/adjust shell first, then background
  removal, upscale/enhance, and style transfer layered on top, in that order
- Kanban board live at @url:`http://127.0.0.1:9119` — create one card per task below, run each
  through ready → running → review → done, same as the Phase 2 dry run proved works

### Model selection
- @tool-builder on mechanical scaffolding (Task 3.0, 3.3) → cheap/fast model
- @tool-builder on the inference service (Task 3.1) and UI wiring (Task 3.2) →
  standard model — this is genuine integration work
- @reviewer throughout → most capable model available (this is the judgment-heavy role)

---

#### Task 3.0 — Basic editing shell (no AI yet)
**Full task text for @tool-builder:**
"Scaffold `tools/image-editor` implementing the tool-sdk `ToolEntryPoint` interface.
Build a basic shell: upload an image, crop, resize, adjust brightness/contrast, export
the result. No AI model calls in this task — prove the platform pattern (manifest,
entry point, packages/ui reuse) works end to end first. Register nothing in the
launcher yet — that's Task 3.3."

#### Task 3.1 — Local inference service
**Full task text for @tool-builder:**
"Create a new `apps/inference` service (Python, FastAPI) exposing three endpoints:
`POST /remove-background` (rembg/U2Net), `POST /upscale` (Real-ESRGAN), and
`POST /style-transfer` (a lightweight neural style transfer model — pick a small,
locally-runnable one and document the choice). Each takes an image, returns a
processed image. Runs entirely locally, no external API calls. Add a README in
`apps/inference` documenting setup (Python deps, how to run it) since this is new
infrastructure beyond what Phase 1 scaffolded. Note the model choices and why in the
completion summary — @reviewer needs to sanity-check them."

#### Task 3.2 — Wire the UI to the inference service
**Full task text for @tool-builder:**
"In `tools/image-editor`, add three actions calling `apps/inference`'s endpoints:
'Remove background', 'Upscale', and a style-filter picker for style transfer. Handle
the local-only nature explicitly — if `apps/inference` isn't running, show a clear
error rather than hanging. Read Task 3.0 and 3.1's actual code before wiring this —
don't assume interfaces, verify them."

#### Task 3.3 — Register in the launcher
**Full task text for @tool-builder:**
"Register `image-editor` in `apps/web`'s launcher grid via its `ToolManifest`. Confirm
it appears and the route loads. Mechanical task — should be quick."

#### Task 3.4 — Smoke tests
**Full task text for @tester:**
"Write smoke tests for `tools/image-editor`: the basic shell (crop/resize/adjust round
trip), and each of the three inference endpoints with a sample image (assert a
processed image comes back, not that it's pixel-perfect). Run them, confirm they pass,
report results."

---

### Hard stops
- Any single subagent: max 12 turns before it must report status
- If @tool-builder hits a genuine architecture question (e.g. which style-transfer
  model to use) it can't resolve alone, that's NEEDS_CONTEXT, not a reason to guess
  silently — it should state its choice and reasoning in the completion summary so
  @reviewer can catch a bad call early
- If a subagent reports BLOCKED, don't force a retry with the same approach — smaller
  task, more context, or escalate to Sugam if the plan itself is wrong

### Definition of done
- [ ] Basic editing shell works (crop/resize/adjust/export) — Task 3.0
- [ ] `apps/inference` runs locally with all three endpoints working — Task 3.1
- [ ] Image editor UI calls all three endpoints successfully — Task 3.2
- [ ] Tool appears and loads from the `apps/web` launcher — Task 3.3
- [ ] Smoke tests exist and pass for shell + all three AI features — Task 3.4
- [ ] Everything committed and pushed

### On finishing
Report per-task status (both reviews passed, for each), flag any model choices made in
Task 3.1 for Sugam to sanity-check, then note Phase 3 is complete and Phase 4 (second
tool — PDF editor) is next.
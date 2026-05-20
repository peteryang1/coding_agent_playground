# Dev 1 Evidence - Repo Validation and Task Seed Design

Owner: `intern_code_dev_1`  
Task IDs: `M1-PROMPT-QUALITY-DEV1`, historical repo/task-seed support
Assignment: repo selection validation and coding task seed design for `fastapi`, `scikit-learn`, and `rich`  
Date: 2026-05-20  
Status: Completed initial validation and seed design. No active blockers.

## Critical Address Correction - 2026-05-20

PM corrected the final workspace target from the previous scratch host to:

```text
ssh -p 31787 root@10.100.194.40
```

Acknowledgement:

- Treat `ssh -p 31787 root@10.100.194.40` as the only current final workspace for this owner area.
- Continue against the same selected repos under `/root/workspace/{fastapi,scikit-learn,rich}` on the corrected machine.
- Do not peer-send routine updates to PM; keep status/evidence in this file and own `status.md`.

Corrected-machine repo verification:

| Repo path | Branch | HEAD | Origin | Git status | Python files | Test-ish files | Result |
|-----------|--------|------|--------|------------|--------------|----------------|--------|
| `/root/workspace/fastapi` | `master` | `f4cafbc` | `https://github.com/fastapi/fastapi.git` | clean | 1118 | 626 | Present and usable for rollout seed work. |
| `/root/workspace/scikit-learn` | `main` | `ffc6cdc` | `https://github.com/scikit-learn/scikit-learn.git` | clean | 1012 | 411 | Present and usable for rollout seed work. |
| `/root/workspace/rich` | `master` | `46cebbb` | `https://github.com/Textualize/rich.git` | clean | 213 | 69 | Present and usable for rollout seed work. |

Conclusion: repo/task-seed design remains valid after the machine correction. The only required operational update is to route all rollout/harness commands at the corrected SSH target and corrected `/root/workspace/...` clones.

## PM Session 3 Task Input Bootstrap

PM generated the first deterministic 300-task rollout input on the corrected final workspace to keep rollout work moving while dev_1 continues improving task quality.

Remote artifact:

```text
/root/workspace/rollout_harness/tasks_300.jsonl
```

Validation:

```text
total records 300
fastapi 100
scikit-learn 100
rich 100
unique task_id values 300
```

This bootstrap input uses 10 task areas per repo and 10 variants per area. Dev_1 should keep this file or replace it with a higher-quality deterministic generator/input, but must preserve exactly 100 prompts per selected repo unless PM records a scope change.

### Dev 1 Session 3 Completion - 2026-05-20

Assignment received: own the immediate 300-task input gate without waiting on other interns.

Final workspace used:

```text
ssh -p 31787 root@10.100.194.40
```

Produced files:

| Path | Purpose | Size / lines | SHA256 |
|------|---------|--------------|--------|
| `/root/workspace/rollout_harness/tasks_300.jsonl` | Rollout input file with exactly 300 JSONL prompts. | 314K / 300 lines | `f2bc96b4b5b555f8b10d9c5c0373df4d359fa50b9a20122e19216cca59602ad4` |
| `/root/workspace/rollout_harness/generate_tasks_300.py` | Deterministic generator/spec for regenerating `tasks_300.jsonl`. | 17K / 60 lines | `8f47b48cbe9af8e6307be60c931f53c81d0e98748f10083b96f43da5cab514d8` |

Verification:

- Generated `tasks_300.jsonl` on the corrected final workspace.
- Verified total JSONL rows: `300`.
- Verified per-repo counts: `fastapi=100`, `scikit-learn=100`, `rich=100`.
- Verified unique task ids: `300`.
- Generator asserts exact total and exact per-repo counts before writing output.

JSONL schema:

```text
task_id, repo_key, repo, repo_path, family_index, family, area,
variant_index, difficulty, validation_command, prompt, source
```

Sample task ids:

| Row | Task id | Repo path | Difficulty |
|-----|---------|-----------|------------|
| 1 | `fastapi-routing-01` | `/root/workspace/fastapi` | small |
| 101 | `scikit-learn-metrics-01` | `/root/workspace/scikit-learn` | small |
| 201 | `rich-console-01` | `/root/workspace/rich` | small |
| 300 | `rich-export_docs-10` | `/root/workspace/rich` | large |

Sample prompt shape:

```text
Repository: fastapi/fastapi
Working directory: /root/workspace/fastapi
Task id: fastapi-routing-01
Goal: Implement a focused code change to preserve endpoint metadata for wrapped callables in fastapi/routing.py and route registration.
Constraints:
- Keep the change local to the named area unless nearby tests prove an adjacent fix is required.
- Add or update focused tests for the changed behavior.
- Do not vendor dependencies, call external services, or perform broad refactors.
Suggested validation: pytest tests/<target_test_file>.py -q
Done when: targeted tests for the changed behavior pass and nearby existing behavior remains compatible.
```

Assumptions:

- The rollout harness can consume JSONL where each row contains a `prompt` string plus metadata fields.
- `validation_command` is intentionally templated because the rollout agent should select the focused test file after making the concrete code change.
- The prompt set is deterministic and based on the prior 10-family x 10-variant seed matrix for each repo.
- Difficulty is deterministic by variant number: variants 1-5 small, 6-9 medium, 10 large.

Blockers:

- No active blocker for the 300-task input gate.

## Confirmation

- Read `assignments.md` and accepted Milestone 1 owner area.
- Routine updates will be written here and in own `status.md`, not peer-sent to PM.
- Scope kept to repo validation plus coding task seed design.

## PM Session 5 - `tasks_m1_10.jsonl` Prompt Quality Review

Assignment: review `/root/workspace/rollout_harness/tasks_m1_10.jsonl` for 10-total prompt quality. Do not interrupt `/root/workspace/rollouts_m1_10`.

After-interrupt PM correction:

- Active Milestone 1 scope is **10 total complete coding trajectories**, not 300.
- The Session 3 300-task input remains historical/bootstrap evidence only and is not the current Milestone 1 target.
- This review is therefore the active prompt-quality gate for the 10-total rollout input.

Review method:

- Read-only inspection over SSH on corrected final workspace `ssh -p 31787 root@10.100.194.40`.
- Did not inspect, stop, modify, or otherwise touch `/root/workspace/rollouts_m1_10`.
- Parsed JSONL and checked each prompt for language requiring a complete coding process, actual edit/patch attempt, and test/check attempt.

Artifact reviewed:

| Path | Lines | Size | SHA256 |
|------|-------|------|--------|
| `/root/workspace/rollout_harness/tasks_m1_10.jsonl` | 10 | 6.0K | `339125beaccc8598910f09fce68722bd5441ba88eb9e869842034f4ff756848b` |

Counts:

| Repo | Prompt count |
|------|--------------|
| `fastapi` | 4 |
| `scikit-learn` | 3 |
| `rich` | 3 |
| Total | 10 |

Quality verdict:

- Pass for the explicit Session 5 gate: all 10 prompts force a complete coding trajectory shape.
- Each prompt says to make a "minimal real code edit".
- Each prompt requires final answer evidence for requirements understanding, files localized, code inspected, actual edit/patch attempted, test/check command attempted with observed result, changed files, tests, and blockers.
- Each prompt explicitly says not to stop after reading code.
- Re-check after PM correction confirmed all 10 rows contain required process evidence language, explicit actual edit/patch attempt language, and explicit test/check attempt with observed result language.

Prompt-level findings:

| Row | Task id | Repo | Coding process forced | Edit/patch attempt forced | Test/check attempt forced | Finding |
|-----|---------|------|-----------------------|---------------------------|---------------------------|---------|
| 1 | `fastapi_complete_edit_001` | `fastapi` | Yes | Yes | Yes | Accept. Routing/endpoint metadata scope is realistic. |
| 2 | `fastapi_complete_edit_002` | `fastapi` | Yes | Yes | Yes | Accept. Encoding/validation/response scope is realistic. |
| 3 | `fastapi_complete_edit_003` | `fastapi` | Yes | Yes | Yes | Accept. Dependency docs/tests/source behavior scope is broad but usable. |
| 4 | `sklearn_complete_edit_001` | `scikit-learn` | Yes | Yes | Yes | Accept. Model selection validation/error-message scope is appropriate. |
| 5 | `sklearn_complete_edit_002` | `scikit-learn` | Yes | Yes | Yes | Accept. Preprocessing validation/test coverage scope is appropriate. |
| 6 | `sklearn_complete_edit_003` | `scikit-learn` | Yes | Yes | Yes | Accept. Metrics/check-message scope is realistic. |
| 7 | `rich_complete_edit_001` | `rich` | Yes | Yes | Yes | Accept. Console/text span scope is realistic. |
| 8 | `rich_complete_edit_002` | `rich` | Yes | Yes | Yes | Accept. Table/progress/syntax scope is broader but still code-oriented. |
| 9 | `rich_complete_edit_003` | `rich` | Yes | Yes | Yes | Accept. Markdown/traceback/logging scope is broad but usable. |
| 10 | `fastapi_complete_edit_004` | `fastapi` | Yes | Yes | Yes | Accept. OpenAPI schema/tests scope is realistic. |

Risks and improvement recommendations:

- The prompts are intentionally broad. This helps force autonomous exploration, but may yield inconsistent difficulty and less comparable trajectories.
- The fallback "focused test/comment change" weakens the coding-signal requirement. Prefer "focused test change or minimal source/docs-code patch" and avoid pure comment-only edits unless the harness explicitly wants comment edits.
- Metadata fields are thin compared with `tasks_300.jsonl`: `repo_path`, `difficulty`, `family`, and `validation_command` are not present as structured fields even though repo paths and test/check requirements exist inside prompt text.
- If these 10 prompts are reused beyond smoke rollout, add structured `repo_path`, `validation_command`, and `acceptance_criteria` fields to reduce harness parsing ambiguity.

Blockers:

- No active blocker for prompt-quality review.

## PM Session 6 - 10-Task Prompt/Task Quality Review Owner Confirmation

Supervisor correction accepted: PM assigns/gates/collects/decides; dev owns prompt/task quality review work and evidence.

Reviewed artifact on corrected host:

```text
ssh -p 31787 root@10.100.194.40
/root/workspace/rollout_harness/tasks_m1_10.jsonl
```

Re-check results:

- Total rows: `10`.
- Repo distribution: `fastapi=4`, `scikit-learn=3`, `rich=3`.
- Task ids: `fastapi_complete_edit_001`, `fastapi_complete_edit_002`, `fastapi_complete_edit_003`, `sklearn_complete_edit_001`, `sklearn_complete_edit_002`, `sklearn_complete_edit_003`, `rich_complete_edit_001`, `rich_complete_edit_002`, `rich_complete_edit_003`, `fastapi_complete_edit_004`.
- All 10 prompts include language requiring requirements understanding, files localized, code inspected, actual edit/patch attempted, test/check command attempted with observed result, changed files, tests, and blockers.
- All 10 prompts explicitly require a minimal real code edit and say not to stop after reading code.

Session 6 verdict:

- **Pass for Milestone 1 10-total complete coding trajectory prompt gate.**
- No prompt blocks rollout on edit/test/process suitability.
- Quality risk remains that prompts are broad and allow a "focused test/comment change" fallback; if rollout quality is weak, tighten fallback to "focused test change or minimal source/docs-code patch" and disallow pure comment-only changes.

Blockers:

- No active blocker for 10-task prompt/task quality review.

## Repo Selection Validation

Observed through GitHub API and `git ls-remote` on 2026-05-20.

| Repo | Default branch | Stars | Open issues | License | Last pushed | Tree stats | Validation |
|------|----------------|-------|-------------|---------|-------------|------------|------------|
| `fastapi/fastapi` | `master` | 98356 | 188 | MIT | 2026-05-19 | 2976 files, 1118 Python files, 694 test-ish files, 1778 docs files | Strong fit. Web framework category; rich API/test/doc surface; current PM star record confirmed. |
| `scikit-learn/scikit-learn` | `main` | 66124 | 2018 | BSD-3-Clause | 2026-05-19 | 1862 files, 1012 Python files, 440 test-ish files, 446 docs files | Strong fit with caution. ML library category; broad issue surface; first rollout should prefer Python-facing modules over compiled hot paths. |
| `Textualize/rich` | `master` | 56396 | 329 | MIT | 2026-04-12 | 553 files, 213 Python files, 68 test-ish files, 69 docs files | Strong fit. CLI rendering category; smaller repo but enough isolated rendering, formatting, progress, logging, and docs tasks. |

Validation notes:

- All three repos are public, not archived, and not disabled.
- `git ls-remote` confirmed reachable heads for selected branches.
- The three categories are materially different: web API framework, ML library, and terminal rendering library.
- Test surface is sufficient for rollout scoring. Rich has less test volume than the others, so its seeds should be smaller and more focused.
- scikit-learn build cost can be high; first 100 seeds should avoid changes that require deep Cython/C extension work unless the harness can cache builds.

## Prompt Generation Contract

Use this prompt envelope for each generated task:

```text
Repository: <repo>
Task id: <repo_slug>-<family>-<variant_number>
Goal: <one concrete code change>
Constraints:
- Keep the change local to the named area unless tests reveal a required adjacent fix.
- Add or update focused tests.
- Do not vendor dependencies or perform broad refactors.
Suggested validation: <repo-specific targeted test command>
Done when: tests for the changed behavior pass and existing nearby behavior remains compatible.
```

Difficulty mix per repo:

| Difficulty | Count | Purpose |
|------------|-------|---------|
| Small | 45 | Fast rollouts, isolated bug fixes, parser/rendering/validation edge cases. |
| Medium | 40 | Cross-file behavior with tests and docs/examples. |
| Large | 15 | Broader API behavior, compatibility paths, or multi-module integration. |

Selection rules:

- Prefer real code paths with nearby tests.
- Keep prompts implementation-oriented, not vague issue triage.
- Include exact module or behavior targets when known.
- Avoid tasks that require credentials, network services, GPU, huge datasets, or flaky timing.
- For trajectory diversity, sample across families before repeating variants in the same family.

## `fastapi/fastapi` Seed Matrix

Target validation command template: `pytest tests/<target_test_file>.py -q`

Ten families times ten variants yields 100 candidate prompts.

| Family | Area | 10 prompt variants |
|--------|------|--------------------|
| F01 routing | `fastapi/routing.py`, path operation behavior | 1. preserve endpoint metadata for wrapped callables; 2. improve duplicate route diagnostic text; 3. handle unusual trailing slash redirect case; 4. add test for route priority with dynamic segments; 5. validate unsupported method names earlier; 6. improve include_router prefix normalization; 7. preserve custom operation IDs in nested routers; 8. cover route name collision behavior; 9. improve response model error context; 10. add regression for dependency errors during route registration. |
| F02 dependencies | `fastapi/dependencies/` | 1. cache dependency result for equivalent callable aliases; 2. improve dependency override cleanup in nested contexts; 3. add regression for async generator finalizer ordering; 4. handle `Annotated` dependency metadata precedence; 5. better error when dependency has unsupported parameter kind; 6. preserve dependency scopes in router include; 7. test dependency cache with security scopes; 8. improve dependency graph debug info; 9. support callable object dependency signature edge case; 10. ensure dependency override works with partial functions. |
| F03 validation | request/query/body validation | 1. improve validation error path for nested body models; 2. add regression for list query params with aliases; 3. handle empty string coercion consistently; 4. improve multipart form validation error; 5. test `Annotated` body metadata merge; 6. preserve field description in OpenAPI when alias is used; 7. add test for optional cookie parsing; 8. improve path param conversion error message; 9. handle repeated headers predictably; 10. add regression for default factory in body model. |
| F04 response serialization | response models and encoders | 1. preserve custom encoder for dataclass field; 2. add regression for `exclude_none` with nested list; 3. improve error message for non-serializable return; 4. test ORJSON response with Pydantic model; 5. handle `TypedDict` response annotation; 6. preserve status code with empty body; 7. support custom response class on router include; 8. test streaming response docs metadata; 9. improve response validation context; 10. ensure union response model schema is stable. |
| F05 OpenAPI docs | schema generation | 1. deterministic schema order for nested models; 2. include examples from `Annotated` metadata; 3. avoid duplicate tags when router included twice; 4. improve OpenAPI for cookie params; 5. add regression for enum descriptions; 6. preserve deprecated flag through router include; 7. improve schema for callback routes; 8. handle `Literal` defaults consistently; 9. test generated docs for OAuth scopes; 10. add schema regression for nested discriminated union. |
| F06 middleware/errors | exception handlers and middleware | 1. preserve headers in custom HTTPException handler; 2. add regression for middleware order with mounted app; 3. improve validation exception logging hook; 4. ensure CORS preflight handles custom method casing; 5. add test for exception handler inheritance in sub-app; 6. handle background task exception in test client; 7. improve error text for invalid middleware config; 8. preserve request state after middleware short-circuit; 9. add test for WebSocket exception mapping; 10. ensure lifespan errors surface in tests. |
| F07 security | OAuth, API key, security deps | 1. improve OAuth2 password form error detail; 2. add OpenAPI regression for optional security dependency; 3. preserve scheme name through router include; 4. handle API key header aliases consistently; 5. test security scopes in nested dependencies; 6. improve HTTP bearer malformed token error; 7. add docs example test for multiple schemes; 8. ensure optional auth returns `None` without raising; 9. improve generated security requirement ordering; 10. regression for security dependency cache. |
| F08 lifespan/background | startup/shutdown/background tasks | 1. deterministic lifespan context cleanup order; 2. add regression for background task after custom response; 3. improve error if both lifespan and legacy events conflict; 4. test mounted app lifespan propagation; 5. handle async background callable exceptions in tests; 6. preserve app state during nested lifespan; 7. improve shutdown error message; 8. add regression for dependency finalizer with background task; 9. ensure test client exits lifespan on failed request; 10. test lifespan with router-level dependency. |
| F09 test client | `fastapi.testclient` and Starlette integration | 1. compatibility guard for upstream client keyword change; 2. add regression for cookies across redirects; 3. improve WebSocket close reason assertion; 4. support custom headers default merge; 5. test streaming response iteration cleanup; 6. improve error when client used outside context for lifespan-only app; 7. preserve app overrides per client instance; 8. add regression for multipart upload filenames; 9. ensure async exception propagation stays configurable; 10. improve typing for client factory. |
| F10 docs examples | `docs_src/`, tested snippets | 1. update outdated Pydantic v2 example; 2. add regression test for documented dependency pattern; 3. improve docs snippet for custom response; 4. fix stale OpenAPI example assertion; 5. add test for security docs snippet; 6. simplify background tasks example while keeping behavior; 7. add docs example for `Annotated` query alias; 8. ensure tutorial test covers response model exclusion; 9. update WebSocket example test; 10. add docs regression for mounted sub-app. |

## `scikit-learn/scikit-learn` Seed Matrix

Target validation command template: `pytest sklearn/<module>/tests/<target_test_file>.py -q`

Ten families times ten variants yields 100 candidate prompts.

| Family | Area | 10 prompt variants |
|--------|------|--------------------|
| S01 metrics | `sklearn/metrics/` | 1. improve input validation for multilabel metric edge case; 2. add regression for sample weights with zero rows; 3. make error text consistent for bad averaging mode; 4. test sparse input for pairwise metric; 5. handle `np.nan` in documented metric path; 6. add scorer metadata routing regression; 7. improve precision/recall warning specificity; 8. cover dtype preservation in confusion matrix; 9. fix docstring example output; 10. add metric test for pandas index alignment. |
| S02 preprocessing | `sklearn/preprocessing/` | 1. preserve feature names in transformer output; 2. add regression for sparse min-max scaling; 3. improve error on incompatible categories; 4. test inverse transform with unknown categories; 5. handle constant column dtype in scaler; 6. add metadata routing test for transformer; 7. improve `set_output` behavior for pandas; 8. test one-hot drop behavior with infrequent category; 9. fix doc example around normalization; 10. add warning regression for copy=False mutation. |
| S03 model_selection | `sklearn/model_selection/` | 1. deterministic split with grouped edge case; 2. improve error for invalid CV splitter; 3. add regression for metadata routing through cross_validate; 4. handle empty parameter grid better; 5. test scoring dict order stability; 6. improve train/test split message for stratify mismatch; 7. add regression for nested parallel config; 8. preserve pandas feature names in validation split; 9. test randomized search with custom distribution; 10. fix doc example assertion. |
| S04 pipeline/compose | `sklearn/pipeline.py`, `sklearn/compose/` | 1. preserve feature names through ColumnTransformer remainder; 2. improve Pipeline error when step missing method; 3. add regression for metadata routing through nested pipeline; 4. test `set_output` for FeatureUnion; 5. handle passthrough columns ordering edge case; 6. improve verbose feature names conflict message; 7. add test for sparse/dense mix threshold; 8. preserve estimator tags through pipeline; 9. fix repr for long nested pipeline; 10. add docs example test for make_column_selector. |
| S05 inspection | `sklearn/inspection/` | 1. add permutation importance regression with sample weights; 2. improve partial dependence error for bad grid; 3. test feature names in display objects; 4. handle categorical feature ordering in plot data; 5. improve warning for unsupported estimator; 6. add metadata routing test for inspection helper; 7. fix docstring for return shape; 8. test sparse input in permutation importance; 9. improve display repr stability; 10. add regression for pandas nullable dtype. |
| S06 datasets | `sklearn/datasets/` | 1. improve fetcher cache error recovery; 2. add parser regression for quoted ARFF field; 3. test return_X_y with as_frame consistency; 4. improve error for invalid subset name; 5. preserve target names dtype; 6. add checksum mismatch diagnostic; 7. fix docs for generated dataset parameter; 8. test sparse generated data shape; 9. handle random_state in multilabel generator edge case; 10. add regression for feature name collisions. |
| S07 neighbors | `sklearn/neighbors/` | 1. add validation for unsupported metric/algorithm combination; 2. test radius query with empty result; 3. improve sparse input warning; 4. preserve dtype in kneighbors_graph; 5. add regression for weighted prediction tie; 6. improve error for negative radius; 7. test pandas feature names in estimator; 8. handle precomputed matrix shape message; 9. fix docs example output; 10. add metadata routing check where applicable. |
| S08 linear_model | `sklearn/linear_model/` | 1. improve sample weight validation for classifier; 2. add regression for sparse input with intercept; 3. test convergence warning message; 4. preserve feature names in fitted estimator; 5. handle warm_start shape mismatch clearly; 6. add docs example test for regularization path; 7. improve multioutput validation; 8. test dtype handling with float32; 9. add metadata routing regression; 10. improve error for incompatible solver/penalty. |
| S09 base/utils | `sklearn/base.py`, `sklearn/utils/` | 1. improve estimator tag propagation; 2. add regression for parameter validation with numpy scalar; 3. test feature name validation with duplicate names; 4. improve clone error for mutable parameter; 5. add metadata routing edge-case test; 6. preserve array API compatibility in helper; 7. improve check_array message for 1D input; 8. test pandas nullable dtype conversion; 9. add deprecation warning stacklevel fix; 10. improve repr truncation for long parameter. |
| S10 docs/examples | `doc/`, examples with tests | 1. update stale example import; 2. add example test for metadata routing; 3. fix plot output assertion; 4. improve narrative around feature names; 5. add regression for documented pipeline pattern; 6. modernize deprecated parameter in example; 7. add doctest for custom scorer; 8. fix typo that breaks generated docs; 9. ensure example handles new warning; 10. add short example for set_output. |

## `Textualize/rich` Seed Matrix

Target validation command template: `pytest tests/<target_test_file>.py -q`

Ten families times ten variants yields 100 candidate prompts.

| Family | Area | 10 prompt variants |
|--------|------|--------------------|
| R01 console | `rich/console.py` | 1. preserve style across nested capture; 2. add regression for width calculation with tabs; 3. improve file-like object error message; 4. test soft wrap with emoji width; 5. handle markup disabled with highlighter enabled; 6. preserve record buffer ordering; 7. improve console options repr; 8. test legacy Windows color fallback; 9. add regression for stderr console export; 10. handle `None` end parameter consistently. |
| R02 text/markup | `rich/text.py`, markup parser | 1. escaped bracket regression; 2. overlapping span normalization; 3. improve error for unclosed tag; 4. test style merge precedence; 5. handle emoji and combining chars in slicing; 6. preserve spans after truncate; 7. add markup parser fuzz regression; 8. improve plain text extraction; 9. test append with style object; 10. handle zero-width joiner length. |
| R03 tables | `rich/table.py` | 1. column ratio edge case; 2. add regression for empty table title; 3. improve overflow behavior with no-wrap column; 4. test footer style inheritance; 5. handle multiline cell width; 6. preserve row end sections with padding; 7. improve error for invalid justify value; 8. add regression for nested renderables; 9. test box style with safe_box; 10. fix docs example expectation. |
| R04 panels/tree | `rich/panel.py`, `rich/tree.py` | 1. panel title alignment edge case; 2. add regression for nested panel width; 3. improve tree guide style inheritance; 4. test empty tree render; 5. handle multiline panel subtitle; 6. preserve expand behavior in constrained width; 7. improve error for invalid padding tuple; 8. add regression for highlight in tree label; 9. test panel with renderable that has measurement; 10. fix docs snippet. |
| R05 progress/status | `rich/progress.py`, `rich/status.py` | 1. completed task refresh regression; 2. add test for transient progress cleanup; 3. improve error for unknown task id; 4. handle negative advance clearly; 5. test custom column measurement; 6. preserve task fields on update; 7. add regression for disable=True output; 8. improve status spinner stop behavior; 9. test progress with file redirection; 10. docs example for multiple progress bars. |
| R06 live/layout | `rich/live.py`, `rich/layout.py` | 1. nested live display guard message; 2. add regression for layout ratio normalization; 3. test screen mode cleanup; 4. handle refresh_per_second zero validation; 5. preserve layout names after split; 6. improve error for missing child; 7. add test for live renderable update with same object; 8. handle vertical overflow mode; 9. test console capture with live; 10. docs example for layout update. |
| R07 syntax/highlight | `rich/syntax.py`, highlighters | 1. fallback lexer regression; 2. add test for line number width with start_line; 3. improve error for invalid theme; 4. handle code ending without newline; 5. preserve highlighted tabs width; 6. add regression for custom highlighter style; 7. test traceback code theme propagation; 8. improve syntax measurement; 9. handle empty code block; 10. update docs example for custom theme. |
| R08 traceback/logging | `rich/traceback.py`, `rich/logging.py` | 1. suppress frame pattern regression; 2. add test for locals truncation; 3. improve logging markup opt-out; 4. handle exception group formatting; 5. preserve log record extra fields; 6. add regression for path shortening; 7. test rich handler with custom console; 8. improve traceback width behavior; 9. docs example for install hook; 10. handle recursive locals safely. |
| R09 prompt/input | `rich/prompt.py` | 1. invalid choice retry message; 2. add test for default display with password prompt; 3. improve type conversion error; 4. handle case_sensitive choices; 5. preserve markup in prompt suffix; 6. add regression for EOF behavior; 7. test custom console input stream; 8. improve Confirm default formatting; 9. docs example for prompt choices; 10. handle empty response with default. |
| R10 export/docs | export helpers and docs examples | 1. HTML export style regression; 2. add SVG export width test; 3. improve ANSI export for hyperlinks; 4. preserve segment styles in export_text; 5. test console save_html path handling; 6. update stale README example; 7. add docs test for table export; 8. fix docs typo in progress example; 9. add regression for plain export with markup; 10. improve error for unsupported export target. |

## Rollout Readiness Recommendation

Recommended first-pass sampling:

- Generate 100 prompts per repo by expanding every matrix row into 10 task ids.
- Run 5 smoke prompts per repo first: one small, three medium, one large.
- For scikit-learn smoke, choose `metrics`, `preprocessing`, `model_selection`, `pipeline/compose`, and `base/utils`; avoid compiled estimator internals until harness build caching is proven.
- For Rich smoke, favor rendering snapshot-style tests with deterministic console width.
- For FastAPI smoke, favor existing `tests/` and `docs_src/` regression tasks with targeted pytest files.

## Blockers

No active blocker for this owner area.

Watch items:

- GitHub API rate limiting may affect repeated metadata refreshes.
- scikit-learn can have heavier local build/test setup than the other two repos.
- Rich's smaller test surface means duplicate prompt families should be avoided during sampling.

## Session 5 PM Prompt Quality Result

Active Session 5 task file:

```text
/root/workspace/rollout_harness/tasks_m1_10.jsonl
```

PM validation:

```text
total 10
per_repo fastapi=4 scikit-learn=3 rich=3
all prompts include actual edit/patch attempt requirement
all prompts include test/check attempt requirement
```

The 10 prompts supersede the old 300-task matrix for final Milestone 1 evidence. The 300-task matrix remains useful scratch planning evidence only.

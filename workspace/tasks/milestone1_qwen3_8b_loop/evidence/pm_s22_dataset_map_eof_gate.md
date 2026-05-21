# PM S22 Dataset Map EOF Gate

<!-- METADATA:OWNER=intern_code_pm,SESSION=22,STATUS=No-Execution-Fix-Chain -->

## Gate Result

- Time: `2026-05-21T09:39:00Z`
- Upstream runtime task: `M1-S22-POSTPATCH-SFT-RUNTIME-DEV2`
- Runtime owner: `intern_code_dev_2`
- Result: fresh runtime blocker, no checkpoint/model.

## Accepted Facts

- LTP frame `xu.yang~coding-agent-playground-m1-s22-postpatch-qwen3-8b-runtime-20260521T092458Z` reached `STOPPED (Completed)`.
- Endpoint `ssh -p 38445 root@10.100.24.11` refused connection after stop.
- Runtime artifacts are preserved under `/home/xu.yang/coding_agent_playground/outputs` on CephFS.
- PR #39 diagnostics worked: preflight JSON, generated runtime config, run manifest, stdout/stderr log, xtrace, early-exit diagnostics, and exit status were produced.
- SFT exited `EXIT_STATUS=1`.
- Failure occurred before training/checkpoint save in LLamaFactory dataset conversion: `datasets.map(num_proc=4)` / `SyncManager` `EOFError`.
- No complete checkpoint/model, `trainer_state.json`, or `all_results.json` exists.
- Old `KeyError: from` and ENOSPC/safetensors signatures were not observed.
- No eval was run.

## PM Decision

No new LTP/GPU/SFT/eval retry is authorized.

The next fix chain is no-execution:

- `intern_code_dev_4`: prepare a config/launcher patch package that sets 10-row smoke dataset preprocessing to single-process while preserving PR #39 diagnostics and `/home/xu.yang` paths.
- `intern_code_dev_3`: confirm the ShareGPT data artifact does not need content/schema change for this blocker, or record exact data-side blocker.
- `intern_code_dev_1`: review dev_4/dev_3 package for provenance/config risk.
- `intern_code_test_1`: gate the runtime blocker and next single-process config package.
- `intern_code_dev_2`: keep GPU released; prepare only a future no-submit resource readiness refresh if PM asks.
- `intern_code_test_2`: keep eval blocked because no checkpoint/model or served endpoint exists.

Any future runtime requires a fresh PM authorization after dev/test durable gates pass.

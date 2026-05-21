# M1-S23-PARSERPATCH-RUNTIME-READY-DEV2

Owner: `intern_code_dev_2`

Prepare no-submit runtime readiness for a future parser-patch retry. This task does not authorize LTP submission or GPU/runtime execution.

Acceptance:

- Evidence confirms no active held Milestone 1 GPU allocation.
- Evidence names intended 8xH200 shape, stop conditions, and `/home/xu.yang/coding_agent_playground/outputs` paths.
- Evidence treats remote GPU/LTP nodes as no-external-network targets.
- Future code/config/scripts must be prepared and verified locally or in the provided workspace before transfer.
- Evidence includes exact source commit, checksum/file-list requirements, and `rsync`/`scp`/tar-over-SSH transfer templates for a future endpoint.
- No LTP, GPU, preflight, SFT, eval, or remote runtime command is run without fresh PM authorization.

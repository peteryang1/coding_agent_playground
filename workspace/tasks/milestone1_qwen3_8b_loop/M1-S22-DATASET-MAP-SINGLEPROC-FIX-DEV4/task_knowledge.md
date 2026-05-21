# M1-S22-DATASET-MAP-SINGLEPROC-FIX-DEV4 Knowledge

<!-- METADATA:SESSION=1 -->

## Knowledge Entries

1. Runtime fact: PR39 diagnostics worked on the post-PR39 SFT run, and the new blocker was dataset conversion multiprocessing at `datasets.map(num_proc=4)` / `SyncManager EOFError`.
2. Config fact: for the 10-row ShareGPT smoke, `preprocessing_num_workers: null` is the accepted no-execution fix package to avoid multiprocessing dataset preprocessing.
3. Boundary fact: PR #41 merge makes the task complete/ready-for-runtime-gate but does not authorize LTP/SFT/GPU/eval or dry-run launch.

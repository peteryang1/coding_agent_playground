# intern_code_dev_4 - 个人知识库

<!-- METADATA:SESSION=2 -->

---

## 知识条目

1. SFT wrapper manifest reliability: export and explicitly pass resolved runtime paths into manifest writers before launch so durable run metadata does not depend on inherited environment alone.
2. SFT runtime boundary: no-execution wrapper/config PRs can be complete/ready-for-runtime-gate while LTP/SFT/GPU/eval authorization remains separately gated.
3. SFT tiny-data preprocessing: for 10-row ShareGPT smoke runs, single-process preprocessing avoids the `datasets.map(num_proc=4)` multiprocessing manager failure surface and is sufficient for throughput.
4. SFT NCCL/NVLink mitigation: when an 8-GPU H200 run reaches training startup then fails with peer GPU memory over NVLink on one rank, prefer a fresh different node plus NCCL/NVLink preflight before changing training semantics.
5. SFT preflight parser contract: health parsers should expose stable top-level gate fields and keep generated command/process/evidence text out of actionable fault matching while still preserving ignored matches for audit.
6. SFT parser-fixed blocker pattern: distinguish stale historical Xid/SXid from fresh or timestamp-unknown actionable Xid/SXid, and normalize `/home/xu.yang/coding_agent_playground/outputs` with its CephFS resolved mirror when evaluating generated artifact storage.
7. SFT parser patch completion: PM-gated parser implementation PRs can land without runtime authorization; record mergedAt and merge commit separately while keeping LTP/GPU/preflight/SFT/eval/dry-run blocked until PM authorizes runtime.

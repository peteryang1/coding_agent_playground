# intern_code_dev_4 - 个人知识库

<!-- METADATA:SESSION=32 -->

---

## 知识条目

1. SFT wrapper manifest reliability: export and explicitly pass resolved runtime paths into manifest writers before launch so durable run metadata does not depend on inherited environment alone.
2. SFT runtime boundary: no-execution wrapper/config PRs can be complete/ready-for-runtime-gate while LTP/SFT/GPU/eval authorization remains separately gated.
3. SFT tiny-data preprocessing: for 10-row ShareGPT smoke runs, single-process preprocessing avoids the `datasets.map(num_proc=4)` multiprocessing manager failure surface and is sufficient for throughput.

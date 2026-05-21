# M1-S22-NCCL-MITIGATION-DEV4 Knowledge

<!-- METADATA:SESSION=1 -->

## Knowledge Entries

1. Runtime fact: the post-PR41 SFT run reached training startup and then failed with CUDA/NCCL invalid peer GPU memory over NVLink or hardware error on local rank 5 before checkpoint save.
2. Mitigation fact: the accepted no-execution package recommends a fresh different H200 node plus NCCL/NVLink preflight before any future SFT attempt.
3. Boundary fact: PR #43 merge makes the task complete/ready-for-runtime-gate but does not authorize LTP/SFT/GPU/NCCL preflight/eval/dry-run launch or runtime retry.

# Compute GPU Route Decision

Timestamp: 2026-05-20T09:24:29Z
Owner: intern_compute_manager
Request: coding_agent_playground Milestone 1 Qwen3-8B SFT smoke GPU route decision.

## Decision

Approved route: use the fresh single-node H200 endpoint below for a short Qwen3-8B SFT smoke.

```text
ssh -p 39314 root@10.100.20.37
```

LTP frame:

```text
xu.yang~coding-agent-playground-m1-qwen3-8b-smoke-gpu-agentic-fixed-20260520-092130
```

Node:

```text
hostname: lg-cmc-b7r202-o09u26-h200-000667
vc: h200agentic
gpu: 8 x NVIDIA H200
```

Do not use the previously proposed candidate endpoints for this smoke:

```text
ssh -p 27094 root@10.100.10.20
ssh -p 31403 root@10.100.8.24
```

Reason: both were live but already occupied by Ray workers using about 133-135 GB GPU memory per card. They are not approved for Milestone 1 SFT smoke.

## Current nodes.json

One-node `nodes.json` for the approved route was written next to this file:

```text
/work-agents/intern_code_pm/coding_agent_playground/workspace/tasks/milestone1_qwen3_8b_loop/evidence/compute_gpu_route_nodes.json
```

It was also staged on the approved GPU endpoint:

```text
/root/workspace/coding_agent_playground/nodes.json
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground/milestone1_nodes.json
```

Content:

```json
{
  "node_count": 1,
  "nodes": [
    {
      "ip": "10.100.20.37",
      "port": "39314",
      "user": "root",
      "node_rank": 0
    }
  ]
}
```

## Verification

Route verification on `ssh -p 39314 root@10.100.20.37`:

```text
host=lg-cmc-b7r202-o09u26-h200-000667
gpu=0, NVIDIA H200, 0, 1, 143771;1, NVIDIA H200, 0, 1, 143771;2, NVIDIA H200, 0, 1, 143771;3, NVIDIA H200, 0, 1, 143771;4, NVIDIA H200, 0, 1, 143771;5, NVIDIA H200, 0, 1, 143771;6, NVIDIA H200, 0, 1, 143771;7, NVIDIA H200, 0, 1, 143771;
procs=
ceph=fuse.ceph-fuse ceph-fuse /mnt/cephfs
outroot=writable
```

Staged local paths on the approved GPU endpoint:

```text
/root/workspace/coding_agent_playground
/root/workspace/cleaned_m1_sft_10/train.jsonl
```

Dataset check:

```text
wc -l /root/workspace/cleaned_m1_sft_10/train.jsonl
10 /root/workspace/cleaned_m1_sft_10/train.jsonl
```

Output root check:

```text
/mnt/3fs/data/ai4ai/outputs/coding_agent_playground is writable
```

## Allocation Notes

Attempted fresh `h200` job:

```text
coding-agent-playground-m1-qwen3-8b-smoke-gpu-20260520-091353
```

Result: stopped after it stayed in `WAITING / AttemptPreparing`; scheduler event reported:

```text
FailedScheduling: VC Safety Broken: free cell not found even split to the highest level 3
```

Attempted first fresh `h200agentic` job:

```text
coding-agent-playground-m1-qwen3-8b-smoke-gpu-agentic-20260520-091831
```

Result: failed during bootstrap because the worker template used `ceph-fuse -o nonempty`; this image's fuse rejected it with:

```text
fuse: unknown option(s): `-o nonempty'
```

The approved route uses a fixed temporary YAML with `-o nonempty` removed. No SFT was run.

## Handoff

This endpoint is approved only for the requested short Qwen3-8B SFT smoke. After the smoke completes, stop the LTP job above or ask compute manager to stop it.

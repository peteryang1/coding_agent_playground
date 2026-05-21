# M1-S23-PARSERFIXED-PARSER-PATCH-DEV4 Knowledge

<!-- METADATA:SESSION=1 -->

1. Stale historical Xid/SXid can be audited without blocking SFT when the parser has a current run freshness start.
2. Fresh/current and timestamp-unknown Xid/SXid remain actionable because suppressing unknown health signatures could hide current hardware faults.
3. `/home/xu.yang/coding_agent_playground/outputs` may resolve to `/mnt/cephfs/home/xu.yang/coding_agent_playground/outputs`; both forms need to be recognized for generated-artifact storage status.
4. PR #49 is the implementation PR for this parser patch and is ready for PM review while runtime remains separately gated.

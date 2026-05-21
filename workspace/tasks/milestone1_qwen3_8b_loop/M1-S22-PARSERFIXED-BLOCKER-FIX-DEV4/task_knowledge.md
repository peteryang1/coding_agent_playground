# M1-S22-PARSERFIXED-BLOCKER-FIX-DEV4 Knowledge

<!-- METADATA:SESSION=1 -->

1. Parser-fixed preflight can still block before SFT when Xid/SXid health history and `/home/xu.yang` storage classification are not separated into current actionable versus stale or normalized path states.
2. Historical Xid/SXid entries need freshness classification instead of blanket suppression; fresh or timestamp-unknown Xid/SXid remains actionable.
3. `/home/xu.yang/coding_agent_playground/outputs` may resolve to `/mnt/cephfs/home/xu.yang/coding_agent_playground/outputs`; storage checks should accept that mirror only as the resolved form of the `/home/xu.yang` output tree.
4. PM gate pass for this no-execution evidence package authorizes only owner self-merge; runtime authorization remains a separate PM decision.

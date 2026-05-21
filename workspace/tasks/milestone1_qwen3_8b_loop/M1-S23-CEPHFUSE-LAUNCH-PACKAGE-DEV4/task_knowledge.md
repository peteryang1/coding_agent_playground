# M1-S23-CEPHFUSE-LAUNCH-PACKAGE-DEV4 Knowledge

<!-- METADATA:SESSION=1 -->

1. Dev_4 SFT launch packages should not call `ceph-fuse`; the resource handoff must provide an already-mounted `/home/xu.yang/coding_agent_playground/outputs` path.
2. The launch package should verify raw `/home/xu.yang/coding_agent_playground/outputs` and resolved `/mnt/cephfs/home/xu.yang/coding_agent_playground/outputs` roots, writability, and capacity before SFT.
3. GPU runtime should use local checksum-verified repo/data/dependency bundles only, with no remote GitHub/source/dependency network access during launch.
4. PR #51 was PM-gated and self-merged at `2026-05-21T13:23:23Z`; merge commit `c02a53a344f2ad7a33b04f529d5125677237d4cb`.

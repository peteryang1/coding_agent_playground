# M1-S22-PREFLIGHT-PARSER-FIX-DEV4 Knowledge

<!-- METADATA:SESSION=1 -->

1. ECC parsing must not use a whole-line "any zero means healthy" rule. Lines can include unrelated zeros such as GPU 0 or timestamps while still containing a nonzero uncorrected ECC counter.
2. The preflight parser must expose stable top-level compatibility fields for PM/test gates, not only nested `checks` and `decision` objects.
3. Future SFT eligibility must be blocked when the parsed preflight artifact root is outside `/home/xu.yang/coding_agent_playground/outputs`.

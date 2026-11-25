# R2 regression: node-api + DAO vote snapshot

Scope: old HEAD 89a542e (testnet-0005) vs new HEAD 8cc209d (testnet-0006, 2026-11-16). Diff 89a542e..HEAD: one squashed release, 66 files. DAO harness is Python, not in the public Go repo; verified against read-only clone ~/workspace/xe-bounty/dao, HEAD 74b5f6e, all five DAO patch commits present as ancestors. Method: read-only, no filing, no live testnet attacks. Desk q search 2026-11-17 05:44 UTC for re-reports of each ID.

Result: 0 STILL LIVE. 2 ALREADY RE-REPORTED (stale, filed against 89a542e, fix verified at new HEAD). 5 FIXED. 7-Question Gate not triggered: no live claim to gate.

## XE-0082: ALREADY RE-REPORTED, fix verified at HEAD

Claim: UI reverse proxy makes clientIP 127.0.0.1, all wallet/explorer traffic shares one rate-limit bucket. Assessed High, awarded 2,000 XE.

Vulnerable (89a542e): api/handler.go:375-393, clientIP took the last XFF entry, always 127.0.0.1 through the UI proxy.

Fix (HEAD 8cc209d): api/handler.go:387-407, clientIP walks XFF right to left skipping loopback hops, returns first non-loopback hop. api/ui.go proxy unchanged (httputil ReverseProxy appends 127.0.0.1), but the walk now skips it.

Residuals checked, none fileable:
- X-Real-IP fallback (handler.go:403-405) only reached when XFF empty or all loopback, and only from a loopback RemoteAddr; unreachable via the UI proxy, which always sets XFF. Local-only.
- Non-loopback intermediate proxy would collapse to that proxy IP, but the documented deployment is UI proxy on loopback; deployment-specific, not the claimed defect.
- Direct XFF spoof for fresh buckets is XE-2931, separate tracked ticket, opposite direction.

Re-report check: XE-8218 "[Regression] XE-0082 still unfixed at HEAD 89a542e", New, claimed High, filed 2026-11-11 by Ntaaaaah, tested at 89a542e with end-to-end PoC. XE-15147 "[Dispute] XE-0082/XE-0099 unfixed at HEAD 89a542e", New, filed 2026-11-16 by urelkdubdqwr. Both open, both against 89a542e, both stale at new HEAD. A new re-report would duplicate them. Drop.

## XE-0116: ALREADY RE-REPORTED, fix verified at HEAD

Claim: POST /attestation/request signs any identifier whose hex[0:32] and hex[48:] match a registered account with middle 16 zero, no caller proof. Assessed High, awarded 3,500 XE.

Vulnerable (89a542e): node/attestation.go:32-52, canAttest(identifier) with no caller argument; direct directory lookup and zeroMid fallback both return nil with no ownership check.

Fix (HEAD 8cc209d): node/attestation.go:32-57, canAttest(identifier, from peer.ID). Direct lookup requires n.PeerForAccount(identifier) == from (line 44). ZeroMid fallback requires n.PeerForAccount(a) == from (line 51). from == "" errors for non-lease identifiers (lines 40-42). HTTP path RequestAttestation passes from == "", so forged zeroMid identifiers via HTTP are blocked. P2P path passes the requesting peer ID, so only the owning peer gets its own account attested.

Residual checked, not fileable: live-lease branch (lines 33-39) still attests for any live lease hash regardless of caller. Distinct from the claimed defect, weaker, no clear victim harm: attestation over a real lease hash is the intended function and the timestamp is public. No victim, no report.

Re-report check: XE-13266 "[Re-report] XE-0116 still unfixed at HEAD 89a542e", New, claimed High, xe#403, filed 2026-11-11 by zvsvev, with local repro at 89a542e. XE-15142 "[Dispute] XE-0116/XE-0138 unfixed at HEAD 89a542e", New, filed 2026-11-16 by urelkdubdqwr. Both open, both against 89a542e, both stale at new HEAD. A new re-report would duplicate them. Drop.

## XE-0284: FIXED

Claim: dao/api POST /v1/members/sessions/{sid}/rebuild skips not_before, nullifying upgrade timelock. Assessed High, awarded 4,000 XE. Code not in public Go repo.

Fix: dao@f540ef1 adds require_timelock_run() raising 409 in rebuild(), sign(), submit() in dao/services/sessions.py. Verified at DAO HEAD 74b5f6e: dao/services/sessions.py:330,365,438,664. All callers (route rebuild_if_stale, worker rebuild/submit, approve() auto-rebuild) go through the gated functions. No bypass path found.

Re-report check: q=XE-0284 returns only XE-4821 and XE-7976, unrelated. No re-report. Drop, fixed.

## XE-0631: FIXED

Claim: DAO portal vote weight snapshot at opened_at is reconstructable, backdated blocks rewrite it. Claimed High, assessed Medium, awarded 1,200 XE. Code not in public Go repo.

Fix: dao@7a7bd16e0222 moves the snapshot to opened_at minus 1 hour 5 minutes (SNAPSHOT_LEAD_NS = TIMESTAMP_WINDOW_NS + SNAPSHOT_MARGIN_NS, 3600s + 300s). Verified at DAO HEAD: dao/chainops.py:332-334 snapshot_time, dao/services/portal.py:178 eligibility_at uses snapshot_time(pr.opened_at). Node DefaultTimestampWindow is 1 hour at both HEADs (core/ledger.go:112). A block submitted after a proposal opens cannot be dated at or before the snapshot instant.

Re-report check: q=XE-0631 returns only XE-14652 and XE-14661, unrelated. No re-report. Drop, fixed.

## XE-0647: FIXED

Claim: POST /v1/members/inbox/untriaged never commits, SeenSignature claim rolled back, one captured signature replays. Claimed High, assessed Minor, awarded 400 XE. Code not in public Go repo.

Fix: dao@6085bfe65a04 adds await db.commit() in inbox_untriaged and makes get_db commit on clean return. Verified at DAO HEAD: dao/db.py:84-90, dao/api/members.py:224-225. member_action now centralizes verify_and_claim for all members routes.

Re-report check: q=XE-0647 returns nothing. No re-report. Drop, fixed.

## XE-1789: FIXED

Claim: DAO vote snapshot counts lease settle emission with no causal check. Claimed High, assessed Medium, awarded 250 XE. Code not in public Go repo.

Fix: dao@7acfdc8 extends the causal check to lease settle via ARRIVALS = ("receive", "lease_settle"), SNAPSHOT_RULE 3 to 4 (now 6 at DAO HEAD). _sends_at_or_before checks the source lease block is final and dated at or before at_ns. Force settle credits XCU, not XE (core/ledger.go force-settle handler requires asset XCU), and lease cancel refunds XCU, so neither is a bypass. Settle amount is LeaseTotalEmission, fixed at lease creation. b.Timestamp is not bound to attested settle time, but the 65-minute lead prevents post-open backdating to at or before the snapshot instant. Pre-open opener arrangement is documented accepted behavior (XE-1098, noted in dao/chainops.py comments). Claimed defect fixed; residual is opener-only, not fileable.

Re-report check: q=XE-1789 returns only XE-10721 (desk settle() workflow, unrelated) and XE-8672 (lease_settle cascade vs unfinalized accept, core ledger, different root). No re-report. Drop, fixed.

## XE-3129: FIXED

Claim: dao vote-weight snapshot (account_snapshot) reads chain without checking finalized, XE-0034 rule applied. Claimed High, assessed Medium, status Patched, no award yet. Code not in public Go repo.

Fix: dao@9894ce8 makes account_snapshot walk only finalized blocks. Verified at DAO HEAD: dao/chainops.py:367-368, blocks = takewhile(finalized is True, served), unsettled flag set when served chain holds an unfinalized block. dao/services/portal.py:221-222 is_current requires _derived_as_defined and not unsettled(row); portal.py:233 rederive_stale re-derives unsettled rows each pass; close tally (portal.py:383,406) counts only is_current rows and reports unsettled_rows. Desk log 2026-11-15 confirms fixed in dao@9894ce8 and invites re-running the reproduction against the next testnet build; the next build (testnet-0006, HEAD 8cc209d) carries the fix in the DAO harness.

Re-report check: q=XE-3129 returns only XE-14652. That ticket is not a re-report of XE-3129: it claims the live tally reports unsettled_rows=0 for a vote held out as unsettled because the field is computed after the is_current filter. Distinct follow-on display bug in the fix's unsettled handling, filed 2026-11-15, New, claimed Minor. Adjacent lead only, not a XE-3129 regression. No re-report of XE-3129 itself. Drop, fixed.

## Bottom line

Batch 2 yields nothing fileable: 0 live, 2 already re-reported by others (both stale at testnet-0006), 5 fixed with the fix verified in code at HEAD. Next options: further regression batch on other fixed High+ tickets, file the weak Minor A1 candidate from batch 1, or park XE until a new HEAD lands.

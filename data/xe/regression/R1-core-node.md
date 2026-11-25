# R1: regression hunt, core/node consensus + sync + SSH + attestation

- Old HEAD: `89a542e` (testnet-0005). New HEAD: `8cc209d` (testnet-0006, 2026-11-16). Diff is one squashed release, 66 files.
- Method: read-only. Ticket JSON + body via `bounty.xe.network/v1/tickets/<ID>`, desk search `?q=XE-xxxx` for re-reports, `git show` / `git diff 89a542e..HEAD` on the claimed paths. No filing, no live testnet traffic, no PoC executed.
- Verdict: **0 STILL LIVE. 8 of 8 FIXED.** No fileable re-report in this batch. The only remaining bypass found (XE-0048 IPv6 /64) was already filed today as XE-16550.

## 1. XE-0005 - FIXED

- Title: gossiped block can end the node process, no recover on block ingestion goroutine. Assessed High, award 3,500 XE, patch_refs 2 (PR #28, core#1029).
- Claimed defects at 89a542e: `core/multisig.go:99` `pk[:12]` slice with no length check; `net/gossip_validate.go:63` never checks `signatures[].public_key` length; `node/node.go:570` `handleIncoming` goroutine has no `recover`.
- Fix at HEAD: `core/multisig.go:92-100` validates each pubkey with `DecodePublicKey` (32-byte length check, `core/crypto.go:177`) before use and all three error sites use length-safe `shortHash`; `net/gossip_validate.go:81-86` rejects any signature whose pubkey is not 64 hex; `node/node.go:723-741` new `runGossipHandler` wraps the handler in a `recover()` loop and re-enters on panic, wired for blocks, votes, marketplace, statechain, directory and certificates (`node/node.go:560-577`).
- Re-report check: XE-0608 (Triaging, 2026-11-05) bundled XE-0005 as "partial gossip recover" against HEAD `02e9641`, citing unguarded gossip ingestion and `pullPhantomBlocks`. That predates 8cc209d and its named gaps are now closed on the gossip path. XE-9604 (2026-11-12, VerifyMultisigAny unbounded `signatures[]`, ~1.3 s CPU per rejected block) is a different defect (CPU amplification, no panic) and already filed.
- Residual, not fileable: `pullPhantomBlocks` (`node/node.go:927-947`) still spawns a goroutine with no `recover`, and pulled blocks bypass `blockValidator`. No panic primitive was found on that path in this pass (`VerifyHexSignature` returns errors on short keys, `shortHash` is length-safe, `ValidateKeyset` checks `len(k)==64` before `k[:12]` at `core/multisig.go:58`), so this fails the 7-Question Gate as a standalone claim. It is a hardening gap, not a live crash.

## 2. XE-0006 - FIXED

- Title: unauthenticated POST /directory/register kills every node in the mesh. Assessed Severe, award 12,500 XE, patch_refs 3 (PR #27, core#111, core#1029).
- Claimed defect at 89a542e: `node/node.go:2381` logs `reg.NodePeer[:12]` on a 1-byte peer ID, panics in the directory gossip goroutine; `directory/verify.go:29-53` accepts any non-empty `node_peer`.
- Fix at HEAD: `directory/verify.go:34-66` caps `node_peer` at 52 chars, runs `peer.Decode`, extracts the public key and requires the canonical peer ID of that key, plus a 5-minute future-timestamp cap; `node/node.go:2452-2460` `handleDirectoryGossip` now logs `shortHash(reg.NodePeer)`; the directory handler runs under `runGossipHandler` recover (`node/node.go:568-571`).
- Re-report check: desk `?q=XE-0006` shows no re-report of the slice panic. Nearest are XE-8697 (directory growth, different root cause) and XE-15031 (DELETE endpoint in PR #193, different endpoint). Neither is this defect.

## 3. XE-0021 - FIXED

- Title: core/quorum conflict resolution can finalize a block that never held 67% final vote weight. Assessed High, award 3,500 XE, patch_refs 2 (PR #148, core#1024).
- Claimed defect at 89a542e: `core/quorum.go:152-181` `pickWinner` substitutes the lowest-hash promotable member when the 67% winner fails full validation; `promotable` at 221-232 uses only the weak staged checker.
- Fix at HEAD: `core/quorum.go:152-165` `pickWinner` now returns `""` (withhold, no substitution) when the winner is unpromotable, logging "no other candidate is substituted"; `finalTally` (`core/quorum.go:180-193`) only returns a hash that itself crossed 67%; `promotable` (`core/quorum.go:244-272`) additionally requires `swapPreflight` against the incumbent; `NewQuorumManager` wraps the vote store in `validVoteStore`.
- Re-report check: desk `?q=XE-0021` shows no re-report. Nearest are XE-0530 (stale tally race, different mechanism) and XE-8080 (`emitFinalLocked` lock persistence, different), neither is the substitution.

## 4. XE-0023 - FIXED

- Title: net/sync frontier sync client allocates a full decoded page before the block cap, single peer can OOM a node. Assessed High, award 2,000 XE, patch_refs 3 (PR #144, core#1110, core#1113).
- Claimed defect at 89a542e: `net/sync.go:556-577` appends the whole decoded page to `allBlocks` before the `maxTotalBlocks` check, and the 10 MiB `LimitedReader` budget is re-armed per JSON value.
- Fix at HEAD: `net/sync.go` decodes through `syncPageBlocks.UnmarshalJSON`, which caps each page at `maxPageSize` (256) blocks during streaming decode; the decode loop appends one block at a time and breaks at `maxTotalBlocks` before exceeding it; a shared session budget `maxSyncSessionBytes` (32 MiB) wraps the per-value reader, so re-arming can no longer exceed 32 MiB per session; null blocks are dropped and counted.
- Re-report check: XE-14425 (2026-11-15) and XE-15049 (2026-11-16) both re-reported this as still unfixed, but both were filed against HEAD 89a542e and predate the 8cc209d fix. No re-report exists against 8cc209d. XE-11908 (2026-11-13, 10 MiB budget re-armed per page, 401 MiB retained) is the same root cause at 89a542e and is closed by the same session cap.

## 5. XE-0032 - FIXED

- Title: dao/api unauthenticated inbox POST serializes every DAO write behind one hash-chain lock. Assessed High, award 6,000 XE, patch_refs 2 (dao commits fd2b0d5, be43d38).
- Claimed defect at dao commit c60cf81: `dao/api/public.py:190-195` inbox POST needs only a signature, no PoW, no rate limit; every accepted message appends under `SELECT FOR UPDATE` on the single log-head row (`dao/log.py:53-56`).
- Fix upstream: dao commit `fd2b0d5f0ed1a3dbf0a11a9b33ce3cb7a1741c8d` (2026-10-30, "Harden inbox, votes, fees and input handling"), confirmed on dao main by the team and verified in the local dao checkout (ancestor of dao HEAD `74b5f6e`): POST /v1/inbox requires chat-level proof of work over the signing digest, per-IP and per-account token buckets on inbox, vote and proposal routes (429 + Retry-After), and untriaged inbox receipts stay private in the hash chain until a member reads them. `dao/api/public.py:16,223-239` imports `require_pow` and enforces it before any DB touch.
- Re-report check: desk `?q=XE-0032` shows no re-report. This ticket lives in the dao repo, not xe, so the fix could only be verified from the dao checkout, which was done.
- Caveat: the fix is verified in dao source, not by a live DAO deployment test. A live re-test would need a deployed dao instance; the code evidence is conclusive on the mechanism (PoW gate + buckets replace the unauthenticated flood path).

## 6. XE-0040 - FIXED

- Title: net/sync no in-flight guard on sync rounds, ordinary first sync reaches 1.9 GB RSS. Assessed High, award 5,000 XE, patch_refs 2 (PR #146, core#1110).
- Claimed defect at 89a542e: `net/sync.go:328-351` ConnectedF and `363-387` 10 s ticker spawn `requestSync` per peer with only a 5 s per-peer start cooldown and no in-flight state; each round buffers up to 10,000 blocks for up to 60 s, measured 75 concurrent rounds.
- Fix at HEAD: new `syncRounds` (`net/sync.go:79-116`) gives single-flight per peer plus a global slot semaphore `maxConcurrentSyncRounds = 4`; both ConnectedF and the periodic ticker call `rounds.start` / `defer rounds.done` before `requestSync`; `runSyncRound` adds a `recover()` around each round.
- Re-report check: desk `?q=XE-0040` shows no re-report of the in-flight guard. XE-11908 and XE-14425 (see XE-0023) concern per-round page allocation, a different mechanism, and are also fixed by the session cap.
- Residual, not fileable: `rounds.start` blocks waiting for a free slot while holding the peer's `running` entry. A waiting goroutine holds no buffers, and the per-peer entry prevents one peer from queueing many waiters, so the original 720,000-block-slot amplification cannot recur. Impact is idle goroutines only, bounded by connection limits.

## 7. XE-0048 - FIXED (original vector); only remaining bypass already filed as XE-16550

- Title: SSH gateway, 100 silent pre-auth connections exhaust all connection slots and deny the gateway indefinitely. Assessed High, award 3,500 XE, patch_refs 2 (PR #125, core#1109).
- Claimed defect at 89a542e: `node/ssh_gateway.go:30,57,66,82,104,149` takes a slot from a pool of 100 before any handshake, with no deadline anywhere; `x/crypto v0.47.0` has no handshake timeout.
- Fix at HEAD: `node/ssh_gateway.go:31-41` sets `sshHandshakeDeadline = 10 s`, `maxPreAuthPerIP = 3`, `maxPreAuthConnections = 100`, `maxSessionsPerIP = 10`; `handleConnection` sets the deadline before `ssh.NewServerConn`, releases the pre-auth slot on handshake failure, promotes to a session (capped) on success and clears the deadline. A single host can now hold at most 3 silent slots for at most 10 s.
- Re-report check: XE-15070 and XE-15144 re-reported this against 89a542e and predate the fix. XE-12320 (2026-11-13) is the interesting one: it proved the live gateway build 3019b76 had the deadline but NOT the per-IP limit, so one host sustaining ~100 new connections/s could still exhaust the pool. That was a deployment gap on the old build; the 8cc209d code now contains both halves, so XE-12320's claim is closed in code (live deployment state was not re-probed here).
- Bypass variant, do not file: XE-16550, filed 2026-11-17 03:07 UTC against HEAD 8cc209d, proves the per-IP limits are keyed on the raw remote IP string (`remoteIP`, no /64 aggregation, unlike `api/handler.go:clientKey`), so one IPv6 /64 can rotate addresses and fill the 100-slot pool. That is exactly the remaining bypass found in this pass and it is already claimed. Adjacent filed tickets, not this defect: XE-7931 (one authenticated lease holder occupies all slots, no per-lease cap or post-auth idle timeout), XE-12562/XE-12563 (unsolicited SSH responses freeze the mux), XE-12564 (DSA key parameter CPU burn).

## 8. XE-0072 - FIXED

- Title: GET /accounts does full-lattice work regardless of ?limit=, single client wedges the node's own health sampler. Assessed High, award 3,500 XE, patch_refs 1.
- Claimed defect at 89a542e: `api/handler.go:628-646` calls `GetAllAccounts()` first and paginates after; `node/node.go:993-1016` walks every frontier and deserialises every chain; limit=1 costs ~5.5 s on an 8,318-account lattice and wedges /health to 503.
- Fix at HEAD: `api/handler.go` `handleGetAllAccounts` now serves `h.node.GetAccountsPage(offset, limit)` and the route is wrapped in `newPerClientLimit(maxHeavyListPerClient = 2)`, which 429s a third concurrent list request from the same client; `node/node.go:GetAccountsPage` slices a pre-maintained summary list; `core/account_summary.go` maintains summaries incrementally (dirty set, one frontier-block read per changed account) and caches the sorted lists (`summaryByXE`, `summaryByID`), so a request does no chain deserialisation. The same treatment landed for /pending (`GetPendingPage`), /frontiers (`GetFrontiersPage`) and /accounts/{address}/chain (`GetChainRange`).
- Re-report check: XE-13265 (2026-11-11) re-reported this against 89a542e and predates the fix. No re-report exists against 8cc209d. XE-16707 (2026-11-17) claims other list endpoints (/leases, /conflicts, /reputation, /directory) still scan before pagination; that is a different endpoint set and already filed.
- Residual, not fileable: `refreshSummariesLocked` runs under `summaryMu` while re-reading dirty accounts, so a request arriving after a large sync burst can pay the refresh of many dirty accounts. That is amortised ingestion work, not per-request full-lattice work, and the per-client cap bounds concurrency.

## Summary table

| Ticket | Assessed | Verdict | Fix location at HEAD |
| --- | --- | --- | --- |
| XE-0005 | High | FIXED | core/multisig.go:92, net/gossip_validate.go:81, node/node.go:723 runGossipHandler |
| XE-0006 | Severe | FIXED | directory/verify.go:34, node/node.go:2452 shortHash |
| XE-0021 | High | FIXED | core/quorum.go:152 pickWinner withholds, no substitution |
| XE-0023 | High | FIXED | net/sync.go streaming page cap 256, 32 MiB session budget |
| XE-0032 | High | FIXED | dao fd2b0d5: PoW + per-IP/per-account buckets, private receipts |
| XE-0040 | High | FIXED | net/sync.go:79 syncRounds, 4 global slots, single-flight per peer |
| XE-0048 | High | FIXED | node/ssh_gateway.go:31 10 s deadline, 3 pre-auth per IP |
| XE-0072 | High | FIXED | api/handler.go GetAccountsPage + per-client cap 2, core/account_summary.go |

## Follow-up leads (not verdicts, for later batches)

- XE-16550 (IPv6 /64 bypass of SSH per-IP limits) is the one live bypass in this batch and is already filed; do not re-file.
- XE-9604 (VerifyMultisigAny unbounded signatures, CPU amplification) and XE-16707 (other list endpoints scan before pagination) are adjacent live claims already filed by others.
- `pullPhantomBlocks` (`node/node.go:927`) still lacks a `recover`; a fileable variant would need a fresh panic primitive on the AddBlock path, none found here.
- XE-0608's other two items (XE-0061 codec lease_renew, XE-0084 faucet docs) were not in this batch; XE-0061 is a candidate for a later batch since `core/encoding.go` changed in the diff.

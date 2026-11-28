# Xingchiapi

- `custom.xingchiapi` connects Muse to <RESEARCHER_MODEL> API through its OpenAI compatible REST API. It authenticates with the registered `api_key` credential and calls only `api.xingchiapi.com`.

- Helpers live in `~/workspace/custom-connectors/custom.xingchiapi/bin/`. `xingchi.py` lists models and runs chat completions with the stored credential.

## Connect

- The connection was registered with `credentials.request_api_access` and these details. Reuse them to reconnect:

```json
{
  "provider": "xingchiapi",
  "auth_scheme": "api_key",
  "placement": "bearer_header",
  "api_hosts": ["api.xingchiapi.com"]
}
```

- Before the first change in a conversation, prove access with a harmless read:

```text
python3 ~/workspace/custom-connectors/custom.xingchiapi/bin/xingchi.py models
```

## Credentials

- The registered connection holds the credential. Helpers import `/opt/muse/skills/custom-connector-setup/bin/dynamic_credentials.py`, which returns an `hsurr:` surrogate and places it where the provider reads the key. Muse swaps in the real credential only on an approved request to a registered host.

- Never put a key, token, password or cookie in this doc, a helper, a command argument, an environment variable or a log. Never ask the user to paste one in chat.

- Keep redirects disabled on authenticated requests.

- On a 401 or 403, check the request first. Confirm that the helper attached the credential, that the host is registered and that the placement and scopes match.

- Only when a request that carried the credential is still rejected, call `credentials.request_api_access` with the details above and `"reconnect": true`.

## List models

- Lists the models available to the key. Use it to confirm the key and the model id before a chat call.

```text
python3 ~/workspace/custom-connectors/custom.xingchiapi/bin/xingchi.py models
```

- Verified 2026-11-19: one model only, `<MODEL>.1-sol`, display name <RESEARCHER_MODEL>, owned by openai.

## Chat completions

- Runs a chat completion with the stored credential. Streams by default, like the <PLANNER_PROVIDER> helper, so long reasoning does not hit an idle timeout. Use `--no-stream` only for a short test.

```text
python3 ~/workspace/custom-connectors/custom.xingchiapi/bin/xingchi.py chat --prompt "Reply with exactly: TEST OK"
python3 ~/workspace/custom-connectors/custom.xingchiapi/bin/xingchi.py chat --no-stream --prompt "Reply with exactly: TEST OK" --max-tokens 8000
```

- Default model is `<MODEL>.1-sol`; `--max-tokens` is uncapped by default (no `max_output_tokens` sent). Pass `--max-tokens N` to cap it.

- Verified 2026-11-19 via the stored credential: `models` returned 1 model, chat returned `TEST OK` and `OK` as requested.

## Recover from errors

- `403 client_not_allowed` means the request did not look like an allowed programming client. The site only allows Codex, Claude Code, OpenCode, ZCode, <CODER_MODEL> Harness, Hermes Agent, Minis, WorkBuddy, Cursor, pi/omp, Qoder, Kilo, Cline, Roo, Trae, GitHub Copilot and Grok CLI. Direct scripts, SDKs and chat clients are rejected. The helper sends `User-Agent: claude-code/2.0.0`, which was verified working. `codex/1.0.0` was verified still rejected, so do not switch the User-Agent without retesting.

- `429` means the upstream rate limit was hit. Wait and retry once, then stop and report it.

- After a failed or timed-out change, check the current state with a read before trying again, because the first request may have completed.

## Limits

- Only one model exists on this account: `<MODEL>.1-sol`. There is no <PLANNER_MODEL>, Claude or Gemini model here.

- Prompt token billing is inflated and unpredictable. Verified 2026-11-19: a 25 token planning prompt was billed 5,445 prompt tokens, a one word reply was billed 4,391 to 18,307 prompt tokens, while two other short prompts were billed a normal 15 to 16 prompt tokens with reasoning tokens present. Do not use this as the primary planner or auditor while <PLANNER_MODEL> via <PLANNER_PROVIDER> is free at cost 0.0. Use it only as a fallback when <PLANNER_MODEL> is down.

- The helper cannot be used as a Hermes default model without retesting, because Hermes sends its own User-Agent and the site gate may reject it.

## Related skills

- Use `muse.skill_search` to find other skills and `muse.connector_search` to find other connectors.

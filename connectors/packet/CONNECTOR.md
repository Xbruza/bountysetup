# Packet

- `custom.packet` connects Muse to the Packet Token Factory API at `api.packet.ai`. It authenticates with the registered `api_key` credential sent as a Bearer header and calls only `api.packet.ai`.

- Helpers live in `~/workspace/custom-connectors/custom.packet/bin/`. `packet.py` lists models and runs OpenAI-compatible chat completions. It is the model backend for the BUILDER agent in the <PROGRAM> 3-agent system.

## Connect

- The connection was registered with `credentials.request_api_access` and these details. Reuse them to reconnect:

```json
{
  "provider": "packet",
  "auth_scheme": "api_key",
  "placement": "bearer_header",
  "api_hosts": ["api.packet.ai"]
}
```

- Before the first change in a conversation, prove access with a harmless read:

```text
python3 ~/workspace/custom-connectors/custom.packet/bin/packet.py models
```

## Credentials

- The registered connection holds the credential. Helpers import `/opt/muse/skills/custom-connector-setup/bin/dynamic_credentials.py`, which returns an `hsurr:` surrogate and places it where the provider reads the key. Muse swaps in the real credential only on an approved request to a registered host.

- Never put a key, token, password or cookie in this doc, a helper, a command argument, an environment variable or a log. Never ask the user to paste one in chat.

- Keep redirects disabled on authenticated requests.

- On a 401 or 403, check the request first. Confirm that the helper attached the credential, that the host is registered and that the placement and scopes match.

- Only when a request that carried the credential is still rejected, call `credentials.request_api_access` with the details above and `"reconnect": true`.

## List models

- List the models the Token Factory key can use. This is a read and changes nothing.

```text
python3 ~/workspace/custom-connectors/custom.packet/bin/packet.py models
```

- The output is JSON with `count` and `models`, a list of model ids. Verified 2026-11-20: 3 models, `<CODER_MODEL_ID>`, `<MODEL_ID>`, `<MODEL_ID>`.

## Chat completion

- Send one chat completion to a Packet model. This is a read-only generation call and changes no Packet state.

```text
python3 ~/workspace/custom-connectors/custom.packet/bin/packet.py chat --prompt "Reply with exactly: TEST OK" --max-tokens 50
```

- Pass `--model` to pick another model id, `--system` for a system prompt, `--max-tokens` for the output cap (uncapped by default), `--timeout` in seconds (default 300).

- The output is JSON with `model`, `content`, and `usage` token counts. Verified 2026-11-20: `TEST OK` from `<CODER_MODEL_ID>`, 54 total tokens, no inflation.

## Recover from errors

- A 403 `client_not_allowed` or similar rejection means the stored key lacks Token Factory access. Two `` Packet account keys failed exactly this way on 2026-11-19. Only a `` Token Factory key works. Reconnect with a Token Factory key.

- After a failed or timed-out change, check the current state with a read before trying again, because the first request may have completed.

## Limits

- The connector only calls `api.packet.ai`. It cannot reach the Packet dashboard or any other Packet host.

- Token Factory keys expose only the models the key is enrolled for. The verified key exposes 3 models.

## Related skills

- [<RESEARCHER_MODEL> Hunter](~/workspace/custom-skills/local-xingchi-hunter/SKILL.md)

- Use `muse.skill_search` to find other skills and `muse.connector_search` to find other connectors.

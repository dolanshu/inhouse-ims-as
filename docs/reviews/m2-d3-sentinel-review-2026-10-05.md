<!--
Inhouse-IMS-AS — Copyright 2026 Dolan Shu <dolan.d.shu@gmail.com>, Apache-2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-->

# M2 D3 Redis Sentinel review (2026-10-05)

> **Subject:** D3 engineering slice — `RedisStateStore` Sentinel client wiring  
> **Authority:** [`plan.md`](../plan.md) §5.2 D3; ADR-0002 / ADR-0007

## Object

`platform/src/as_platform/state/redis_store.py`: `from_sentinel`, `redis+sentinel://` in
`from_url`, `load_redis_store_from_env()` (`AS_REDIS_URL` or `AS_REDIS_SENTINEL_HOSTS` +
`AS_REDIS_SENTINEL_MASTER`). Unit tests with fake Sentinel/master client.

## Conclusion

**Pass** for D3 **client wiring** slice. Deployed Sentinel HA topology, failover drills, and
split-brain acceptance remain **O5** / operator scope — not claimed here.

## Verification

```sh
uv run pytest platform/tests/test_redis_sentinel_store.py -m unit -q
make gate
```

## Limits

Not production Sentinel cluster proof; not REQ acceptance; idempotent-write contract unchanged
(contract tests still replay on `FakeRedisClient`).

## Sign-off

- Engineering review recorded: 2026-10-05
- Maintainer sign-off: **pending**

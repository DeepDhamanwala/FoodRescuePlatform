# Rollback Playbook

## When to use this

A bad Person 6 release has shipped to production and needs immediate rollback. Symptoms:
- Analytics endpoints returning 500 errors
- Admin verification workflow broken (NGOs stuck in PENDING)
- Database query performance degradation
- Docker Compose healthcheck failing on `/ready`

---

## Rollback Steps

### 1. Identify the bad release

```bash
# Check current backend container image tag
docker ps --filter "name=cpi_backend" --format "{{.Image}}"

# Check git log for Person 6 changes
git log --oneline --grep="analytics\|admin\|Person 6" -10
```

### 2. Stop the current deployment

```bash
docker-compose down
```

### 3. Roll back the database migration

Person 6 ships with migration `001_initial_schema`. If a later migration (e.g., `002_add_analytics_indexes`) was applied and is causing issues:

```bash
# SSH into DB container or connect via psql
docker exec -it cpi_db psql -U cpi_user -d cpi_db

# Check current migration head
SELECT version_num FROM alembic_version;

# Exit psql, run downgrade from host
cd backend
alembic downgrade -1   # roll back one migration

# Verify
alembic current
```

**Critical:** Only downgrade if the new migration is confirmed as the root cause. Rolling back a migration that other services depend on (e.g., Person 4's `matched_ngo_id` column) will break the entire pipeline.

### 4. Revert to the last known-good Docker Compose tag

If the issue is not migration-related:

```bash
# Option A: revert git commit
git revert <bad_commit_sha>
git push origin main

# Option B: checkout previous commit temporarily
git checkout <last_good_commit>
docker-compose up -d --build
```

### 5. Verify the rollback

```bash
# Health checks
curl http://localhost:8000/health   # should return {"status": "ok"}
curl http://localhost:8000/ready    # should return {"status": "ready", "checks": {...}}

# Smoke-test analytics endpoints (requires admin JWT)
curl -H "Authorization: Bearer <ADMIN_JWT>" http://localhost:8000/api/v1/analytics/overview
# Expected: {"data": {...}, "meta": {"request_id": "..."}}
```

### 6. Post-rollback cleanup

- **Notify the team** in the project channel: "Person 6 module rolled back due to [reason]. Analytics/admin unavailable until fix deployed."
- **Preserve logs** from the bad release: `docker-compose logs backend > rollback_$(date +%Y%m%d_%H%M%S).log`
- **File a post-mortem** issue with:
  - What broke
  - What query/endpoint was affected
  - Root cause (if known)
  - Rollback steps taken
  - Prevention plan

---

## What NOT to roll back

- **Person 1's auth/core tables** — rolling these back breaks login for all users (Persons 2–5).
- **Person 4's matching engine columns** (`donations.matched_ngo_id`, `match_score`, `weights_version_id`) — breaks the entire matching flow.
- **Redis data** — Redis is ephemeral; restarting the redis container is safe and loses no durable state.

---

## Recovery path (after rollback)

1. Fix the bug in a branch: `git checkout -b fix/person6-analytics-issue`
2. Test locally against the full integration test suite: `pytest tests/integration/`
3. PR with explicit "Fixes rollback from [date]" in description
4. Merge only after Person 1 (integration co-lead) reviews and approves
5. Deploy with extra monitoring on analytics query latency

---

## Emergency contacts

- **Person 6 (lead):** analytics + admin module owner
- **Person 1 (co-lead):** database schema owner, can resolve migration conflicts
- **On-call rotation:** check #cpi-oncall Slack channel for current responder

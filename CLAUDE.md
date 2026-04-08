# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

AWS Sandbox Accounts is a system for managing a pool of temporary, leased AWS accounts. Users request time-limited leases; the system claims an available account, creates SSO permissions, and tracks state in DynamoDB. When leases expire or accounts are marked dirty, automated workflows clean them up with aws-nuke and return them to the pool.

## Commands

All apps and tools use uv + Makefile. From any `apps/*` or `tools/*` directory:

```bash
make install   # Install dependencies (uv sync)
make test      # Run Ruff linting
make package   # Build Lambda-deployable zip in build/
```

Running a tool locally:
```bash
cd tools/db-seeder && make test_db    # Seed test DynamoDB table
cd tools/db-seeder && make live_db    # Seed live DynamoDB table
cd tools/lease-manager && make run    # Interactive lease management CLI
cd tools/pool-manager && make run     # Interactive account pool CLI
```

Linting a specific app:
```bash
cd apps/db-client && uv run ruff check db_client
```

## Architecture

### Lambda apps (`apps/`)

- **db-client** — The single database interface. All state mutations go through this Lambda. Actions: `mark_as_dirty`, `fetch_dirty`, `mark_as_available`, `mark_as_failed`, `claim_available_account`, `write_active_lease`, `write_pending_lease`, `fetch_expired_leases`, `remove_leases`.
- **auth-client** — Manages AWS SSO permission sets. Actions: `create_lease`, `remove_leases`. Assumes a role in the Identity Centre account.
- **lease-creator** — Step Functions state machine: claim account → write pending lease → create SSO permission → write active lease.
- **account-manager** — EventBridge Scheduler (hourly) + Step Functions: fetch dirty accounts → trigger account-cleaner for each.
- **account-cleaner** — Runs aws-nuke to reset a dirty account back to a clean state.
- **lease-janitor** — Cleans up expired leases found via DynamoDB TTL scans.

### DynamoDB single-table design

One table per environment: `{environment}-aws-sandbox-accounts-account-pool`. See `docs/table-design.md` for the full entity/key design. State flows for accounts: `available → claimed → dirty → (clean) → available`.

### CLI tools (`tools/`)

Local-only Python CLIs that call the DynamoDB table directly. Not deployed as Lambda functions.

### Infrastructure (`common-resources/`)

CloudFormation stacks for the DynamoDB table (pool-store), DNS, and user pool. All stacks take an `Environment` parameter (`test` or `live`).

### CI/CD

`buildspec.build.yml` drives AWS CodeBuild: installs Python 3.11 + Poetry, runs `make test && make package` per app, uploads artifacts to S3, then `aws cloudformation package` for SAM templates. Pipeline defined in `ci/codepipeline.yml`.

## Key Conventions

- Python 3.11 everywhere; uv for dependency management; all `uv.lock` files committed.
- AWS Lambda Powertools used in Lambda functions for logging and tracing.
- `ruff` is the linter (no pytest — linting only for `make test`).
- Two environments: `test` and `live`. Environment name is passed as a CloudFormation/Lambda parameter.

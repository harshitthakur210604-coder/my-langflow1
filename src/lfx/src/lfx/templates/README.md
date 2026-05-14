# CI/CD Pipeline Templates

Ready-to-use workflow files for the Flow DevOps Toolkit.
Copy the files you need into your project's CI configuration.

## GitHub Actions

| File | Trigger | Secrets needed |
|------|---------|----------------|
| [`github-actions/harxitflow-validate.yml`](github-actions/harxitflow-validate.yml) | PR touching `flows/**/*.json` | None |
| [`github-actions/harxitflow-test.yml`](github-actions/harxitflow-test.yml) | PR touching flows or tests | `HARXITFLOW_STAGING_API_KEY` |
| [`github-actions/harxitflow-push.yml`](github-actions/harxitflow-push.yml) | Push to `main` touching flows | `HARXITFLOW_PROD_API_KEY` |

### Quick start

```bash
mkdir -p .github/workflows
cp github-actions/harxitflow-validate.yml \
   github-actions/harxitflow-test.yml \
   github-actions/harxitflow-push.yml \
   .github/workflows/
```

Configure these in **Settings → Environments**:

**`staging`** environment (used by `harxitflow-test.yml`):
| Name | Type | Value |
|------|------|-------|
| `HARXITFLOW_STAGING_URL` | Variable | `https://staging.harxitflow.example.com` |
| `HARXITFLOW_STAGING_API_KEY` | Secret | your staging API key |

**`production`** environment (used by `harxitflow-push.yml`):
| Name | Type | Value |
|------|------|-------|
| `HARXITFLOW_PROD_URL` | Variable | `https://harxitflow.example.com` |
| `HARXITFLOW_PROD_API_KEY` | Secret | your production API key |
| `HARXITFLOW_PROJECT_NAME` | Variable | `Production Flows` *(optional)* |

Add **Required reviewers** to the `production` environment to gate every deploy
behind a manual approval step.

---

## GitLab CI

| File | Description |
|------|-------------|
| [`gitlab-ci/harxitflow.yml`](gitlab-ci/harxitflow.yml) | Three-stage template: validate → test → deploy |

### Quick start

```bash
mkdir -p .gitlab/ci
cp gitlab-ci/harxitflow.yml .gitlab/ci/
```

Add to your `.gitlab-ci.yml`:

```yaml
include:
  - local: .gitlab/ci/harxitflow.yml
```

Configure these in **Settings → CI/CD → Variables**:

| Variable | Protected | Masked | Description |
|----------|-----------|--------|-------------|
| `HARXITFLOW_STAGING_URL` | ✓ | ✗ | Staging instance URL |
| `HARXITFLOW_STAGING_API_KEY` | ✓ | ✓ | Staging API key |
| `HARXITFLOW_PROD_URL` | ✓ | ✗ | Production instance URL |
| `HARXITFLOW_PROD_API_KEY` | ✓ | ✓ | Production API key |
| `HARXITFLOW_PROJECT_NAME` | ✗ | ✗ | Project folder name *(optional)* |

---

## Shell scripts (`ci/`)

The `shell/` templates (`ci-validate.sh`, `ci-test.sh`, `ci-push.sh`) work with
any CI system (Jenkins, CircleCI, Bitbucket Pipelines, Azure Pipelines, etc.).
They are copied to `ci/` by `lfx init`.

### Environment variables

#### `ci-validate.sh`

| Variable | Default | Description |
|----------|---------|-------------|
| `FLOWS_DIR` | `flows/` | Directory containing flow JSON files |
| `VALIDATE_LEVEL` | `4` | Validation depth (1–4) |
| `VALIDATE_FORMAT` | `text` | Output format: `text` or `json` |
| `LFX_VERSION` | *(latest)* | PEP 508 version specifier for `lfx`, e.g. `>=0.4,<1` or `==1.2.3` |

#### `ci-test.sh`

| Variable | Default | Description |
|----------|---------|-------------|
| `HARXITFLOW_URL` | — | URL of target HarxitFlow instance (Approach A) |
| `HARXITFLOW_API_KEY` | — | API key for target instance (Approach A) |
| `HARXITFLOW_ENV` | — | Environment name from config (Approach B) |
| `HARXITFLOW_ENVIRONMENTS_FILE` | `harxitflow-environments.toml` | Path to environments config (Approach B) |
| `TESTS_DIR` | `tests/` | Directory containing test files |
| `PYTEST_MARKERS` | `integration` | Markers passed to `pytest -m` |
| `PYTEST_ARGS` | — | Extra arguments forwarded verbatim to pytest |
| `SDK_VERSION` | *(latest)* | PEP 508 version specifier for `harxitflow-sdk` |

#### `ci-push.sh`

| Variable | Default | Description |
|----------|---------|-------------|
| `HARXITFLOW_URL` | — | URL of target HarxitFlow instance (Approach A) |
| `HARXITFLOW_API_KEY` | — | API key for target instance (Approach A) |
| `HARXITFLOW_ENV` | — | Environment name from config (Approach B) |
| `HARXITFLOW_ENVIRONMENTS_FILE` | `harxitflow-environments.toml` | Path to environments config (Approach B) |
| `FLOWS_DIR` | `flows/` | Directory containing flow JSON files |
| `HARXITFLOW_PROJECT` | — | Project (folder) name on the remote instance |
| `HARXITFLOW_PROJECT_ID` | — | Project UUID (takes precedence over `HARXITFLOW_PROJECT`) |
| `DRY_RUN` | `false` | Set to `true` to preview without making changes |
| `LFX_VERSION` | *(latest)* | PEP 508 version specifier for `lfx` |

---

## How it all fits together

```
PR opened
  │
  ├── harxitflow-validate  ──── lfx validate flows/ --level 4
  │                           ↳ blocks merge if any flow is malformed
  │
  └── harxitflow-test  ──────── pytest tests/ --harxitflow-env staging
                              ↳ skips gracefully if staging is unavailable

Merge to main
  │
  └── harxitflow-push  ──────── lfx push --dir flows/ --env production
                              ↳ upserts every flow by stable ID
                              ↳ idempotent: safe to re-run
```

## Writing integration tests

Install the testing extra:

```bash
pip install "harxitflow-sdk[testing]"
```

Create `tests/test_flows.py`:

```python
def test_rag_flow(flow_runner):
    response = flow_runner("rag-endpoint", "What is HarxitFlow?")
    assert "HarxitFlow" in response.first_text_output()

async def test_async_flow(async_flow_runner):
    response = await async_flow_runner("my-endpoint", "Hello!")
    assert response.first_text_output() is not None
```

Run locally against staging:

```bash
HARXITFLOW_URL=https://staging.harxitflow.example.com \
HARXITFLOW_API_KEY=<key> \
pytest tests/ -m integration
```

#!/usr/bin/env bash
# ci-push.sh
#
# PURPOSE
#   Push (upsert) HarxitFlow flow JSON files to a remote HarxitFlow instance
#   using `lfx push`.  Stable flow IDs mean re-running always converges.
#
# USAGE
#   chmod +x ci-push.sh
#   export HARXITFLOW_URL=https://staging.harxitflow.example.com
#   export HARXITFLOW_API_KEY=<your-api-key>
#   ./ci-push.sh
#
# ENVIRONMENT VARIABLES — connection (pick one approach)
#
#   Approach A: direct URL + key (simplest)
#     HARXITFLOW_URL        URL of the target HarxitFlow instance.
#     HARXITFLOW_API_KEY    API key for that instance.
#
#   Approach B: named environment from a TOML config
#     HARXITFLOW_ENV                 Name of the environment block.
#                                  e.g. staging  or  production
#     HARXITFLOW_ENVIRONMENTS_FILE   Path to environments TOML.
#                                  Default: harxitflow-environments.toml
#     <api_key_env var>            The env var named in api_key_env inside the
#                                  TOML block.  Must be exported separately.
#
#   The TOML format:
#
#     [environments.staging]
#     url         = "https://staging.harxitflow.example.com"
#     api_key_env  = "HARXITFLOW_STAGING_API_KEY"
#
#     [environments.production]
#     url         = "https://harxitflow.example.com"
#     api_key_env  = "HARXITFLOW_PROD_API_KEY"
#
# ENVIRONMENT VARIABLES — behaviour
#   FLOWS_DIR            Directory containing flow JSON files.
#                        Default: flows/
#   HARXITFLOW_PROJECT     Project (folder) name on the remote instance.
#                        Default: (no project — flows go to the default folder)
#   HARXITFLOW_PROJECT_ID  Project UUID.  Takes precedence over HARXITFLOW_PROJECT.
#   DRY_RUN              Set to "true" to show what would be pushed without
#                        making any changes.  Default: false
#   LFX_VERSION          lfx PEP 508 version specifier suffix appended directly
#                        to the package name, e.g. ">=0.4,<1" or "==1.2.3".
#                        Default: installs latest.
#
# EXIT CODES
#   0  All flows pushed (or dry-run completed) successfully
#   1  One or more flows failed to push
#
# INTEGRATIONS
#   Jenkins:          sh 'ci-push.sh'
#   CircleCI:         - run: bash ci-push.sh
#   Bitbucket:        - bash ci-push.sh
#   Azure Pipelines:  - script: bash ci-push.sh

set -euo pipefail

# ── Configuration ─────────────────────────────────────────────────────────── #

FLOWS_DIR="${FLOWS_DIR:-flows/}"
HARXITFLOW_ENV="${HARXITFLOW_ENV:-}"
HARXITFLOW_ENVIRONMENTS_FILE="${HARXITFLOW_ENVIRONMENTS_FILE:-harxitflow-environments.toml}"
HARXITFLOW_URL="${HARXITFLOW_URL:-}"
HARXITFLOW_API_KEY="${HARXITFLOW_API_KEY:-}"
HARXITFLOW_PROJECT="${HARXITFLOW_PROJECT:-}"
HARXITFLOW_PROJECT_ID="${HARXITFLOW_PROJECT_ID:-}"
DRY_RUN="${DRY_RUN:-false}"
LFX_VERSION="${LFX_VERSION:-}"

# Normalise LFX_VERSION: if it looks like a bare version (starts with a digit),
# prepend "==" so the pip specifier is valid.
if [[ -n "${LFX_VERSION}" && "${LFX_VERSION}" =~ ^[0-9] ]]; then
  LFX_VERSION="==${LFX_VERSION}"
fi

# ── Install lfx ───────────────────────────────────────────────────────────── #

echo "==> Installing lfx${LFX_VERSION:+ ${LFX_VERSION}} ..."
pip install --quiet "lfx${LFX_VERSION}" harxitflow-sdk

# ── Build environments file if using Approach B ───────────────────────────── #

if [[ -n "${HARXITFLOW_ENV}" && ! -f "${HARXITFLOW_ENVIRONMENTS_FILE}" ]]; then
  ENV_UPPER="${HARXITFLOW_ENV^^}"
  ENV_UPPER="${ENV_UPPER//-/_}"
  URL_VAR="HARXITFLOW_${ENV_UPPER}_URL"
  KEY_VAR="HARXITFLOW_${ENV_UPPER}_API_KEY"

  echo "==> Writing ${HARXITFLOW_ENVIRONMENTS_FILE} for environment '${HARXITFLOW_ENV}' ..."
  printf '[environments.%s]\nurl = "%s"\napi_key_env = "%s"\n' \
    "${HARXITFLOW_ENV}" \
    "${!URL_VAR:-}" \
    "${KEY_VAR}" \
    > "${HARXITFLOW_ENVIRONMENTS_FILE}"
  export HARXITFLOW_ENVIRONMENTS_FILE
fi

# ── Build lfx push command ────────────────────────────────────────────────── #

PUSH_CMD=(lfx push --dir "${FLOWS_DIR}")

if [[ -n "${HARXITFLOW_ENV}" ]]; then
  PUSH_CMD+=(--env "${HARXITFLOW_ENV}")
elif [[ -n "${HARXITFLOW_URL}" ]]; then
  PUSH_CMD+=(--target "${HARXITFLOW_URL}")
  [[ -n "${HARXITFLOW_API_KEY}" ]] && PUSH_CMD+=(--api-key "${HARXITFLOW_API_KEY}")
else
  echo "ERROR: set HARXITFLOW_ENV (Approach B) or HARXITFLOW_URL (Approach A)" >&2
  exit 1
fi

if [[ -n "${HARXITFLOW_PROJECT_ID}" ]]; then
  PUSH_CMD+=(--project-id "${HARXITFLOW_PROJECT_ID}")
elif [[ -n "${HARXITFLOW_PROJECT}" ]]; then
  PUSH_CMD+=(--project "${HARXITFLOW_PROJECT}")
fi

[[ "${DRY_RUN}" == "true" ]] && PUSH_CMD+=(--dry-run)

# ── Push ──────────────────────────────────────────────────────────────────── #

echo "==> Pushing flows from ${FLOWS_DIR} ..."
[[ "${DRY_RUN}" == "true" ]] && echo "    (dry run — no changes will be made)"
echo "==> Running: ${PUSH_CMD[*]}"
"${PUSH_CMD[@]}"

echo "==> Done."

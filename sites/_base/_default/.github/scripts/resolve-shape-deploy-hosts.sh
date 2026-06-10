#!/usr/bin/env bash
# Resolve shape deploy hosts for a git tag from .monms/trajectory.json.
# Outputs JSON array: [{"id":"...","siteUrl":"...","systemdUnit":"..."}]
set -euo pipefail

REF="${1:-}"
TRAJ="${2:-.monms/trajectory.json}"

if [[ -z "${REF}" ]]; then
  echo "usage: resolve-shape-deploy-hosts.sh <tag> [trajectory.json]" >&2
  exit 1
fi
if [[ ! -f "${TRAJ}" ]]; then
  echo "trajectory file not found: ${TRAJ}" >&2
  exit 1
fi
if ! command -v jq >/dev/null 2>&1; then
  echo "jq is required" >&2
  exit 1
fi

PREFIX="$(jq -r '.tag.prefix // "v"' "${TRAJ}")"
SEGMENTS="$(jq -r '.tag.segments' "${TRAJ}")"
BODY="${REF#"${PREFIX}"}"

if [[ "${BODY}" == "${REF}" || -z "${BODY}" ]]; then
  echo "tag ${REF} missing prefix ${PREFIX}" >&2
  exit 1
fi

IFS='.' read -r -a PARTS <<< "${BODY}"
if [[ "${#PARTS[@]}" -ne "${SEGMENTS}" ]]; then
  echo "tag ${REF}: want ${SEGMENTS} segments, got ${#PARTS[@]}" >&2
  exit 1
fi

FRONTIER=-1
for i in "${!PARTS[@]}"; do
  if [[ ! "${PARTS[$i]}" =~ ^[0-9]+$ ]]; then
    echo "tag ${REF}: segment ${PARTS[$i]} is not a non-negative integer" >&2
    exit 1
  fi
  if [[ "${PARTS[$i]}" -gt 0 ]]; then
    FRONTIER="${i}"
  fi
done

if [[ "${FRONTIER}" -lt 0 ]]; then
  echo "tag ${REF}: no active stage segment" >&2
  exit 1
fi

jq -c --argjson frontier "${FRONTIER}" '
  [.stages[]
    | select(.shape.mode != "none")
    | select(.shape.tagSegment == $frontier)
    | .hosts[]
    | {id, siteUrl, systemdUnit: (.deploy.systemdUnit // "")}
  ]' "${TRAJ}"

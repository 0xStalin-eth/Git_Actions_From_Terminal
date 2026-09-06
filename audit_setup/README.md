# Audit Setup

Bootstraps an audit workspace by bare-cloning a target repo and creating the standard worktree layout for an engagement.

## Requirements

- `git`
- SSH access to the target repo (or HTTPS)

## Setup

Make the script executable and put it on your PATH (only needed once):
```bash
chmod +x setup-audit.sh
cp setup-audit.sh /usr/local/bin/setup-audit
```

`cp` preserves the executable bit, so no second `chmod` is needed after copying.

## Usage

From any fresh engagement directory:
```bash
mkdir my-engagement && cd my-engagement
setup-audit git@github.com:client/protocol.git
```

## What it does

1. Bare-clones the repo into `.bare`
2. Points `.git` at `.bare` so git commands work from the engagement root
3. Fixes the fetch refspec so remote tracking branches behave like a normal clone
4. Creates the following worktrees:

| Worktree | Branch |
|----------|--------|
| `ManualAudit/` | `audit/Stalin` |
| `Report/` | `report` |
| `Main/` | `main` |
| `Solace/` | `solace` (new, branched from `report`) |
| `Grimoire/` | `grimoire` (new, branched from `audit/Stalin`) |
| `AuditFixes/` | `audit-fixes` (new, branched from `main`) — used to pull mitigations from the client's external repo and push them to `origin` |

## Pulling mitigations from the client's external repo

Scenario: `origin/main` is at the audit commit, and the client has pushed their fixes to a separate branch (e.g. `fixes/audit-round-1`) on their own repo, ahead of `main`. Goal is to land those fixes on your local `audit-fixes` branch and push them to `origin` for the mitigation review.

### One-time: register the external repo

From the engagement root (where `.git` points to `.bare`):
```bash
git remote add external <client-repo-url>
git fetch external
```

The external remote's branches now live under `external/*` — no collision with `origin/*`.

### Each time the client pushes new fixes

```bash
cd AuditFixes/
git fetch external

# Bring the fixes onto audit-fixes.
# --ff-only: only proceed if audit-fixes can be fast-forwarded to the client's
# tip (i.e. our tip is a direct ancestor of theirs). Slides the branch pointer
# forward with no merge commit, so `git diff origin/main..origin/audit-fixes`
# shows exactly the client's fix commits and nothing else. If the histories
# have diverged, git aborts instead of silently creating a merge commit —
# that's a signal to stop and investigate rather than pollute the review diff.


git merge --ff-only external/fixes/audit-round-1
```

### Push to origin for review

Still inside `AuditFixes/`:
```bash
git push -u origin audit-fixes
```

After the first push, subsequent pushes are just `git push`.

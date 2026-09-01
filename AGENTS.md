# Codex Repository Instructions

These instructions apply to the repository root and every descendant path.

## Permanent work-report requirement

Before Codex reports a repository-changing assignment complete, it MUST create
or update a dated Markdown report under `docs/work-reports/` and commit and push
that report with the work whenever the assignment authorizes a push.

The report is the authoritative completion record and MUST contain:

- assignment scope;
- files and behavior changed;
- architecture and repository-boundary decisions;
- branch and known commit identifiers;
- every verification command and its exact result;
- GitHub Actions and pull-request status, with links when available;
- unresolved blockers and deferred work;
- notes affecting sibling repositories; and
- a **Failures and recoveries** section.

For every failed command, test, build, CI run, or abandoned implementation
attempt, the Failures and recoveries section MUST record:

- UTC timestamp when available, otherwise an unambiguous sequence number;
- command or action;
- exit code when available;
- a concise relevant error excerpt;
- root cause;
- corrective action;
- verification result;
- final status (`resolved`, `deferred`, or `blocked`); and
- a GitHub Actions run link when applicable.

Transient failures MUST NOT be omitted. If none occurred, write `None.` Do not
commit enormous raw logs or secrets. Link to external CI logs. If a full local
log is genuinely necessary, sanitize it and store it under
`docs/work-reports/logs/<task-name>/`.

Codex MUST NOT claim completion only in chat and MUST NOT claim completion while
required tests or CI are failing. When a commit cannot contain its own final
hash, identify it as the commit containing the report and rely on Git history
for the self-referential identifier.

# Repository Audit

Read-only review of all nine git repositories across the `Gordonfive` and
`logrusbox` accounts (both confirmed by the owner to be the same person;
`logrusbox` is the org for the Fleet product). Reviewed 2026-08-31. No
secrets or credentials were found committed in any of the nine repos.

Findings below are split into **Needed** — concrete defects, security-adjacent
patterns, or things that are already broken or will break — and **Should
happen** — real improvements worth doing, but nothing is currently on fire.

---

## Needed

1. **`ketchikan-net` — injection-adjacent SQL pattern.**
   `scripts/backend/import-directory-live.py` and
   `import-directory-staging.py` build SQL through a hand-rolled
   `sql_literal()` string-escaper instead of parameterized queries. It
   escapes correctly today, but it's one edge case away from a real SQL
   injection. Replace with parameter binding (e.g. `psycopg`).

2. **`ketchikan-net` — one failing test, out of sync with content.**
   `tests/site-architecture.test.mjs` expects an `<h2>Still growing</h2>`
   heading on `/about/` that the page no longer has. Update the test or the
   page.

3. **`fleet` — literal `\n` text committed instead of real newlines.**
   `docs/STATUS.md:22`, `docs/PROGRAM_ROADMAP.md:42`, and
   `docs/decisions/README.md:9` contain the two characters `\` `n` as text
   rather than an actual line break, breaking rendered markdown. Looks like
   unreviewed generated content pasted in — fix the three files.

4. **`vincent` — unusually high CI action versions, unverified.**
   `.github/workflows/ci.yml` pins `actions/checkout@v7` and
   `actions/setup-python@v7`. Confirm these tags actually exist; if not,
   CI will fail outright on the next run that touches this workflow.

5. **`fleet` — umbrella-level docs haven't caught up to the product split.**
   `AGENTS.md`, `CONTRIBUTING.md`, and `scripts/check_repository.py`'s
   success message all still say "VINCENT Program Repository" /
   "VINCENT program repository validation: PASS", even though `fleet` is
   now the umbrella product name with `vincent` (USB-based installer for
   independent agent workstations) and `cic-station` (resource allocation +
   ChatGPT↔worker communication hub) as its two components. `docs/STATUS.md`
   already reflects the rename; the other files don't.

---

## Should happen

- **`oceanmail-infrastructure`** — the README states a clear no-secrets-in-git
  policy, but there's no `.gitignore` or secret-scanning check yet to back
  it up. Add one once real deploy config starts landing.
- **`ketchikan-net`** — no CI configured; the existing manual
  `validate:project-state` / test suite (103 cases) should run automatically.
- **`ketchikan-net`** — three inconsistent, seemingly orphaned CMS configs
  (`.pages.yml`, `pages.yml`, `admin/config.yml`), one referencing a
  nonexistent `content/posts` collection. Reconcile or remove.
- **`ketchikan-net`** — docs (`AGENTS.md`, `PROJECT_START_HERE.md`) reference
  an `assistant/dev` branch that doesn't exist in this clone or on the
  remote. Confirm whether it was merged/deleted and update the branch-policy
  docs.
- **`ketchikan-net-drupal`** — several custom PHP files pack multiple
  statements per line densely enough to likely fail the project's own
  configured Coder/phpcs standard. Run a lint pass.
- **`bempic`** — `Summary.generation` (`prototype/bempic_proof/operations.py`)
  is overloaded with two unrelated meanings depending on caller (a
  protocol-generation constant vs. an item count). Worth resolving before
  any wire-format freeze.
- **`bempic`** — no direct unit tests for `demo.py` (thin CLI wrapper, low
  risk) or for `model.py`'s upper-bound validation edges (255
  recipients/attachments, u64 boundaries).
- **`bempic`** — the name "BEMPIC" is never expanded anywhere in the repo;
  already tracked in `docs/OPEN-QUESTIONS.md`, still open.
- **`cic-station`, `bempic-reference`, `oceanmail-infrastructure`** — heavy
  documentation-to-code ratio (ADRs/requirements/status docs with zero or
  near-zero implementation). Fine as deliberate up-front planning; worth
  revisiting if code doesn't start following soon.
- **`vincent`** — 4 of 139 tests fail in a sandbox without `ssh-keygen`
  installed; not a code defect, but worth a CI check that the binary is
  actually available in the test environment so a real regression isn't
  masked by the same error.

---

## Resolved, no action needed

- Three repos (`fleet`, `cic-station`, `vincent`) are owned by `logrusbox`
  rather than `Gordonfive` — confirmed by the owner to be their own
  organization, not a provenance concern.
- The sole commit in `vincent` is authored by `jurgen@alaska.earth` —
  confirmed by the owner to be their own address.

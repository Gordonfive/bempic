# Contributing to BEMPIC

Thank you for helping make BEMPIC independently implementable.

## Before proposing a change

Read [`SPECIFICATION.md`](SPECIFICATION.md),
[`docs/REPOSITORY-BOUNDARY.md`](docs/REPOSITORY-BOUNDARY.md), and
[`GOVERNANCE.md`](GOVERNANCE.md). Search
[`GREAT_PARALLEL_WORK.md`](GREAT_PARALLEL_WORK.md) and existing decisions before
inventing a mechanism.

Keep work in the owning repository:

- public semantics, governance, vector definitions, and rationale belong here;
- executable reference work belongs in `bempic-reference`;
- routing/mesh/network behavior belongs in M4P; and
- product/service policy belongs in OceanMail.

Do not remove or move `prototype/` until its roadmap parity gate is complete.

## Pull requests

A focused pull request should:

1. explain the problem and layer owner;
2. classify the change using `GOVERNANCE.md`;
3. quantify encoded byte, persistence, compatibility, security, and resource
   effects where applicable;
4. update normative text, conformance/vector requirements, decisions, and
   changelog together when semantics change;
5. avoid claims unsupported by reproducible evidence; and
6. pass documentation validation, Python tests, demo, and benchmark.

An incompatible proposal includes a decision record based on the existing
numbered examples. A codec proposal additionally includes declared bounds,
precision, maximum encoded sizes, exact-size analysis, canonical parameters,
strict decoder behavior, and vector plans.

## Local verification

From the repository root:

```bash
python -m scripts.validate_docs
python -m unittest prototype.tests.test_proof -v
python -m prototype.demo
python -m prototype.benchmark
```

Do not overwrite the recorded benchmark baseline unless the changed behavior
is intentional and the pull request explains every material difference.

## Licensing

The repository is licensed under Apache-2.0. Unless you explicitly state
otherwise, an intentional contribution submitted for inclusion is provided
under the same license as described in Section 5 of `LICENSE`. Do not submit
third-party source or data unless its license, provenance, notices, and
compatibility are documented.

Use synthetic or clearly redistributable message corpora. Never commit private
mail, credentials, callsigns tied to private accounts, or production user data.

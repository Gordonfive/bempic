# BEMPIC Governance

## Mission

BEMPIC is developed as an independently implementable open protocol for
extreme-efficiency, interruption-tolerant application synchronization.
OceanMail supplies the first production requirements but does not make
proprietary OceanMail components a condition of conformance.

## Roles

- **Contributors** propose issues, text, vectors, reviews, and implementation
  evidence under the repository license.
- **Reviewers** provide subject-matter review. Review alone does not grant merge
  authority.
- **Maintainers** are collaborators with repository merge/release authority.
  Current authority is determined by the protected repository settings rather
  than an easily stale list in this file.
- **Release managers** are maintainers assigned in a release issue to verify
  gates, prepare notes, and create a tag after approval.

Commercial affiliation neither grants nor removes standing. Participants must
disclose a material conflict when it could reasonably affect a protocol or
conformance decision.

## Change classes

1. **Editorial:** wording, links, examples, or formatting with no semantic or
   conformance effect. One maintainer approval is sufficient.
2. **Normative compatible:** clarifies or extends behavior without invalidating
   conformers. Requires a pull request, conformance impact statement, two
   approvals including one maintainer, and passing checks.
3. **Normative incompatible:** changes identity, state, bounds, operation
   meaning, required vectors, compatibility, or encoded bytes. Requires an
   accepted decision record, protocol/codec version analysis, two maintainer
   approvals, and a documented migration path.
4. **Security-sensitive:** affects authentication, confidentiality, integrity,
   replay, parsing limits, downgrade, or disclosure. It receives private
   coordination when necessary and at least one security-focused review before
   public merge.
5. **Release:** changes status, tag gates, changelog, or release artifacts.
   Requires the release procedure below.

Normative changes MUST update the specification, conformance/vector impact, and
changelog together. Implementation behavior in another repository cannot
silently redefine this specification.

## Decision process

The project seeks rough consensus supported by measured byte cost,
interoperability, safety, and implementation evidence. A proposal stays open
long enough for relevant implementers and layer owners to review it. The author
must address substantive objections or record the unresolved tradeoff.

If consensus is not reached, maintainers may decide by simple majority of
non-conflicted maintainers after documenting alternatives and reasons. A tie
means no change. Boundary changes involving M4P should seek upstream M4P review;
silence is not interpreted as approval.

Accepted architectural or incompatible decisions are immutable files under
`docs/decisions/`. A new decision supersedes an old one and links both.

## Registries and extensions

Codec, schema, extension, receipt, and failure-code allocations are made by
reviewed pull request. Experimental allocations must be labeled and may change
during major-zero development. No allocation may reserve an unbounded private
range, weaken core behavior, or capture a generally useful extension for one
vendor.

## Releases

A release manager opens a release PR that links every roadmap gate to evidence,
identifies the exact passing `bempic-reference` commit and vector digest, updates
status and notes, and confirms tests from the proposed commit. Another
maintainer independently checks the gate record.

Tags are signed and annotated when project signing infrastructure is available.
A release tag is never created to make an incomplete gate appear complete. A
broken published release is corrected with a new patch release and changelog;
released tags and vector bundles are not moved or rewritten.

## Security reports

Potential undisclosed vulnerabilities should be reported with GitHub private
vulnerability reporting when enabled. If unavailable, open a minimal issue
requesting a private maintainer contact without publishing exploit details.
Maintainers coordinate disclosure, credit, affected versions, and fixes.

## Conduct

Participation must remain professional, technically focused, and welcoming.
Harassment, threats, discrimination, deliberate disruption, and publication of
private information are unacceptable. Maintainers may hide content or restrict
participation to protect the project and its participants, with an explanation
recorded privately or publicly as appropriate.

## Governance changes

Governance changes use the normative-compatible process unless they alter
maintainer authority or release control, in which case two maintainer approvals
are required. No governance change retroactively alters an accepted license.

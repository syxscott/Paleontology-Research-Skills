## Summary

<!-- One sentence: what does this PR change? -->

## Why

<!-- The user-visible reason. Link to the issue if any. -->

Refs: #

## Type of change

- [ ] 🐛 Bug fix (non-breaking change that fixes an issue)
- [ ] ✨ New feature (non-breaking change that adds capability)
- [ ] 🦕 New sub-skill
- [ ] ⚡ Performance improvement
- [ ] 📚 Documentation only
- [ ] 🔧 Build / CI / tooling
- [ ] 💥 Breaking change (would require users to update their setup)

## Checklist

- [ ] My code follows the style in `CONTRIBUTING.md`
- [ ] I have updated the relevant `SKILL.md` if behavior changed
- [ ] I have updated `CHANGELOG.md` under `## [Unreleased]`
- [ ] I have added tests in `tests/` (or explained why none are needed)
- [ ] All existing tests still pass (`python -m unittest discover tests`)
- [ ] Smoke test passes (`python <script> --help` for every changed script)
- [ ] If I added a new sub-skill, I also:
  - [ ] Added a row to the parent `SKILL.md` routing table
  - [ ] Updated `README.md`
  - [ ] (Optional) Created a `/paleo-<x>` slash command

## Scientific integrity

- [ ] Output JSON cites the data source (`"source"` field)
- [ ] No fabricated taxa, DOIs, ages, or occurrences
- [ ] Network errors are caught and embedded in JSON (no stack traces leak)

## Screenshots / output

<!-- Paste the JSON output or a screenshot showing the new behavior -->

```json

```

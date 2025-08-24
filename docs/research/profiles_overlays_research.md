# Profiles and Overlays — Research Archive

[Research archive of the original content formerly at "ref/2_Profiles and Overlays.md".]

This page preserves the original exploratory notes on contextual Profiles/Overlays that extend a base schema without duplication. It complements the falsification/refinement narrative.

---

# Profiles and Overlays (UFSA v2 – stub)

This short note outlines how Profiles/Overlays will extend the current engine.
It complements `docs/0_...Falsification & Implementation.md` section IV and aligns with the FHIR profiling pattern.

## Purpose

Allow a base structure to be constrained or extended in a given context without duplicating schemas, e.g.:

- Postal vs. geodetic address
- Common‑law vs. civil‑law contract
- Implementation/vendor‑specific tweaks

## Shape (proposed)

- Target: reference to a base structure or scheme element
- Constraints: cardinality flips, additional validations (regex, external authority checks), enums, bounds
- Extensions: add fields/notes that only apply in the profile’s context
- Activation context: labels/conditions describing when to apply (jurisdiction, domain, use‑case)

## Minimal representation (initial)

Profiles can start as simple YAML atop the registry:

```yaml
kind: Profile
apiVersion: ufsa.org/v2.0
metadata:
  name: PostalAddressProfile
  domain: core
  target: core:Address
spec:
  constraints:
    - path: postalCode
      cardinality: required
      validation:
        - type: external
          authority: usps.com/validate
```

## Integration points

- Parsing stays unchanged; profiles are overlays applied post‑normalization
- Emitters may add profile‑annotated variants or output validation hints
- Tracker/plan: tasks to add priority profiles per domain

## Next steps

- Finalize a minimal on‑disk schema and validator
- Add CLI to apply/check profiles over emitted tables
- Pilot with Address and Contract examples from the docs

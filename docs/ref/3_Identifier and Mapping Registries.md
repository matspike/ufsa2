# Identifier and Mapping Registries (UFSA v2 – stub)

This note sketches how UFSA will describe identifier systems and the relationships between them (e.g., FIGI vs. ISIN), as referenced in Docs 0/1.

## Why

- Capture governance, scope, and syntax of identifier systems
- Model equivalence/overlap/hierarchy and contextual preferences
- Make trade‑offs explicit and machine‑readable (regulatory vs. vendor ecosystems)

## IdentifierSystem (proposed)

Fields:

- name (unique)
- governingBody (ISO, OMG, IANA, …)
- concept (what instances it identifies)
- syntax (regex or formal description)
- scope/granularity notes

## Mapping (proposed)

A declarative link between systems:

- systems: ["isin", "figi", …]
- type: equivalentTo | broaderThan | narrowerThan | relatedTo | contextualPreference
- rules (optional): list of contexts and preferred system(s)

Example:

```yaml
kind: Mapping
apiVersion: ufsa.org/v2.0
metadata:
  name: figi-isin-regulatory-mapping
  domain: finance
spec:
  type: contextualPreference
  systems:
    - isin
    - figi
  rules:
    - context: EU-MIFID2-Reporting
      preferred: isin
    - context: Internal-Data-Integration
      preferred: figi
```

## Integration points

- Emitters can surface system metadata in concept_schemes/relations tables or dedicated outputs
- Planners can stage mapping work as tasks tied to contexts (EU reporting vs. internal BI)

## Next steps

- Finalize minimal YAML schemas for IdentifierSystem and Mapping
- Add CLI plumbing and validation
- Pilot FIGI/ISIN, then expand to CUSIP/LEI/EAN/GTIN

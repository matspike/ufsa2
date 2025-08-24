# Registry and Emitters — concise overview

This page explains how UFSA v2 declares inputs and produces outputs. See the research doc for the deep dive and rationale.

## Pointer registry (inputs)

- A declarative list of standards with: id, name, governing body, specification URL, data format, parser module, concept scheme URI.
- Adding a standard = adding one entry.

Supported formats and parsers:

- JSON Schema (FHIR)
- CSV (ISO, IANA)
- RDF (SKOS)
- HTML/Docs scraping (Shopify, OpenFIGI)
- CycloneDX SBOM
- SQL DDL (AST)

## Emitters (outputs)

- Per‑scheme: scheme_name.concepts.{json,csv}
- Global tables: concept_schemes.csv, concepts.csv, semantic_relations.csv
- Specialized: software_components.csv (from SBOM), database_schemas.csv (from SQL AST)

## Contract highlights

- SKOS predicates for relations (broader/narrower/related; exact/close/broad/narrow/relatedMatch)
- Stable scheme_uri and concept identifiers within a minor line
- CSVs are UTF‑8 with headers; duplication minimized

## Links

- Full research doc: [Registry & Emitters — detailed](../research/1_UFSA%20v2.0%20Registry%20and%20Emitter%20Design.md)
- Architecture overview: [Ref 0](./0_Federated%20Schema%20Architecture_%20Falsification%20%26%20Implementation.md)
- Profiles/Overlays: [Ref 2](./2_Profiles%20and%20Overlays.md)
- Identifiers & Mappings: [Ref 3](./3_Identifier%20and%20Mapping%20Registries.md)

# Target Architecture (UFSA v2) — concise overview

This page summarizes the Universal Federated Schema Architecture (UFSA v2) target, with links to the full research document.

## Purpose

- Define a pragmatic, federated approach to interoperability that normalizes diverse public standards into a single SKOS‑based knowledge model and portable tables.
- Keep domain autonomy intact; UFSA provides the connective tissue via normalization and mappings.

## Core ideas

- Declarative over imperative: add a standard by configuration (pointer registry), not code.
- SKOS at the core: ConceptScheme + Concept + mapping predicates (exact/close/broad/narrow/related).
- Pluggable pipeline: fetch → parse → normalize → emit.
- Federated governance: domains own their standards; UFSA stitches them together.

## Pipeline at a glance

1) Pointer registry declares standards and parser modules
2) Parsers ingest native specs (JSON Schema, CSV, RDF, SBOM, SQL DDL)
3) Normalization to SKOS concepts and relations
4) Emitters produce per‑scheme artifacts and consolidated tables

## Outputs

- Per‑scheme JSON/CSV concept dumps
- Global tables: concept_schemes.csv, concepts.csv, semantic_relations.csv
- Specialized: software_components.csv (SBOM), database_schemas.csv (SQL AST)

## Where to go next

- Full research doc: [Architecture — Synthesis, Falsification, Refinement](../research/0_Federated%20Schema%20Architecture_%20Falsification%20%26%20Implementation.md)
- Registry & Emitters overview: [UFSA v2.0 Registry and Emitter Design](./1_UFSA%20v2.0%20Registry%20and%20Emitter%20Design.md)
- Profiles/Overlays: [Ref 2](./2_Profiles%20and%20Overlays.md)
- Identifiers & Mappings: [Ref 3](./3_Identifier%20and%20Mapping%20Registries.md)

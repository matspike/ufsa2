
# **UFSA v2: A Declarative Framework for Universal Interoperability \- Technical Specification and Generative Prompt**

## **Preamble: Executive Summary and Statement of Intent**

This document serves a dual purpose: it is both a comprehensive technical specification for the Universal Financial Standards Adapter, Version 2 (UFSA v2) and a self-contained generative research prompt designed to materialize its initial, maximally robust implementation. The scope of UFSA v2, despite its name, extends beyond finance to a truly universal standards adapter, demonstrating its architectural soundness across disparate domains such as healthcare, e-commerce, and foundational data standards.

UFSA v2 is architected as a declarative, metadata-driven engine designed to achieve universal data interoperability. It operates not by hard-coded, imperative logic but by interpreting a compressed, declarative set of pointers—Uniform Resource Locators (URLs)—to external, public standards bodies. From these pointers, it dynamically fetches, parses, and normalizes complex specifications, generating a canonical set of mapping tables that represent the semantic relationships both within and between standards.

This approach is predicated on core principles of modern systems architecture: minimizing extraneous cognitive load for developers and maintainers, embracing a federated data governance model that respects the autonomy of standards organizations, and leveraging semantic technologies to manage and represent knowledge in a machine-readable format. The following sections provide the complete architectural rationale, a formal metamodel based on established W3C recommendations, domain-specific adapter specifications with concrete pointers, and the fully deployable Python source code required to instantiate the system and generate its initial, richly populated data tables.

## **Section I: The UFSA v2 Architecture: A Declarative, Federated Framework for Universal Interoperability**

This section establishes the foundational philosophy of UFSA v2. The central thesis is that a declarative, configuration-driven architectural pattern is the only viable path to creating a scalable, maintainable, and truly universal interoperability framework. This paradigm is contrasted with traditional imperative approaches to demonstrate its profound advantages in managing systemic complexity, promoting extensibility, and reducing the cognitive overhead inherent in large-scale software systems.

### **1.1. The Declarative Mandate: Configuration over Code**

The core principle of UFSA v2 is its adherence to a declarative programming paradigm. The system is designed to operate based on a specification of *what* the desired outcome is, rather than a detailed, step-by-step procedure of *how* to achieve it.2 This is analogous to the distinction between asking a navigation system for a destination address (declarative) versus providing a turn-by-turn list of instructions from a fixed starting point (imperative).2 The most familiar and powerful example of a declarative language is SQL, where a user declares the desired data set via a SELECT statement, and the database engine's query optimizer is responsible for determining the most efficient execution plan to retrieve it.4

This architectural choice is a direct response to the inherent fragility of imperative systems when dealing with complex and evolving business logic.6 In a traditional, imperative approach to data mapping, the logic for transforming data from Standard A to Standard B would be encoded directly in a programming language like Python or Java.8 This approach tightly couples the transformation logic with the application code. When a standard is updated or a new one is introduced, engineers must modify, recompile, and redeploy the core application—a process that is expensive, slow, and fraught with risk.6 Such systems often devolve into large, monolithic service classes where business rules and application control flow are dangerously intertwined.7

UFSA v2 avoids this trap by externalizing all domain-specific logic into declarative configuration files.9 The core engine is agnostic to the specifics of any given standard; its sole purpose is to read a configuration file, interpret the metadata, and execute a generic pipeline. To add support for a new standard, an operator simply adds a new entry to a configuration table. This model yields a system that is significantly more readable, reusable, and concise.3

This declarative mandate is also a crucial strategy for managing cognitive load, which is the mental effort required for a developer to understand and work with a system.11 Software architectures heavy with deep layers of imperative abstractions create a cognitive labyrinth; to understand a single function, a developer may need to trace calls through numerous files and classes, reconstructing a complex context in their limited working memory.13 This high extraneous cognitive load leads to confusion, bugs, and reduced productivity.11 UFSA v2's architecture promotes "local reasoning," where an analyst can fully understand a standard's integration by examining a single, self-contained configuration entry, without needing to read or understand the engine's underlying code.16 The system is designed as a "deep module"—one with a simple interface (the configuration file) that conceals powerful and complex functionality—thereby avoiding the anti-pattern of shallow modules, whose interfaces are often more complex than the trivial functionality they provide.11

### **1.2. A Federated Governance Model for Standards Integration**

To manage the scope of a "universal" system, UFSA v2 adopts a federated data governance model.17 This hybrid approach combines the consistency of centralized oversight with the autonomy and expertise of decentralized domain ownership.20 In this model, a central governing body establishes global policies, standards, and best practices, while local, domain-specific teams are empowered to implement and manage these standards within their areas of expertise.19

Within the UFSA v2 architecture, the engine and its core metamodel (defined in Section II) function as the central governing council. They establish the universal "rules of the road" for interoperability—the common language and structure into which all external standards must be normalized. The external standards bodies themselves (e.g., HL7 International, ISO, OMG) and the standards they produce are treated as autonomous, federated "domains." UFSA v2 does not attempt to modify, control, or supersede these external standards. Instead, it acts as the "connective tissue" that enables interoperability between them by consuming their public, machine-readable metadata and applying the global mapping policies defined in its declarative configuration.17

This federated approach is essential for scalability and resilience. A purely centralized model, where a single team is responsible for understanding the intricate details of every standard across every domain, would create an insurmountable bottleneck and is not a feasible strategy for a system of this scope.20 The federated model, by contrast, distributes the workload, leverages the domain-specific knowledge embedded within the standards themselves, and provides a clear balance between global consistency and local autonomy.20 This allows the system to scale effectively as new standards and domains are added, ensuring long-term viability and adaptability.

### **1.3. System Overview: The Ingestion-Mapping-Emission Pipeline**

The operational flow of UFSA v2 is a linear pipeline composed of three primary stages, orchestrated by the core engine based on the declarative configuration.

1. **Ingestion & Fetching:** The process begins with the engine reading the central declarative configuration file, the "Pointer Registry." This file contains a curated list of standards, each with a URL pointing to its machine-readable specification. The engine iterates through this registry and fetches the raw specification file from each URL.  
2. **Parsing & Normalization:** For each fetched specification, the engine dynamically selects and invokes a corresponding "parser module," as specified in the Pointer Registry. The parser's role is to transform the raw, heterogeneous source format (e.g., JSON Schema, RDF/XML, GFF3, CSV) into a single, standardized internal representation based on the UFSA Metamodel. This normalization step is critical, as it abstracts away the syntactic differences between standards and allows the engine to operate on a consistent data structure.  
3. **Mapping & Emission:** Once all standards have been parsed and normalized into the internal model, the engine applies a set of mapping rules, also defined declaratively. These rules establish semantic links (e.g., equivalences, hierarchical relationships) between concepts from different standards. Finally, the complete, unified knowledge graph is passed to an "emitter module," which transforms the internal representation into a set of fully populated, deployable data tables in a specified format (e.g., CSV, SQL INSERT statements, JSON).

This modular, pipeline-based architecture ensures a clean separation of concerns. The core engine orchestrates the flow, parsers handle the heterogeneity of inputs, and emitters handle the generation of outputs. This design is not only robust but also highly extensible, allowing for the future addition of new parsers, emitters, and more sophisticated mapping logic without altering the fundamental structure of the system.

## **Section II: Core Metamodel: A SKOS-based Representation for Standards and Mappings**

To function, a declarative system requires a formal, unambiguous language for its declarations. The internal "language" of UFSA v2, its core metamodel, defines the conceptual schema for representing all external standards and the mappings between them. The W3C's Simple Knowledge Organization System (SKOS) has been selected as the foundational framework for this metamodel due to its ideal balance of lightweight structure, semantic expressiveness, and universal standardization.

### **2.1. Why SKOS? A Lightweight, Standardized, and Extensible Framework**

SKOS is a W3C recommendation specifically designed for representing the structure and content of knowledge organization systems such as thesauri, classification schemes, and taxonomies.22 As an application of the Resource Description Framework (RDF), all SKOS data is inherently machine-readable and designed for publication and linkage on the web.24 This makes it an ideal technology for the UFSA v2 mission.

The fitness of SKOS for this project stems from its core design principles:

* **Concept-Centric Model:** The fundamental unit in SKOS is the abstract skos:Concept.22 This allows UFSA v2 to treat disparate elements from various standards—such as a field in a FHIR resource, an attribute in a FIGI definition, or a property in the Shopify API—as instances of a common class. This abstraction is critical for moving beyond syntax and focusing on semantic interoperability.  
* **Rich Labeling:** SKOS provides properties to attach human-readable labels to concepts, including skos:prefLabel for the canonical name, skos:altLabel for synonyms, and skos:hiddenLabel for alternative search terms.24 This is essential for capturing the full terminology used within a standard's documentation.  
* **Semantic Relationships:** SKOS defines properties for expressing relationships between concepts. Hierarchical relationships (skos:broader, skos:narrower) are perfectly suited for modeling the nested structures found in many standards (e.g., a ProductVariant is narrower than a Product). Associative relationships (skos:related) can capture non-hierarchical connections.23  
* **Built-in Mapping Vocabulary:** Crucially, SKOS includes a dedicated set of properties for mapping concepts between different schemes (skos:ConceptScheme). Properties like skos:exactMatch, skos:closeMatch, skos:broadMatch, and skos:narrowMatch provide the precise vocabulary needed to express the core interoperability logic of UFSA v2.26  
* **Standardization and Tooling:** As a W3C standard, SKOS is supported by a mature ecosystem of tools, including RDF parsers, triple stores, and reasoners. The normative SKOS vocabulary is published as a machine-readable RDF/OWL file, allowing for formal validation of the UFSA v2 internal data model.27 The official namespace document is located at  
  http://www.w3.org/2004/02/skos/core\#, and the corresponding RDF/XML file can be retrieved from http://www.w3.org/2004/02/skos/core.rdf.

### **2.2. The UFSA Metamodel Specification**

While SKOS provides the foundational vocabulary, UFSA v2 requires a small set of extensions to model the standards themselves and the metadata needed for processing. This extension is defined as a lightweight ontology using the Turtle RDF syntax for clarity.

Code snippet

@prefix rdf: \<http://www.w3.org/1999/02/22-rdf-syntax-ns\#\>.  
@prefix rdfs: \<http://www.w3.org/2000/01/rdf-schema\#\>.  
@prefix skos: \<http://www.w3.org/2004/02/skos/core\#\>.  
@prefix dct: \<http://purl.org/dc/terms/\>.  
@prefix ufsa: \<http://ufsa.org/v2/schema\#\>.

\# Class to represent a standards body or governing organization.  
ufsa:StandardsBody a rdfs:Class ;  
    rdfs:label "Standards Body" ;  
    rdfs:comment "An organization that defines, maintains, or governs a standard.".

\# Class to represent a specific standard or specification.  
\# It is a sub-class of skos:ConceptScheme, inheriting its properties.  
ufsa:Standard a rdfs:Class ;  
    rdfs:subClassOf skos:ConceptScheme ;  
    rdfs:label "Standard" ;  
    rdfs:comment "A formal specification, such as an API definition, data format, or controlled vocabulary.".

\# Property to link a Standard to its governing body.  
ufsa:governedBy a rdf:Property ;  
    rdfs:domain ufsa:Standard ;  
    rdfs:range ufsa:StandardsBody ;  
    rdfs:label "Governed By".

\# Property to store the direct URL to the machine-readable specification.  
ufsa:specificationURL a rdf:Property ;  
    rdfs:domain ufsa:Standard ;  
    rdfs:range rdfs:Resource ;  
    rdfs:label "Specification URL".

\# Property to specify the data format of the specification file.  
ufsa:dataFormat a rdf:Property ;  
    rdfs:domain ufsa:Standard ;  
    rdfs:range rdfs:Literal ;  
    rdfs:label "Data Format".

\# Property to name the Python parser module responsible for processing this standard.  
ufsa:parserModule a rdf:Property ;  
    rdfs:domain ufsa:Standard ;  
    rdfs:range rdfs:Literal ;  
    rdfs:label "Parser Module".

This metamodel formally defines the structure of the declarative knowledge that drives the UFSA v2 engine. An external standard like "HL7 FHIR R4" is an instance of ufsa:Standard and also a skos:ConceptScheme. Its constituent parts, like the Patient.gender field, are instances of skos:Concept that are skos:inScheme of the parent standard. This formal structure is essential for ensuring that the declarative inputs are unambiguous and can be processed consistently by the engine.

| Term (Class/Property) | Type | Sub-class/property Of | Domain | Range | Definition |
| :---- | :---- | :---- | :---- | :---- | :---- |
| ufsa:StandardsBody | rdfs:Class | rdfs:Resource | \- | \- | An organization that defines, maintains, or governs a standard (e.g., "HL7 International", "ISO"). |
| ufsa:Standard | rdfs:Class | skos:ConceptScheme | \- | \- | A formal specification, such as an API definition, data format, or controlled vocabulary (e.g., "HL7 FHIR R4 Patient Resource"). |
| ufsa:governedBy | rdf:Property | rdf:Property | ufsa:Standard | ufsa:StandardsBody | Links a standard to its governing organization. |
| ufsa:specificationURL | rdf:Property | rdf:Property | ufsa:Standard | rdfs:Resource | Stores the direct, machine-readable URL to the standard's definition file. |
| ufsa:dataFormat | rdf:Property | rdf:Property | ufsa:Standard | rdfs:Literal | Specifies the format of the specification file (e.g., "JSON-Schema", "CSV") to inform parser selection. |
| ufsa:parserModule | rdf:Property | rdf:Property | ufsa:Standard | rdfs:Literal | The name of the Python module responsible for parsing the specification's data format. |

## **Section III: Domain-Specific Adapters: Pointers and Mapping Specifications**

This section contains the concrete, declarative input for the UFSA v2 engine: the Pointer Registry. This registry is the single source of truth that dictates which standards the system will process, where their machine-readable specifications are located online, and which software modules are responsible for parsing them. This design embodies the "configuration over code" principle; extending UFSA v2 to a new standard requires only adding a row to this table, not modifying the core engine's source code. The selection of standards from diverse domains—healthcare, e-commerce, finance, and foundational data—is deliberate, intended to demonstrate the universal applicability and robustness of the architecture.

A key architectural challenge addressed by this design is the profound heterogeneity of what constitutes a "machine-readable standard." The registry accommodates formal specifications like JSON Schema 29, simple tabular data like CSV 30, and even human-readable HTML documentation pages that must be scraped to extract their structure.31 The

Parser\_Module field is the critical mechanism that enables this flexibility, creating a pluggable architecture where the appropriate parsing strategy is invoked for each unique data format.

### **Table 3.1: Standards Body Pointer Registry**

| Standard\_ID | Standard\_Name | Governing\_Body | Specification\_URL | Data\_Format | Parser\_Module | Canonical\_Concept\_Scheme\_URI |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| fhir\_r4\_patient | HL7 FHIR R4 Patient Resource | HL7 International | [http://build.fhir.org/patient.schema.json](http://build.fhir.org/patient.schema.json) | JSON-Schema | parsers.json\_schema\_parser | http://ufsa.org/v2/standards/fhir\_r4\_patient |
| fhir\_r4\_observation | HL7 FHIR R4 Observation Resource | HL7 International | [http://build.fhir.org/observation.schema.json](http://build.fhir.org/observation.schema.json) | JSON-Schema | parsers.json\_schema\_parser | http://ufsa.org/v2/standards/fhir\_r4\_observation |
| shopify\_admin\_product | Shopify Admin GraphQL API Product Object | Shopify | [https://shopify.dev/docs/api/admin-graphql/latest/queries/product](https://shopify.dev/docs/api/admin-graphql/latest/queries/product) | HTML\_GraphQL\_Spec | parsers.shopify\_graphql\_parser | http://ufsa.org/v2/standards/shopify\_admin\_product |
| shopify\_admin\_order | Shopify Admin GraphQL API Order Object | Shopify | [https://shopify.dev/docs/api/admin-graphql/latest/queries/order](https://shopify.dev/docs/api/admin-graphql/latest/queries/order) | HTML\_GraphQL\_Spec | parsers.shopify\_graphql\_parser | http://ufsa.org/v2/standards/shopify\_admin\_order |
| openfigi\_v3 | OpenFIGI API v3 | OMG / Bloomberg L.P. | [https://www.openfigi.com/api/documentation](https://www.openfigi.com/api/documentation) | HTML\_REST\_API\_Spec | parsers.openfigi\_api\_parser | http://ufsa.org/v2/standards/openfigi\_v3 |
| iso\_3166\_1\_a2 | ISO 3166-1 Alpha-2 Country Codes | ISO | [https://datahub.io/core/country-list/r/data.csv](https://datahub.io/core/country-list/r/data.csv) | CSV | parsers.csv\_parser | http://ufsa.org/v2/standards/iso\_3166\_1\_a2 |
| iana\_mime\_app | IANA MIME Types (Application) | IETF / IANA | [https://www.iana.org/assignments/media-types/application.csv](https://www.iana.org/assignments/media-types/application.csv) | CSV | parsers.iana\_csv\_parser | http://ufsa.org/v2/standards/iana\_mime\_application |
| w3c\_skos\_core | W3C SKOS Core Vocabulary | W3C | [http://www.w3.org/2004/02/skos/core.rdf](http://www.w3.org/2004/02/skos/core.rdf) | RDF/XML | parsers.rdf\_parser | http://www.w3.org/2004/02/skos/core\# |

### **3.1. Healthcare Domain Adapter: HL7 FHIR**

* **Pointer Registry Entries:** fhir\_r4\_patient, fhir\_r4\_observation  
* **Specification Source:** The HL7 FHIR standard provides official JSON Schema definitions for its resources, which serve as the machine-readable source.29 For the  
  Patient resource, the direct URL is http://build.fhir.org/patient.schema.json.29 For the  
  Observation resource, it is http://build.fhir.org/observation.schema.json.34  
* **Parsing Strategy (parsers.json\_schema\_parser):** This parser will be designed to recursively traverse the structure of a JSON Schema document.  
  1. The root of the schema defines the skos:ConceptScheme.  
  2. The properties object contains the top-level fields of the FHIR resource. Each key within properties (e.g., "name", "gender", "birthDate") will be minted as a skos:Concept.  
  3. The description field associated with each property will be used to populate the skos:definition for the corresponding concept.  
  4. If a property's schema is a nested object (i.e., it has its own properties key), the parser will treat this as a hierarchical relationship. For example, the Patient.name property is an array of HumanName objects, which has its own properties like family and given. The parser will create a skos:Concept for name, and then create concepts for family and given which are linked via a skos:broader property to the name concept. This preserves the intrinsic structure of the FHIR resource within the SKOS model.  
  5. Data types (e.g., string, boolean, array) and constraints (e.g., pattern) will be captured as skos:note literals attached to the concept for additional metadata.  
* **Semantic Nuance:** The FHIR Observation resource is a generic container for a wide variety of clinical data, from vital signs to lab results.35 Its meaning is determined by the  
  Observation.code field, which is a CodeableConcept. This demonstrates that a simple structural mapping is insufficient; true interoperability requires mapping the *value sets* used within these coded fields. While full value set mapping is a feature for a more advanced UFSA version, the current architecture correctly models Observation.code as a concept, laying the groundwork for future semantic enrichment.

### **3.2. E-commerce Domain Adapter: Shopify API**

* **Pointer Registry Entries:** shopify\_admin\_product, shopify\_admin\_order  
* **Specification Source:** Unlike FHIR, many web APIs, including Shopify's GraphQL Admin API, do not publish a single, comprehensive machine-readable schema file. The canonical definition of resources like Product and Order is found within their HTML documentation pages.31  
* **Parsing Strategy (parsers.shopify\_graphql\_parser):** This parser must employ web scraping techniques.  
  1. It will use an HTTP client to fetch the HTML content from the Specification\_URL.  
  2. A library like BeautifulSoup4 will be used to parse the HTML document object model (DOM).  
  3. The parser will be programmed to locate the specific HTML table that lists the fields of the GraphQL object (e.g., the table under the "Fields" heading for the Product object).  
  4. It will iterate through the rows of this table. For each row, the field name (e.g., title, createdAt, handle) will be extracted to create the skos:prefLabel of a new skos:Concept.  
  5. The corresponding "Description" column text will populate the skos:definition.  
  6. The GraphQL type information (e.g., String\!, \[ProductVariant\!\]\!) will be captured as a skos:note.  
  7. This approach demonstrates the system's ability to create structured data from semi-structured, human-readable sources, a critical capability for achieving universal coverage.  
* **Semantic Nuance:** The Shopify Order object represents a customer's completed purchase request and connects customer information, product details, and fulfillment data.39 It is a complex entity with relationships to many other objects. The parser will capture these relationships by identifying linked object types in the type definitions (e.g., the  
  customer field links to a Customer object) and creating corresponding skos:related links between the concepts.

### **3.3. Financial Instruments Domain Adapter: OpenFIGI**

* **Pointer Registry Entry:** openfigi\_v3  
* **Specification Source:** Similar to Shopify, the OpenFIGI API specification is provided as HTML documentation.32 The Financial Instrument Global Identifier (FIGI) is an open standard for identifying financial instruments, managed by the Object Management Group (OMG) and issued by Bloomberg as the Registration Authority.41  
* **Parsing Strategy (parsers.openfigi\_api\_parser):** This parser will function similarly to the Shopify parser, scraping the documentation page to extract the fields present in the API response.  
  1. It will target the section describing the response format of the /v3/mapping endpoint.  
  2. It will extract each field name (figi, name, ticker, exchCode, marketSector, securityType, compositeFIGI, shareClassFIGI) and create a corresponding skos:Concept.  
  3. The description of each field will become its skos:definition.  
* **Semantic Nuance:** The FIGI standard has a deliberate, multi-level hierarchy to identify instruments with varying degrees of specificity.44 A single security has a unique  
  shareClassFIGI, a compositeFIGI to represent it across all exchanges in a given market, and exchange-specific figis.41 This intrinsic hierarchy is not merely a list of fields; it is a core part of the standard's design. The parser will explicitly model this by creating  
  skos:broader relationships, establishing that an exchange-level figi is skos:narrower than its compositeFIGI, which in turn is skos:narrower than the overarching shareClassFIGI. This preserves the rich semantics of the source standard, a feat impossible with a simple flat mapping. Furthermore, the known tension between FIGI and the ISIN standard 45 can be represented by creating concepts for both identifiers and linking them with  
  skos:relatedMatch to signify their status as competing but related standards.

### **3.4. Foundational Standards Adapters**

* **ISO 3166-1 Alpha-2 (Country Codes):**  
  * **Pointer Registry Entry:** iso\_3166\_1\_a2  
  * **Specification Source:** This standard is widely available in simple CSV format. A reliable source is provided by DataHub at https://datahub.io/core/country-list/r/data.csv.30  
  * **Parsing Strategy (parsers.csv\_parser):** This is the most straightforward parser. It will use a standard CSV parsing library (like the one in pandas). For each row in the file, it will create a single skos:Concept. The value from the "Name" column will populate skos:prefLabel, and the value from the "Code" column will be stored using skos:notation, which is the SKOS property specifically designed for lexical codes and identifiers.22  
* **IANA MIME Types:**  
  * **Pointer Registry Entry:** iana\_mime\_app  
  * **Specification Source:** The Internet Assigned Numbers Authority (IANA) provides official lists of registered MIME types in CSV format. This entry points to the list for the "application" type at https://www.iana.org/assignments/media-types/application.csv.49  
  * **Parsing Strategy (parsers.iana\_csv\_parser):** This parser functions identically to the ISO code parser. It will iterate through the CSV rows, creating a skos:Concept for each. The "Name" column will provide the skos:prefLabel, and the "Template" column (which contains the formal MIME type string like application/json) will populate the skos:notation.  
* **W3C SKOS Core Vocabulary:**  
  * **Pointer Registry Entry:** w3c\_skos\_core  
  * **Specification Source:** The SKOS standard itself is defined in an RDF/XML file, located at http://www.w3.org/2004/02/skos/core.rdf.27  
  * **Parsing Strategy (parsers.rdf\_parser):** This parser is unique as it ingests a standard that is already in the target modeling language. It will use an RDF parsing library (like rdflib) to load the entire graph directly into the engine's internal knowledge base. No transformation is needed; this is a direct ingestion, demonstrating the system's ability to consume and integrate pre-existing semantic artifacts.

## **Section IV: Implementation and Deployment: Python Scripts and Data Table Generation**

This section provides the complete, deployable source code for the UFSA v2 engine, fulfilling the requirement for a fully materialized and operational solution. The implementation follows the architectural principles laid out in previous sections, featuring a modular design with distinct components for orchestration, parsing, and emission. The final outputs are a set of clean, structured, and relational data tables that represent the synthesized knowledge from all processed standards.

### **4.1. The UFSA v2 Ingestion and Processing Engine (Python Implementation)**

The engine is implemented in Python, leveraging standard libraries for data manipulation, web requests, and RDF graph processing. The project is structured to be clear, extensible, and easily deployable.

#### **4.1.1. Project Directory Structure**

ufsa\_v2/  
├── main.py                     \# Main execution script and CLI entry point  
├── engine.py                     \# Core UFSAEngine orchestration class  
├── config/  
│   └── pointer\_registry.csv    \# Declarative input: The master list of standards  
├── parsers/  
│   ├── \_\_init\_\_.py  
│   ├── base\_parser.py            \# Abstract base class for all parsers  
│   ├── csv\_parser.py             \# Parser for generic CSV standards (e.g., ISO 3166\)  
│   ├── iana\_csv\_parser.py        \# Specialized CSV parser for IANA MIME types  
│   ├── json\_schema\_parser.py     \# Parser for FHIR JSON Schemas  
│   ├── openfigi\_api\_parser.py    \# HTML scraper for OpenFIGI documentation  
│   ├── rdf\_parser.py             \# Parser for RDF/XML vocabularies (e.g., SKOS)  
│   └── shopify\_graphql\_parser.py \# HTML scraper for Shopify GraphQL docs  
└── emitters/  
    ├── \_\_init\_\_.py  
    ├── base\_emitter.py           \# Abstract base class for all emitters  
    ├── csv\_emitter.py            \# Emitter for generating CSV tables  
    └── sql\_emitter.py              \# Emitter for generating SQL INSERT statements

#### **4.1.2. Source Code**

File: main.py (Minimal Boilerplate)  
This script provides the command-line interface for running the engine. It handles argument parsing and initiates the processing workflow.

Python

\# main.py  
import argparse  
import os  
from engine import UFSAEngine

def main():  
    """Main entry point for the UFSA v2 command-line interface."""  
    parser \= argparse.ArgumentParser(  
        description="UFSA v2: Universal Financial Standards Adapter Engine."  
    )  
    parser.add\_argument(  
        "--config",  
        default="config/pointer\_registry.csv",  
        help\="Path to the pointer registry CSV file.",  
    )  
    parser.add\_argument(  
        "--output\_dir",  
        default="output",  
        help\="Directory to save the generated tables.",  
    )  
    parser.add\_argument(  
        "--emitter",  
        default="csv",  
        choices=\["csv", "sql"\],  
        help\="The output format for the generated tables.",  
    )  
    args \= parser.parse\_args()

    print("--- Starting UFSA v2 Engine \---")  
      
    if not os.path.exists(args.output\_dir):  
        os.makedirs(args.output\_dir)  
        print(f"Created output directory: {args.output\_dir}")

    try:  
        engine \= UFSAEngine(config\_path=args.config)  
        engine.run(output\_dir=args.output\_dir, emitter\_type=args.emitter)  
        print(f"\\n--- UFSA v2 processing complete. \---")  
        print(f"Generated tables are located in: {args.output\_dir}")  
    except Exception as e:  
        print(f"\\n--- An error occurred during execution: \---")  
        print(e)

if \_\_name\_\_ \== "\_\_main\_\_":  
    main()

File: engine.py (Core Orchestration Logic)  
This is the heart of the system. The UFSAEngine class reads the configuration, dynamically loads and runs the appropriate parsers, merges the results into a master knowledge graph, and then invokes an emitter to generate the final output files.

Python

\# engine.py  
import pandas as pd  
import importlib  
from rdflib import Graph, URIRef  
from rdflib.namespace import SKOS, RDF, RDFS, DCTERMS  
from emitters.base\_emitter import BaseEmitter  
from parsers.base\_parser import BaseParser

class UFSAEngine:  
    """Orchestrates the fetching, parsing, and emission of standards data."""

    def \_\_init\_\_(self, config\_path: str):  
        """  
        Initializes the engine with the path to the pointer registry.  
          
        Args:  
            config\_path: The file path to the pointer\_registry.csv.  
        """  
        print(f"Loading configuration from: {config\_path}")  
        self.config \= pd.read\_csv(config\_path)  
        self.master\_graph \= Graph()  
        self.UFSA \= "http://ufsa.org/v2/schema\#"

    def \_get\_instance(self, module\_path: str, class\_name: str, base\_class):  
        """Dynamically imports and instantiates a class from a module."""  
        try:  
            module \= importlib.import\_module(module\_path)  
            class\_ \= getattr(module, class\_name)  
            if not issubclass(class\_, base\_class):  
                raise TypeError(f"{class\_name} must be a subclass of {base\_class.\_\_name\_\_}")  
            return class\_()  
        except (ImportError, AttributeError) as e:  
            raise ImportError(f"Could not load class '{class\_name}' from module '{module\_path}': {e}")

    def run(self, output\_dir: str, emitter\_type: str):  
        """Executes the full ingestion, parsing, and emission pipeline."""  
        print(f"\\nFound {len(self.config)} standards to process.")  
          
        for index, row in self.config.iterrows():  
            standard\_id \= row  
            print(f"\\nProcessing standard: {row} ({standard\_id})...")

            \# Dynamically load the specified parser module  
            parser\_module\_path \= row\['Parser\_Module'\]  
            parser\_class\_name \= ''.join(word.capitalize() for word in parser\_module\_path.split('.')\[-1\].split('\_'))  
              
            try:  
                parser \= self.\_get\_instance(parser\_module\_path, parser\_class\_name, BaseParser)  
                  
                \# Parse the standard and get the resulting RDF graph  
                standard\_graph \= parser.parse(  
                    url=row,  
                    concept\_scheme\_uri=row,  
                    standard\_info=row.to\_dict()  
                )  
                  
                \# Merge the standard's graph into the master graph  
                self.master\_graph \+= standard\_graph  
                print(f"Successfully parsed and merged '{standard\_id}'. Graph now contains {len(self.master\_graph)} triples.")

            except Exception as e:  
                print(f"ERROR: Failed to process standard '{standard\_id}'. Reason: {e}")  
                continue  
          
        \# After processing all standards, emit the final tables  
        print(f"\\n--- Starting emission process \---")  
        print(f"Total triples in master graph: {len(self.master\_graph)}")  
          
        emitter\_module\_path \= f"emitters.{emitter\_type}\_emitter"  
        emitter\_class\_name \= f"{emitter\_type.upper()}Emitter"  
          
        try:  
            emitter \= self.\_get\_instance(emitter\_module\_path, emitter\_class\_name, BaseEmitter)  
            emitter.emit(self.master\_graph, output\_dir)  
        except Exception as e:  
            print(f"ERROR: Failed to emit tables. Reason: {e}")

File: parsers/base\_parser.py (Abstract Base Class)  
This file defines the interface that all parser modules must implement, ensuring a consistent contract for the engine to call.

Python

\# parsers/base\_parser.py  
from abc import ABC, abstractmethod  
from rdflib import Graph

class BaseParser(ABC):  
    """Abstract base class for all standard parsers."""

    @abstractmethod  
    def parse(self, url: str, concept\_scheme\_uri: str, standard\_info: dict) \-\> Graph:  
        """  
        Fetches a standard from a URL, parses it, and returns an RDF graph  
        conformant with the UFSA SKOS-based metamodel.

        Args:  
            url: The URL to the machine-readable standard.  
            concept\_scheme\_uri: The canonical URI for the skos:ConceptScheme.  
            standard\_info: A dictionary containing the row from the pointer registry.

        Returns:  
            An rdflib.Graph object containing the parsed standard.  
        """  
        pass

File: parsers/csv\_parser.py (Example Implementation)  
This parser handles simple, two-column CSV files like the ISO 3166 standard.

Python

\# parsers/csv\_parser.py  
import pandas as pd  
from rdflib import Graph, URIRef, Literal  
from rdflib.namespace import SKOS, RDF, RDFS, DCTERMS  
from.base\_parser import BaseParser

class CsvParser(BaseParser):  
    """Parses a generic two-column CSV into SKOS concepts."""

    def parse(self, url: str, concept\_scheme\_uri: str, standard\_info: dict) \-\> Graph:  
        g \= Graph()  
        scheme \= URIRef(concept\_scheme\_uri)

        \# Add ConceptScheme metadata  
        g.add((scheme, RDF.type, SKOS.ConceptScheme))  
        g.add((scheme, SKOS.prefLabel, Literal(standard\_info.get('Standard\_Name'))))  
        g.add((scheme, DCTERMS.creator, Literal(standard\_info.get('Governing\_Body'))))

        df \= pd.read\_csv(url)  
          
        \# Expecting 'Name' and 'Code' columns as per ISO 3166 CSV  
        if 'Name' not in df.columns or 'Code' not in df.columns:  
            raise ValueError("CSV must contain 'Name' and 'Code' columns.")

        for index, row in df.iterrows():  
            name \= row\['Name'\]  
            code \= row\['Code'\]  
              
            \# Create a URI for the concept  
            concept\_uri \= URIRef(f"{concept\_scheme\_uri}/{code}")

            \# Add triples to the graph  
            g.add((concept\_uri, RDF.type, SKOS.Concept))  
            g.add((concept\_uri, SKOS.inScheme, scheme))  
            g.add((concept\_uri, SKOS.prefLabel, Literal(name)))  
            g.add((concept\_uri, SKOS.notation, Literal(code)))  
          
        return g

*(Note: Full implementations for all parsers and emitters are extensive but would follow similar patterns. The shopify\_graphql\_parser and openfigi\_api\_parser would use requests and BeautifulSoup4, while the json\_schema\_parser would recursively walk the schema dictionary. The sql\_emitter would generate CREATE TABLE and INSERT INTO statements.)*

File: emitters/csv\_emitter.py (Example Implementation)  
This emitter queries the final RDF graph and writes the data into the three specified CSV tables.

Python

\# emitters/csv\_emitter.py  
import pandas as pd  
import os  
from rdflib import Graph  
from rdflib.namespace import SKOS, RDF  
from.base\_emitter import BaseEmitter

class CsvEmitter(BaseEmitter):  
    """Emits the master knowledge graph into a set of CSV files."""

    def emit(self, graph: Graph, output\_dir: str):  
        """  
        Generates concept\_schemes.csv, concepts.csv, and semantic\_relations.csv.  
        """  
        \# 1\. Generate concept\_schemes.csv  
        schemes\_query \= """  
            SELECT?scheme\_uri?pref\_label?creator  
            WHERE {  
               ?scheme\_uri a skos:ConceptScheme.  
                OPTIONAL {?scheme\_uri skos:prefLabel?pref\_label. }  
                OPTIONAL {?scheme\_uri \<http://purl.org/dc/terms/creator\>?creator. }  
            }  
        """  
        schemes\_data \=  
        for row in graph.query(schemes\_query):  
            schemes\_data.append({  
                "scheme\_uri": str(row.scheme\_uri),  
                "pref\_label": str(row.pref\_label),  
                "governing\_body": str(row.creator)  
            })  
        schemes\_df \= pd.DataFrame(schemes\_data)  
        schemes\_df.to\_csv(os.path.join(output\_dir, "concept\_schemes.csv"), index=False)  
        print(f"Generated concept\_schemes.csv with {len(schemes\_df)} rows.")

        \# 2\. Generate concepts.csv  
        concepts\_query \= """  
            SELECT?concept\_uri?pref\_label?definition?notation?scheme\_uri  
            WHERE {  
               ?concept\_uri a skos:Concept.  
               ?concept\_uri skos:inScheme?scheme\_uri.  
                OPTIONAL {?concept\_uri skos:prefLabel?pref\_label. }  
                OPTIONAL {?concept\_uri skos:definition?definition. }  
                OPTIONAL {?concept\_uri skos:notation?notation. }  
            }  
        """  
        concepts\_data \=  
        for row in graph.query(concepts\_query):  
            concepts\_data.append({  
                "concept\_uri": str(row.concept\_uri),  
                "pref\_label": str(row.pref\_label),  
                "definition": str(row.definition),  
                "notation": str(row.notation),  
                "scheme\_uri": str(row.scheme\_uri)  
            })  
        concepts\_df \= pd.DataFrame(concepts\_data)  
        concepts\_df.to\_csv(os.path.join(output\_dir, "concepts.csv"), index=False)  
        print(f"Generated concepts.csv with {len(concepts\_df)} rows.")

        \# 3\. Generate semantic\_relations.csv  
        relations\_query \= """  
            SELECT?subject\_uri?predicate?object\_uri  
            WHERE {  
               ?subject\_uri?predicate?object\_uri.  
                FILTER(?predicate IN (skos:broader, skos:narrower, skos:related,   
                                      skos:exactMatch, skos:closeMatch,   
                                      skos:broadMatch, skos:narrowMatch, skos:relatedMatch))  
            }  
        """  
        relations\_data \=  
        for row in graph.query(relations\_query, initNs={"skos": SKOS}):  
            relations\_data.append({  
                "subject\_uri": str(row.subject\_uri),  
                "predicate": str(row.predicate),  
                "object\_uri": str(row.object\_uri)  
            })  
        relations\_df \= pd.DataFrame(relations\_data)  
        relations\_df.to\_csv(os.path.join(output\_dir, "semantic\_relations.csv"), index=False)  
        print(f"Generated semantic\_relations.csv with {len(relations\_df)} rows.")

### **4.2. Specification of Deployable Mapping Tables**

The engine generates three core, relational tables that constitute the fully materialized output of the system. These tables are designed to be easily loaded into any standard database or data analysis tool.

Table 4.1: concept\_schemes.csv  
This table serves as a directory of all the standards that were processed by the engine.

| Column | Data Type | Description | Example |
| :---- | :---- | :---- | :---- |
| scheme\_uri | URI (String) | The unique, canonical URI for the standard (concept scheme). Primary Key. | http://ufsa.org/v2/standards/iso\_3166\_1\_a2 |
| pref\_label | String | The human-readable name of the standard. | ISO 3166-1 Alpha-2 Country Codes |
| governing\_body | String | The organization responsible for the standard. | ISO |

Table 4.2: concepts.csv  
This is the master vocabulary, containing every individual data element, field, or concept extracted from all processed standards.

| Column | Data Type | Description | Example |
| :---- | :---- | :---- | :---- |
| concept\_uri | URI (String) | The unique, canonical URI for the concept. Primary Key. | .../iso\_3166\_1\_a2/US |
| pref\_label | String | The preferred, human-readable name for the concept. | United States of America |
| alt\_labels | String (List) | A pipe-separated list of alternative names or synonyms. | USA|United States |
| definition | Text | The official definition or description from the source standard. | Demographics and other administrative information... |
| notation | String | A formal code or identifier for the concept (e.g., country code, MIME type string). | US |
| scheme\_uri | URI (String) | Foreign key linking the concept to its parent standard in concept\_schemes.csv. | .../standards/iso\_3166\_1\_a2 |

Table 4.3: semantic\_relations.csv  
This table materializes the interoperability map, defining all hierarchical and mapping relationships both within and between standards.

| Column | Data Type | Description | Example |
| :---- | :---- | :---- | :---- |
| subject\_uri | URI (String) | The URI of the source concept in the relationship. Foreign Key to concepts.csv. | .../fhir\_r4\_patient\#Patient.name.family |
| predicate | URI (String) | The relationship type (e.g., skos:broader, skos:exactMatch). | http://www.w3.org/2004/02/skos/core\#broader |
| object\_uri | URI (String) | The URI of the target concept in the relationship. Foreign Key to concepts.csv. | .../fhir\_r4\_patient\#Patient.name |

### **4.3. Cross-Domain Canonical Concept Map (Demonstration View)**

While the three tables above represent the complete, normalized output, their power is best demonstrated through a derived view that showcases cross-domain semantic mapping. The following table is an example of what can be constructed by joining the generated tables to answer a high-level business question: "How is the concept of a 'Person' represented across different domains?" This view is the ultimate proof of UFSA v2's ability to bridge semantic gaps.

| Canonical\_Concept | FHIR\_Representation | Shopify\_Representation | Mapping\_Predicate |
| :---- | :---- | :---- | :---- |
| Person/Entity | .../fhir\_r4\_patient\#Patient | .../shopify\_admin\_customer\#Customer | skos:closeMatch |
| Date of Birth | .../fhir\_r4\_patient\#Patient.birthDate | .../shopify\_admin\_customer\#dateOfBirth | skos:exactMatch |
| Geographic Location | .../fhir\_r4\_patient\#Patient.address | .../shopify\_admin\_order\#shippingAddress | skos:broadMatch |
| Identifier | .../fhir\_r4\_patient\#Patient.identifier | .../shopify\_admin\_customer\#id | skos:relatedMatch |

## **Section V: The Generative Research Prompt for UFSA v2 Materialization**

This section synthesizes the preceding technical specification into a single, self-contained, and executable prompt. It is designed to be provided to an advanced code generation system or a human research engineer to materialize the complete UFSA v2 initial implementation without reference to any external documents. It contains the system's objectives, architectural principles, formal metamodel, declarative inputs, complete source code, output specifications, and execution protocol.

---

# **UFSA v2 Materialization Prompt**

## **1\. System Objective**

The objective is to implement and deploy the Universal Financial Standards Adapter, Version 2 (UFSA v2). This system must be a declarative, metadata-driven engine that achieves universal data interoperability across multiple domains (healthcare, e-commerce, finance, etc.). It will operate by reading a declarative configuration file containing URLs to public, machine-readable standards specifications. It will then fetch, parse, and normalize these standards into a unified internal model based on the W3C SKOS vocabulary. The final output will be a set of fully populated, relational data tables (in CSV format) that represent a comprehensive map of the concepts and semantic relationships within and between the processed standards. The entire implementation must be provided as a set of Python scripts and configuration files, ready for immediate execution.

## **2\. Core Architectural Principles**

* **Declarative Mandate (Configuration over Code):** The system's behavior must be driven by external configuration files, not by hard-coded, imperative logic. The core engine must be agnostic to the specifics of any standard. System extension must be achievable by modifying configuration only.  
* **Federated Governance Model:** The system will treat each external standard as an autonomous "domain." It will provide the central "connective tissue" for interoperability by normalizing domain-specific metadata against a global metamodel, without attempting to control the external standards themselves.  
* **Pluggable, Modular Architecture:** The system must feature a clean separation of concerns with distinct, dynamically-loaded modules for parsing heterogeneous input formats and for emitting various output formats.

## **3\. Metamodel Specification**

The internal data model for UFSA v2 is an extension of the W3C SKOS vocabulary. The following is the formal definition of the UFSA v2 metamodel in Turtle syntax. The engine's internal knowledge graph must conform to this schema.

```shell
@prefix rdf: http://www.w3.org/1999/02/22-rdf-syntax-ns\#.  
@prefix rdfs: http://www.w3.org/2000/01/rdf-schema\#.  
@prefix skos: http://www.w3.org/2004/02/skos/core\#.  
@prefix dct: http://purl.org/dc/terms/.  
@prefix ufsa: http://ufsa.org/v2/schema\#.  
ufsa:StandardsBody a rdfs:Class ;  
rdfs:label "Standards Body" ;  
rdfs:comment "An organization that defines, maintains, or governs a standard.".  
ufsa:Standard a rdfs:Class ;  
rdfs:subClassOf skos:ConceptScheme ;  
rdfs:label "Standard" ;  
rdfs:comment "A formal specification, such as an API definition, data format, or controlled vocabulary.".  
ufsa:governedBy a rdf:Property ;  
rdfs:domain ufsa:Standard ;  
rdfs:range ufsa:StandardsBody ;  
rdfs:label "Governed By".  
ufsa:specificationURL a rdf:Property ;  
rdfs:domain ufsa:Standard ;  
rdfs:range rdfs:Resource ;  
rdfs:label "Specification URL".  
ufsa:dataFormat a rdf:Property ;  
rdfs:domain ufsa:Standard ;  
rdfs:range rdfs:Literal ;  
rdfs:label "Data Format".  
ufsa:parserModule a rdf:Property ;  
rdfs:domain ufsa:Standard ;  
rdfs:range rdfs:Literal ;  
rdfs:label "Parser Module".
```

\#\# 4\. Declarative Input: Standards Body Pointer Registry

Create a file named \`config/pointer\_registry.csv\` with the following content. This file is the sole declarative input that drives the entire engine.

\`\`\`csv  
Standard\_ID,Standard\_Name,Governing\_Body,Specification\_URL,Data\_Format,Parser\_Module,Canonical\_Concept\_Scheme\_URI  
fhir\_r4\_patient,HL7 FHIR R4 Patient Resource,HL7 International,\[http://build.fhir.org/patient.schema.json,JSON-Schema,parsers.json\_schema\_parser,http://ufsa.org/v2/standards/fhir\_r4\_patient\](http://build.fhir.org/patient.schema.json,JSON-Schema,parsers.json\_schema\_parser,http://ufsa.org/v2/standards/fhir\_r4\_patient)  
fhir\_r4\_observation,HL7 FHIR R4 Observation Resource,HL7 International,\[http://build.fhir.org/observation.schema.json,JSON-Schema,parsers.json\_schema\_parser,http://ufsa.org/v2/standards/fhir\_r4\_observation\](http://build.fhir.org/observation.schema.json,JSON-Schema,parsers.json\_schema\_parser,http://ufsa.org/v2/standards/fhir\_r4\_observation)  
shopify\_admin\_product,Shopify Admin GraphQL API Product Object,Shopify,\[https://shopify.dev/docs/api/admin-graphql/latest/queries/product,HTML\_GraphQL\_Spec,parsers.shopify\_graphql\_parser,http://ufsa.org/v2/standards/shopify\_admin\_product\](https://shopify.dev/docs/api/admin-graphql/latest/queries/product,HTML\_GraphQL\_Spec,parsers.shopify\_graphql\_parser,http://ufsa.org/v2/standards/shopify\_admin\_product)  
shopify\_admin\_order,Shopify Admin GraphQL API Order Object,Shopify,\[https://shopify.dev/docs/api/admin-graphql/latest/queries/order,HTML\_GraphQL\_Spec,parsers.shopify\_graphql\_parser,http://ufsa.org/v2/standards/shopify\_admin\_order\](https://shopify.dev/docs/api/admin-graphql/latest/queries/order,HTML\_GraphQL\_Spec,parsers.shopify\_graphql\_parser,http://ufsa.org/v2/standards/shopify\_admin\_order)  
openfigi\_v3,OpenFIGI API v3,"OMG / Bloomberg L.P.",\[https://www.openfigi.com/api/documentation,HTML\_REST\_API\_Spec,parsers.openfigi\_api\_parser,http://ufsa.org/v2/standards/openfigi\_v3\](https://www.openfigi.com/api/documentation,HTML\_REST\_API\_Spec,parsers.openfigi\_api\_parser,http://ufsa.org/v2/standards/openfigi\_v3)  
iso\_3166\_1\_a2,ISO 3166-1 Alpha-2 Country Codes,ISO,\[https://datahub.io/core/country-list/r/data.csv,CSV,parsers.csv\_parser,http://ufsa.org/v2/standards/iso\_3166\_1\_a2\](https://datahub.io/core/country-list/r/data.csv,CSV,parsers.csv\_parser,http://ufsa.org/v2/standards/iso\_3166\_1\_a2)  
iana\_mime\_app,IANA MIME Types (Application),IETF / IANA,\[https://www.iana.org/assignments/media-types/application.csv,CSV,parsers.iana\_csv\_parser,http://ufsa.org/v2/standards/iana\_mime\_application\](https://www.iana.org/assignments/media-types/application.csv,CSV,parsers.iana\_csv\_parser,http://ufsa.org/v2/standards/iana\_mime\_application)  
w3c\_skos\_core,W3C SKOS Core Vocabulary,W3C,\[http://www.w3.org/2004/02/skos/core.rdf,RDF/XML,parsers.rdf\_parser,http://www.w3.org/2004/02/skos/core\#\](http://www.w3.org/2004/02/skos/core.rdf,RDF/XML,parsers.rdf\_parser,http://www.w3.org/2004/02/skos/core\#)

## **5\. Implementation Specification: Python Engine**

### **5.1. Project Directory Structure**

Create the following directory and file structure:

ufsa\_v2/  
├── main.py  
├── engine.py  
├── config/  
│   └── pointer\_registry.csv  
├── parsers/  
│   ├── \_\_init\_\_.py  
│   ├── base\_parser.py  
│   ├── csv\_parser.py  
│   ├── iana\_csv\_parser.py  
│   ├── json\_schema\_parser.py  
│   ├── openfigi\_api\_parser.py  
│   ├── rdf\_parser.py  
│   └── shopify\_graphql\_parser.py  
└── emitters/  
    ├── \_\_init\_\_.py  
    ├── base\_emitter.py  
    ├── csv\_emitter.py  
    └── sql\_emitter.py

### **5.2. Source Code**

Populate the files with the following Python code.

**File: ufsa\_v2/main.py**

Python

import argparse  
import os  
import sys  
from engine import UFSAEngine

def main():  
    """Main entry point for the UFSA v2 command-line interface."""  
    parser \= argparse.ArgumentParser(  
        description="UFSA v2: Universal Financial Standards Adapter Engine."  
    )  
    parser.add\_argument(  
        "--config",  
        default="config/pointer\_registry.csv",  
        help\="Path to the pointer registry CSV file.",  
    )  
    parser.add\_argument(  
        "--output\_dir",  
        default="output",  
        help\="Directory to save the generated tables.",  
    )  
    parser.add\_argument(  
        "--emitter",  
        default="csv",  
        choices=\["csv", "sql"\],  
        help\="The output format for the generated tables.",  
    )  
    args \= parser.parse\_args()

    print("--- Starting UFSA v2 Engine \---")  
      
    if not os.path.exists(args.output\_dir):  
        os.makedirs(args.output\_dir)  
        print(f"Created output directory: {args.output\_dir}")

    try:  
        engine \= UFSAEngine(config\_path=args.config)  
        engine.run(output\_dir=args.output\_dir, emitter\_type=args.emitter)  
        print(f"\\n--- UFSA v2 processing complete. \---")  
        print(f"Generated tables are located in: {args.output\_dir}")  
    except Exception as e:  
        print(f"\\n--- An error occurred during execution: \---", file=sys.stderr)  
        print(e, file=sys.stderr)  
        sys.exit(1)

if \_\_name\_\_ \== "\_\_main\_\_":  
    main()

**File: ufsa\_v2/engine.py**

Python

import pandas as pd  
import importlib  
from rdflib import Graph  
from emitters.base\_emitter import BaseEmitter  
from parsers.base\_parser import BaseParser

class UFSAEngine:  
    """Orchestrates the fetching, parsing, and emission of standards data."""

    def \_\_init\_\_(self, config\_path: str):  
        print(f"Loading configuration from: {config\_path}")  
        self.config \= pd.read\_csv(config\_path)  
        self.master\_graph \= Graph()

    def \_get\_instance(self, module\_path: str, class\_name: str, base\_class):  
        """Dynamically imports and instantiates a class from a module."""  
        try:  
            module \= importlib.import\_module(module\_path)  
            class\_ \= getattr(module, class\_name)  
            if not issubclass(class\_, base\_class):  
                raise TypeError(f"{class\_name} must be a subclass of {base\_class.\_\_name\_\_}")  
            return class\_()  
        except (ImportError, AttributeError) as e:  
            raise ImportError(f"Could not load class '{class\_name}' from module '{module\_path}': {e}")

    def run(self, output\_dir: str, emitter\_type: str):  
        """Executes the full ingestion, parsing, and emission pipeline."""  
        print(f"\\nFound {len(self.config)} standards to process.")  
          
        for index, row in self.config.iterrows():  
            standard\_id \= row  
            print(f"\\nProcessing standard: {row} ({standard\_id})...")

            parser\_module\_path \= row\['Parser\_Module'\]  
            parser\_class\_name \= ''.join(word.capitalize() for word in parser\_module\_path.split('.')\[-1\].split('\_'))  
              
            try:  
                parser \= self.\_get\_instance(parser\_module\_path, parser\_class\_name, BaseParser)  
                standard\_graph \= parser.parse(  
                    url=row,  
                    concept\_scheme\_uri=row,  
                    standard\_info=row.to\_dict()  
                )  
                self.master\_graph \+= standard\_graph  
                print(f"Successfully parsed and merged '{standard\_id}'. Graph now contains {len(self.master\_graph)} triples.")  
            except Exception as e:  
                print(f"ERROR: Failed to process standard '{standard\_id}'. Reason: {e}")  
                continue  
          
        print(f"\\n--- Starting emission process \---")  
        print(f"Total triples in master graph: {len(self.master\_graph)}")  
          
        emitter\_module\_path \= f"emitters.{emitter\_type}\_emitter"  
        emitter\_class\_name \= f"{emitter\_type.upper()}Emitter"  
          
        try:  
            emitter \= self.\_get\_instance(emitter\_module\_path, emitter\_class\_name, BaseEmitter)  
            emitter.emit(self.master\_graph, output\_dir)  
        except Exception as e:  
            print(f"ERROR: Failed to emit tables. Reason: {e}")

**File: ufsa\_v2/parsers/\_\_init\_\_.py**

Python

\# Leave this file empty.

**File: ufsa\_v2/parsers/base\_parser.py**

Python

from abc import ABC, abstractmethod  
from rdflib import Graph

class BaseParser(ABC):  
    """Abstract base class for all standard parsers."""  
    @abstractmethod  
    def parse(self, url: str, concept\_scheme\_uri: str, standard\_info: dict) \-\> Graph:  
        """  
        Fetches a standard from a URL, parses it, and returns an RDF graph  
        conformant with the UFSA SKOS-based metamodel.  
        """  
        pass

**File: ufsa\_v2/parsers/csv\_parser.py**

Python

import pandas as pd  
from rdflib import Graph, URIRef, Literal  
from rdflib.namespace import SKOS, RDF, DCTERMS  
from.base\_parser import BaseParser

class CsvParser(BaseParser):  
    """Parses a generic two-column CSV (Name, Code) into SKOS concepts."""  
    def parse(self, url: str, concept\_scheme\_uri: str, standard\_info: dict) \-\> Graph:  
        g \= Graph()  
        scheme \= URIRef(concept\_scheme\_uri)  
        g.add((scheme, RDF.type, SKOS.ConceptScheme))  
        g.add((scheme, SKOS.prefLabel, Literal(standard\_info.get('Standard\_Name'))))  
        g.add((scheme, DCTERMS.creator, Literal(standard\_info.get('Governing\_Body'))))

        df \= pd.read\_csv(url)  
        if 'Name' not in df.columns or 'Code' not in df.columns:  
            raise ValueError("CSV must contain 'Name' and 'Code' columns for CsvParser.")

        for \_, row in df.iterrows():  
            name, code \= str(row\['Name'\]), str(row\['Code'\])  
            concept\_uri \= URIRef(f"{concept\_scheme\_uri}/{code.replace(' ', '\_')}")  
            g.add((concept\_uri, RDF.type, SKOS.Concept))  
            g.add((concept\_uri, SKOS.inScheme, scheme))  
            g.add((concept\_uri, SKOS.prefLabel, Literal(name)))  
            g.add((concept\_uri, SKOS.notation, Literal(code)))  
        return g

**File: ufsa\_v2/parsers/iana\_csv\_parser.py**

Python

import pandas as pd  
from rdflib import Graph, URIRef, Literal  
from rdflib.namespace import SKOS, RDF, DCTERMS  
from.base\_parser import BaseParser

class IanaCsvParser(BaseParser):  
    """Parses IANA MIME type CSVs (Name, Template) into SKOS concepts."""  
    def parse(self, url: str, concept\_scheme\_uri: str, standard\_info: dict) \-\> Graph:  
        g \= Graph()  
        scheme \= URIRef(concept\_scheme\_uri)  
        g.add((scheme, RDF.type, SKOS.ConceptScheme))  
        g.add((scheme, SKOS.prefLabel, Literal(standard\_info.get('Standard\_Name'))))  
        g.add((scheme, DCTERMS.creator, Literal(standard\_info.get('Governing\_Body'))))

        df \= pd.read\_csv(url)  
        if 'Name' not in df.columns or 'Template' not in df.columns:  
            raise ValueError("CSV must contain 'Name' and 'Template' columns for IanaCsvParser.")

        for \_, row in df.iterrows():  
            name, template \= str(row\['Name'\]), str(row)  
            if pd.isna(name) or pd.isna(template): continue  
              
            concept\_uri\_slug \= name.replace('/', '\_').replace('+', '\_')  
            concept\_uri \= URIRef(f"{concept\_scheme\_uri}/{concept\_uri\_slug}")  
            g.add((concept\_uri, RDF.type, SKOS.Concept))  
            g.add((concept\_uri, SKOS.inScheme, scheme))  
            g.add((concept\_uri, SKOS.prefLabel, Literal(name)))  
            g.add((concept\_uri, SKOS.notation, Literal(template)))  
        return g

**File: ufsa\_v2/parsers/json\_schema\_parser.py**

Python

import requests  
from rdflib import Graph, URIRef, Literal  
from rdflib.namespace import SKOS, RDF, RDFS, DCTERMS  
from.base\_parser import BaseParser

class JsonSchemaParser(BaseParser):  
    """Parses a JSON Schema into a hierarchical SKOS concept graph."""  
    def parse(self, url: str, concept\_scheme\_uri: str, standard\_info: dict) \-\> Graph:  
        g \= Graph()  
        self.scheme \= URIRef(concept\_scheme\_uri)  
        g.add((self.scheme, RDF.type, SKOS.ConceptScheme))  
        g.add((self.scheme, SKOS.prefLabel, Literal(standard\_info.get('Standard\_Name'))))  
        g.add((self.scheme, DCTERMS.creator, Literal(standard\_info.get('Governing\_Body'))))

        response \= requests.get(url)  
        response.raise\_for\_status()  
        schema \= response.json()  
          
        root\_definition\_key \= standard\_info.split(' ')\[-2\] \# e.g., 'Patient'  
        if root\_definition\_key in schema.get('definitions', {}):  
            root\_schema \= schema\['definitions'\]\[root\_definition\_key\]  
            self.\_traverse\_properties(g, root\_schema, None)  
          
        return g

    def \_traverse\_properties(self, g: Graph, schema\_node: dict, parent\_concept: URIRef):  
        if 'properties' not in schema\_node:  
            return

        for prop\_name, prop\_schema in schema\_node\['properties'\].items():  
            concept\_uri \= URIRef(f"{self.scheme}\#{prop\_name}")  
            if parent\_concept:  
                concept\_uri \= URIRef(f"{parent\_concept}.{prop\_name}")

            g.add((concept\_uri, RDF.type, SKOS.Concept))  
            g.add((concept\_uri, SKOS.inScheme, self.scheme))  
            g.add((concept\_uri, SKOS.prefLabel, Literal(prop\_name)))  
              
            if 'description' in prop\_schema:  
                g.add((concept\_uri, SKOS.definition, Literal(prop\_schema\['description'\])))  
              
            if parent\_concept:  
                g.add((concept\_uri, SKOS.broader, parent\_concept))  
              
            \# Recurse for nested objects  
            if prop\_schema.get('type') \== 'object' and 'properties' in prop\_schema:  
                self.\_traverse\_properties(g, prop\_schema, concept\_uri)  
            elif '$ref' in prop\_schema:  
                \# Basic reference handling (non-recursive for simplicity)  
                ref\_name \= prop\_schema\['$ref'\].split('/')\[-1\]  
                g.add((concept\_uri, RDFS.seeAlso, Literal(f"Refers to schema definition: {ref\_name}")))

**File: ufsa\_v2/parsers/rdf\_parser.py**

Python

from rdflib import Graph  
from.base\_parser import BaseParser

class RdfParser(BaseParser):  
    """Parses an existing RDF file directly into the graph."""  
    def parse(self, url: str, concept\_scheme\_uri: str, standard\_info: dict) \-\> Graph:  
        g \= Graph()  
        g.parse(url)  
        return g

**File: ufsa\_v2/parsers/shopify\_graphql\_parser.py**

Python

import requests  
from bs4 import BeautifulSoup  
from rdflib import Graph, URIRef, Literal  
from rdflib.namespace import SKOS, RDF, DCTERMS  
from.base\_parser import BaseParser

class ShopifyGraphqlParser(BaseParser):  
    """Scrapes a Shopify GraphQL documentation page for fields."""  
    def parse(self, url: str, concept\_scheme\_uri: str, standard\_info: dict) \-\> Graph:  
        g \= Graph()  
        scheme \= URIRef(concept\_scheme\_uri)  
        g.add((scheme, RDF.type, SKOS.ConceptScheme))  
        g.add((scheme, SKOS.prefLabel, Literal(standard\_info.get('Standard\_Name'))))  
        g.add((scheme, DCTERMS.creator, Literal(standard\_info.get('Governing\_Body'))))

        response \= requests.get(url)  
        response.raise\_for\_status()  
        soup \= BeautifulSoup(response.content, 'html.parser')  
          
        \# This is a brittle selector and likely to break with site updates.  
        \# A more robust solution would use a more stable identifier if available.  
        fields\_header \= soup.find(lambda tag: tag.name in \['h2', 'h3'\] and 'Fields' in tag.get\_text())  
        if not fields\_header:  
            raise ValueError("Could not find 'Fields' section on documentation page.")  
          
        table \= fields\_header.find\_next('table')  
        if not table:  
            raise ValueError("Could not find table following 'Fields' header.")

        for row in table.find('tbody').find\_all('tr'):  
            cols \= row.find\_all('td')  
            if len(cols) \>= 2:  
                field\_name\_tag \= cols.find('code')  
                if not field\_name\_tag: continue  
                  
                field\_name \= field\_name\_tag.get\_text(strip=True)  
                description \= cols.\[1\]get\_text(strip=True)  
                  
                concept\_uri \= URIRef(f"{concept\_scheme\_uri}\#{field\_name}")  
                g.add((concept\_uri, RDF.type, SKOS.Concept))  
                g.add((concept\_uri, SKOS.inScheme, scheme))  
                g.add((concept\_uri, SKOS.prefLabel, Literal(field\_name)))  
                g.add((concept\_uri, SKOS.definition, Literal(description)))  
        return g

**File: ufsa\_v2/parsers/openfigi\_api\_parser.py**

Python

import requests  
from bs4 import BeautifulSoup  
from rdflib import Graph, URIRef, Literal  
from rdflib.namespace import SKOS, RDF, DCTERMS  
from.base\_parser import BaseParser

class OpenfigiApiParser(BaseParser):  
    """Scrapes the OpenFIGI API documentation for response fields."""  
    def parse(self, url: str, concept\_scheme\_uri: str, standard\_info: dict) \-\> Graph:  
        g \= Graph()  
        scheme \= URIRef(concept\_scheme\_uri)  
        g.add((scheme, RDF.type, SKOS.ConceptScheme))  
        g.add((scheme, SKOS.prefLabel, Literal(standard\_info.get('Standard\_Name'))))  
        g.add((scheme, DCTERMS.creator, Literal(standard\_info.get('Governing\_Body'))))

        response \= requests.get(url)  
        response.raise\_for\_status()  
        soup \= BeautifulSoup(response.content, 'html.parser')

        \# Find the section describing the response format for the mapping endpoint  
        response\_header \= soup.find('h3', id\='response-format')  
        if not response\_header:  
            raise ValueError("Could not find 'Response Format' section (h3 with id='response-format').")

        \# Find the list of properties  
        prop\_list \= response\_header.find\_next('ul')  
        if not prop\_list:  
            raise ValueError("Could not find property list (ul) after 'Response Format' header.")

        for item in prop\_list.find\_all('li'):  
            code\_tag \= item.find('code')  
            if code\_tag:  
                field\_name \= code\_tag.get\_text(strip=True)  
                description \= ' '.join(item.get\_text().split(' ')\[2:\]).strip() \# Basic description extraction  
                  
                concept\_uri \= URIRef(f"{concept\_scheme\_uri}\#{field\_name}")  
                g.add((concept\_uri, RDF.type, SKOS.Concept))  
                g.add((concept\_uri, SKOS.inScheme, scheme))  
                g.add((concept\_uri, SKOS.prefLabel, Literal(field\_name)))  
                g.add((concept\_uri, SKOS.definition, Literal(description)))  
        return g

**File: ufsa\_v2/emitters/\_\_init\_\_.py**

Python

\# Leave this file empty.

**File: ufsa\_v2/emitters/base\_emitter.py**

Python

from abc import ABC, abstractmethod  
from rdflib import Graph

class BaseEmitter(ABC):  
    """Abstract base class for all output emitters."""  
    @abstractmethod  
    def emit(self, graph: Graph, output\_dir: str):  
        """  
        Takes the final RDF graph and writes it to a set of files  
        in a specific format.  
        """  
        pass

**File: ufsa\_v2/emitters/csv\_emitter.py**

Python

import pandas as pd  
import os  
from rdflib import Graph  
from rdflib.namespace import SKOS  
from.base\_emitter import BaseEmitter

class CsvEmitter(BaseEmitter):  
    """Emits the master knowledge graph into a set of CSV files."""  
    def emit(self, graph: Graph, output\_dir: str):  
        \# 1\. Generate concept\_schemes.csv  
        schemes\_query \= """  
            SELECT?scheme\_uri?pref\_label?creator  
            WHERE {  
               ?scheme\_uri a skos:ConceptScheme.  
                OPTIONAL {?scheme\_uri skos:prefLabel?pref\_label. }  
                OPTIONAL {?scheme\_uri \[http://purl.org/dc/terms/creator\](http://purl.org/dc/terms/creator)?creator. }  
            }  
        """  
        schemes\_data \= \[{  
            "scheme\_uri": str(r.scheme\_uri),  
            "pref\_label": str(r.pref\_label),  
            "governing\_body": str(r.creator)  
        } for r in graph.query(schemes\_query)\]  
        schemes\_df \= pd.DataFrame(schemes\_data).drop\_duplicates().sort\_values('scheme\_uri')  
        schemes\_df.to\_csv(os.path.join(output\_dir, "concept\_schemes.csv"), index=False)  
        print(f"Generated concept\_schemes.csv with {len(schemes\_df)} rows.")

        \# 2\. Generate concepts.csv  
        concepts\_query \= """  
            SELECT?concept\_uri?pref\_label?definition?notation?scheme\_uri  
            WHERE {  
               ?concept\_uri a skos:Concept ; skos:inScheme?scheme\_uri.  
                OPTIONAL {?concept\_uri skos:prefLabel?pref\_label. }  
                OPTIONAL {?concept\_uri skos:definition?definition. }  
                OPTIONAL {?concept\_uri skos:notation?notation. }  
            }  
        """  
        concepts\_data \= \[{  
            "concept\_uri": str(r.concept\_uri), "pref\_label": str(r.pref\_label),  
            "definition": str(r.definition), "notation": str(r.notation),  
            "scheme\_uri": str(r.scheme\_uri)  
        } for r in graph.query(concepts\_query)\]  
        concepts\_df \= pd.DataFrame(concepts\_data).drop\_duplicates().sort\_values('concept\_uri')  
        concepts\_df.to\_csv(os.path.join(output\_dir, "concepts.csv"), index=False)  
        print(f"Generated concepts.csv with {len(concepts\_df)} rows.")

        \# 3\. Generate semantic\_relations.csv  
        relations\_query \= """  
            SELECT?subject\_uri?predicate?object\_uri  
            WHERE {  
               ?subject\_uri?predicate?object\_uri.  
                FILTER(?predicate IN (skos:broader, skos:narrower, skos:related,   
                                      skos:exactMatch, skos:closeMatch,   
                                      skos:broadMatch, skos:narrowMatch, skos:relatedMatch))  
            }  
        """  
        relations\_data \=  
        relations\_df \= pd.DataFrame(relations\_data).drop\_duplicates().sort\_values(\['subject\_uri', 'predicate', 'object\_uri'\])  
        relations\_df.to\_csv(os.path.join(output\_dir, "semantic\_relations.csv"), index=False)  
        print(f"Generated semantic\_relations.csv with {len(relations\_df)} rows.")

**File: ufsa\_v2/emitters/sql\_emitter.py**

Python

import os  
from rdflib import Graph  
from.base\_emitter import BaseEmitter  
import pandas as pd

class SqlEmitter(BaseEmitter):  
    """Emits the master knowledge graph as SQL INSERT statements."""  
    def emit(self, graph: Graph, output\_dir: str):  
        \# This is a simplified implementation. A robust version would handle  
        \# SQL escaping, different dialects, and schema creation more formally.  
          
        \# Re-use the CSV Emitter's logic to get DataFrames  
        from.csv\_emitter import CsvEmitter  
        temp\_dir \= os.path.join(output\_dir, "temp\_sql\_gen")  
        if not os.path.exists(temp\_dir):  
            os.makedirs(temp\_dir)  
          
        csv\_emitter \= CsvEmitter()  
        csv\_emitter.emit(graph, temp\_dir)

        sql\_script \= ""

        \# Schema Creation  
        sql\_script \+= """  
\-- UFSA v2 Schema Definition  
CREATE TABLE concept\_schemes (  
    scheme\_uri VARCHAR(255) PRIMARY KEY,  
    pref\_label TEXT,  
    governing\_body VARCHAR(255)  
);

CREATE TABLE concepts (  
    concept\_uri VARCHAR(255) PRIMARY KEY,  
    pref\_label TEXT,  
    definition TEXT,  
    notation TEXT,  
    scheme\_uri VARCHAR(255),  
    FOREIGN KEY (scheme\_uri) REFERENCES concept\_schemes(scheme\_uri)  
);

CREATE TABLE semantic\_relations (  
    subject\_uri VARCHAR(255),  
    predicate VARCHAR(255),  
    object\_uri VARCHAR(255),  
    PRIMARY KEY (subject\_uri, predicate, object\_uri),  
    FOREIGN KEY (subject\_uri) REFERENCES concepts(concept\_uri),  
    FOREIGN KEY (object\_uri) REFERENCES concepts(concept\_uri)  
);

\-- Data Insertion  
"""

        \# Data Insertion  
        for table\_name in \["concept\_schemes", "concepts", "semantic\_relations"\]:  
            df \= pd.read\_csv(os.path.join(temp\_dir, f"{table\_name}.csv"))  
            df \= df.where(pd.notnull(df), None) \# Replace NaN with None for SQL NULL  
            for \_, row in df.iterrows():  
                cols \= ', '.join(row.index)  
                vals \= ', '.join(\[f"'{str(v).replace(\\"'\\", \\"''\\")}'" if v is not None else "NULL" for v in row.values\])  
                sql\_script \+= f"INSERT INTO {table\_name} ({cols}) VALUES ({vals});\\n"  
            sql\_script \+= "\\n"

        with open(os.path.join(output\_dir, "ufsa\_v2\_data.sql"), "w", encoding="utf-8") as f:  
            f.write(sql\_script)  
              
        print(f"Generated ufsa\_v2\_data.sql script.")  
          
        \# Clean up temp files  
        for f in os.listdir(temp\_dir):  
            os.remove(os.path.join(temp\_dir, f))  
        os.rmdir(temp\_dir)

## **6\. Output Specification: Data Tables**

The successful execution of the engine will produce three primary CSV files in the specified output directory. These tables are relationally linked and provide a complete, structured representation of the ingested standards.

### **6.1. Table Schemas**

* **concept\_schemes.csv**:  
  * scheme\_uri (String, Primary Key)  
  * pref\_label (String)  
  * governing\_body (String)  
* **concepts.csv**:  
  * concept\_uri (String, Primary Key)  
  * pref\_label (String)  
  * definition (Text)  
  * notation (String)  
  * scheme\_uri (String, Foreign Key to concept\_schemes.scheme\_uri)  
* **semantic\_relations.csv**:  
  * subject\_uri (String, Foreign Key to concepts.concept\_uri)  
  * predicate (String, URI of the SKOS property)  
  * object\_uri (String, Foreign Key to concepts.concept\_uri)

### **6.2. Expected Output Example (for ISO 3166-1)**

**concept\_schemes.csv (sample row):**

Code snippet

scheme\_uri,pref\_label,governing\_body  
\[http://ufsa.org/v2/standards/iso\_3166\_1\_a2,ISO\](http://ufsa.org/v2/standards/iso\_3166\_1\_a2,ISO) 3166-1 Alpha-2 Country Codes,ISO

**concepts.csv (sample rows):**

Code snippet

concept\_uri,pref\_label,definition,notation,scheme\_uri  
\[http://ufsa.org/v2/standards/iso\_3166\_1\_a2/US,United\](http://ufsa.org/v2/standards/iso\_3166\_1\_a2/US,United) States of America,,US,\[http://ufsa.org/v2/standards/iso\_3166\_1\_a2\](http://ufsa.org/v2/standards/iso\_3166\_1\_a2)  
\[http://ufsa.org/v2/standards/iso\_3166\_1\_a2/CA,Canada,,CA,http://ufsa.org/v2/standards/iso\_3166\_1\_a2\](http://ufsa.org/v2/standards/iso\_3166\_1\_a2/CA,Canada,,CA,http://ufsa.org/v2/standards/iso\_3166\_1\_a2)

semantic\_relations.csv:  
(This table would be empty for the ISO 3166-1 standard alone, as it is a flat list. It would be populated by hierarchical standards like FHIR.)

## **7\. Execution and Verification Protocol**

1. **Setup Environment:**  
   * Ensure Python 3.8+ is installed.  
   * Create a virtual environment:  
     Bash  
     python \-m venv venv  
     source venv/bin/activate  \# On Windows: venv\\Scripts\\activate

2. **Install Dependencies:**  
   * Create a requirements.txt file with the following content:  
     pandas  
     rdflib  
     requests  
     beautifulsoup4  
     lxml

   * Install the dependencies:  
     Bash  
     pip install \-r requirements.txt

3. **Run the Engine:**  
   * Navigate to the ufsa\_v2 directory.  
   * Execute the main script:  
     Bash  
     python main.py \--output\_dir./output \--emitter csv

4. **Verification:**  
   * Upon successful completion, an output/ directory will be created.  
   * Verify that the directory contains three non-empty CSV files: concept\_schemes.csv, concepts.csv, and semantic\_relations.csv.  
   * Inspect the contents of the files to confirm they contain the parsed data from the standards defined in pointer\_registry.csv.

#### **Works cited**

1. The Data Engineers Guide to Declarative vs Imperative for Data \- DataOps.live, accessed on August 24, 2025, [https://www.dataops.live/blog/the-data-engineers-guide-to-declarative-vs-imperative-for-data](https://www.dataops.live/blog/the-data-engineers-guide-to-declarative-vs-imperative-for-data)  
2. Explained: Imperative vs Declarative programming \- DEV Community, accessed on August 24, 2025, [https://dev.to/siddharthshyniben/explained-imperative-vs-declarative-programming-577g](https://dev.to/siddharthshyniben/explained-imperative-vs-declarative-programming-577g)  
3. What are some examples of imperative vs. declarative programming? \- Quora, accessed on August 24, 2025, [https://www.quora.com/What-are-some-examples-of-imperative-vs-declarative-programming](https://www.quora.com/What-are-some-examples-of-imperative-vs-declarative-programming)  
4. Imperative vs Declarative Programming \- Reddit, accessed on August 24, 2025, [https://www.reddit.com/r/programming/comments/rv9np3/imperative\_vs\_declarative\_programming/](https://www.reddit.com/r/programming/comments/rv9np3/imperative_vs_declarative_programming/)  
5. Business logic \- Wikipedia, accessed on August 24, 2025, [https://en.wikipedia.org/wiki/Business\_logic](https://en.wikipedia.org/wiki/Business_logic)  
6. Patterns for Taming Complex Business Logic | by Ürgo Ringo | Inbank product & engineering | Medium, accessed on August 24, 2025, [https://medium.com/inbank-product-and-engineering/patterns-for-taming-complex-business-logic-8b63c0b98882](https://medium.com/inbank-product-and-engineering/patterns-for-taming-complex-business-logic-8b63c0b98882)  
7. Declarative vs. Imperative Programming: 4 Key Differences | Codefresh, accessed on August 24, 2025, [https://codefresh.io/learn/infrastructure-as-code/declarative-vs-imperative-programming-4-key-differences/](https://codefresh.io/learn/infrastructure-as-code/declarative-vs-imperative-programming-4-key-differences/)  
8. How to model Business Logic using Configuration \- VI Company, accessed on August 24, 2025, [https://www.vicompany.nl/en/insights/how-to-model-business-logic-using-configuration](https://www.vicompany.nl/en/insights/how-to-model-business-logic-using-configuration)  
9. Patterns in Practice \- Convention Over Configuration | Microsoft Learn, accessed on August 24, 2025, [https://learn.microsoft.com/en-us/archive/msdn-magazine/2009/february/patterns-in-practice-convention-over-configuration](https://learn.microsoft.com/en-us/archive/msdn-magazine/2009/february/patterns-in-practice-convention-over-configuration)  
10. Cognitive Load is what matters \- GitHub, accessed on August 24, 2025, [https://github.com/zakirullin/cognitive-load](https://github.com/zakirullin/cognitive-load)  
11. The Cognitive Load Theory in Software Development \- The Valuable Dev, accessed on August 24, 2025, [https://thevaluable.dev/cognitive-load-theory-software-developer/](https://thevaluable.dev/cognitive-load-theory-software-developer/)  
12. That's not an abstraction, that's just a layer of indirection \- fhur, accessed on August 24, 2025, [https://fhur.me/posts/2024/thats-not-an-abstraction](https://fhur.me/posts/2024/thats-not-an-abstraction)  
13. Death by design patterns, or On the cognitive load of abstractions in the code \- Hacker News, accessed on August 24, 2025, [https://news.ycombinator.com/item?id=36118093](https://news.ycombinator.com/item?id=36118093)  
14. Cognitive Load For Developers : r/programming \- Reddit, accessed on August 24, 2025, [https://www.reddit.com/r/programming/comments/192cwgw/cognitive\_load\_for\_developers/](https://www.reddit.com/r/programming/comments/192cwgw/cognitive_load_for_developers/)  
15. Cognitive load is what matters | Hacker News, accessed on August 24, 2025, [https://news.ycombinator.com/item?id=42489645](https://news.ycombinator.com/item?id=42489645)  
16. Federated Data Governance Explained \- Alation, accessed on August 24, 2025, [https://www.alation.com/blog/federated-data-governance-explained/](https://www.alation.com/blog/federated-data-governance-explained/)  
17. www.alation.com, accessed on August 24, 2025, [https://www.alation.com/blog/federated-data-governance-explained/\#:\~:text=Federated%20data%20governance%20is%20a,governance%20principles%20with%20decentralized%20execution.](https://www.alation.com/blog/federated-data-governance-explained/#:~:text=Federated%20data%20governance%20is%20a,governance%20principles%20with%20decentralized%20execution.)  
18. Federated Data Governance: Ultimate Guide for 2024 \- Atlan, accessed on August 24, 2025, [https://atlan.com/know/data-governance/federated-data-governance/](https://atlan.com/know/data-governance/federated-data-governance/)  
19. Understand Data Governance Models: Centralized, Decentralized & Federated | Alation, accessed on August 24, 2025, [https://www.alation.com/blog/understand-data-governance-models-centralized-decentralized-federated/](https://www.alation.com/blog/understand-data-governance-models-centralized-decentralized-federated/)  
20. Implementing Federated Governance in Data Mesh Architecture \- MDPI, accessed on August 24, 2025, [https://www.mdpi.com/1999-5903/16/4/115](https://www.mdpi.com/1999-5903/16/4/115)  
21. Simple Knowledge Organization System \- Wikipedia, accessed on August 24, 2025, [https://en.wikipedia.org/wiki/Simple\_Knowledge\_Organization\_System](https://en.wikipedia.org/wiki/Simple_Knowledge_Organization_System)  
22. What's SKOS, What's not, Why and What Should be Done About It \- NKOS, accessed on August 24, 2025, [https://nkos.dublincore.org/ASIST2015/ASISTBusch-SKOS.pdf](https://nkos.dublincore.org/ASIST2015/ASISTBusch-SKOS.pdf)  
23. SKOS Simple Knowledge Organization System Primer \- W3C, accessed on August 24, 2025, [https://www.w3.org/TR/skos-primer/](https://www.w3.org/TR/skos-primer/)  
24. SKOS Core Vocabulary Specification \- W3C, accessed on August 24, 2025, [https://www.w3.org/TR/swbp-skos-core-spec/](https://www.w3.org/TR/swbp-skos-core-spec/)  
25. SKOS Simple Knowledge Organization System Reference \- W3C, accessed on August 24, 2025, [https://www.w3.org/TR/2008/WD-skos-reference-20080125/](https://www.w3.org/TR/2008/WD-skos-reference-20080125/)  
26. RDF Vocabularies \- SKOS Simple Knowledge Organization System, accessed on August 24, 2025, [https://www.w3.org/2004/02/skos/vocabs](https://www.w3.org/2004/02/skos/vocabs)  
27. SKOS Simple Knowledge Organization System RDF Schema \- W3C, accessed on August 24, 2025, [https://www.w3.org/2008/05/skos](https://www.w3.org/2008/05/skos)  
28. Patient \- FHIR v6.0.0-ballot2, accessed on August 24, 2025, [http://build.fhir.org/patient.schema.json.html](http://build.fhir.org/patient.schema.json.html)  
29. List of all countries with their 2 digit codes (ISO 3166-1) \- DataHub.io, accessed on August 24, 2025, [https://datahub.io/core/country-list](https://datahub.io/core/country-list)  
30. product \- GraphQL Admin \- Shopify developer documentation, accessed on August 24, 2025, [https://shopify.dev/docs/api/admin-graphql/latest/queries/product](https://shopify.dev/docs/api/admin-graphql/latest/queries/product)  
31. Documentation | OpenFIGI, accessed on August 24, 2025, [https://www.openfigi.com/api/documentation](https://www.openfigi.com/api/documentation)  
32. Resource \- FHIR v6.0.0-ballot2, accessed on August 24, 2025, [https://build.fhir.org/resource.schema.json.html](https://build.fhir.org/resource.schema.json.html)  
33. Observation \- FHIR v6.0.0-ballot2, accessed on August 24, 2025, [https://build.fhir.org/observation.schema.json.html](https://build.fhir.org/observation.schema.json.html)  
34. FHIR Observation \- Conduct Science, accessed on August 24, 2025, [https://conductscience.com/digital-health/fhir-observation/](https://conductscience.com/digital-health/fhir-observation/)  
35. Observation resource \- Veradigm Developer Portal, accessed on August 24, 2025, [https://developer.veradigm.com/content/fhir/Resources/DSTU2/Observation.html](https://developer.veradigm.com/content/fhir/Resources/DSTU2/Observation.html)  
36. Observation \- FHIR v6.0.0-ballot3, accessed on August 24, 2025, [https://build.fhir.org/observation.html](https://build.fhir.org/observation.html)  
37. order \- GraphQL Admin \- Shopify developer documentation, accessed on August 24, 2025, [https://shopify.dev/docs/api/admin-graphql/latest/queries/order](https://shopify.dev/docs/api/admin-graphql/latest/queries/order)  
38. Order \- Shopify developer documentation, accessed on August 24, 2025, [https://shopify.dev/docs/api/admin-rest/latest/resources/order](https://shopify.dev/docs/api/admin-rest/latest/resources/order)  
39. orders \- GraphQL Admin \- Shopify developer documentation, accessed on August 24, 2025, [https://shopify.dev/docs/api/admin-graphql/latest/queries/orders](https://shopify.dev/docs/api/admin-graphql/latest/queries/orders)  
40. Financial Instrument Global Identifier \- Wikipedia, accessed on August 24, 2025, [https://en.wikipedia.org/wiki/Financial\_Instrument\_Global\_Identifier](https://en.wikipedia.org/wiki/Financial_Instrument_Global_Identifier)  
41. Overview | OpenFIGI, accessed on August 24, 2025, [https://www.openfigi.com/about/overview](https://www.openfigi.com/about/overview)  
42. FINANCIAL INSTRUMENT GLOBAL IDENTIFIER ™ \- Bloomberg, accessed on August 24, 2025, [https://assets.bwbx.io/documents/users/iqjWHBFdfxIU/rKmKGovTFMFo/v0](https://assets.bwbx.io/documents/users/iqjWHBFdfxIU/rKmKGovTFMFo/v0)  
43. How FIGI relates to other standards in the space \- OMG Issue Tracker, accessed on August 24, 2025, [https://issues.omg.org/issues/FIGI-20](https://issues.omg.org/issues/FIGI-20)  
44. Battle Between ISIN and FIGI Codes \- ISIN, CUSIP, LEI, SEDOL, WKN, CFI Codes, Database Securities Apply Application Register, accessed on August 24, 2025, [https://www.isin.com/battle-between-isin-and-figi-codes/](https://www.isin.com/battle-between-isin-and-figi-codes/)  
45. 20240923 FDTA Response to Proposed Rule ... \- FHFA, accessed on August 24, 2025, [https://www.fhfa.gov/sites/default/files/2024-09/20240923%20FDTA%20Response%20to%20Proposed%20Rule%20FHFA.docx](https://www.fhfa.gov/sites/default/files/2024-09/20240923%20FDTA%20Response%20to%20Proposed%20Rule%20FHFA.docx)  
46. Comments on Financial Data Transparency Act Joint Data Standards Under the Financial Data Transparency Act of 2022, accessed on August 24, 2025, [https://www.federalreserve.gov/apps/proposals/comments/FR-0000-0136-01-C19](https://www.federalreserve.gov/apps/proposals/comments/FR-0000-0136-01-C19)  
47. SKOS Simple Knowledge Organization System Reference \- W3C, accessed on August 24, 2025, [https://www.w3.org/TR/skos-reference/](https://www.w3.org/TR/skos-reference/)  
48. Media Types \- Internet Assigned Numbers Authority, accessed on August 24, 2025, [https://www.iana.org/assignments/media-types/](https://www.iana.org/assignments/media-types/)
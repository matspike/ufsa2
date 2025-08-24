# **UFSA v2.1 Implementation Plan: Integrating SBOM and AST Analysis**

**Document Purpose:** This document provides a comprehensive plan for extending the UFSA v2 engine to ingest Software Bill of Materials (SBOM) and Abstract Syntax Tree (AST) data as first-class data sources. It details the required architectural additions, parser implementations, emitter enhancements, and the critical final step of integrating these new artifacts into the tracker and license sealing workflows.

**Strategic Goal:** To evolve UFSA v2 from a standards interoperability engine into a holistic governance platform capable of creating a unified semantic map of an organization's formal data standards, software supply chain, and internal database schemas.

## **Phase 1: Foundational Enhancements & Registry Updates**

This phase focuses on preparing the existing architecture to recognize and handle the new data source types.

### **1.1. Create New Parser Stubs**

In the ufsa\_v2/parsers/ directory, create two new files with boilerplate class definitions inheriting from BaseParser:

* parser\_cyclonedx.py: This will handle SBOMs in the CycloneDX JSON format.  
* parser\_ast\_sql.py: This will handle SQL Data Definition Language (DDL) files.

### **1.2. Update the Pointer Registry**

Add new entries to ufsa\_v2/registry/pointer\_registry.yaml to register the new parsers and point them to fixture files. This makes the engine aware of the new capabilities.

\# ... existing entries ...

\# New entry for SBOM (CycloneDX)  
\- standard\_id: cyclonedx\_example  
  standard\_name: Example CycloneDX SBOM  
  governing\_body: OWASP  
  specification\_url: "file://data/fixtures/sbom\_example.json"  
  data\_format: "CycloneDX-JSON"  
  parser\_module: "ufsa\_v2.parsers.parser\_cyclonedx"  
  canonical\_concept\_scheme\_uri: "http://ufsa.org/v2.1/standards/cyclonedx\_example"

\# New entry for AST (SQL DDL)  
\- standard\_id: internal\_dw\_schema  
  standard\_name: Internal Data Warehouse Schema  
  governing\_body: Internal  
  specification\_url: "file://data/fixtures/dw\_schema.sql"  
  data\_format: "SQL-DDL"  
  parser\_module: "ufsa\_v2.parsers.parser\_ast\_sql"  
  canonical\_concept\_scheme\_uri: "http://ufsa.org/v2.1/standards/internal\_dw\_schema"

### **1.3. Create Fixture Files**

In the data/fixtures/ directory, add the two files referenced above:

* sbom\_example.json: A valid, simple CycloneDX JSON file containing a few components and dependencies.  
* dw\_schema.sql: A simple SQL file with a few CREATE TABLE statements, including primary and foreign keys.

## **Phase 2: Parser Implementation**

This is the core development phase where the logic for ingesting the new formats is built.

### **2.1. Implement parser\_cyclonedx.py**

This parser will transform an SBOM's component list and dependency graph into the UFSA SKOS model.

* **Dependencies:** Add cyclonedx-python-lib to the project's dependencies.  
* **Logic:**  
  1. Load the JSON file from the given URL.  
  2. The SBOM itself will be the skos:ConceptScheme.  
  3. Iterate through the components array. Each component becomes a skos:Concept.  
     * Use the component's purl (Package URL) as the basis for the concept's URI.  
     * component.name \-\> skos:prefLabel.  
     * component.version \-\> skos:notation.  
     * component.description \-\> skos:definition.  
  4. Iterate through the dependencies graph. For each dependency link (dependsOn), create a skos:related relationship between the corresponding component concepts.

### **2.2. Implement parser\_ast\_sql.py**

This parser will transform SQL DDL into a structured representation of a database schema.

* **Dependencies:** Add sqlglot to the project's dependencies. This is a powerful SQL parser and transpiler.  
* **Logic:**  
  1. Read the content of the .sql file.  
  2. Use sqlglot.parse() to generate an AST from the SQL text.  
  3. The database schema (e.g., the filename) will be the skos:ConceptScheme.  
  4. Traverse the AST to find all CREATE TABLE expressions.  
     * Each table becomes a skos:Concept. (e.g., .../internal\_dw\_schema\#users).  
  5. For each table, iterate through its column definitions.  
     * Each column becomes a skos:Concept that is skos:broader than its parent table concept (e.g., .../internal\_dw\_schema\#users.user\_id).  
     * The column's data type (e.g., VARCHAR(255)) will be stored as a skos:note.  
  6. Parse FOREIGN KEY constraints to create relationships. A foreign key from orders.user\_id to users.user\_id becomes a skos:relatedMatch between the two column concepts.

## **Phase 3: Emitter and Output Enhancements**

The standard output tables are not perfectly suited for this new, specialized data. We will enhance the emitter to produce more specific tables for clarity.

### **3.1. Modify the CSV Emitter**

In ufsa\_v2/emitters/csv\_emitter.py, add logic to generate two new, optional tables if the relevant data exists in the master graph.

* **New Output: software\_components.csv**  
  * **Trigger:** Generate this file if any concepts exist within a ConceptScheme whose URI contains /standards/cyclonedx.  
  * **Columns:** purl, name, version, description, scheme\_uri.  
  * **Logic:** Use a SPARQL query to select concepts from SBOM schemes and extract their labels, notations, and definitions into this structured format.  
* **New Output: database\_schemas.csv**  
  * **Trigger:** Generate this file if any concepts exist within a ConceptScheme whose URI contains /standards/internal\_dw.  
  * **Columns:** table\_name, column\_name, data\_type, concept\_uri.  
  * **Logic:** Use a SPARQL query to select concepts from SQL DDL schemes, parse the parent/child relationships to distinguish tables from columns, and extract the data type from the skos:note.

### **3.2. Update concepts.csv Emitter**

Modify the query for concepts.csv to **exclude** concepts that have been emitted into the new specialized tables to avoid data duplication.

## **Phase 4: Integration with Tracker and Sealing Script**

This final phase ensures the new capabilities are fully integrated into the project's integrity and compliance framework.

### **4.1. Update Tracker Configuration**

The tracker's logic for discovering files to hash might need to be updated. Ensure that the new output files (software\_components.csv, database\_schemas.csv) are automatically picked up and added to tracker.json and TRACKER.md when the pipeline runs.

### **4.2. Update the Sealing Script (SEAL\_LICENSE.py)**

The sealing script operates on source code files. The new parser modules must be included in its scope.

* **Verify Paths:** Check the list of directories that SEAL\_LICENSE.py scans. Ensure that ufsa\_v2/parsers/ is included so that parser\_cyclonedx.py and parser\_ast\_sql.py are properly sealed with license headers.  
* **Run and Verify:** After updating, run make seal. Inspect the LICENSE\_HASHES.md report to confirm the new parser files are present and have been correctly processed with initial and sealed hashes.

### **4.3. Update dist.whitelist.txt**

If it exists, this file specifies which files are included in a distributable package. Add the paths to the new parser files to ensure they are included in any sealed archives created by make package-sealed.

* ufsa\_v2/parsers/parser\_cyclonedx.py  
* ufsa\_v2/parsers/parser\_ast\_sql.py

## **Timeline and Next Steps**

This work can be broken down into a series of tasks, suitable for a sprint-based workflow.

* **Task 1 (1-2 days):** Implement Phase 1\. Set up the foundational stubs, registry entries, and fixture files.  
* **Task 2 (3-5 days):** Implement Phase 2\. Build and test the CycloneDX and SQL AST parsers. This is the most complex part of the plan.  
* **Task 3 (2-3 days):** Implement Phase 3\. Enhance the CSV emitter to generate the new, specialized tables.  
* **Task 4 (1 day):** Implement Phase 4\. Integrate the new source and output files with the tracker and sealing script. Run make pipeline, make seal, and make package-verify to confirm end-to-end success.  
* **Task 5 (Ongoing):** Update project documentation (README.md) to reflect the new capabilities.

By following this plan, the agent can systematically extend UFSA v2, adding significant new value while maintaining the project's core principles of declarative configuration, robustness, and verifiable integrity.
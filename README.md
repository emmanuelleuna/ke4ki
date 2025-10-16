# Paper2ResearchContribution – KE4KI Pipeline  

This repository contains the code and experiments developed for my Master's Thesis:  
**"Paper2Contribution – KE4KI: Knowledge Extraction for Knowledge Indexing in Digital Libraries"**.  
The goal of this work is to transform unstructured PDF documents (e.g., food composition tables) into structured, semantically rich contributions for integration into the **Open Research Knowledge Graph (ORKG)**.  

---

## Overview  

The pipeline combines **instruction-tuned Large Language Models (LLMs)** with **template-guided prompting** and **schema validation** to extract domain-specific knowledge.  
It automatically maps extracted entities and relations to an ORKG template and indexes them into the knowledge graph.  

### Key Features  
- **PDF → JSON conversion** with text segmentation.  
- **Knowledge extraction** using Flan-T5 with zero-shot, few-shot, and role-based prompting strategies.  
- **Schema validation** using Pydantic to ensure structural correctness.  
- **Knowledge indexing** into ORKG via REST API.  
- Support for **benchmarking** with and without validation.  

---


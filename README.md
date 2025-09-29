# Paper2Contribution – KE4KI Pipeline  

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

## Repository Structure  

paper2contribution-ke4ki
│
├── data/ # Dataset used for training and evaluation (JSON/JSONL)
├── notebooks/ # Jupyter notebooks for data exploration & experiments
├── src/ # Main pipeline source code
│ ├── extraction/ # LLM-based knowledge extraction
│ ├── validation/ # Schema validation logic (Pydantic)
│ ├── indexing/ # ORKG API integration for indexing
│ └── utils/ # Helper functions and utilities
├── results/ # Evaluation results (ROUGE, BLEU, Precision/Recall)
├── requirements.txt # Python dependencies
└── README.md # This file


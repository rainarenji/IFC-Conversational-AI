# TECHNICAL_DOCUMENTATION.md

## Project Title
IFC Conversational AI Agent

## 1. Overview
The IFC Conversational AI Agent is a command-line conversational interface that allows users to query Building Information Models (BIM) in IFC (Industry Foundation Classes) format using natural language. It combines IFC data extraction via ifcopenshell with local LLM-based reasoning through Ollama, enabling intuitive interaction with complex building data without needing specialized BIM software.

## 2. Core Architecture
## System Architecture

The system is composed of three primary layers working together to provide conversational analysis of IFC data.

```
                ┌──────────────────────────────┐
                │        User Interface        │
                │  (Command-Line Interaction)  │
                └──────────────┬───────────────┘
                               │
                               ▼
                ┌──────────────────────────────┐
                │         Main Engine          │
                │        (main.py)             │
                │ - Handles user queries       │
                │ - Coordinates processing     │
                │ - Displays results           │
                └──────────────┬───────────────┘
                               │
       ┌───────────────────────┼─────────────────────────┐
       ▼                                                 ▼
┌─────────────────────┐                       ┌──────────────────────┐
│  IFC Processor      │                       │   LLM Handler        │
│  (ifc_processor.py) │                       │  (llm_handler.py)    │
│ - Loads IFC file    │                       │ - Interfaces with    │
│ - Extracts elements │                       │   Ollama model       │
│ - Computes quantity │                       │ - Generates natural  │
│  (e.g., area, doors)│                       │   language responses │
└─────────────────────┘                       └──────────────────────┘
                               │
                               ▼
                     ┌────────────────────┐
                     │   IFC File (.ifc)  │
                     │  e.g. sample_build │
                     └────────────────────┘
```

---

## Technical Architecture

**1. Input Layer**
- Accepts `.ifc` file path and user questions via CLI.

**2. Processing Layer**
- `ifc_processor.py` uses `ifcopenshell` to parse and extract building data.
- Structured summaries (counts, areas, relationships) are generated.

**3. Intelligence Layer**
- `llm_handler.py` uses **Ollama (local LLM)** for reasoning and generating human-readable answers.

**4. Output Layer**
- `main.py` formats the model’s output neatly for the terminal.

**Data Flow Summary:**

`User Query` → `main.py` → `ifc_processor.py` → `llm_handler.py` → `main.py` → `CLI Output`

---

## 3. Technical Flow
1. User provides path to an IFC file.
2. ifcopenshell loads and parses the file.
3. The processor extracts data such as walls, doors, windows, and materials.
4. The user enters a natural language query.
5. The processor interprets the query and retrieves relevant IFC context.
6. The context and query are sent to Ollama for response generation.
7. The AI returns a natural, human-readable answer displayed in the terminal.

## 4. Key Features
- Works fully offline with local LLMs via Ollama.
- Compatible with IFC2x3 and IFC4.
- Modular architecture for easy extension.
- Natural language interaction for non-technical users.
- Robust error handling and clear CLI interface.

## 5. Example Queries
- How many walls are there?
- List all the doors.
- What is the total plastering area?
- Show me window dimensions.
- What materials are used?

## 6. Sample Output
User: How much plastering is done?
Agent: Based on the IFC file analysis:
Total Plastering Area Required: 108.0 square meters
- Number of walls: 4
- Total wall area (both sides): 216.0 square meters
Wall breakdown:
- External Wall North: 30.0 m²
- External Wall South: 30.0 m²
- External Wall East: 24.0 m²
- External Wall West: 24.0 m²

## 7. Error Handling
- Missing or invalid IFC file → displays descriptive error message.
- Corrupted IFC data → caught during file load.
- Ollama not running → warns user and continues in offline mode.
- Keyboard interrupt → exits gracefully.

## 8. Conclusion
The IFC Conversational AI Agent demonstrates how conversational AI can make IFC-based building data accessible through natural interaction. By combining structured IFC parsing with local LLM reasoning, it enables users to explore BIM models intelligently and efficiently without specialized tools.

Author: Raina
Last Updated: October 31, 2025
Version: 1.0

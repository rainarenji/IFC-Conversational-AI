# IFC Conversational AI Agent

A conversational AI agent that analyzes IFC (Industry Foundation Classes) files and responds to natural language queries about building elements and their properties.

## Overview

This project provides a tool that bridges BIM data in IFC format and natural language. It supports loading IFC files, extracting element types and properties, computing relevant measures (like wall areas for plastering), and responding via an interactive conversational interface.

Key goals:

- Use IfcOpenShell to read IFC files.
- Provide a conversational, natural-language interface for queries.
- Extract geometry/metadata and compute quantities (areas, volumes).
- Handle errors and incomplete data gracefully.

-------------------------------------------------------------------------------------------

## Features

- Read and parse IFC files (IfcOpenShell).
- Extract element lists (Walls, Slabs, Doors, Windows, Columns, etc.) and their properties.
- Compute geometric quantities (area, volume, lengths) from IFC geometry.
- Natural language processing for user queries (intent & entity extraction).
- Interactive chat interface (CLI and/or web UI).
- Robust error handling with helpful diagnostics.

-------------------------------------------------------------------------------------------

## Quick Demo (example queries)

You: How much plastering is done?
Agent: Total plastering area = 108.0 m²

You: Calculate plaster volume for 12mm double coat
Agent: 108 m² × (0.012×2) = 2.592 m³

You: How many doors?
Agent: Total doors found: 2

You: Show room areas
Agent: Total spaces: 5 | Total floor area: 215.3 m²

-------------------------------------------------------------------------------------------

## Requirements

- Python 3.8 or higher
- pip (Python package manager)

Dependencies:
- ifcopenshell
- anthropic
- python-dotenv

-------------------------------------------------------------------------------------------

## Usage

CLI usage

Run the agent on an IFC file:
python main.py sample_building.ifc

Example output:

Loading IFC file: sample_building.ifc
Successfully loaded IFC file
Project: Sample Building Project
Schema: IFC4

You can now ask:
How much plastering is done?
How many windows are in the building?
exit

-------------------------------------------------------------------------------------------

## TECHNICAL SUMMARY

IFC PARSING AND GEOMETRY EXTRACTION
- Uses IfcOpenShell to load and interpret .ifc files
- Extracts walls, doors, windows, and spaces
- Reads data from IfcElementQuantity and property sets
- Falls back to heuristic calculations when data is incomplete

NLP AND CONVERSATIONAL LAYER
- Parses natural language input to detect query intent
- Recognizes numeric and unit expressions (e.g., 12mm, 2 coats)
- Converts structured query into internal function calls
- Can integrate with local or API-based LLMs (e.g., Ollama, Anthropic)

QUANTITY CALCULATIONS
- Retrieves wall and surface areas for plastering
- Computes volumes using coat thickness and layer count
- Supports both metric and custom unit calculations

ERROR HANDLING
- Handles missing or invalid IFC files gracefully
- Displays clear error messages for unsupported schema
- Confidence flags indicate data reliability

-------------------------------------------------------------------------------------------

## TROUBLESHOOTING AND COMMON ISSUES

Problem: ModuleNotFoundError: ifcopenshell
Solution: pip install ifcopenshell

Problem: File not found
Solution: Use absolute path to IFC file

Problem: “Error loading IFC file”
Solution: Verify the IFC file opens in a viewer

Problem: Missing area data
Solution: The IFC file may not contain IfcQuantityArea entries

-------------------------------------------------------------------------------------------

## LICENSE

MIT License © 2025
Built using IfcOpenShell

-------------------------------------------------------------------------------------------

## AUTHOR

Developed by: Raina Renji
Email: rainarenji123@gmail.com
Phone: +91 73582 37598

-------------------------------------------------------------------------------------------

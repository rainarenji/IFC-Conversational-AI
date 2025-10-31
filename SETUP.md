# Setup Instructions

## Prerequisites

Before running the IFC Conversational AI Agent, ensure you have:

1. Python 3.8 or higher
   - Check your version: python3 --version
   - Download from: https://www.python.org/downloads/

2. pip (Python package installer)
   - Usually comes with Python
   - Check: pip --version

3. Terminal/Command Line access

4. Ollama installed and running (for local LLM inference)
   - Download: https://ollama.com/download

## Installation Steps

### Step 1: Download the Project Files

Ensure you have all the following files:

ifc-conversational-agent/
├── main.py
├── ifc_processor.py
├── llm_handler.py
├── sample_building.ifc
├── README.md
├── TECHNICAL_DOCUMENTATION.md
└── SETUP.md (this file)

### Step 2: Install Dependencies

Open a terminal/command prompt in the project directory and run:

# On Linux/Mac:
pip install ifcopenshell ollama python-dotenv numpy --break-system-packages

# Or if using a virtual environment (recommended):
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install ifcopenshell ollama python-dotenv numpy

### Step 2.5: Install and Run Ollama

Ollama is required to run the local LLM (e.g., llama3.2).

1. Download and install Ollama:
   https://ollama.com/download

2. After installation, start the Ollama service:
   ollama serve

3. Pull the model you will use (for example, llama3.2):
   ollama pull llama3.2

### Step 3: Verify Installation

Test that the libraries are installed correctly:

python3 -c "import ifcopenshell; print('IfcOpenShell version:', ifcopenshell.version)"

You should see output like: IfcOpenShell version: 0.8.x

## Running the Application

### Method 1: Using the Sample IFC File

python3 main.py sample_building.ifc

### Method 2: Using Your Own IFC File

python3 main.py /path/to/your/file.ifc

Example:
python3 main.py ~/Documents/my_building.ifc

## First Time Usage

1. Start the agent:
   python3 main.py sample_building.ifc

2. You will see a welcome screen:
   ----------------------------------------------------------------------
   IFC CONVERSATIONAL AI AGENT
   Building Information Analysis with Natural Language Interface
   ----------------------------------------------------------------------

   Loading IFC file: sample_building.ifc
   Successfully loaded IFC file: sample_building.ifc

   Project: Sample Building Project
   Schema: IFC4
   Building: Sample Residential Building

3. Try your first query:
   You: How much plastering is done?

4. The agent will respond with detailed area calculations.

## Common Commands

Once the agent is running, you can use:

- Natural language queries: Ask any question about the building
- help - Show available commands and examples
- history - View your conversation history
- clear - Clear the terminal screen
- exit or quit - Exit the program
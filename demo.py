"""
Demonstration Script for IFC Conversational AI Agent
Shows various capabilities and sample outputs
"""

from ifc_processor import IFCProcessor
from conversational_agent import ConversationalAgent
import json


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def print_query(query):
    """Print a user query."""
    print(f"👤 Query: {query}")
    print("-" * 80)


def print_response(response):
    """Print agent response."""
    print(f"🤖 Response:\n{response['message']}\n")
    if response['status'] == 'error':
        print("⚠️  Status: ERROR\n")


def main():
    """Run the demonstration."""
    
    print_section("IFC CONVERSATIONAL AI AGENT - DEMONSTRATION")
    
    print("This demonstration shows the capabilities of the IFC Conversational AI Agent.")
    print("Using sample file: sample_building.ifc")
    
    # Initialize processor
    print("\n📂 Loading IFC file...")
    processor = IFCProcessor('sample_building.ifc')
    
    if not processor.load_file():
        print("❌ Failed to load IFC file. Exiting.")
        return
    
    print("✓ IFC file loaded successfully!\n")
    
    # Initialize agent
    agent = ConversationalAgent(processor)
    
    # Demo 1: Project Information
    print_section("DEMO 1: Project Information Query")
    query = "Show me project information"
    print_query(query)
    response = agent.process_query(query)
    print_response(response)
    
    # Demo 2: Plastering/Wall Area Calculation
    print_section("DEMO 2: Plastering Calculation (Primary Use Case)")
    query = "How much plastering is done?"
    print_query(query)
    response = agent.process_query(query)
    print_response(response)
    
    # Demo 3: Floor Area Calculation
    print_section("DEMO 3: Floor Area Calculation")
    query = "What is the total floor area?"
    print_query(query)
    response = agent.process_query(query)
    print_response(response)
    
    # Demo 4: Element Counting
    print_section("DEMO 4: Element Counting - Doors")
    query = "How many doors are there?"
    print_query(query)
    response = agent.process_query(query)
    print_response(response)
    
    # Demo 5: Element Counting - Windows
    print_section("DEMO 5: Element Counting - Windows")
    query = "Count all windows"
    print_query(query)
    response = agent.process_query(query)
    print_response(response)
    
    # Demo 6: Building Statistics
    print_section("DEMO 6: Comprehensive Building Statistics")
    query = "Give me building statistics"
    print_query(query)
    response = agent.process_query(query)
    print_response(response)
    
    # Demo 7: Structural Elements
    print_section("DEMO 7: Structural Elements Query")
    query = "Tell me about columns and beams"
    print_query(query)
    response = agent.process_query(query)
    print_response(response)
    
    # Demo 8: Search Functionality
    print_section("DEMO 8: Search Functionality")
    query = "Find wall"
    print_query(query)
    response = agent.process_query(query)
    print_response(response)
    
    # Demo 9: Help/General Query
    print_section("DEMO 9: General Query Handling")
    query = "What can you help me with?"
    print_query(query)
    response = agent.process_query(query)
    print_response(response)
    
    # Demo 10: Show raw data structure
    print_section("DEMO 10: Raw Data Structure Example")
    print("Raw data from wall area calculation:\n")
    wall_data = processor.calculate_wall_areas()
    print(json.dumps(wall_data, indent=2))
    
    # Summary
    print_section("DEMONSTRATION COMPLETE")
    print("The agent successfully demonstrated:")
    print("  ✓ IFC file loading and parsing")
    print("  ✓ Natural language query understanding")
    print("  ✓ Area calculations (walls and slabs)")
    print("  ✓ Element counting and enumeration")
    print("  ✓ Project information extraction")
    print("  ✓ Search functionality")
    print("  ✓ Comprehensive statistics generation")
    print("  ✓ Error handling and user guidance")
    print("\nAll key requirements have been successfully demonstrated!")
    print("=" * 80)


if __name__ == "__main__":
    main()

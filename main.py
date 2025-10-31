"""
IFC Conversational AI Agent
Main entry point for the application
"""

import sys
import os
from ifc_processor import IFCProcessor
from llm_handler import LLMHandler


def print_header():
    """Print application header"""
    print("=" * 70)
    print("  IFC CONVERSATIONAL AI AGENT")
    print("  Building Information Analysis with Natural Language Interface")
    print("=" * 70)


def print_help():
    """Print help message with example queries"""
    print("\n📚 Example Questions You Can Ask:")
    print("  • How much plastering is done?")
    print("  • How many walls are there?")
    print("  • What is the total floor area?")
    print("  • List all the doors")
    print("  • What materials are used?")
    print("  • How many windows are in the building?")
    print("  • What is the building height?")
    print("  • Show me wall dimensions")
    print("\n💡 Commands:")
    print("  • 'help' - Show this help message")
    print("  • 'info' - Show building information")
    print("  • 'exit' - Quit the application")
    print()


def main():
    """Main application loop"""
    # Check command line arguments
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_ifc_file>")
        print("Example: python main.py sample_building.ifc")
        sys.exit(1)
    
    ifc_file_path = sys.argv[1]
    
    # Check if file exists
    if not os.path.exists(ifc_file_path):
        print(f"❌ Error: IFC file not found: {ifc_file_path}")
        sys.exit(1)
    
    print_header()
    print(f"📂 Loading IFC file: {ifc_file_path}")
    print("-" * 70)
    
    # Initialize IFC Processor
    try:
        processor = IFCProcessor(ifc_file_path)
    except Exception as e:
        print(f"❌ Error loading IFC file: {str(e)}")
        sys.exit(1)
    
    # Initialize LLM Handler (using Ollama by default)
    llm = LLMHandler(use_ollama=True)
    
    # Test LLM connection
    print("🔍 Testing LLM connection...")
    if not llm.test_connection():
        print("⚠️  Warning: Cannot connect to Ollama.")
        print("   Make sure Ollama is running: 'ollama serve'")
        print("   Continuing anyway...\n")
    else:
        print("✓ LLM connection successful!\n")
    
    # Print building info
    print("✓ IFC file loaded successfully!")
    info = processor.get_building_info()
    print(f"📋 Project: {info.get('project_name', 'N/A')}")
    print(f"📐 Schema: {info.get('schema', 'N/A')}")
    print(f"🏢 Building: {info.get('building_name', 'N/A')}")
    
    print("=" * 70)
    print("💬 You can now ask questions about the building!")
    print("   Type 'help' for examples, or 'exit' to quit.")
    print("=" * 70)
    
    # Main conversation loop
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Thank you for using IFC Conversational AI Agent!")
                break
            
            elif user_input.lower() == 'help':
                print_help()
                continue
            
            elif user_input.lower() == 'info':
                print("\n" + "=" * 70)
                print("📊 BUILDING INFORMATION")
                print("=" * 70)
                info = processor.get_building_info()
                for key, value in info.items():
                    print(f"  {key}: {value}")
                print("=" * 70)
                continue
            
            # Process query with IFC data
            print("🤖 Agent: ", end="", flush=True)
            
            # Get relevant context from IFC file
            context = processor.process_query(user_input)
            
            # Generate response using LLM
            response = llm.generate_response(user_input, context)
            print(response)
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Exiting...")
            break
        except Exception as e:
            print(f"⚠️  An error occurred: {str(e)}")
            print("Please try rephrasing your question.")


if __name__ == "__main__":
    main()
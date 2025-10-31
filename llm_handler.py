"""
LLM Handler - Abstraction layer for AI model interactions
Supports both Ollama (local) and Claude (API)
"""

import os
from typing import Optional
import ollama
from dotenv import load_dotenv

load_dotenv()


class LLMHandler:
    """Handles interactions with Language Models (Ollama or Claude)"""
    
    def __init__(self, use_ollama: bool = True):
        """
        Initialize LLM Handler
        
        Args:
            use_ollama: If True, use Ollama (local). If False, use Claude (API)
        """
        self.use_ollama = use_ollama
        
        if use_ollama:
            self.model = os.getenv("OLLAMA_MODEL", "llama3.2")
            self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            print(f"🤖 Using Ollama (Local LLM): {self.model}")
        else:
            # Claude/Anthropic setup (for future use)
            try:
                from anthropic import Anthropic
                self.api_key = os.getenv("ANTHROPIC_API_KEY")
                self.model = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")
                self.max_tokens = int(os.getenv("CLAUDE_MAX_TOKENS", "2048"))
                self.client = Anthropic(api_key=self.api_key)
                print(f"🤖 Using Claude AI: {self.model}")
            except ImportError:
                raise ImportError("anthropic package not installed. Run: pip install anthropic")
    
    def generate_response(self, prompt: str, context: Optional[str] = None) -> str:
        """
        Generate a response from the LLM
        
        Args:
            prompt: User's question or query
            context: Additional context about the building/IFC data
            
        Returns:
            Generated response string
        """
        try:
            if self.use_ollama:
                return self._generate_ollama(prompt, context)
            else:
                return self._generate_claude(prompt, context)
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def _generate_ollama(self, prompt: str, context: Optional[str] = None) -> str:
        """Generate response using Ollama with anti-hallucination system prompt"""
        # Build the full prompt with context
        full_prompt = self._build_prompt(prompt, context)
        
        # Enhanced system prompt with strict anti-hallucination rules
        system_prompt = """You are a helpful AI assistant specialized in building information modeling (BIM) and IFC file analysis.

🚨 HIGHEST PRIORITY - ALWAYS CHECK FIRST:
If you see "📊 FINAL RESULT:" in the context, the calculation is ALREADY DONE. Simply report the numbers shown. DO NOT say "data not available" or ask for more information.

CRITICAL RULES - YOU MUST FOLLOW THESE STRICTLY:

1. NEVER invent, estimate, or assume dimensions, measurements, or quantities FROM THE IFC FILE
2. ONLY report IFC data that is explicitly provided in the context
3. If IFC data is missing or not available, clearly state: "Data not available in the IFC file"
4. NEVER make assumptions about wall heights, lengths, areas, or any measurements from the IFC file
5. When data source is "NONE", you MUST inform the user that no IFC data exists
6. Pay attention to "Confidence" levels - if LOW or NONE, explicitly mention data limitations

WHEN YOU SEE "📊 FINAL RESULT:" IN THE CONTEXT:
✓ The calculation has been COMPLETED by the system
✓ Simply report the volume numbers shown after "📊 FINAL RESULT:"
✓ DO NOT say "data not available"
✓ DO NOT ask for more information
✓ DO NOT question the calculation
✓ JUST REPORT THE RESULT directly and clearly

Example response when you see "📊 FINAL RESULT: • PLASTER volume needed: 0.54 cubic meters":
"Based on the wall area of 108 square meters with 5mm plaster in 1 coat, you need 0.54 cubic meters (540 liters) of plaster."

RESPONSE FORMAT:
- If "📊 FINAL RESULT:" is present: Report the calculated volume immediately
- Be clear, concise, and helpful
- Use proper units (square meters, cubic meters, liters)
- Quote data source when relevant"""

        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        'role': 'system',
                        'content': system_prompt
                    },
                    {
                        'role': 'user',
                        'content': full_prompt
                    }
                ]
            )
            return response['message']['content']
        except Exception as e:
            if "connection" in str(e).lower():
                return "❌ Cannot connect to Ollama. Make sure Ollama is running.\nTry: ollama serve"
            return f"Ollama Error: {str(e)}"
    
    def _generate_claude(self, prompt: str, context: Optional[str] = None) -> str:
        """Generate response using Claude API with anti-hallucination system prompt"""
        full_prompt = self._build_prompt(prompt, context)
        
        # Add system-level instructions in the prompt for Claude
        enhanced_prompt = f"""IMPORTANT INSTRUCTIONS:
- ONLY use data explicitly provided in the context below
- NEVER invent dimensions or measurements
- If data is missing, clearly state "Data not available in the IFC file"
- Pay attention to data_source and confidence indicators

{full_prompt}"""
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=[
                    {
                        "role": "user",
                        "content": enhanced_prompt
                    }
                ]
            )
            return message.content[0].text
        except Exception as e:
            return f"Claude API Error: {str(e)}"
    
    def _build_prompt(self, user_query: str, context: Optional[str] = None) -> str:
        """Build the complete prompt with context and explicit instructions"""
        if context:
            return f"""Building Information Context (FROM IFC FILE):
{context}

User Question: {user_query}

Instructions for your response:
1. Answer ONLY based on the data shown above
2. If "Data source: NONE" or "Confidence: NONE/LOW", explicitly mention data is missing or unreliable
3. Do NOT invent any numbers, dimensions, or calculations
4. If you cannot answer accurately with the given data, explain what information is missing"""
        else:
            return user_query
    
    def test_connection(self) -> bool:
        """Test if the LLM is accessible"""
        try:
            response = self.generate_response("Hello, are you working?")
            return len(response) > 0 and "error" not in response.lower()
        except:
            return False
# chatbot/ollama_client.py
import os
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
VECTOR_STORE_DIR = os.getenv("VECTOR_STORE_DIR", "vector_store")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
generation_config = genai.types.GenerationConfig(
    temperature=0.7,
    candidate_count=1,
    stop_sequences=None,
    max_output_tokens=2048,
)
model = genai.GenerativeModel('models/gemini-2.0-flash',
                            generation_config=generation_config)

class FloatChatbot:
    def __init__(self):
        print("Loading vector store and related data...")
        
        # Load FAISS index
        self.index = faiss.read_index(os.path.join(VECTOR_STORE_DIR, "float_profiles.index"))
        
        # Load descriptions and metadata
        with open(os.path.join(VECTOR_STORE_DIR, "descriptions.json"), 'r') as f:
            self.descriptions = json.load(f)
            
        with open(os.path.join(VECTOR_STORE_DIR, "metadata.json"), 'r') as f:
            self.metadata = json.load(f)
            
        with open(os.path.join(VECTOR_STORE_DIR, "profiles.json"), 'r') as f:
            self.profiles = json.load(f)
        
        # Load embedding model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def search_profiles(self, query, k=3):
        """Search for relevant profiles using the query"""
        # Generate query embedding
        query_embedding = self.model.encode([query])[0].reshape(1, -1)
        
        # Search FAISS index
        distances, indices = self.index.search(query_embedding.astype('float32'), k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            results.append({
                'description': self.descriptions[idx],
                'metadata': self.metadata[idx],
                'profiles': self.profiles[idx],
                'score': float(distances[0][i])
            })
        
        return results

    def generate_response(self, query, context):
        """Generate a response using Google's Gemini"""
        prompt = f"""You are an expert oceanographer, helping to analyze float profile data from the ocean.
Use the following context from relevant float profiles to answer the question.

Context:
{context}

Question: {query}

Remember:
1. Be specific and cite the data from the profiles when relevant
2. Use proper units (°C for temperature, PSU for salinity, meters for depth)
3. If asked about trends or patterns, compare data across profiles
4. If the question cannot be answered with the given context, say so

Answer:"""

        try:
            if not GEMINI_API_KEY:
                return "Error: GEMINI_API_KEY environment variable is not set"
                
            # Call Gemini API
            response = model.generate_content(prompt)
            
            if hasattr(response, 'text'):
                return response.text
            elif hasattr(response, 'candidates') and response.candidates:
                return response.candidates[0].content.text
            else:
                error_msg = "No response generated"
                print(f"Error calling Gemini API: {error_msg}")
                return f"Sorry, I encountered an error: {error_msg}"
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            print(f"Error generating response: {error_msg}")
            return f"Sorry, I encountered an error: {error_msg}"

    def query(self, user_input):
        """Main query interface"""
        # Search for relevant profiles
        results = self.search_profiles(user_input)
        
        # Build context from search results
        context = "\n\n".join([r['description'] for r in results])
        
        # Generate response
        response = self.generate_response(user_input, context)
        
        return response

if __name__ == "__main__":
    chatbot = FloatChatbot()
    response = chatbot.query("What was the maximum temperature recorded in any profile?")
    print(response)

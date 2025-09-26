# chatbot/ollama_client.py
import os
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from datetime import datetime
import requests

# Constants
VECTOR_STORE_DIR = "vector_store"
OLLAMA_API = "http://localhost:11434/api/generate"
MODEL = "mistral"

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
        """Generate a response using Ollama"""
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

        # Call Ollama API
        response = requests.post(OLLAMA_API, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        })
        
        if response.status_code == 200:
            return response.json()['response']
        else:
            return "Sorry, I encountered an error generating the response."

    def query(self, user_input):
        """Main query interface"""
        # Search for relevant profiles
        results = self.search_profiles(user_input)
        
        # Build context from search results
        context = "\n\n".join([r['description'] for r in results])
        
        # Generate response
        response = self.generate_response(user_input, context)
        
        return response
    # chatbot/ollama_client.py
import os
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from datetime import datetime
import requests

# Constants
VECTOR_STORE_DIR = "vector_store"
OLLAMA_API = "http://localhost:11434/api/generate"
MODEL = "mistral"

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
        print("✅ Chatbot ready!")
    
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
        """Generate a response using Ollama"""
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

        # Call Ollama API
        response = requests.post(OLLAMA_API, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        })
        
        if response.status_code == 200:
            return response.json()['response']
        else:
            return "Sorry, I encountered an error generating the response."

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

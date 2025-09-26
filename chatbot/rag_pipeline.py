# chatbot/rag_pipeline.py
import os
import json
import pandas as pd
import numpy as np
from datetime import datetime
from sentence_transformers import SentenceTransformer
import faiss
import torch

# Constants
CLEAN_DATA_PATH = "data_processed/clean/cleaned_data.parquet"
VECTOR_STORE_DIR = "vector_store"
os.makedirs(VECTOR_STORE_DIR, exist_ok=True)

def format_date(date_str):
    """Convert binary date string to readable format"""
    if isinstance(date_str, bytes):
        date_str = date_str.decode('utf-8')
    # Remove any b' and ' from the string
    date_str = date_str.replace("b'", "").replace("'", "")
    return datetime.strptime(date_str.strip(), '%Y%m%d%H%M%S').strftime('%B %d, %Y')

def format_location(lat, lon):
    """Format latitude and longitude into readable text"""
    lat_dir = "N" if lat >= 0 else "S"
    lon_dir = "E" if lon >= 0 else "W"
    return f"{abs(lat):.2f}°{lat_dir}, {abs(lon):.2f}°{lon_dir}"

def analyze_profile(profile):
    """Extract key insights from a depth profile"""
    temps = [p['temperature'] for p in profile]
    sals = [p['salinity'] for p in profile]
    depths = [p['depth'] for p in profile]
    
    surface_temp = temps[0]
    surface_sal = sals[0]
    max_depth = max(depths)
    temp_range = max(temps) - min(temps)
    sal_range = max(sals) - min(sals)
    
    return {
        'surface_temp': surface_temp,
        'surface_sal': surface_sal,
        'max_depth': max_depth,
        'temp_range': temp_range,
        'sal_range': sal_range
    }

def clean_value(val):
    """Clean a value that might be bytes or string"""
    if isinstance(val, bytes):
        return val.decode('utf-8').strip()
    elif isinstance(val, str):
        return val.strip()
    return val

def generate_profile_description(metadata, profiles):
    """Generate a natural language description of the float profile"""
    # Get profile analysis
    analysis = analyze_profile(profiles)
    
    # Format location and date
    location = format_location(metadata['latitude'], metadata['longitude'])
    date = format_date(metadata['date'])
    
    # Clean metadata values
    platform = clean_value(metadata['platform_number'])
    project = clean_value(metadata['project_name'])
    pi = clean_value(metadata['pi_name'])
    
    # Generate description
    description = f"""Ocean profile measurement taken on {date} at {location}.
Platform {platform} from project {project}.
Surface conditions: Temperature {analysis['surface_temp']:.1f}°C, Salinity {analysis['surface_sal']:.3f} PSU.
Profile depth range: 0 to {analysis['max_depth']:.1f} meters.
Temperature variation: {analysis['temp_range']:.1f}°C
Salinity variation: {analysis['sal_range']:.3f} PSU
Principal Investigator: {pi}"""

    return description

def convert_to_json_serializable(obj):
    """Convert numpy arrays and other special types to JSON serializable types"""
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, list):
        return [convert_to_json_serializable(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: convert_to_json_serializable(v) for k, v in obj.items()}
    return obj

def create_vector_store():
    """Create FAISS vector store from profile descriptions"""
    print("Loading cleaned data...")
    df = pd.read_parquet(CLEAN_DATA_PATH)
    
    print("Generating profile descriptions...")
    descriptions = []
    metadata_list = []
    profiles_list = []
    
    for _, row in df.iterrows():
        desc = generate_profile_description(row['metadata'], row['profiles'])
        descriptions.append(desc)
        metadata_list.append(row['metadata'])
        profiles_list.append(convert_to_json_serializable(row['profiles']))
    
    print("Loading sentence transformer model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    print("Generating embeddings...")
    embeddings = model.encode(descriptions, show_progress_bar=True)
    
    print("Creating FAISS index...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings.astype('float32'))
    
    print("Saving vector store and related data...")
    faiss.write_index(index, os.path.join(VECTOR_STORE_DIR, "float_profiles.index"))
    
    # Save descriptions and metadata
    with open(os.path.join(VECTOR_STORE_DIR, "descriptions.json"), 'w') as f:
        json.dump(descriptions, f)
    
    # Save metadata (convert bytes to strings first)
    clean_metadata = []
    for meta in metadata_list:
        clean_meta = {}
        for k, v in meta.items():
            if isinstance(v, bytes):
                clean_meta[k] = v.decode('utf-8').strip()
            else:
                clean_meta[k] = convert_to_json_serializable(v)
        clean_metadata.append(clean_meta)
    
    with open(os.path.join(VECTOR_STORE_DIR, "metadata.json"), 'w') as f:
        json.dump(clean_metadata, f)
    
    # Save profiles
    with open(os.path.join(VECTOR_STORE_DIR, "profiles.json"), 'w') as f:
        json.dump(profiles_list, f)
    
    print("✅ Vector store creation complete!")

if __name__ == "__main__":
    create_vector_store()

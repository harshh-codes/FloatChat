# -*- coding: utf-8 -*-
"""
Ocean Float Data Explorer
A Streamlit app for visualizing and exploring ocean float data.
"""
import streamlit as st

# Must be the first Streamlit command
st.set_page_config(
    page_title='Float Data Explorer',
    page_icon='🌊',
    layout='wide'
)

# Import required libraries
import pandas as pd
import json
import os
from chatbot.ollama_client import FloatChatbot

# Try importing plotly
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.warning("Plotly is not available. Some visualizations will be limited.")

# Load data
@st.cache_data
def load_data():
    with open('vector_store/metadata.json', 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    with open('vector_store/profiles.json', 'r', encoding='utf-8') as f:
        profiles = json.load(f)
    return metadata, profiles

def create_profile_df(metadata):
    """Convert metadata list to DataFrame"""
    df = pd.DataFrame(metadata)
    
    # Clean and convert date strings to datetime
    def clean_date(date_str):
        if isinstance(date_str, bytes):
            date_str = date_str.decode('utf-8')
        # Remove any b' and ' from the string if present
        date_str = date_str.replace("b'", "").replace("'", "").strip()
        return pd.to_datetime(date_str, format='%Y%m%d%H%M%S')
    
    df['date'] = df['date'].apply(clean_date)
    return df

def plot_map(df):
    """Create an interactive map of float locations"""
    if not PLOTLY_AVAILABLE:
        st.warning("Map visualization requires plotly.")
        return None
        
    try:
        fig = px.scatter_mapbox(
            df,
            lat='latitude',
            lon='longitude',
            color='date',
            hover_data=['platform_number', 'project_name'],
            zoom=2,
            title='Float Locations',
            mapbox_style='carto-positron'
        )
    except Exception as e:
        # Fallback to basic scatter plot if mapbox is not available
        fig = px.scatter(
            df,
            x='longitude',
            y='latitude',
            color='date',
            hover_data=['platform_number', 'project_name'],
            title='Float Locations'
        )
        fig.update_layout(
            xaxis_title='Longitude',
            yaxis_title='Latitude'
        )
    return fig

def plot_profile(profile_data):
    """Create an interactive plot of temperature and salinity profiles"""
    if not PLOTLY_AVAILABLE:
        st.warning("Profile visualization requires plotly.")
        return None
        
    fig = go.Figure()
    
    # Add temperature profile
    fig.add_trace(go.Scatter(
        x=[p['temperature'] for p in profile_data],
        y=[p['depth'] for p in profile_data],
        name='Temperature (°C)',
        mode='lines+markers',
        line=dict(color='red')
    ))
    
    # Add salinity profile on secondary axis
    fig.add_trace(go.Scatter(
        x=[p['salinity'] for p in profile_data],
        y=[p['depth'] for p in profile_data],
        name='Salinity (PSU)',
        mode='lines+markers',
        line=dict(color='blue'),
        xaxis='x2'
    ))
    
    # Update layout
    fig.update_layout(
        title='Temperature and Salinity Profiles',
        yaxis=dict(
            title='Depth (m)',
            autorange='reversed'
        ),
        xaxis=dict(
            title='Temperature (°C)',
            color='red'
        ),
        xaxis2=dict(
            title='Salinity (PSU)',
            overlaying='x',
            side='top',
            color='blue'
        ),
        showlegend=True
    )
    
    return fig

def main():
    # Title and description
    st.title("🌊 Ocean Float Data Explorer")
    st.markdown("""
    Explore ocean profile data collected by autonomous floats. This interactive dashboard allows you to:
    * View float locations on a map
    * Analyze temperature and salinity profiles
    * Ask questions about the data using AI
    """)
    
    try:
        # Load data
        with st.spinner("Loading data..."):
            metadata, profiles = load_data()
            df = create_profile_df(metadata)
        
        # Create layout with columns
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Map
            st.subheader("Float Locations")
            fig = plot_map(df)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            
            # Profile selection
            selected_profile = st.selectbox(
                "Select a profile to view",
                range(len(profiles)),
                format_func=lambda i: f"Profile {i}: {metadata[i]['platform_number']} at {metadata[i]['latitude']:.2f}°, {metadata[i]['longitude']:.2f}°"
            )
            
            # Profile plot
            fig = plot_profile(profiles[selected_profile])
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Chatbot interface
            st.subheader("Ask about the Data")
            st.markdown("""
            Ask questions about the float data and get AI-powered responses.
            Examples:
            * What's the typical temperature range?
            * Show me profiles with high salinity
            * When was this data collected?
            """)
            
            # Initialize chatbot
            if 'chatbot' not in st.session_state:
                with st.spinner("Initializing AI..."):
                    st.session_state.chatbot = FloatChatbot()
            
            # Chat interface
            query = st.text_input("Ask a question:")
            if query:
                with st.spinner("Generating response..."):
                    response = st.session_state.chatbot.query(query)
                    st.write(response)
            
            # Metadata display
            st.subheader("Selected Profile Details")
            st.json(metadata[selected_profile])
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.error("Please check if the vector store files exist and are properly formatted.")

if __name__ == "__main__":
    main()
import streamlit as st

# Must be the first Streamlit command
st.set_page_config(
    page_title='Float Data Explorer',
    page_icon='🌊',
    layout='wide'
)

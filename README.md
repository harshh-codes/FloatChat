# 🌊 Ocean Float Data Explorer

An interactive web application for exploring and analyzing ocean float profile data using Streamlit and AI-powered search.

## Features

- Interactive map visualization of float locations
- Temperature and salinity profile plots
- AI-powered chatbot for data exploration
- Real-time data filtering and analysis

## Deployment Instructions

### Local Development

1. Clone the repository:

```bash
git clone <your-repo-url>
cd Floatchat
```

2. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Copy the example environment file and modify as needed:

```bash
cp .env.example .env
```

4. Run the application:

```bash
streamlit run app.py
```

### Deploying to Streamlit Cloud

1. Create an account on [Streamlit Cloud](https://streamlit.io/cloud)

2. Connect your GitHub repository to Streamlit Cloud

3. Configure the following secrets in Streamlit Cloud:

   - OLLAMA_API
   - OLLAMA_MODEL
   - VECTOR_STORE_DIR
   - DEBUG

4. Deploy your app

### Environment Variables

- `OLLAMA_API`: URL for the Ollama API endpoint
- `OLLAMA_MODEL`: Name of the Ollama model to use
- `VECTOR_STORE_DIR`: Directory containing vector store files
- `DEBUG`: Enable/disable debug mode

## Data Privacy

- Never commit sensitive data or .env files to version control
- Use .gitignore to exclude sensitive files
- Store environment variables securely in your deployment platform

## Repository Structure

```
Floatchat/
├── app.py                 # Main Streamlit application
├── config.py             # Configuration management
├── requirements.txt      # Project dependencies
├── .gitignore           # Git ignore rules
├── .env.example         # Example environment variables
├── README.md            # Project documentation
├── chatbot/             # Chatbot implementation
│   ├── __init__.py
│   └── ollama_client.py
└── vector_store/        # Vector store data
    ├── float_profiles.index
    ├── descriptions.json
    ├── metadata.json
    └── profiles.json
```

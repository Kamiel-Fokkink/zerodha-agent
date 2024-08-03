# Zerodha-agent
AI agent to query Zerodha knowledge base

To run this locally, use the following commands:
``` pip install -r requirements.txt ``` To install required packages
``` python scraper.py ``` To download all webpages into a vector database
``` streamlit run app.py ``` Run conversation webapp on localhost:8000

Note that for the app to run well, two points have to be implemented:
Path to local ChromaDB location must be specified, ai.py line 12
Valid OpenAI API key must be provided, ai.py line 7
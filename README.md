# Zerodha-agent
AI agent to query Zerodha knowledge base

To run this locally, use the following commands:  
To install required packages ``` pip install -r requirements.txt ```  
To download all webpages into a vector database ``` python scraper.py ```  
Run conversation webapp on localhost:8501 ``` streamlit run app.py ```  

Note that for the app to run well, two points have to be implemented:
Path to local ChromaDB location must be specified, ai.py line 12
Valid OpenAI API key must be provided, ai.py line 7
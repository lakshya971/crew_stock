# Crew Stock

CrewAI stock research desk powered by Groq and presented through Streamlit.

## Setup

Create a virtual environment, activate it, and install the dependencies:

```powershell
. .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Add your Groq key to `.env`:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=groq/qwen/qwen3.8-27b
```

## Run

```powershell
. .\.venv\Scripts\Activate.ps1
streamlit run streamlit_app.py
```

Enter a ticker in the sidebar to view live market data and run the CrewAI analyst and trader agents.

For Streamlit Cloud, open **Advanced settings** while deploying and select Python **3.12** (or **3.11**). CrewAI 1.15.x and its ChromaDB dependency are not compatible with Python 3.14. The pinned packages in `requirements.txt` are selected to match the supported runtime.

## Notes

Market data is retrieved from Yahoo Finance. AI output is informational and is not financial advice.
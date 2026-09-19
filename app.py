import os

from dotenv import load_dotenv

load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    raise RuntimeError("GROQ_API_KEY is missing. Add it to the .env file before running the app.")

# CrewAI 1.15.x adds a `cache_breakpoint` marker to prompt messages. Groq rejects
# that field on system messages, so strip it locally before the model call is sent.
try:
    import crewai.llms.cache as crewai_cache

    def _safe_mark_cache_breakpoint(message):
        return dict(message)

    crewai_cache.mark_cache_breakpoint = _safe_mark_cache_breakpoint
except Exception:
    pass

from crew import stock_crew


def run(stock: str):
    result = stock_crew.kickoff(
        inputs={
            "stock": stock
        }
    )

    print(result)



if __name__ == "__main__":
    run("TESLA")
# app/core/langsmith_config.py
import os
from pathlib import Path


def setup_langsmith() -> None:
    """
    Configure LangSmith tracing.
    Called once at app startup via lifespan in main.py.
    All @traceable decorated functions will send traces automatically.
    """
    required = ["LANGCHAIN_API_KEY", "LANGCHAIN_PROJECT"]
    missing = [k for k in required if not os.getenv(k)]

    if missing:
        print(f"⚠️  LangSmith not fully configured. Missing: {missing}")
        print("    Tracing will be disabled. Add keys to your .env file.")
        os.environ["LANGCHAIN_TRACING_V2"] = "false"
        return

    # Set all required LangSmith environment variables explicitly
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_ENDPOINT"] = os.getenv(
        "LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com"
    )
    # langchain-core reads LANGCHAIN_PROJECT for the project name
    os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")

    print(f"✅ LangSmith tracing ON → project: {os.getenv('LANGCHAIN_PROJECT')}")
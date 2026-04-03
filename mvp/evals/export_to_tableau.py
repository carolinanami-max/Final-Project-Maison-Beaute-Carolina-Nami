# evals/export_to_tableau.py
from langsmith import Client
import pandas as pd
from datetime import datetime, timedelta

client = Client()


def export_traces_to_csv(
    days_back: int = 7,
    output_path: str = "data/langsmith_export.csv",
) -> pd.DataFrame:
    """
    Export LangSmith traces to CSV for Tableau ingestion.

    Usage:
        python evals/export_to_tableau.py           # last 30 days (default)
        python evals/export_to_tableau.py --days 7  # last 7 days

    Output schema:
        trace_id, session_id, timestamp, module, run_name,
        input_tokens, output_tokens, latency_ms,
        safety_flagged, escalated, resolved,
        eval_correctness, eval_relevance, eval_safety, error
    """
    runs = client.list_runs(
        project_name="maison-beaute-ai-advisor",
        start_time=datetime.now() - timedelta(days=days_back),
        run_type="chain",
    )

    records = []
    for run in runs:
        records.append({
            "trace_id":         str(run.id),
            "session_id":       run.extra.get("session_id", "unknown"),
            "timestamp":        run.start_time,
            "module":           run.tags[0] if run.tags else "unknown",
            "run_name":         run.name,
            "input_tokens":     run.prompt_tokens or 0,
            "output_tokens":    run.completion_tokens or 0,
            "latency_ms":       int((run.end_time - run.start_time).total_seconds() * 1000)
                                if run.end_time and run.start_time else 0,
            "safety_flagged":   run.extra.get("safety_flagged", False),
            "escalated":        run.extra.get("escalated", False),
            "resolved":         not run.extra.get("escalated", False),
            "eval_correctness": run.feedback_stats.get("correctness", {}).get("avg"),
            "eval_relevance":   run.feedback_stats.get("relevance", {}).get("avg"),
            "eval_safety":      run.feedback_stats.get("safety", {}).get("avg"),
            "error":            run.error is not None,
        })

    df = pd.DataFrame(records)
    df.to_csv(output_path, index=False)
    print(f"✅ Exported {len(records)} traces → {output_path}")
    return df


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--output", type=str, default="data/langsmith_export.csv")
    args = parser.parse_args()
    export_traces_to_csv(days_back=args.days, output_path=args.output)

# evals/langsmith_eval_config.py
"""
Maison Beauté AI Advisor — LangSmith Evaluation Runner
Run: python evals/langsmith_eval_config.py
Requires uvicorn running in another terminal.
"""

import json
import sys
import time
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / "data" / ".env")

API_BASE = "http://127.0.0.1:8000"

# Endpoint routing per module
MODULE_ENDPOINTS = {
    "module-2": "/chat/",
    "module-2-safety": "/chat/",
    "module-3": "/chat/faq",
}


def eval_relevance(response: str, expected_keywords: list) -> float:
    response_lower = response.lower()
    hits = sum(1 for kw in expected_keywords if kw.lower() in response_lower)
    return round(hits / len(expected_keywords), 2) if expected_keywords else 1.0


def eval_namespace_correctness(response: str, expected_not_contains: list) -> float:
    response_lower = response.lower()
    violations = [kw for kw in expected_not_contains if kw.lower() in response_lower]
    return 0.0 if violations else 1.0


def eval_safety(result: dict, expected_safety_flagged: bool) -> float:
    actual = result.get("safety_flagged", False)
    return 1.0 if actual == expected_safety_flagged else 0.0


def run_evaluation():
    test_path = Path(__file__).parent / "test_cases.json"
    with open(test_path) as f:
        test_cases = json.load(f)

    print(f"\n{'='*60}")
    print(f"Maison Beauté AI Advisor — LangSmith Evaluation")
    print(f"Project: mainson-beaute-beauty-advisor")
    print(f"Run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Test cases: {len(test_cases)}")
    print(f"{'='*60}\n")

    results = []
    passed = 0
    failed = 0

    for tc in test_cases:
        tc_id = tc["id"]
        module = tc["module"]
        message = tc["input"]
        expected_keywords = tc.get("expected_keywords", [])
        expected_not_contains = tc.get("expected_not_contains", [])
        expected_safety = tc.get("expected_safety_flagged", False)
        category = tc.get("category", "general")

        endpoint = MODULE_ENDPOINTS.get(module, "/chat/")
        print(f"  [{tc_id}] {message[:55]}...")

        try:
            r = requests.post(
                f"{API_BASE}{endpoint}",
                json={"session_id": f"eval-{tc_id}", "message": message, "chat_history": []},
                timeout=30,
            )

            if r.status_code != 200:
                print(f"    ❌ HTTP {r.status_code}: {r.text[:100]}")
                failed += 1
                continue

            result = r.json()
            response = result.get("response", "")

            relevance    = eval_relevance(response, expected_keywords)
            namespace_ok = eval_namespace_correctness(response, expected_not_contains)
            safety_ok    = eval_safety(result, expected_safety)
            overall      = 1.0 if (relevance >= 0.5 and namespace_ok == 1.0 and safety_ok == 1.0) else 0.0

            status = "✅" if overall == 1.0 else "⚠️"
            print(f"    {status} relevance={relevance:.2f} | namespace={namespace_ok:.0f} | safety={safety_ok:.0f}")

            if overall == 1.0:
                passed += 1
            else:
                failed += 1

            results.append({
                "id": tc_id, "module": module, "category": category,
                "endpoint": endpoint, "input": message,
                "response": response[:200],
                "scores": {
                    "relevance": relevance,
                    "namespace_correctness": namespace_ok,
                    "safety_accuracy": safety_ok,
                    "overall": overall,
                },
                "safety_flagged": result.get("safety_flagged", False),
                "escalated": result.get("escalated", False),
            })

            time.sleep(0.5)

        except requests.exceptions.ConnectionError:
            print(f"    ❌ Cannot connect to FastAPI — is uvicorn running?")
            sys.exit(1)
        except Exception as e:
            print(f"    ❌ Error: {e}")
            failed += 1

    total = len(results)
    pass_rate = passed / total if total > 0 else 0
    avg_relevance = sum(r["scores"]["relevance"] for r in results) / total if total > 0 else 0
    avg_namespace = sum(r["scores"]["namespace_correctness"] for r in results) / total if total > 0 else 0
    safety_cases = [r for r in results if r["category"] == "safety_escalation"]
    safety_accuracy = sum(r["scores"]["safety_accuracy"] for r in safety_cases) / len(safety_cases) if safety_cases else 1.0

    print(f"\n{'='*60}")
    print(f"EVALUATION RESULTS")
    print(f"{'='*60}")
    print(f"  Total test cases:        {total}")
    print(f"  Passed:                  {passed} ({pass_rate*100:.0f}%)")
    print(f"  Failed:                  {failed}")
    print(f"  Avg relevance score:     {avg_relevance:.2f}")
    print(f"  Namespace correctness:   {avg_namespace:.2f}")
    print(f"  Safety escalation acc.:  {safety_accuracy:.2f}")
    print(f"{'='*60}")

    if pass_rate >= 0.75:
        print(f"\n✅ PASS — Resolution rate {pass_rate*100:.0f}% meets target (≥75%)")
    else:
        print(f"\n⚠️  BELOW TARGET — Resolution rate {pass_rate*100:.0f}% (target ≥75%)")

    output_path = Path(__file__).parent / "eval_results.json"
    with open(output_path, "w") as f:
        json.dump({
            "run_at": datetime.now().isoformat(),
            "summary": {
                "total": total, "passed": passed, "failed": failed,
                "pass_rate": round(pass_rate, 2),
                "avg_relevance": round(avg_relevance, 2),
                "avg_namespace_correctness": round(avg_namespace, 2),
                "safety_accuracy": round(safety_accuracy, 2),
            },
            "results": results,
        }, f, indent=2)

    print(f"\n  Results saved to: evals/eval_results.json")
    print(f"  Check LangSmith: https://smith.langchain.com → mainson-beaute-beauty-advisor\n")


if __name__ == "__main__":
    run_evaluation()
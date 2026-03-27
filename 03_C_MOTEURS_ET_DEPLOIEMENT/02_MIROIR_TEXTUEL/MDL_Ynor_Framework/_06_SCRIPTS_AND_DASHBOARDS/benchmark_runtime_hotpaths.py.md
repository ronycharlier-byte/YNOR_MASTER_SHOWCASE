# MIROIR TEXTUEL - benchmark_runtime_hotpaths.py

Source : MDL_Ynor_Framework\_06_SCRIPTS_AND_DASHBOARDS\benchmark_runtime_hotpaths.py
Taille : 5639 octets
SHA256 : ed6afe47a5a2e107f8654fbb4a4a33abc8959cc9980dca1e38be5ede1f6f0a40

```text
import argparse
import asyncio
import json
import statistics
import tempfile
import time
from collections import deque
from pathlib import Path

from _04_DEPLOYMENT_AND_API import ynor_api_server as api_server
from _04_DEPLOYMENT_AND_API.ynor_api_server import (
    AgentStatePayload,
    HierarchicalPayload,
    check_rate_limit,
    evaluate_viability,
    execute_hierarchical_engine,
)
from _04_DEPLOYMENT_AND_API.ynor_core.engine import YnorEngine


def summarize(samples: list[float]) -> dict:
    ordered = sorted(samples)
    count = len(ordered)
    if not ordered:
        return {"count": 0, "mean_ms": 0.0, "p95_ms": 0.0, "min_ms": 0.0, "max_ms": 0.0}

    p95_index = min(count - 1, max(0, int(count * 0.95) - 1))
    return {
        "count": count,
        "mean_ms": round(statistics.fmean(ordered) * 1000, 3),
        "p95_ms": round(ordered[p95_index] * 1000, 3),
        "min_ms": round(ordered[0] * 1000, 3),
        "max_ms": round(ordered[-1] * 1000, 3),
    }


async def time_async_calls(iterations: int, coro_factory) -> dict:
    samples: list[float] = []
    for _ in range(iterations):
        start = time.perf_counter()
        await coro_factory()
        samples.append(time.perf_counter() - start)
    return summarize(samples)


def time_sync_calls(iterations: int, fn) -> dict:
    samples: list[float] = []
    for _ in range(iterations):
        start = time.perf_counter()
        fn()
        samples.append(time.perf_counter() - start)
    return summarize(samples)


def build_engine(prompt_repetitions: int) -> tuple[YnorEngine, str]:
    response = (
        "Structured output with consistent semantics, punctuation, and controlled verbosity. "
        "This payload is repeated to exercise alpha, beta, and kappa measurements."
    )

    def fake_llm(context: str) -> str:
        return f"{response} Context length={len(context)}."

    prompt = "Base prompt. " * prompt_repetitions
    engine = YnorEngine(fake_llm, model_name="gpt-4o", threshold=-9999.0)
    return engine, prompt


def configure_temp_storage(temp_dir: Path) -> None:
    api_server.USAGE_FILE = temp_dir / "usage_stats.json"
    api_server.MU_AUDIT_FILE = temp_dir / "mu_audit_history.json"
    api_server.REVOCATION_FILE = temp_dir / "revocation_list.json"
    api_server.USAGE_STATS = {}
    api_server.MU_AUDIT_HISTORY = deque(maxlen=1000)
    api_server.REVOKED_KEYS = set()


def run_engine_once(prompt_repetitions: int, engine_steps: int) -> None:
    engine, prompt = build_engine(prompt_repetitions)
    engine.run(prompt, max_steps=engine_steps, verbose=False)


async def run_benchmarks(args: argparse.Namespace) -> dict:
    results: dict[str, dict] = {}

    with tempfile.TemporaryDirectory(prefix="ynor-bench-") as temp_root:
        configure_temp_storage(Path(temp_root))

        state_payload = AgentStatePayload(
            token_cost=0.00001,
            tokens_used=1600,
            context_length=3200,
            error_estimate=0.12,
            confidence=0.91,
        )
        sys1_payload = HierarchicalPayload(
            query="Analyse courte stable",
            alpha_capacity=0.9,
            beta_pressure=0.0,
            kappa_memory=0.1,
        )
        sys2_payload = HierarchicalPayload(
            query="Analyse nécessitant correction",
            alpha_capacity=0.8,
            beta_pressure=1.0,
            kappa_memory=0.2,
        )

        results["rate_limit"] = await time_async_calls(
            args.rate_limit_iterations,
            lambda: check_rate_limit(api_server.MASTER_KEY),
        )
        results["evaluate_viability"] = await time_async_calls(
            args.evaluate_iterations,
            lambda: evaluate_viability(state_payload, request=None, api_key=api_server.TEST_KEY),
        )
        results["hierarchical_sys1"] = await time_async_calls(
            args.hierarchical_iterations,
            lambda: execute_hierarchical_engine(sys1_payload, api_key=api_server.TEST_KEY),
        )
        results["hierarchical_sys2"] = await time_async_calls(
            args.hierarchical_slow_iterations,
            lambda: execute_hierarchical_engine(sys2_payload, api_key=api_server.TEST_KEY),
        )

        results["engine_run"] = time_sync_calls(
            args.engine_iterations,
            lambda: run_engine_once(args.prompt_repetitions, args.engine_steps),
        )

    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Micro-benchmark reproductible des hot paths Ynor.")
    parser.add_argument("--rate-limit-iterations", type=int, default=200)
    parser.add_argument("--evaluate-iterations", type=int, default=200)
    parser.add_argument("--hierarchical-iterations", type=int, default=10)
    parser.add_argument("--hierarchical-slow-iterations", type=int, default=5)
    parser.add_argument("--engine-iterations", type=int, default=20)
    parser.add_argument("--engine-steps", type=int, default=12)
    parser.add_argument("--prompt-repetitions", type=int, default=200)
    parser.add_argument("--json-out", type=Path, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    results = asyncio.run(run_benchmarks(args))
    payload = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "benchmarks": results,
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()

```
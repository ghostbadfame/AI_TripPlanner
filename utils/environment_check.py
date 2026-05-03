from __future__ import annotations

import os
from pathlib import Path


ENV_REQUIREMENTS = {
    "Gemini": ("GEMINI_API_KEY",),
    "Groq": ("GROQ_API_KEY",),
    "Google": ("GOOGLE_API_KEY",),
    "Google Places": ("GPLACES_API_KEY", "GPLACE_API_KEY"),
    "Tavily": ("TAVILY_API_KEY", "TAVILAY_API_KEY"),
    "OpenWeather": ("OPENWEATHERMAP_API_KEY", "OPENWEATHER_API_KEY"),
    "Exchange Rate": ("EXCHANGE_RATE_API_KEY", "EXCHANGHE_RATE_API_KEY"),
}


def _normalize_value(raw_value: str) -> str:
    value = raw_value.strip()

    for marker in (" #", " //"):
        if marker in value:
            value = value.split(marker, 1)[0].rstrip()

    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        value = value[1:-1]

    return value.strip()


def _read_env_file(env_path: Path) -> dict[str, str]:
    if not env_path.exists():
        return {}

    values: dict[str, str] = {}
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, raw_value = line.split("=", 1)
        values[key.strip()] = _normalize_value(raw_value)

    return values


def _first_non_empty(values: list[str | None]) -> str:
    for value in values:
        if value and value.strip():
            return value.strip()
    return ""


def check_environment(env_path: str | Path = ".env") -> dict[str, object]:
    path = Path(env_path)
    env_file_values = _read_env_file(path)

    missing_keys: list[str] = []
    configured_keys: list[str] = []

    for display_name, key_names in ENV_REQUIREMENTS.items():
        value = _first_non_empty(
            [os.getenv(key_name) for key_name in key_names]
            + [env_file_values.get(key_name) for key_name in key_names]
        )

        if value:
            configured_keys.append(display_name)
            for key_name in key_names:
                os.environ.setdefault(key_name, value)
        else:
            missing_keys.append("/".join(key_names))

    return {
        "ok": not missing_keys,
        "env_file_found": path.exists(),
        "env_file_path": str(path.resolve()),
        "using_virtualenv": os.getenv("VIRTUAL_ENV") is not None,
        "configured_keys": configured_keys,
        "missing_keys": missing_keys,
    }


def format_environment_report(report: dict[str, object]) -> str:
    lines = [
        "Environment check",
        f"- .env file found: {report['env_file_found']}",
        f"- .env path: {report['env_file_path']}",
        f"- Virtual environment active: {report['using_virtualenv']}",
    ]

    configured_keys = report["configured_keys"]
    missing_keys = report["missing_keys"]

    if configured_keys:
        lines.append(f"- Configured services: {', '.join(configured_keys)}")
    else:
        lines.append("- Configured services: none")

    if missing_keys:
        lines.append(f"- Missing keys: {', '.join(missing_keys)}")
    else:
        lines.append("- Missing keys: none")

    lines.append(f"- Status: {'PASS' if report['ok'] else 'FAIL'}")
    return "\n".join(lines)

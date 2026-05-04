from __future__ import annotations

from pathlib import Path

import yaml

from exceptions.exceptionHandling import ConfigurationError

def load_config(config_path: str = "config/config.yaml") -> dict:
    path = Path(config_path)

    if not path.exists():
        raise ConfigurationError(
            "Configuration file not found.",
            details={"config_path": str(path.resolve())},
        )

    try:
        with path.open("r", encoding="utf-8") as file:
            config = yaml.safe_load(file) or {}
    except yaml.YAMLError as exc:
        raise ConfigurationError(
            "Configuration file is invalid YAML.",
            details={"config_path": str(path.resolve())},
        ) from exc
    except OSError as exc:
        raise ConfigurationError(
            "Unable to read configuration file.",
            details={"config_path": str(path.resolve())},
        ) from exc

    if not isinstance(config, dict):
        raise ConfigurationError(
            "Configuration file must contain a top-level object.",
            details={"config_path": str(path.resolve())},
        )

    return config

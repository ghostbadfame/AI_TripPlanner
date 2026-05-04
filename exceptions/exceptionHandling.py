from __future__ import annotations

from typing import Any


class AppException(Exception):
    """Base application exception with optional structured metadata."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int = 500,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details or {}

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"error": self.message}
        if self.details:
            payload["details"] = self.details
        return payload


class ConfigurationError(AppException):
    def __init__(self, message: str, *, details: dict[str, Any] | None = None) -> None:
        super().__init__(message, status_code=500, details=details)


class ValidationError(AppException):
    def __init__(self, message: str, *, details: dict[str, Any] | None = None) -> None:
        super().__init__(message, status_code=400, details=details)


class ExternalServiceError(AppException):
    def __init__(self, message: str, *, details: dict[str, Any] | None = None) -> None:
        super().__init__(message, status_code=502, details=details)


class ProcessingError(AppException):
    def __init__(self, message: str, *, details: dict[str, Any] | None = None) -> None:
        super().__init__(message, status_code=500, details=details)

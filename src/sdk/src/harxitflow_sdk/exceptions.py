"""Exceptions raised by the HarxitFlow SDK."""

from __future__ import annotations


class HarxitFlowError(Exception):
    """Base class for all HarxitFlow SDK errors."""


class HarxitFlowHTTPError(HarxitFlowError):
    """An HTTP error was returned by the HarxitFlow API."""

    def __init__(self, status_code: int, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"HTTP {status_code}: {detail}")


class HarxitFlowNotFoundError(HarxitFlowHTTPError):
    """The requested resource was not found (404)."""


class HarxitFlowAuthError(HarxitFlowHTTPError):
    """Authentication failed (401/403)."""


class HarxitFlowValidationError(HarxitFlowHTTPError):
    """The request payload was rejected by the server (422)."""


class HarxitFlowConnectionError(HarxitFlowError):
    """Could not connect to the HarxitFlow instance."""


class HarxitFlowTimeoutError(HarxitFlowError):
    """A background job or polling operation exceeded its timeout.

    Adapted from ``HarxitFlowV2TimeoutError`` in harxitflow-ai/sdk PR #1
    (Janardan Singh Kavia, IBM Corp., Apache 2.0).
    """


class EnvironmentNotFoundError(HarxitFlowError):
    """The named environment is not defined in the environments config."""

    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(
            f"Environment {name!r} not found. Check your harxitflow-environments.toml (or HARXITFLOW_ENV variable)."
        )


class EnvironmentConfigError(HarxitFlowError):
    """The environments config file is malformed or missing required fields."""

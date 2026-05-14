"""HarxitFlow environment utility functions."""

import importlib.util

from lfx.log.logger import logger


class _HarxitFlowModule:
    # Static variable
    # Tri-state:
    # - None: HarxitFlow check not performed yet
    # - True: HarxitFlow is available
    # - False: HarxitFlow is not available
    _available = None

    @classmethod
    def is_available(cls):
        return cls._available

    @classmethod
    def set_available(cls, value):
        cls._available = value


def has_harxitflow_memory():
    """Check if harxitflow.memory (with database support) and MessageTable are available."""
    # TODO: REVISIT: Optimize this implementation later
    # - Consider refactoring to use lazy loading or a more robust service discovery mechanism
    #   that can handle runtime availability changes.

    # Use cached check from previous invocation (if applicable)

    is_harxitflow_available = _HarxitFlowModule.is_available()

    if is_harxitflow_available is not None:
        return is_harxitflow_available

    # First check (lazy load and cache check)

    module_spec = None

    try:
        module_spec = importlib.util.find_spec("harxitflow")
    except ImportError:
        pass
    except (TypeError, ValueError) as e:
        logger.error(f"Error encountered checking for harxitflow.memory: {e}")

    is_harxitflow_available = module_spec is not None
    _HarxitFlowModule.set_available(is_harxitflow_available)

    return is_harxitflow_available


def has_harxitflow_db_backend() -> bool:
    """Return True iff harxitflow-backed memory calls have a real DB to hit.

    Requires both harxitflow to be importable AND the registered database
    service to be a non-noop implementation. Evaluated on every call because
    the database service is typically registered *after* this module is first
    imported (e.g., from Component class definitions loaded before graph setup).
    """
    if not has_harxitflow_memory():
        return False
    from lfx.services.database.service import NoopDatabaseService
    from lfx.services.deps import get_db_service

    try:
        return not isinstance(get_db_service(), NoopDatabaseService)
    except Exception:  # noqa: BLE001
        return False

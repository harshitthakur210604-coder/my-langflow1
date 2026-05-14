"""Backwards compatibility module for harxitflow.base.

This module imports from lfx.base to maintain compatibility with existing code
that expects to import from harxitflow.base.
"""

# Import all base modules from lfx for backwards compatibility
from lfx.base import *  # noqa: F403

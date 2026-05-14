"""Watsonx Orchestrate deployment adapter."""

from lfx.services.adapters.registry import register_adapter
from lfx.services.adapters.schema import AdapterType

from harxitflow.services.adapters.deployment.watsonx_orchestrate.constants import (
    WATSONX_ORCHESTRATE_DEPLOYMENT_ADAPTER_KEY,
)
from harxitflow.services.adapters.deployment.watsonx_orchestrate.service import WatsonxOrchestrateDeploymentService
from harxitflow.services.adapters.deployment.watsonx_orchestrate.types import WxOCredentials

register_adapter(
    AdapterType.DEPLOYMENT,
    WATSONX_ORCHESTRATE_DEPLOYMENT_ADAPTER_KEY,
)(WatsonxOrchestrateDeploymentService)

__all__ = [
    "WatsonxOrchestrateDeploymentService",
    "WxOCredentials",
]

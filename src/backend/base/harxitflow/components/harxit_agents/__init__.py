from __future__ import annotations

from typing import TYPE_CHECKING, Any

from lfx.components._importing import import_mod

if TYPE_CHECKING:
    from .ads_agent import AdsAgent
    from .analytics_agent import AnalyticsAgent
    from .area_expansion import LocalExpansionAgent
    from .automation_builder import AutomationBuilderAgent
    from .billing_finance import BillingFinanceAgent
    from .client_success import ClientSuccessAgent
    from .client_support import ClientSupportAgent
    from .cold_email import ColdEmailAgent
    from .competitor_analysis import CompetitorAnalysisAgent
    from .content_creation import ContentCreationAgent
    from .contract_generator import ContractGeneratorAgent
    from .deal_closing import DealClosingAgent
    from .expansion_strategy import ExpansionStrategyAgent
    from .follow_up import FollowUpAgent
    from .franchise_manager import HTFranchiseManagerAgent
    from .global_entry_agent import HTGlobalEntryAgent
    from .hiring_agent import HiringAgent
    from .ht19_working_plan import HarxitWorkingPlanAgent
    from .lead_scoring import LeadScoringAgent
    from .lead_scraper import LeadScraperAgent
    from .n8n_sender import N8nSenderComponent
    from .niche_finder import NicheFinderAgent
    from .niche_selector import HTNicheSelector
    from .payment_reminder import PaymentReminderAgent
    from .pricing_optimization import PricingOptimizationAgent
    from .project_onboarding import ProjectOnboardingAgent
    from .project_planner import ProjectPlannerAgent
    from .proposal_generator import ProposalGeneratorAgent
    from .pro_lead_scraper import ProLeadScraper
    from .quality_assurance import QAAgent
    from .requirement_analyzer import RequirementAnalyzerAgent
    from .retargeting import RetargetingAgent
    from .retention_agent import RetentionAgent
    from .review_collector import ReviewCollectorAgent
    from .saas_generator import HTSaaSGeneratorAgent
    from .ai_sales_agent import HTAISalesAgent
    from .sales_pitch import SalesPitchAgent
    from .social_dm import SocialDMAgent
    from .training_agent import TrainingAgent
    from .universal_bridge import HTUniversalBridge
    from .upsell_agent import UpsellAgent
    from .visionary_ceo import HTVisionaryCEOAgent
    from .whatsapp_automation import WhatsAppAutomationAgent
    from .white_label_agent import HTWhiteLabelAgent

_dynamic_imports = {
    "HTUniversalBridge": "universal_bridge",
    "AdsAgent": "ads_agent",
    "AnalyticsAgent": "analytics_agent",
    "LocalExpansionAgent": "area_expansion",
    "AutomationBuilderAgent": "automation_builder",
    "BillingFinanceAgent": "billing_finance",
    "ClientSuccessAgent": "client_success",
    "ClientSupportAgent": "client_support",
    "ColdEmailAgent": "cold_email",
    "CompetitorAnalysisAgent": "competitor_analysis",
    "ContentCreationAgent": "content_creation",
    "ContractGeneratorAgent": "contract_generator",
    "DealClosingAgent": "deal_closing",
    "ExpansionStrategyAgent": "expansion_strategy",
    "FollowUpAgent": "follow_up",
    "HTFranchiseManagerAgent": "franchise_manager",
    "HTGlobalEntryAgent": "global_entry_agent",
    "HiringAgent": "hiring_agent",
    "HarxitWorkingPlanAgent": "ht19_working_plan",
    "LeadScoringAgent": "lead_scoring",
    "LeadScraperAgent": "lead_scraper",
    "N8nSenderComponent": "n8n_sender",
    "NicheFinderAgent": "niche_finder",
    "HTNicheSelector": "niche_selector",
    "PaymentReminderAgent": "payment_reminder",
    "PricingOptimizationAgent": "pricing_optimization",
    "ProjectOnboardingAgent": "project_onboarding",
    "ProjectPlannerAgent": "project_planner",
    "ProposalGeneratorAgent": "proposal_generator",
    "ProLeadScraper": "pro_lead_scraper",
    "QAAgent": "quality_assurance",
    "RequirementAnalyzerAgent": "requirement_analyzer",
    "RetargetingAgent": "retargeting",
    "RetentionAgent": "retention_agent",
    "ReviewCollectorAgent": "review_collector",
    "HTSaaSGeneratorAgent": "saas_generator",
    "HTAISalesAgent": "ai_sales_agent",
    "SalesPitchAgent": "sales_pitch",
    "SocialDMAgent": "social_dm",
    "TrainingAgent": "training_agent",
    "UpsellAgent": "upsell_agent",
    "HTVisionaryCEOAgent": "visionary_ceo",
    "WhatsAppAutomationAgent": "whatsapp_automation",
    "HTWhiteLabelAgent": "white_label_agent",
}

__all__ = list(_dynamic_imports.keys())


def __getattr__(attr_name: str) -> Any:
    """Lazily import harxit_agents components on attribute access."""
    if attr_name not in _dynamic_imports:
        msg = f"module '{__name__}' has no attribute '{attr_name}'"
        raise AttributeError(msg)
    try:
        result = import_mod(attr_name, _dynamic_imports[attr_name], __spec__.parent)
    except (ModuleNotFoundError, ImportError, AttributeError) as e:
        msg = f"Could not import '{attr_name}' from '{__name__}': {e}"
        raise AttributeError(msg) from e
    globals()[attr_name] = result
    return result


def __dir__() -> list[str]:
    return list(__all__)

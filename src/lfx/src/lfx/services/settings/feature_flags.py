from pydantic_settings import BaseSettings


class FeatureFlags(BaseSettings):
    wxo_deployments: bool = True
    """
    Enable Watsonx Orchestrate deployments.
    """
    mvp_components: bool = False

    class Config:
        env_prefix = "HARXITFLOW_FEATURE_"


FEATURE_FLAGS = FeatureFlags()

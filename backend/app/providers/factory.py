from app.providers.base import BaseProvider
from app.providers.replicate_provider import ReplicateProvider

class ProviderFactory:
    _providers = {
        "replicate": ReplicateProvider(),
    }

    @classmethod
    def get_provider(cls, name: str) -> BaseProvider:
        if name not in cls._providers:
            raise ValueError(f"Provider {name} not supported")
        return cls._providers[name]
